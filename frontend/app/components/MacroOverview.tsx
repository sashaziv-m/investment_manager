import { useState, useEffect } from 'react';
import { fetchMacroData, MacroData } from '@/app/lib/api';

export default function MacroOverview() {
    const [data, setData] = useState<MacroData[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function loadData() {
            const result = await fetchMacroData();
            setData(result);
            setIsLoading(false);
        }
        loadData();
    }, []);

    if (isLoading) return <div className="animate-pulse h-20 bg-gray-100 rounded-lg"></div>;

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            {data.map((item) => (
                <div key={item.symbol} className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm dark:border-neutral-700 dark:bg-neutral-800">
                    <div className="text-xs text-neutral-500 uppercase tracking-wider font-semibold">{item.name}</div>
                    <div className="mt-1 flex items-baseline gap-2">
                        <span className="text-xl font-bold text-neutral-900 dark:text-white">
                            {item.price.toFixed(2)}
                            {item.symbol === '^TNX' ? '%' : ''}
                        </span>
                        <span className={`text-xs font-medium ${item.change >= 0 ? 'text-green-600' : 'text-red-600'
                            }`}>
                            {item.change > 0 ? '+' : ''}{item.change.toFixed(2)}%
                        </span>
                    </div>
                </div>
            ))}
        </div>
    );
}
