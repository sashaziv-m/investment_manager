import { useState } from 'react';

// Mock Alert Type
type AlertRule = {
    id: number;
    metric: string;
    operator: string;
    value: number;
    contact: string;
};

export default function AlertConfig() {
    const [alerts, setAlerts] = useState<AlertRule[]>([
        { id: 1, metric: 'VIX', operator: '>', value: 25, contact: 'email@example.com' }
    ]);

    return (
        <div className="rounded-xl border border-gray-200 bg-white shadow-sm dark:border-neutral-700 dark:bg-neutral-800 p-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-neutral-900 dark:text-white">Alert Rules</h3>
                <button className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700">
                    New Rule
                </button>
            </div>

            <div className="space-y-3">
                {alerts.map(alert => (
                    <div key={alert.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-neutral-900/50 rounded-lg">
                        <div className="text-sm">
                            <span className="font-semibold">{alert.metric}</span>
                            <span className="mx-2 text-neutral-500">{alert.operator}</span>
                            <span className="font-mono">{alert.value}</span>
                        </div>
                        <div className="text-xs text-neutral-500">
                            {alert.contact}
                        </div>
                    </div>
                ))}
                {alerts.length === 0 && <p className="text-sm text-neutral-500 italic">No active alerts.</p>}
            </div>
        </div>
    );
}
