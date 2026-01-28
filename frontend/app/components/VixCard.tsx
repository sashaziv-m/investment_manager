import { VixData } from '@/app/lib/api';

type Props = {
    data: VixData | null;
    isLoading: boolean;
};

export default function VixCard({ data, isLoading }: Props) {
    if (isLoading) {
        return (
            <div className="rounded-xl border border-neutral-200 bg-white p-6 shadow-sm dark:border-neutral-700 dark:bg-neutral-800 animate-pulse">
                <div className="h-6 w-24 bg-gray-200 rounded mb-4"></div>
                <div className="h-10 w-16 bg-gray-200 rounded"></div>
            </div>
        );
    }

    if (!data || typeof data.price !== 'number') {
        return (
            <div className="rounded-xl border border-red-200 bg-red-50 p-6 shadow-sm dark:border-red-900 dark:bg-red-900/20">
                <h3 className="text-lg font-medium text-red-800 dark:text-red-200">VIX Unavailable</h3>
                <p className="text-sm text-red-600 dark:text-red-300">
                    {/* @ts-ignore - handling error response that matches VixData on explicit check */}
                    {(data as any)?.error || "Could not fetch data"}
                </p>
            </div>
        );
    }

    let statusColor = "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300";
    let statusBorder = "border-green-200 dark:border-green-800";

    if (data.status === 'Caution') {
        statusColor = "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300";
        statusBorder = "border-yellow-200 dark:border-yellow-800";
    } else if (data.status === 'Crisis') {
        statusColor = "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
        statusBorder = "border-red-200 dark:border-red-800";
    }

    return (
        <div className={`rounded-xl border ${statusBorder} bg-white dark:bg-neutral-800 p-6 shadow-sm`}>
            <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-neutral-500 dark:text-neutral-400">Market Volatility (VIX)</h3>
                <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${statusColor}`}>
                    {data.status}
                </span>
            </div>
            <div className="flex items-baseline">
                <span className="text-3xl font-bold text-neutral-900 dark:text-white">
                    {data.price.toFixed(2)}
                </span>
                <span className="ml-2 text-sm text-neutral-500">
                    Threshold: {data.thresholds.caution}
                </span>
            </div>
        </div>
    );
}
