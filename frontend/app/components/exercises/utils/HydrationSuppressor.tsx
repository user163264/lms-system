'use client';

import React, { ReactNode } from 'react';

/**
 * HydrationSuppressor component
 * 
 * This utility component applies suppressHydrationWarning to its children
 * to prevent hydration errors caused by browser extensions that modify the DOM.
 */
interface HydrationSuppressorProps {
  children: ReactNode;
  className?: string;
}

const HydrationSuppressor: React.FC<HydrationSuppressorProps> = ({ 
  children, 
  className = '' 
}) => {
  return (
    <div className={className} suppressHydrationWarning>
      {children}
    </div>
  );
};

export default HydrationSuppressor; 