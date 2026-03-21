'use client';
import Link from 'next/link';
import { useState } from 'react';

export default function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md p-8 bg-white rounded-xl border shadow-sm">
        <h1 className="text-2xl font-bold text-center mb-2">Sign In to ArbiEdge</h1>
        <p className="text-gray-500 text-center mb-6">Welcome back</p>
        <div className="space-y-4">
          <div><label className="block text-sm font-medium mb-1">Email</label><input type="email" value={email} onChange={e => setEmail(e.target.value)} className="w-full border rounded-lg px-3 py-2" /></div>
          <div><label className="block text-sm font-medium mb-1">Password</label><input type="password" value={password} onChange={e => setPassword(e.target.value)} className="w-full border rounded-lg px-3 py-2" /></div>
          <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700">Sign In</button>
          <button className="w-full border py-3 rounded-lg font-semibold hover:bg-gray-50">Continue with Google</button>
        </div>
        <p className="text-sm text-gray-500 text-center mt-6">No account? <Link href="/sign-up" className="text-blue-600 hover:underline">Sign up</Link></p>
      </div>
    </div>
  );
}
