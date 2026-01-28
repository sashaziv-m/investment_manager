import { useState, useEffect } from 'react';
import { fetchUnusualOptions, OptionFlow } from '@/app/lib/api';

export default function OptionsFlow() {
    const [flow, setFlow] = useState<OptionFlow[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function loadData() {
            const data = await fetchUnusualOptions();
            setFlow(data);
            setIsLoading(false);
        }
        loadData();
    }, []);

    return (
        <div className="rounded-xl border border-gray-200 bg-white shadow-sm dark:border-neutral-700 dark:bg-neutral-800">
            <div className="p-6 border-b border-gray-100 dark:border-neutral-700 flex justify-between items-center">
                <h3 className="text-lg font-medium text-neutral-900 dark:text-white">Unusual Options Activity</h3>
                <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full dark:bg-purple-900/30 dark:text-purple-300">
                    Vol {'>'} OI
                </span>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                    <thead className="bg-gray-50 dark:bg-neutral-900/50 text-neutral-500">
                        <tr>
                            <th className="px-6 py-3 font-medium">Ticker</th>
                            <th className="px-6 py-3 font-medium">Exp</th>
                            <th className="px-6 py-3 font-medium">Strike</th>
                            <th className="px-6 py-3 font-medium">Type</th>
                            <th className="px-6 py-3 font-medium">Vol / OI</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 dark:divide-neutral-700">
                        {flow.map((row, idx) => (
                            <tr key={idx} className="hover:bg-gray-50 dark:hover:bg-neutral-800/50">
                                <td className="px-6 py-3 font-medium text-neutral-900 dark:text-white">{row.symbol}</td>
                                <td className="px-6 py-3 text-neutral-500 whitespace-nowrap">{row.expiration}</td>
                                <td className="px-6 py-3 text-neutral-600 dark:text-neutral-400">${row.strike}</td>
                                <td className="px-6 py-3">
                                    <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset ${row.type === 'Call'
                                            ? 'bg-green-50 text-green-700 ring-green-600/20 dark:bg-green-900/30 dark:text-green-400 dark:ring-green-900/10'
                                            : 'bg-red-50 text-red-700 ring-red-600/20 dark:bg-red-900/30 dark:text-red-400 dark:ring-red-900/10'
                                        }`}>
                                        {row.type}
                                    </span>
                                </td>
                                <td className="px-6 py-3 text-neutral-600 dark:text-neutral-400">
                                    <div className="flex flex-col">
                                        <span className="font-mono">{row.volume}</span>
                                        <span className="text-xs text-neutral-400">Ratio: {row.vol_oi_ratio}x</span>
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {flow.length === 0 && !isLoading && (
                            <tr>
                                <td colSpan={5} className="px-6 py-8 text-center text-neutral-500 italic">
                                    No unusual activity found for watchlist tickers.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
            {isLoading && (
                <div className="p-6 space-y-3 animate-pulse">
                    <div className="h-4 bg-gray-200 rounded w-full"></div>
                    <div className="h-4 bg-gray-200 rounded w-full"></div>
                    <div className="h-4 bg-gray-200 rounded w-full"></div>
                </div>
            )}
        </div>
    );
}
