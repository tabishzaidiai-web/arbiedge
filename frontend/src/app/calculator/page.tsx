'use client';
import { useState } from 'react';
import Link from 'next/link';
import { calculateProfit } from '@/lib/api';
import { signOut } from '@/lib/auth';

const CATEGORIES = ['Electronics', 'Kitchen', 'Sports', 'Office', 'Books', 'Clothing', 'Toys', 'Health', 'Automotive', 'Other'];

interface CalcResult {
  gross_profit: number;
  net_profit: number;
  roi_percent: number;
  referral_fee: number;
  fba_fee: number;
  total_fees: number;
  margin_percent: number;
}

export default function CalculatorPage() {
  const [form, setForm] = useState({ buy_price: '18.99', sell_price: '34.99', category: 'Electronics', weight_oz: '8.0' });
  const [result, setResult] = useState<CalcResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleCalculate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await calculateProfit({
        buy_price: parseFloat(form.buy_price),
        sell_price: parseFloat(form.sell_price),
        category: form.category,
        weight_oz: parseFloat(form.weight_oz),
      }) as CalcResult;
      setResult(data);
    } catch {
      // Fallback: local calculation
      const buyP = parseFloat(form.buy_price);
      const sellP = parseFloat(form.sell_price);
      const referralFee = sellP * 0.15;
      const fbaFee = 3.22;
      const totalFees = referralFee + fbaFee;
      const netProfit = sellP - buyP - totalFees;
      setResult({
        gross_profit: sellP - buyP,
        net_profit: netProfit,
        roi_percent: Math.round((netProfit / buyP) * 100 * 10) / 10,
        referral_fee: referralFee,
        fba_fee: fbaFee,
        total_fees: totalFees,
        margin_percent: Math.round((netProfit / sellP) * 100 * 10) / 10,
      });
    } finally {
      setLoading(false);
    }
  };

  const profitColor = result && result.net_profit > 0 ? 'text-green-600' : 'text-red-600';

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-6 py-3 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold text-blue-700">ArbiEdge</Link>
        <div className="flex gap-6 items-center">
          <Link href="/dashboard" className="text-gray-600 hover:text-blue-600">Dashboard</Link>
          <Link href="/deals" className="text-gray-600 hover:text-blue-600">Deals</Link>
          <Link href="/calculator" className="text-blue-600 font-medium">Calculator</Link>
          <button onClick={signOut} className="text-sm text-red-500 hover:text-red-700">Sign out</button>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-6">ROI Calculator</h1>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Input Form */}
          <div className="bg-white rounded-xl border p-6">
            <h2 className="text-lg font-semibold mb-4">Product Details</h2>
            <form onSubmit={handleCalculate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Buy Price ($)</label>
                <input
                  type="number" step="0.01" value={form.buy_price}
                  onChange={e => setForm({...form, buy_price: e.target.value})}
                  className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  placeholder="18.99" required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Sell Price ($)</label>
                <input
                  type="number" step="0.01" value={form.sell_price}
                  onChange={e => setForm({...form, sell_price: e.target.value})}
                  className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  placeholder="34.99" required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Category</label>
                <select
                  value={form.category}
                  onChange={e => setForm({...form, category: e.target.value})}
                  className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                >
                  {CATEGORIES.map(c => <option key={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Weight (oz)</label>
                <input
                  type="number" step="0.1" value={form.weight_oz}
                  onChange={e => setForm({...form, weight_oz: e.target.value})}
                  className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  placeholder="8.0"
                />
              </div>
              <button
                type="submit" disabled={loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Calculating...' : 'Calculate ROI'}
              </button>
            </form>
          </div>

          {/* Results */}
          <div className="bg-white rounded-xl border p-6">
            <h2 className="text-lg font-semibold mb-4">Results</h2>
            {result ? (
              <div className="space-y-3">
                <div className="p-4 bg-gray-50 rounded-lg text-center">
                  <p className="text-sm text-gray-500">Net Profit</p>
                  <p className={`text-3xl font-bold ${profitColor}`}>${result.net_profit?.toFixed(2)}</p>
                  <p className={`text-lg font-semibold ${profitColor}`}>ROI: {result.roi_percent}%</p>
                </div>
                {[
                  { label: 'Gross Profit', value: `$${result.gross_profit?.toFixed(2)}` },
                  { label: 'Referral Fee (15%)', value: `$${result.referral_fee?.toFixed(2)}` },
                  { label: 'FBA Fulfillment Fee', value: `$${result.fba_fee?.toFixed(2)}` },
                  { label: 'Total Fees', value: `$${result.total_fees?.toFixed(2)}` },
                  { label: 'Profit Margin', value: `${result.margin_percent}%` },
                ].map(item => (
                  <div key={item.label} className="flex justify-between text-sm py-2 border-b last:border-0">
                    <span className="text-gray-600">{item.label}</span>
                    <span className="font-semibold">{item.value}</span>
                  </div>
                ))}
                <div className={`mt-4 p-3 rounded-lg text-center text-sm font-medium ${
                  result.roi_percent >= 30 ? 'bg-green-50 text-green-700' :
                  result.roi_percent >= 15 ? 'bg-yellow-50 text-yellow-700' :
                  'bg-red-50 text-red-700'
                }`}>
                  {result.roi_percent >= 30 ? 'Excellent deal - proceed!' :
                   result.roi_percent >= 15 ? 'Decent deal - review carefully' :
                   'Low ROI - consider skipping'}
                </div>
              </div>
            ) : (
              <div className="text-center text-gray-400 py-12">
                <p className="text-4xl mb-3">📊</p>
                <p>Enter product details and click Calculate to see your FBA profit breakdown</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
