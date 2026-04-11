// ArbiEdge API Client
import { authHeaders } from './auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

// Dashboard
export const getDashboardKpis = () => request('/dashboard/kpis');
export const getDashboardDeals = () => request('/dashboard/deals');

// Deals
export const getDeals = (params?: Record<string, string>) => {
  const query = params ? '?' + new URLSearchParams(params).toString() : '';
  return request(`/deals${query}`);
};
export const getDeal = (id: string) => request(`/deals/${id}`);
export const saveDeal = (id: string) => request(`/deals/${id}/save`, { method: 'POST' });
export const purchaseDeal = (id: string) => request(`/deals/${id}/purchase`, { method: 'POST' });
export const archiveDeal = (id: string) => request(`/deals/${id}/archive`, { method: 'DELETE' });

// Profit / ROI Calculator
export const calculateProfit = (data: {
  buy_price: number;
  sell_price: number;
  category: string;
  weight_oz?: number;
  dimensions?: { length: number; width: number; height: number };
}) => request('/profit/calculate', { method: 'POST', body: JSON.stringify(data) });

export const getFbaFees = (asin: string) => request(`/profit/fba-fees/${asin}`);

// Products
export const searchProducts = (q: string) => request(`/products/search?q=${encodeURIComponent(q)}`);
export const getProduct = (asin: string) => request(`/products/${asin}`);

// Prices
export const getPriceCrossRef = (asin: string) => request(`/prices/cross-reference/${asin}`);
export const getPriceSnapshot = (asin: string) => request(`/prices/snapshot/${asin}`);

// Reports
export const getDailyReport = () => request('/reports/daily');
export const getReportHistory = () => request('/reports/history');
export const generateReport = () => request('/reports/generate', { method: 'POST' });

// User
export const getUserPreferences = () => request('/user/preferences');
export const updateUserPreferences = (data: Record<string, unknown>) =>
  request('/user/preferences', { method: 'POST', body: JSON.stringify(data) });
export const updateUserSettings = (data: Record<string, unknown>) =>
  request('/user/settings', { method: 'PUT', body: JSON.stringify(data) });

// Scan
export const triggerScan = () => request('/scan/trigger', { method: 'POST' });
export const getScanStatus = (jobId: string) => request(`/scan/status/${jobId}`);
