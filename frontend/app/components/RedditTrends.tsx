import { useState, useEffect } from 'react';
import { fetchRedditTrends, RedditTrend } from '@/app/lib/api';

export default function RedditTrends() {
    const [trends, setTrends] = useState<RedditTrend[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function loadData() {
            const data = await fetchRedditTrends();
            setTrends(data);
            setIsLoading(false);
        }
        loadData();
    }, []);

    if (isLoading) {
        return (
            <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-neutral-700 dark:bg-neutral-800 animate-pulse">
                <div className="h-6 w-32 bg-gray-200 rounded mb-4"></div>
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
            <div className="flex items-center justify-between p-6 border-b border-gray-100 dark:border-neutral-700">
                <h3 className="text-lg font-medium text-neutral-900 dark:text-white">Reddit Trends (r/WSB)</h3>
                {/* Mock/Live Indicator */}
                <span className="text-xs px-2 py-1 bg-gray-100 dark:bg-neutral-700 rounded text-neutral-500">
                    Last 50 Hot Posts
                </span>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                    <thead className="bg-gray-50 dark:bg-neutral-900/50 text-neutral-500">
                        <tr>
                            <th className="px-6 py-3 font-medium">Symbol</th>
                            <th className="px-6 py-3 font-medium">Mentions</th>
                            <th className="px-6 py-3 font-medium">Sentiment</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 dark:divide-neutral-700">
                        {trends.map((item) => (
                            <tr key={item.symbol} className="hover:bg-gray-50 dark:hover:bg-neutral-800/50">
                                <td className="px-6 py-3 font-medium text-neutral-900 dark:text-white">{item.symbol}</td>
                                <td className="px-6 py-3 text-neutral-600 dark:text-neutral-400">{item.mentions}</td>
                                <td className="px-6 py-3">
                                    <div className="flex items-center space-x-2">
                                        <span className={`h-2.5 w-2.5 rounded-full ${item.sentiment > 0.1 ? 'bg-green-500' :
                                                item.sentiment < -0.1 ? 'bg-red-500' : 'bg-gray-400'
                                            }`} />
                                        <span className="text-neutral-600 dark:text-neutral-400">
                                            {item.sentiment > 0 ? '+' : ''}{item.sentiment}
                                        </span>
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {trends.length === 0 && (
                            <tr>
                                <td colSpan={3} className="px-6 py-8 text-center text-neutral-500 italic">
                                    No trending tickers found.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
