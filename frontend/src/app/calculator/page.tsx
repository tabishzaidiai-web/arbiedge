'use client';
import { useState } from 'react';
import Link from 'next/link';

export default function CalculatorPage() {
  const [buyPrice, setBuyPrice] = useState('18.99');
  const [sellPrice, setSellPrice] = useState('34.99');
  const [weight, setWeight] = useState('1.0');
  const [result, setResult] = useState(null as any);

  const calculate = () => {
    const buy = parseFloat(buyPrice);
    const sell = parseFloat(sellPrice);
    const w = parseFloat(weight);
    const referralFee = +(sell * 0.15).toFixed(2);
    const fulfillmentFee = +(w <= 1 ? 3.86 : w <= 2 ? 5.40 : 5.40 + 0.40 * (w - 2)).toFixed(2);
    const storageFee = 0.45;
    const prepCost = 0.50;
    const shippingCost = +(w * 0.40).toFixed(2);
    const totalCosts = +(buy + referralFee + fulfillmentFee + storageFee + prepCost + shippingCost).toFixed(2);
    const netProfit = +(sell - totalCosts).toFixed(2);
    const roi = +((netProfit / buy) * 100).toFixed(1);
    setResult({ referralFee, fulfillmentFee, storageFee, prepCost, shippingCost, totalCosts, netProfit, roi });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-6 py-3 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold text-blue-700">ArbiEdge</Link>
        <div className="flex gap-6 text-sm">
          <Link href="/dashboard" className="text-gray-600">Dashboard</Link>
          <Link href="/deals" className="text-gray-600">Deals</Link>
          <Link href="/calculator" className="text-blue-600 font-medium">Calculator</Link>
        </div>
      </nav>
      <div className="max-w-3xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-6">ROI Calculator</h1>
        <div className="bg-white rounded-xl border p-6">
          <div className="grid md:grid-cols-2 gap-4 mb-6">
            <div><label className="block text-sm font-medium mb-1">Buy Price ($)</label><input type="number" value={buyPrice} onChange={e => setBuyPrice(e.target.value)} className="w-full border rounded-lg px-3 py-2" /></div>
            <div><label className="block text-sm font-medium mb-1">Sell Price ($)</label><input type="number" value={sellPrice} onChange={e => setSellPrice(e.target.value)} className="w-full border rounded-lg px-3 py-2" /></div>
            <div><label className="block text-sm font-medium mb-1">Weight (lbs)</label><input type="number" value={weight} onChange={e => setWeight(e.target.value)} className="w-full border rounded-lg px-3 py-2" /></div>
          </div>
          <button onClick={calculate} className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700">Calculate Profit</button>
          {result && (
            <div className="mt-6 border-t pt-6">
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="text-center p-4 bg-green-50 rounded-lg"><p className="text-sm text-gray-600">Net Profit</p><p className="text-3xl font-bold text-green-600">${'{'}result.netProfit{'}'}</p></div>
                <div className="text-center p-4 bg-blue-50 rounded-lg"><p className="text-sm text-gray-600">ROI</p><p className="text-3xl font-bold text-blue-600">{result.roi}%</p></div>
              </div>
              <h3 className="font-semibold mb-3">Fee Breakdown</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between"><span className="text-gray-600">Referral Fee</span><span>${'{'}result.referralFee{'}'}</span></div>
                <div className="flex justify-between"><span className="text-gray-600">Fulfillment Fee</span><span>${'{'}result.fulfillmentFee{'}'}</span></div>
                <div className="flex justify-between"><span className="text-gray-600">Storage Fee</span><span>${'{'}result.storageFee{'}'}</span></div>
                <div className="flex justify-between"><span className="text-gray-600">Prep Cost</span><span>${'{'}result.prepCost{'}'}</span></div>
                <div className="flex justify-between"><span className="text-gray-600">Shipping</span><span>${'{'}result.shippingCost{'}'}</span></div>
                <div className="flex justify-between border-t pt-2 font-semibold"><span>Total Costs</span><span>${'{'}result.totalCosts{'}'}</span></div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
