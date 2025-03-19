#!/usr/bin/env python3
"""
Script Name: check_plagiarism.py
Description: Analyzes student submissions for potential plagiarism

Usage:
    python scripts/analysis/check_plagiarism.py [options]
    
Options:
    --assignment ID          Check specific assignment ID
    --course ID              Check all assignments in course ID
    --threshold FLOAT        Similarity threshold (0.0-1.0) [default: 0.8]
    --algorithm ALG          Similarity algorithm (token, ngram, cosine) [default: token]
    --output FILE            Save results to file instead of stdout
    --detailed               Include detailed match information
    
Dependencies:
    - psycopg2
    - pandas
    - scipy
    - difflib
    - nltk
    
Output:
    Plagiarism analysis report
    
Author: LMS Team
Last Modified: 2025-03-19
"""

import argparse
import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
import psycopg2
import psycopg2.extras

# Add the project root to sys.path to enable imports
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

# Try to import relevant modules
try:
    from database.db_manager import get_db_params
    import pandas as pd
    from scipy import spatial
    import difflib
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.util import ngrams
    from collections import Counter
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Make sure you have all required packages installed.")
    sys.exit(1)

# Download required NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Analyze student submissions for potential plagiarism")
    
    # Assignment specification options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--assignment", type=int, help="Check specific assignment ID")
    group.add_argument("--course", type=int, help="Check all assignments in course ID")
    
    # Analysis options
    parser.add_argument("--threshold", type=float, default=0.8, 
                      help="Similarity threshold (0.0-1.0) [default: 0.8]")
    parser.add_argument("--algorithm", choices=["token", "ngram", "cosine"], default="token",
                      help="Similarity algorithm (token, ngram, cosine) [default: token]")
    
    # Output options
    parser.add_argument("--output", type=str, help="Save results to file instead of stdout")
    parser.add_argument("--detailed", action="store_true", help="Include detailed match information")
    
    return parser.parse_args()

def get_submissions(conn, assignment_id=None, course_id=None):
    """Get student submissions for analysis."""
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        if assignment_id:
            # Get submissions for a specific assignment
            query = """
                SELECT 
                    sa.id, 
                    sa.student_id, 
                    s.name as student_name,
                    sa.assignment_id, 
                    a.title as assignment_title,
                    sa.submission_text, 
                    sa.submission_date
                FROM 
                    student_assignment sa
                JOIN 
                    student s ON sa.student_id = s.id
                JOIN 
                    assignment a ON sa.assignment_id = a.id
                WHERE 
                    sa.assignment_id = %s
                    AND sa.submission_text IS NOT NULL
                ORDER BY 
                    sa.student_id
            """
            cursor.execute(query, (assignment_id,))
        
        elif course_id:
            # Get submissions for all assignments in a course
            query = """
                SELECT 
                    sa.id, 
                    sa.student_id, 
                    s.name as student_name,
                    sa.assignment_id, 
                    a.title as assignment_title,
                    sa.submission_text, 
                    sa.submission_date
                FROM 
                    student_assignment sa
                JOIN 
                    student s ON sa.student_id = s.id
                JOIN 
                    assignment a ON sa.assignment_id = a.id
                JOIN
                    course c ON a.course_id = c.id
                WHERE 
                    c.id = %s
                    AND sa.submission_text IS NOT NULL
                ORDER BY 
                    a.id, sa.student_id
            """
            cursor.execute(query, (course_id,))
        
        # Fetch all submissions
        submissions = cursor.fetchall()
        cursor.close()
        
        if not submissions:
            print("No submissions found for analysis")
            return []
        
        print(f"Found {len(submissions)} submissions for analysis")
        return submissions
    
    except Exception as e:
        print(f"Error fetching submissions: {e}")
        return []

def tokenize_submission(text):
    """Tokenize submission text for comparison."""
    # Remove common code comments
    text = re.sub(r'#.*$|//.*$|/\*[\s\S]*?\*/|\'\'\'[\s\S]*?\'\'\'|"""[\s\S]*?"""', '', text, flags=re.MULTILINE)
    
    # Remove whitespace and convert to lowercase
    text = re.sub(r'\s+', ' ', text).lower().strip()
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove common stop words and symbols
    stop_words = ['the', 'and', 'a', 'to', 'of', 'in', 'is', 'it', 'that', 'for']
    tokens = [t for t in tokens if t.isalnum() and t not in stop_words]
    
    return tokens

def create_ngram_profile(tokens, n=3):
    """Create n-gram profile from tokens."""
    n_grams = list(ngrams(tokens, n))
    return Counter(n_grams)

def similarity_token(tokens1, tokens2):
    """Calculate similarity using token comparison."""
    matcher = difflib.SequenceMatcher(None, tokens1, tokens2)
    return matcher.ratio()

def similarity_ngram(tokens1, tokens2, n=3):
    """Calculate similarity using n-gram comparison."""
    profile1 = create_ngram_profile(tokens1, n)
    profile2 = create_ngram_profile(tokens2, n)
    
    # Find common n-grams
    common = sum((profile1 & profile2).values())
    total = sum((profile1 | profile2).values())
    
    # Return Jaccard similarity
    return common / total if total > 0 else 0

