'use client';
import Link from 'next/link';

export default function DealsPage() {
  const deals = [
    { id: 1, title: 'Wireless Earbuds Pro', asin: 'B09XYZ1234', source: 'Walmart', buy: 18.99, sell: 34.99, roi: 52, profit: 8.42, score: 92, label: 'A+ STRONG BUY' },
    { id: 2, title: 'Kitchen Scale Digital', asin: 'B08ABC5678', source: 'Target', buy: 12.49, sell: 24.99, roi: 67, profit: 7.20, score: 88, label: 'A BUY' },
    { id: 3, title: 'LED Desk Lamp USB', asin: 'B07DEF9012', source: 'Walmart', buy: 22.00, sell: 39.99, roi: 45, profit: 9.15, score: 85, label: 'A BUY' },
    { id: 4, title: 'Phone Case Premium', asin: 'B06GHI3456', source: 'Target', buy: 8.99, sell: 19.99, roi: 78, profit: 5.80, score: 82, label: 'A BUY' },
    { id: 5, title: 'Yoga Mat Extra Thick', asin: 'B05JKL7890', source: 'Walmart', buy: 15.99, sell: 29.99, roi: 55, profit: 6.90, score: 79, label: 'B+ CONSIDER' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-6 py-3 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold text-blue-700">ArbiEdge</Link>
        <div className="flex gap-6 text-sm">
          <Link href="/dashboard" className="text-gray-600">Dashboard</Link>
          <Link href="/deals" className="text-blue-600 font-medium">Deals</Link>
          <Link href="/calculator" className="text-gray-600">Calculator</Link>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-6">Deal Feed</h1>
        <div className="space-y-4">
          {deals.map((deal) => (
            <div key={deal.id} className="bg-white rounded-xl border p-5 hover:shadow-md transition">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold">{deal.title} <span className="ml-2 px-2 py-0.5 rounded text-xs font-bold bg-blue-100 text-blue-800">{deal.score} - {deal.label}</span></h3>
                  <p className="text-sm text-gray-500 mt-1">ASIN: {deal.asin} | Source: {deal.source}</p>
                </div>
                <div className="flex items-center gap-6 text-center">
                  <div><p className="text-xs text-gray-500">Buy</p><p className="font-semibold">${'{'}deal.buy{'}'}</p></div>
                  <div><p className="text-xs text-gray-500">Sell</p><p className="font-semibold">${'{'}deal.sell{'}'}</p></div>
                  <div><p className="text-xs text-gray-500">ROI</p><p className="font-semibold text-green-600">{deal.roi}%</p></div>
                  <div><p className="text-xs text-gray-500">Profit</p><p className="font-semibold">${'{'}deal.profit{'}'}</p></div>
                  <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700">Save</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
