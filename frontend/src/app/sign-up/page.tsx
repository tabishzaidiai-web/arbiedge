'use client';
import Link from 'next/link';
import { useState } from 'react';

export default function SignUpPage() {
  const [form, setForm] = useState({ name: '', email: '', password: '' });

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md p-8 bg-white rounded-xl border shadow-sm">
        <h1 className="text-2xl font-bold text-center mb-2">Create Your Account</h1>
        <p className="text-gray-500 text-center mb-6">Start finding profitable deals today.</p>
        <div className="space-y-4">
          <div><label className="block text-sm font-medium mb-1">Full Name</label><input type="text" value={form.name} onChange={e => setForm({...form, name: e.target.value})} className="w-full border rounded-lg px-3 py-2" /></div>
          <div><label className="block text-sm font-medium mb-1">Email</label><input type="email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} className="w-full border rounded-lg px-3 py-2" /></div>
          <div><label className="block text-sm font-medium mb-1">Password</label><input type="password" value={form.password} onChange={e => setForm({...form, password: e.target.value})} className="w-full border rounded-lg px-3 py-2" /></div>
          <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700">Create Account</button>
          <button className="w-full border py-3 rounded-lg font-semibold hover:bg-gray-50">Continue with Google</button>
        </div>
        <p className="text-sm text-gray-500 text-center mt-6">Already have an account? <Link href="/sign-in" className="text-blue-600 hover:underline">Sign in</Link></p>
      </div>
    </div>
  );
}
