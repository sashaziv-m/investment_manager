import { Holding } from '@/app/lib/api';

type Props = {
    holdings: Holding[];
    isLoading: boolean;
};

export default function PortfolioTable({ holdings, isLoading }: Props) {
    if (isLoading) {
        return <div className="animate-pulse h-32 bg-gray-100 rounded-xl dark:bg-neutral-800"></div>;
    }

    if (holdings.length === 0) {
        return (
            <div className="text-center p-8 bg-white rounded-xl border border-dashed border-gray-300 dark:bg-neutral-800 dark:border-neutral-700">
                <p className="text-neutral-500">No holdings yet.</p>
            </div>
        );
    }

    return (
        <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm dark:border-neutral-700 dark:bg-neutral-800">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                <thead className="bg-gray-50 dark:bg-neutral-900/50">
                    <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Symbol</th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Qty</th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Avg Price</th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Value</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-neutral-700">
                    {holdings.map((holding) => (
                        <tr key={holding.id}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                {holding.symbol}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-500 dark:text-gray-400">
                                {holding.quantity}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-500 dark:text-gray-400">
                                ${holding.avg_price.toFixed(2)}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 dark:text-white font-medium">
                                ${(holding.quantity * holding.avg_price).toFixed(2)}
                                {/* Note: In real app we would multiply by current_price if available */}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
