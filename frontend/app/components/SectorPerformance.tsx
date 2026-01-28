import { useState, useEffect } from 'react';
import { fetchSectorPerformance, SectorData } from '@/app/lib/api';

export default function SectorPerformance() {
    const [sectors, setSectors] = useState<SectorData[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function loadData() {
            const data = await fetchSectorPerformance();
            setSectors(data);
            setIsLoading(false);
        }
        loadData();
    }, []);

    if (isLoading) return <div className="animate-pulse h-64 bg-gray-100 rounded-lg"></div>;

    // Top 5 Gainers/Losers
    const displaySectors = sectors.slice(0, 8);

    return (
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-neutral-700 dark:bg-neutral-800">
            <h3 className="text-lg font-medium text-neutral-900 dark:text-white mb-4">Sector Rotation (Daily)</h3>
            <div className="space-y-3">
                {displaySectors.map((sector) => (
                    <div key={sector.symbol} className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <span className="font-mono text-xs text-neutral-400 w-8">{sector.symbol}</span>
                            <span className="text-sm text-neutral-700 dark:text-neutral-300">{sector.name}</span>
                        </div>
                        <div className="flex items-center gap-2 w-32 justify-end">
                            <div className="h-2 w-16 bg-gray-100 rounded-full overflow-hidden flex justify-start dark:bg-neutral-700">
                                <div
                                    className={`h-full rounded-full ${sector.change >= 0 ? 'bg-green-500' : 'bg-red-500'}`}
                                    style={{ width: `${Math.min(Math.abs(sector.change) * 20, 100)}%` }} // Visual scaling
                                ></div>
                            </div>
                            <span className={`text-xs font-medium w-12 text-right ${sector.change >= 0 ? 'text-green-600' : 'text-red-600'
                                }`}>
                                {sector.change > 0 ? '+' : ''}{sector.change.toFixed(2)}%
                            </span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
