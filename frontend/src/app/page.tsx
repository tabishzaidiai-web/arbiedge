import Link from 'next/link';

export default function LandingPage() {
  const features = [
    { title: 'AI Deal Scoring', desc: 'Every deal scored 0-100 based on ROI, BSR velocity, competition, price stability, and availability.' },
    { title: 'Cross-Platform Pricing', desc: 'Real-time price checks across Walmart, Target, Home Depot, Costco and more.' },
    { title: 'FBA Fee Calculator', desc: 'Exact profit calculations including referral fees, fulfillment, storage, prep, and shipping costs.' },
    { title: 'Daily Deal Digest', desc: 'Wake up to a curated list of the best deals matching your ROI thresholds.' },
    { title: 'Best Seller Scanning', desc: 'Automated scanning of Amazon Best Sellers, Movers & Shakers, and Hot New Releases.' },
    { title: 'Smart Alerts', desc: 'Get notified instantly when high-scoring deals appear in your preferred categories.' },
  ];

  const plans = [
    { name: 'Starter', price: '$49', features: ['Up to 50 deals/day', 'Basic deal scoring', 'Daily email digest', '5 category filters', 'Standard support'] },
    { name: 'Pro', price: '$99', popular: true, features: ['Unlimited deals', 'Advanced AI scoring', 'Real-time deal feed', 'Priority scan queue', 'Watchlist alerts', 'API access'] },
    { name: 'Enterprise', price: '$249', features: ['Everything in Pro', 'Multi-user access', 'White-label reports', 'Custom integrations', 'Dedicated account manager'] },
  ];

  return (
    <div className="min-h-screen">
      <nav className="border-b bg-white px-6 py-4 flex items-center justify-between max-w-7xl mx-auto">
        <div className="text-2xl font-bold text-blue-700">ArbiEdge</div>
        <div className="flex gap-4 items-center">
          <Link href="/sign-in" className="text-gray-600 hover:text-gray-900">Sign In</Link>
          <Link href="/sign-up" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">Get Started Free</Link>
        </div>
      </nav>
      <section className="max-w-7xl mx-auto px-6 py-24 text-center">
        <div className="inline-block bg-blue-50 text-blue-700 text-sm font-medium px-3 py-1 rounded-full mb-6">AI-Powered Deal Validation</div>
        <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-6">
          Stop Guessing.<br /><span className="text-blue-600">Start Profiting.</span>
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-10">
          ArbiEdge scans thousands of products, cross-references prices across retailers, and delivers validated arbitrage deals with AI-scored profit confidence.
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/sign-up" className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700">Start Free Trial</Link>
          <Link href="#pricing" className="border border-gray-300 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gray-100">View Pricing</Link>
        </div>
      </section>
      <section className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-12">Everything You Need to Source Smarter</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((f, i) => (
              <div key={i} className="p-6 border rounded-xl hover:shadow-lg transition">
                <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
                <p className="text-gray-600">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      <section id="pricing" className="py-20">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-4">Simple, Transparent Pricing</h2>
          <p className="text-gray-600 text-center mb-12">Start free. Upgrade when you are ready to scale.</p>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {plans.map((plan, i) => (
              <div key={i} className={`p-8 rounded-xl border-2 ${plan.popular ? 'border-blue-600 shadow-xl relative' : 'border-gray-200'}`}>
                {plan.popular && <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full">MOST POPULAR</div>}
                <h3 className="text-xl font-bold">{plan.name}</h3>
                <div className="mt-4"><span className="text-4xl font-bold">{plan.price}</span><span className="text-gray-500">/month</span></div>
                <ul className="mt-6 space-y-3">{plan.features.map((f, j) => <li key={j} className="flex items-center gap-2"><span className="text-green-500">&#10003;</span>{f}</li>)}</ul>
                <button className={`mt-8 w-full py-3 rounded-lg font-semibold ${plan.popular ? 'bg-blue-600 text-white hover:bg-blue-700' : 'border border-gray-300 hover:bg-gray-100'}`}>Get Started</button>
              </div>
            ))}
          </div>
        </div>
      </section>
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <div className="text-xl font-bold text-white mb-4">ArbiEdge</div>
          <p>AI-Powered Deal Validation for Amazon Online Arbitrage</p>
          <p className="mt-4 text-sm">&copy; 2026 ArbiEdge. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
