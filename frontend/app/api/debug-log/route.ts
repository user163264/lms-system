import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const log = await request.json();
    
    // Log to server console
    console.log('CLIENT LOG:', log);
    
    return NextResponse.json({ status: 'success' });
  } catch (error) {
    console.error('Error logging from client:', error);
    return NextResponse.json({ status: 'error' }, { status: 500 });
  }
}

// Simple GET handler for testing the endpoint
export async function GET() {
  return NextResponse.json({ status: 'debug-log endpoint is active' });
} 