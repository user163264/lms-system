import { NextResponse } from 'next/server';

export async function GET() {
  // Add artificial delay to simulate network conditions (0-50ms)
  const delay = Math.floor(Math.random() * 50);
  
  if (delay > 0) {
    await new Promise(resolve => setTimeout(resolve, delay));
  }
  
  return NextResponse.json({ 
    timestamp: new Date().toISOString(),
    status: 'ok',
    message: 'Pong!',
    artificialDelay: delay
  });
} 