import { useState, useEffect } from 'react';
import { runScan, fetchRedditTrends, fetchInsiderTrades, ScanResult, RedditTrend, InsiderTrade } from '@/app/lib/api';

type Opportunity = {
    symbol: string;
    reasons: string[];
    score: number;
};

export default function Opportunities() {
    const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function loadData() {
            try {
                // Fetch all data in parallel
                const [scanResults, redditTrends, insiderTrades] = await Promise.all([
                    runScan(),
                    fetchRedditTrends(),
                    fetchInsiderTrades()
                ]);

                // Aggregate signals
                const signals = new Map<string, string[]>();

                // 1. Momentum Signals (RSI > 70 or < 30 usually, but here just presence in scanner implies momentum)
                scanResults.forEach(item => {
                    const existing = signals.get(item.symbol) || [];
                    if (item.momentum_score > 70) existing.push(`High Momentum (RSI ${item.rsi_14.toFixed(1)})`);
                    else if (item.momentum_score < 30) existing.push(`Oversold (RSI ${item.rsi_14.toFixed(1)})`);
                    // Just adding generic momentum tag if it's in the list and not extreme
                    else existing.push(`Momentum Score: ${item.momentum_score.toFixed(0)}`);

                    signals.set(item.symbol, existing);
                });

                // 2. Reddit Signals
                redditTrends.forEach(item => {
                    const existing = signals.get(item.symbol) || [];
                    existing.push(`Social Sentiment: ${item.sentiment > 0 ? 'Positive' : 'Negative'} (${item.mentions} mentions)`);
                    signals.set(item.symbol, existing);
                });

                // 3. Insider Signals
                insiderTrades.forEach(item => {
                    const existing = signals.get(item.symbol) || [];
                    // Only count significant buys
                    if (item.trade_type === 'Buy' || item.trade_type.includes('Purchase')) {
                        existing.push(`Insider Buying (${item.relation})`);
                    }
                    signals.set(item.symbol, existing);
                });

                // Convert to array and filter for "Opportunities" (at least one valid signal)
                const opps: Opportunity[] = Array.from(signals.entries()).map(([symbol, reasons]) => ({
                    symbol,
                    reasons,
                    score: reasons.length // Simple scoring: number of signals
                }))
                    .filter(o => o.reasons.length > 0)
                    .sort((a, b) => b.score - a.score); // Sort by number of signals

                setOpportunities(opps);
            } catch (error) {
                console.error("Failed to load opportunities", error);
            } finally {
                setIsLoading(false);
            }
        }
        loadData();
    }, []);

    if (isLoading) return null; // Or a skeleton

    // Only show if we have compelling opportunities (score > 1 or specific high conviction)
    const highConviction = opportunities.filter(o => o.score >= 2);
    const notable = opportunities.filter(o => o.score === 1).slice(0, 5); // Top 5 single signals

    return (
        <div className="mb-8 space-y-6">
            {highConviction.length > 0 && (
                <div className="rounded-xl border border-yellow-200 bg-yellow-50 p-6 dark:border-yellow-900/50 dark:bg-yellow-900/20">
                    <div className="flex items-center gap-2 mb-4">
                        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-yellow-100 dark:bg-yellow-900/40 text-yellow-600 dark:text-yellow-400">
                            ★
                        </span>
                        <h2 className="text-xl font-bold text-yellow-800 dark:text-yellow-100">High Conviction Opportunities</h2>
                    </div>
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        {highConviction.map((opp) => (
                            <div key={opp.symbol} className="rounded-lg bg-white p-4 shadow-sm dark:bg-neutral-800 border border-yellow-100 dark:border-yellow-900/30">
                                <div className="flex justify-between items-start">
                                    <h3 className="text-lg font-bold text-neutral-900 dark:text-white">{opp.symbol}</h3>
                                    <span className="inline-flex items-center rounded-full bg-yellow-100 px-2.5 py-0.5 text-xs font-medium text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300">
                                        {opp.score} Signals
                                    </span>
                                </div>
                                <div className="mt-2 space-y-1">
                                    {opp.reasons.map((reason, idx) => (
                                        <div key={idx} className="text-sm text-neutral-600 dark:text-neutral-300 flex items-center gap-1.5">
                                            <span className="h-1.5 w-1.5 rounded-full bg-yellow-500"></span>
                                            {reason}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* If no high conviction, or just to show the grid of single interesting items */}
            {highConviction.length === 0 && notable.length > 0 && (
                <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-neutral-700 dark:bg-neutral-800">
                    <h3 className="text-lg font-medium text-neutral-900 dark:text-white mb-4">Notable Signals</h3>
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                        {notable.map((opp) => (
                            <div key={opp.symbol} className="rounded-lg border border-gray-100 bg-gray-50 p-3 dark:border-neutral-700 dark:bg-neutral-900/50">
                                <div className="font-semibold text-neutral-900 dark:text-white">{opp.symbol}</div>
                                <div className="text-xs text-neutral-500 dark:text-neutral-400 mt-1">{opp.reasons[0]}</div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