def similarity_cosine(tokens1, tokens2):
    """Calculate similarity using cosine similarity."""
    # Create term frequency vectors
    vocab = list(set(tokens1 + tokens2))
    vec1 = [tokens1.count(word) for word in vocab]
    vec2 = [tokens2.count(word) for word in vocab]
    
    # Calculate cosine similarity
    return 1 - spatial.distance.cosine(vec1, vec2)

def analyze_submissions(submissions, threshold=0.8, algorithm="token", detailed=False):
    """Analyze submissions for similarity."""
    # Preprocess submissions
    processed_submissions = []
    for submission in submissions:
        if submission["submission_text"]:
            tokens = tokenize_submission(submission["submission_text"])
            processed_submissions.append({
                "id": submission["id"],
                "student_id": submission["student_id"],
                "student_name": submission["student_name"],
                "assignment_id": submission["assignment_id"],
                "assignment_title": submission["assignment_title"],
                "submission_date": submission["submission_date"],
                "tokens": tokens,
                "text": submission["submission_text"]
            })
    
    # Group by assignment
    assignments = {}
    for sub in processed_submissions:
        assignment_id = sub["assignment_id"]
        if assignment_id not in assignments:
            assignments[assignment_id] = []
        assignments[assignment_id].append(sub)
    
    # Results container
    results = []
    
    # Analyze each assignment group
    for assignment_id, subs in assignments.items():
        print(f"Analyzing assignment {assignment_id}: {subs[0]['assignment_title']}")
        
        # Compare each pair of submissions
        for i in range(len(subs)):
            for j in range(i + 1, len(subs)):
                sub1 = subs[i]
                sub2 = subs[j]
                
                # Calculate similarity based on selected algorithm
                if algorithm == "token":
                    similarity = similarity_token(sub1["tokens"], sub2["tokens"])
                elif algorithm == "ngram":
                    similarity = similarity_ngram(sub1["tokens"], sub2["tokens"])
                elif algorithm == "cosine":
                    similarity = similarity_cosine(sub1["tokens"], sub2["tokens"])
                
                # Check if similarity exceeds threshold
                if similarity >= threshold:
                    # Prepare match details
                    match = {
                        "assignment_id": assignment_id,
                        "assignment_title": sub1["assignment_title"],
                        "student1_id": sub1["student_id"],
                        "student1_name": sub1["student_name"],
                        "student2_id": sub2["student_id"],
                        "student2_name": sub2["student_name"],
                        "similarity": similarity,
                        "algorithm": algorithm
                    }
                    
                    # Add detailed matching segments if requested
                    if detailed:
                        # Use difflib to find matching segments
                        diff = difflib.SequenceMatcher(None, sub1["text"], sub2["text"])
                        matching_blocks = diff.get_matching_blocks()
                        
                        # Extract matching segments longer than a minimum length
                        min_match_length = 20
                        significant_matches = []
                        
                        for block in matching_blocks:
                            if block.size > min_match_length:
                                match_text = sub1["text"][block.a:block.a + block.size]
                                significant_matches.append({
                                    "length": block.size,
                                    "text": match_text
                                })
                        
                        if significant_matches:
                            match["matches"] = significant_matches
                    
                    results.append(match)
    
    # Sort results by similarity (descending)
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    return results

def format_results(results, detailed=False):
    """Format results for output."""
    if not results:
        return "No suspicious similarities detected"
    
    output = []
    output.append(f"Plagiarism Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append(f"Found {len(results)} suspicious similarities")
    output.append("")
    
    for i, match in enumerate(results, 1):
        output.append(f"Match #{i} - Similarity: {match['similarity']:.2f} ({match['algorithm']} algorithm)")
        output.append(f"Assignment: {match['assignment_title']} (ID: {match['assignment_id']})")
        output.append(f"Student 1: {match['student1_name']} (ID: {match['student1_id']})")
        output.append(f"Student 2: {match['student2_name']} (ID: {match['student2_id']})")
        
        if detailed and "matches" in match:
            output.append("\nMatching segments:")
            for j, segment in enumerate(match["matches"], 1):
                output.append(f"  Segment #{j} ({segment['length']} characters):")
                # Truncate very long segments
                text = segment["text"]
                if len(text) > 200:
                    text = text[:197] + "..."
                output.append(f"  {text}")
        
        output.append("-" * 80)
    
    return "\n".join(output)

def save_results(results, filename):
    """Save results to a file."""
    try:
        with open(filename, "w") as f:
            if filename.endswith(".json"):
                json.dump(results, f, indent=2, default=str)
            else:
                f.write(format_results(results, detailed=True))
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")

def main():
    """Main function."""
    args = parse_args()
    
    # Validate threshold
    if args.threshold < 0 or args.threshold > 1:
        print("Threshold must be between 0.0 and 1.0")
        return 1
    
    try:
        # Get database connection parameters
        db_params = get_db_params()
        
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        
        # Get submissions to analyze
        submissions = get_submissions(conn, args.assignment, args.course)
        
        if not submissions:
            conn.close()
            return 1
        
        # Analyze submissions
        results = analyze_submissions(
            submissions, 
            threshold=args.threshold,
            algorithm=args.algorithm,
            detailed=args.detailed
        )
        
        # Close the database connection
        conn.close()
        
        # Format and output results
        formatted_results = format_results(results, args.detailed)
        
        if args.output:
            save_results(results if args.output.endswith(".json") else formatted_results, args.output)
        else:
            print(formatted_results)
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 