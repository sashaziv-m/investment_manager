import { useState, useEffect } from 'react';
import { fetchInsiderTrades, InsiderTrade } from '@/app/lib/api';

export default function InsiderTrades() {
    const [trades, setTrades] = useState<InsiderTrade[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function loadData() {
            const data = await fetchInsiderTrades();
            setTrades(data);
            setIsLoading(false);
        }
        loadData();
    }, []);

    if (isLoading) {
        return (
            <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-neutral-700 dark:bg-neutral-800 animate-pulse">
                <div className="h-6 w-48 bg-gray-200 rounded mb-4"></div>
                <div className="space-y-3">
                    <div className="h-4 w-full bg-gray-200 rounded"></div>
                    <div className="h-4 w-full bg-gray-200 rounded"></div>
                    <div className="h-4 w-full bg-gray-200 rounded"></div>
                </div>
            </div>
        );
    }

    return (
        <div className="rounded-xl border border-gray-200 bg-white shadow-sm dark:border-neutral-700 dark:bg-neutral-800">
            <div className="p-6 border-b border-gray-100 dark:border-neutral-700">
                <h3 className="text-lg font-medium text-neutral-900 dark:text-white">Insider Trades (Last 30 Days)</h3>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                    <thead className="bg-gray-50 dark:bg-neutral-900/50 text-neutral-500">
                        <tr>
                            <th className="px-6 py-3 font-medium">Date</th>
                            <th className="px-6 py-3 font-medium">Tick</th>
                            <th className="px-6 py-3 font-medium">Insider</th>
                            <th className="px-6 py-3 font-medium">Title</th>
                            <th className="px-6 py-3 font-medium">Type</th>
                            <th className="px-6 py-3 font-medium">Value</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 dark:divide-neutral-700">
                        {trades.map((trade, idx) => (
                            <tr key={idx} className="hover:bg-gray-50 dark:hover:bg-neutral-800/50">
                                <td className="px-6 py-3 text-neutral-500 whitespace-nowrap">{trade.date}</td>
                                <td className="px-6 py-3 font-medium text-neutral-900 dark:text-white">{trade.symbol}</td>
                                <td className="px-6 py-3 text-neutral-900 dark:text-white font-medium">
                                    {trade.insider}
                                </td>
                                <td className="px-6 py-3 text-neutral-600 dark:text-neutral-400 text-sm">
                                    {trade.relation}
                                </td>
                                <td className="px-6 py-3">
                                    <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset ${trade.trade_type === 'Buy'
                                        ? 'bg-green-50 text-green-700 ring-green-600/20 dark:bg-green-900/30 dark:text-green-400 dark:ring-green-900/10'
                                        : 'bg-red-50 text-red-700 ring-red-600/20 dark:bg-red-900/30 dark:text-red-400 dark:ring-red-900/10'
                                        }`}>
                                        {trade.trade_type}
                                    </span>
                                </td>
                                <td className="px-6 py-3 text-neutral-600 dark:text-neutral-400">
                                    {typeof trade.value === 'number'
                                        ? `$${(trade.value / 1000000).toFixed(1)}M`
                                        : trade.value
                                    }
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
