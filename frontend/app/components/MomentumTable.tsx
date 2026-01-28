import { useState } from 'react';
import { runScan, ScanResult } from '@/app/lib/api';

export default function MomentumTable() {
    const [results, setResults] = useState<ScanResult[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleScan = async () => {
        setIsLoading(true);
        const data = await runScan();
        setResults(data);
        setIsLoading(false);
    };

    return (
        <div className="rounded-xl border border-gray-200 bg-white shadow-sm dark:border-neutral-700 dark:bg-neutral-800">
            <div className="flex items-center justify-between p-6 border-b border-gray-100 dark:border-neutral-700">
                <h3 className="text-lg font-medium text-neutral-900 dark:text-white">Momentum Scanner</h3>
                <button
                    onClick={handleScan}
                    disabled={isLoading}
                    className="px-3 py-1.5 text-sm bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
                >
                    {isLoading ? 'Scanning...' : 'Run Scan'}
                </button>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                    <thead className="bg-gray-50 dark:bg-neutral-900/50 text-neutral-500">
                        <tr>
                            <th className="px-6 py-3 font-medium">Symbol</th>
                            <th className="px-6 py-3 font-medium">Price</th>
                            <th className="px-6 py-3 font-medium">RSI (14)</th>
                            <th className="px-6 py-3 font-medium">Mom (20d)</th>
                            <th className="px-6 py-3 font-medium">Patterns</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 dark:divide-neutral-700">
                        {results.map((item) => (
                            <tr key={item.symbol} className="hover:bg-gray-50 dark:hover:bg-neutral-800/50">
                                <td className="px-6 py-3 font-medium text-neutral-900 dark:text-white">{item.symbol}</td>
                                <td className="px-6 py-3 text-neutral-600 dark:text-neutral-400">${item.price}</td>
                                <td className={`px-6 py-3 font-medium ${item.rsi_14 > 70 ? 'text-red-500' :
                                    item.rsi_14 < 30 ? 'text-green-500' : 'text-neutral-600'
                                    }`}>
                                    {item.rsi_14}
                                </td>
                                <td className={`px-6 py-3 font-medium ${item.momentum_score > 0 ? 'text-green-500' : 'text-red-500'}`}>
                                    {item.momentum_score}%
                                </td>
                                <td className="px-6 py-3">
                                    {item.golden_cross && (
                                        <span className="inline-flex items-center rounded-md bg-yellow-50 px-2 py-1 text-xs font-medium text-yellow-800 ring-1 ring-inset ring-yellow-600/20 dark:bg-yellow-900/30 dark:text-yellow-500">
                                            Golden Cross
                                        </span>
                                    )}
                                    {item.death_cross && (
                                        <span className="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10 dark:bg-gray-400/10 dark:text-gray-400">
                                            Death Cross
                                        </span>
                                    )}
                                </td>
                            </tr>
                        ))}
                        {results.length === 0 && !isLoading && (
                            <tr>
                                <td colSpan={4} className="px-6 py-8 text-center text-neutral-500 italic">
                                    Run a scan to find opportunities.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div >
    );
}
