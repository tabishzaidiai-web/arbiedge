'use client';
import { useState } from 'react';
import Link from 'next/link';

export default function Dashboard() {
  const kpis = { total_deals: 142, avg_roi: 47.3, total_saved: 28, deals_this_week: 34, total_profit: 2847.50 };
  const topDeals = [
    { title: 'Wireless Earbuds Pro', buy: 18.99, sell: 34.99, roi: 52, score: 92 },
    { title: 'Kitchen Scale Digital', buy: 12.49, sell: 24.99, roi: 67, score: 88 },
    { title: 'LED Desk Lamp', buy: 22.00, sell: 39.99, roi: 45, score: 85 },
    { title: 'Phone Case Premium', buy: 8.99, sell: 19.99, roi: 78, score: 82 },
    { title: 'Yoga Mat Extra Thick', buy: 15.99, sell: 29.99, roi: 55, score: 79 },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-6 py-3 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold text-blue-700">ArbiEdge</Link>
        <div className="flex gap-6 text-sm">
          <Link href="/dashboard" className="text-blue-600 font-medium">Dashboard</Link>
          <Link href="/deals" className="text-gray-600">Deals</Link>
          <Link href="/calculator" className="text-gray-600">Calculator</Link>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border"><p className="text-sm text-gray-500">Total Deals</p><p className="text-2xl font-bold mt-1">{kpis.total_deals}</p></div>
          <div className="bg-white rounded-xl p-4 border"><p className="text-sm text-gray-500">Avg ROI</p><p className="text-2xl font-bold mt-1">{kpis.avg_roi}%</p></div>
          <div className="bg-white rounded-xl p-4 border"><p className="text-sm text-gray-500">Saved</p><p className="text-2xl font-bold mt-1">{kpis.total_saved}</p></div>
          <div className="bg-white rounded-xl p-4 border"><p className="text-sm text-gray-500">This Week</p><p className="text-2xl font-bold mt-1">{kpis.deals_this_week}</p></div>
          <div className="bg-white rounded-xl p-4 border"><p className="text-sm text-gray-500">Profit</p><p className="text-2xl font-bold mt-1">${'{'}kpis.total_profit{'}'}</p></div>
        </div>
        <div className="bg-white rounded-xl border p-6">
          <h2 className="text-lg font-semibold mb-4">Top Deals Today</h2>
          <table className="w-full text-sm">
            <thead><tr className="border-b text-left text-gray-500"><th className="pb-2">Product</th><th className="pb-2">Buy</th><th className="pb-2">Sell</th><th className="pb-2">ROI</th><th className="pb-2">Score</th></tr></thead>
            <tbody>{topDeals.map((d, i) => (<tr key={i} className="border-b"><td className="py-3">{d.title}</td><td className="py-3">${'{'}d.buy{'}'}</td><td className="py-3">${'{'}d.sell{'}'}</td><td className="py-3 text-green-600">{d.roi}%</td><td className="py-3"><span className="px-2 py-1 rounded text-xs font-bold bg-blue-100 text-blue-800">{d.score}</span></td></tr>))}</tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
