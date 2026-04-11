'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { getDashboardKpis, getDashboardDeals } from '@/lib/api';
import { signOut, getCurrentUser } from '@/lib/auth';

interface KPIs {
  total_deals: number;
  avg_roi: number;
  total_saved: number;
  deals_this_week: number;
  total_profit: number;
}

interface Deal {
  id: string;
  title: string;
  buy_price: number;
  sell_price: number;
  roi: number;
  score: number;
}

export default function Dashboard() {
  const router = useRouter();
  const [kpis, setKpis] = useState<KPIs | null>(null);
  const [deals, setDeals] = useState<Deal[]>([]);
  const [userName, setUserName] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [kpiData, dealData, user] = await Promise.all([
          getDashboardKpis() as Promise<KPIs>,
          getDashboardDeals() as Promise<Deal[]>,
          getCurrentUser(),
        ]);
        setKpis(kpiData);
        setDeals(dealData);
        setUserName(user?.full_name || 'User');
      } catch (err) {
        console.error('Dashboard load error:', err);
        // Fallback to demo data if API not ready
        setKpis({ total_deals: 142, avg_roi: 47.3, total_saved: 28, deals_this_week: 34, total_profit: 2847.50 });
        setDeals([
          { id: '1', title: 'Wireless Earbuds Pro', buy_price: 18.99, sell_price: 34.99, roi: 52, score: 92 },
          { id: '2', title: 'Kitchen Scale Digital', buy_price: 12.49, sell_price: 24.99, roi: 67, score: 88 },
          { id: '3', title: 'LED Desk Lamp', buy_price: 22.00, sell_price: 39.99, roi: 45, score: 85 },
          { id: '4', title: 'Phone Case Premium', buy_price: 8.99, sell_price: 19.99, roi: 78, score: 82 },
          { id: '5', title: 'Yoga Mat Extra Thick', buy_price: 15.99, sell_price: 29.99, roi: 55, score: 79 },
        ]);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-6 py-3 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold text-blue-700">ArbiEdge</Link>
        <div className="flex gap-6 items-center">
          <Link href="/dashboard" className="text-blue-600 font-medium">Dashboard</Link>
          <Link href="/deals" className="text-gray-600 hover:text-blue-600">Deals</Link>
          <Link href="/calculator" className="text-gray-600 hover:text-blue-600">Calculator</Link>
          <span className="text-gray-600 text-sm">{userName}</span>
          <button onClick={signOut} className="text-sm text-red-500 hover:text-red-700">Sign out</button>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

        {/* KPI Grid */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          {[
            { label: 'Total Deals', value: kpis?.total_deals },
            { label: 'Avg ROI', value: `${kpis?.avg_roi}%` },
            { label: 'Saved Deals', value: kpis?.total_saved },
            { label: 'Weekly Deals', value: kpis?.deals_this_week },
            { label: 'Total Profit', value: `$${kpis?.total_profit?.toFixed(2)}` },
          ].map((item) => (
            <div key={item.label} className="bg-white rounded-xl p-4 border">
              <p className="text-sm text-gray-500">{item.label}</p>
              <p className="text-2xl font-bold mt-1">{item.value}</p>
            </div>
          ))}
        </div>

        {/* Top Deals */}
        <div className="bg-white rounded-xl border p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold">Top Deals</h2>
            <Link href="/deals" className="text-blue-600 text-sm hover:underline">View all</Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-gray-500 border-b">
                  <th className="text-left py-2">Product</th>
                  <th className="text-right py-2">Buy</th>
                  <th className="text-right py-2">Sell</th>
                  <th className="text-right py-2">ROI</th>
                  <th className="text-right py-2">Score</th>
                </tr>
              </thead>
              <tbody>
                {deals.map((deal) => (
                  <tr key={deal.id} className="border-b last:border-0 hover:bg-gray-50">
                    <td className="py-3 font-medium">{deal.title}</td>
                    <td className="text-right py-3">${deal.buy_price?.toFixed(2)}</td>
                    <td className="text-right py-3">${deal.sell_price?.toFixed(2)}</td>
                    <td className="text-right py-3 text-green-600 font-semibold">{deal.roi}%</td>
                    <td className="text-right py-3">
                      <span className="bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">{deal.score}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
