import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'ArbiEdge - AI-Powered Deal Validator for Amazon OA',
  description: 'Discover profitable Amazon arbitrage deals with AI-powered scoring, real-time price tracking, and automated ROI calculations.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 antialiased">{children}</body>
    </html>
  );
}
