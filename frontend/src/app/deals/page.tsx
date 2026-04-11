'use client';
import Link from 'next/link';
import { useState, useEffect } from 'react';
import { getDeals, saveDeal } from '@/lib/api';
import { signOut } from '@/lib/auth';

const DEMO_DEALS = [
  { id: '1', title: 'Wireless Earbuds Pro', asin: 'B09XYZ1234', source: 'Walmart', buy_price: 18.99, sell_price: 34.99, roi: 52, score: 92, category: 'Electronics' },
  { id: '2', title: 'Kitchen Scale Digital', asin: 'B08ABC5678', source: 'Target', buy_price: 12.49, sell_price: 24.99, roi: 67, score: 88, category: 'Kitchen' },
  { id: '3', title: 'LED Desk Lamp USB', asin: 'B07DEF9012', source: 'Walmart', buy_price: 22.00, sell_price: 39.99, roi: 45, score: 85, category: 'Office' },
  { id: '4', title: 'Phone Case Premium', asin: 'B06GHI3456', source: 'Target', buy_price: 8.99, sell_price: 19.99, roi: 78, score: 82, category: 'Electronics' },
  { id: '5', title: 'Yoga Mat Extra Thick', asin: 'B05JKL7890', source: 'Walmart', buy_price: 15.99, sell_price: 29.99, roi: 55, score: 79, category: 'Sports' },
];

interface Deal {
  id: string;
  title: string;
  asin?: string;
  source?: string;
  buy_price: number;
  sell_price: number;
  roi: number;
  score: number;
  category?: string;
}

export default function DealsPage() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [savedIds, setSavedIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    async function loadDeals() {
      try {
        const data = await getDeals() as Deal[];
        setDeals(Array.isArray(data) ? data : DEMO_DEALS);
      } catch {
        setDeals(DEMO_DEALS);
      } finally {
        setLoading(false);
      }
    }
    loadDeals();
  }, []);

  const handleSave = async (id: string) => {
    try {
      await saveDeal(id);
      setSavedIds(prev => new Set([...prev, id]));
    } catch {
      setSavedIds(prev => new Set([...prev, id])); // Optimistic UI
    }
  };

  const filtered = deals.filter(d =>
    !filter || d.title.toLowerCase().includes(filter.toLowerCase()) ||
    d.category?.toLowerCase().includes(filter.toLowerCase())
  );

  const scoreColor = (score: number) =>
    score >= 90 ? 'bg-green-100 text-green-700' :
    score >= 80 ? 'bg-blue-100 text-blue-700' :
    score >= 70 ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-700';

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-6 py-3 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold text-blue-700">ArbiEdge</Link>
        <div className="flex gap-6 items-center">
          <Link href="/dashboard" className="text-gray-600 hover:text-blue-600">Dashboard</Link>
          <Link href="/deals" className="text-blue-600 font-medium">Deals</Link>
          <Link href="/calculator" className="text-gray-600 hover:text-blue-600">Calculator</Link>
          <button onClick={signOut} className="text-sm text-red-500 hover:text-red-700">Sign out</button>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">Deal Feed</h1>
          <input
            type="text"
            placeholder="Filter by name or category..."
            value={filter}
            onChange={e => setFilter(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mx-auto mb-3"></div>
            <p className="text-gray-500">Loading deals...</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {filtered.map(deal => (
              <div key={deal.id} className="bg-white rounded-xl border p-5 flex items-center justify-between hover:shadow-sm transition-shadow">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1">
                    <h3 className="font-semibold text-gray-900">{deal.title}</h3>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-semibold ${scoreColor(deal.score)}`}>
                      Score: {deal.score}
                    </span>
                  </div>
                  <div className="flex gap-4 text-sm text-gray-500">
                    <span>ASIN: {deal.asin || 'N/A'}</span>
                    <span>Source: {deal.source || 'N/A'}</span>
                    <span>Category: {deal.category || 'N/A'}</span>
                  </div>
                </div>
                <div className="flex items-center gap-6 text-sm">
                  <div className="text-right">
                    <p className="text-gray-500">Buy</p>
                    <p className="font-semibold">${deal.buy_price?.toFixed(2)}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-gray-500">Sell</p>
                    <p className="font-semibold">${deal.sell_price?.toFixed(2)}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-gray-500">ROI</p>
                    <p className="font-bold text-green-600">{deal.roi}%</p>
                  </div>
                  <button
                    onClick={() => handleSave(deal.id)}
                    disabled={savedIds.has(deal.id)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      savedIds.has(deal.id)
                        ? 'bg-green-100 text-green-700 cursor-default'
                        : 'bg-blue-600 text-white hover:bg-blue-700'
                    }`}
                  >
                    {savedIds.has(deal.id) ? 'Saved' : 'Save Deal'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
