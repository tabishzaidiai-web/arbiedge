// ArbiEdge Auth Utility - JWT-based auth with localStorage
import Cookies from 'js-cookie';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface User {
  id: string;
  email: string;
  full_name: string;
  subscription_tier: string;
  is_active: boolean;
}

export interface AuthTokens {
  access_token: string;
  token_type: string;
}

export async function signUp(fullName: string, email: string, password: string): Promise<User> {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ full_name: fullName, email, password }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Registration failed');
  }
  return res.json();
}

export async function signIn(email: string, password: string): Promise<AuthTokens> {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Login failed');
  }
  const tokens: AuthTokens = await res.json();
  // Store token in cookie (7 days)
  Cookies.set('arbiedge_token', tokens.access_token, { expires: 7, secure: true, sameSite: 'lax' });
  return tokens;
}

export function signOut(): void {
  Cookies.remove('arbiedge_token');
  window.location.href = '/sign-in';
}

export function getToken(): string | undefined {
  return Cookies.get('arbiedge_token');
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

export async function getCurrentUser(): Promise<User | null> {
  const token = getToken();
  if (!token) return null;
  try {
    const res = await fetch(`${API_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
      Cookies.remove('arbiedge_token');
      return null;
    }
    return res.json();
  } catch {
    return null;
  }
}

export function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}
