"use client"
import React from "react";

export default function Error({ error }: { error: Error }) {
  // Minimal client-safe error boundary for the app router.
  return (
    <html>
      <body style={{ padding: 20, fontFamily: 'Arial, sans-serif' }}>
        <h1>Something went wrong</h1>
        <pre>{String(error?.message ?? 'Unknown error')}</pre>
      </body>
    </html>
  );
}
