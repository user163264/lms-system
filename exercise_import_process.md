# Exercise Import Process

## Overview
This document outlines the most effective approach for importing exercises into the LMS database.

## Steps

### 1. Database Schema Setup
- Create an SQL file with the table definition for exercises
- Execute using `sudo -u postgres psql -f /tmp/create_exercises_table.sql` to create the table

### 2. Structured JSON Format
- Create a well-defined JSON structure with all necessary fields for different exercise types
- Include lesson_id, exercise_type, and type-specific data fields for each exercise
- Example exercise types: multiple_choice, true_false, fill_blank, short_answer, long_answer, etc.

### 3. Python Import Script
- Develop a script that validates exercise data against required fields
- Include robust error handling for database connection and data validation
- Provide clear success/failure feedback for each imported exercise

### 4. Execution Method
- Copy files to /tmp directory with `sudo cp ~/lms/import_exercise.py /tmp/`
- Set appropriate permissions with `sudo chmod 755 /tmp/import_exercise.py`
- Run as postgres user: `sudo -u postgres python3 /tmp/import_exercise.py /tmp/art_exercises.json`

## Results
This approach successfully imports exercises of various types into the database without errors, as demonstrated by the successful import of 13 art-related exercises.

## Example Database Output
```
 id | lesson_id |  exercise_type  | question                                          
----+-----------+-----------------+-------------------------------------------------------------------
  1 |       101 | multiple_choice | Wie schilderde het beroemde werk 'Sterrennacht'?
  2 |       101 | true_false      | De Mona Lisa werd in 1911 gestolen, wat haar bekendheid vergrootte.
  3 |       101 | fill_blank      | ________ was een Spaanse kunstenaar die bekend stond om...
  4 |       101 | short_answer    | Welke techniek gebruikte Georges Seurat om 'Een Zondagmiddag op...
  5 |       101 | long_answer     | Leg uit waarom 'Guernica' van Picasso...
``` 