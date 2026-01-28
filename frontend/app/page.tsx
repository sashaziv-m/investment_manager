"use client";

import { useEffect, useState } from 'react';
import { fetchVixData, VixData, fetchHoldings, Holding } from '@/app/lib/api';
import VixCard from '@/app/components/VixCard';
import PortfolioTable from '@/app/components/PortfolioTable';

export default function Home() {
  const [vixData, setVixData] = useState<VixData | null>(null);
  const [holdings, setHoldings] = useState<Holding[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      const [vix, portfolio] = await Promise.all([
        fetchVixData(),
        fetchHoldings()
      ]);
      setVixData(vix);
      setHoldings(portfolio);
      setIsLoading(false);
    }
    loadData();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center p-8 lg:p-24 bg-gray-50 dark:bg-neutral-900">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex mb-12">
        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-500 dark:from-blue-400 dark:to-indigo-300">
          Investment Dashboard
        </h1>
        <div className="mt-4 lg:mt-0 px-4 py-2 bg-white dark:bg-neutral-800 rounded-lg shadow-sm text-neutral-500">
          Status: <span className="text-green-500 font-semibold">Live</span>
        </div>
      </div>

      <div className="grid w-full max-w-5xl gap-6 lg:grid-cols-3">
        {/* Defense Column */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold text-neutral-700 dark:text-neutral-200 border-b pb-2">Defense</h2>
          <VixCard data={vixData} isLoading={isLoading} />

          <div className="opacity-100">
            <h3 className="text-sm font-medium mb-2 text-neutral-600 dark:text-neutral-400">Portfolio Holdings</h3>
            <PortfolioTable holdings={holdings} isLoading={isLoading} />
          </div>
        </div>

        {/* Offense Column */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold text-neutral-700 dark:text-neutral-200 border-b pb-2">Offense</h2>
          <div className="p-6 rounded-xl bg-white dark:bg-neutral-800 shadow-sm opacity-60">
            <h3 className="text-sm font-medium mb-2">Momentum Scanner</h3>
            <p className="text-xs text-neutral-500">Coming soon...</p>
          </div>
        </div>

        {/* Social Column */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold text-neutral-700 dark:text-neutral-200 border-b pb-2">Social</h2>
          <div className="p-6 rounded-xl bg-white dark:bg-neutral-800 shadow-sm opacity-60">
            <h3 className="text-sm font-medium mb-2">Reddit Trends</h3>
            <p className="text-xs text-neutral-500">Coming soon...</p>
          </div>
        </div>
      </div>
    </main>
  );
}
