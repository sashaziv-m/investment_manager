import { useState, useEffect } from 'react';
import { fetchAlerts, createAlert, deleteAlert, AlertRule } from '@/app/lib/api';

export default function AlertConfig() {
    const [alerts, setAlerts] = useState<AlertRule[]>([]);
    const [isCreating, setIsCreating] = useState(false);
    const [newRule, setNewRule] = useState<Partial<AlertRule>>({ metric: 'VIX', operator: '>', value: 20, contact: '', active: true });

    useEffect(() => {
        loadAlerts();
    }, []);

    async function loadAlerts() {
        const data = await fetchAlerts();
        setAlerts(data);
    }

    async function handleCreate() {
        if (!newRule.contact) return alert("Contact required");
        const created = await createAlert(newRule as any);
        if (created) {
            setAlerts([...alerts, created]);
            setIsCreating(false);
            setNewRule({ metric: 'VIX', operator: '>', value: 20, contact: '', active: true });
        }
    }

    async function handleDelete(id: number) {
        const success = await deleteAlert(id);
        if (success) {
            setAlerts(alerts.filter(a => a.id !== id));
        }
    }

    return (
        <div className="rounded-xl border border-gray-200 bg-white shadow-sm dark:border-neutral-700 dark:bg-neutral-800 p-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-medium text-neutral-900 dark:text-white">Alert Rules</h3>
                <button
                    onClick={() => setIsCreating(true)}
                    className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                    New Rule
                </button>
            </div>

            {isCreating && (
                <div className="mb-4 p-4 bg-gray-50 dark:bg-neutral-900/50 rounded-lg space-y-3">
                    <div className="grid grid-cols-3 gap-2">
                        <select
                            className="p-2 border rounded"
                            value={newRule.metric}
                            onChange={e => setNewRule({ ...newRule, metric: e.target.value })}
                        >
                            <option value="VIX">VIX</option>
                            <option value="RSI">RSI (SPY)</option>
                            <option value="PRICE">Price Target</option>
                        </select>
                        <select
                            className="p-2 border rounded"
                            value={newRule.operator}
                            onChange={e => setNewRule({ ...newRule, operator: e.target.value })}
                        >
                            <option value=">">&gt;</option>
                            <option value="<">&lt;</option>
                        </select>
                        <input
                            type="number"
                            className="p-2 border rounded"
                            value={newRule.value}
                            onChange={e => setNewRule({ ...newRule, value: parseFloat(e.target.value) })}
                        />
                    </div>
                    {newRule.metric === 'PRICE' && (
                        <input
                            type="text"
                            className="w-full p-2 border rounded uppercase"
                            placeholder="Symbol (e.g. NVDA)"
                            value={newRule.symbol || ''}
                            onChange={e => setNewRule({ ...newRule, symbol: e.target.value.toUpperCase() })}
                        />
                    )}
                    <input
                        type="email"
                        className="w-full p-2 border rounded"
                        placeholder="Email for alerts"
                        value={newRule.contact}
                        onChange={e => setNewRule({ ...newRule, contact: e.target.value })}
                    />
                    <div className="flex gap-2 justify-end">
                        <button onClick={() => setIsCreating(false)} className="text-sm text-neutral-500">Cancel</button>
                        <button onClick={handleCreate} className="px-3 py-1 text-sm bg-green-600 text-white rounded">Save</button>
                    </div>
                </div>
            )}

            <div className="space-y-3">
                {alerts.map(alert => (
                    <div key={alert.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-neutral-900/50 rounded-lg group">
                        <div className="text-sm">
                            <span className="font-semibold">{alert.metric}</span>
                            <span className="mx-2 text-neutral-500">{alert.operator}</span>
                            <span className="font-mono">{alert.value}</span>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="text-xs text-neutral-500">
                                {alert.contact}
                            </div>
                            <button
                                onClick={() => handleDelete(alert.id)}
                                className="text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                            >
                                ×
                            </button>
                        </div>
                    </div>
                ))}
                {alerts.length === 0 && <p className="text-sm text-neutral-500 italic">No active alerts.</p>}
            </div>
        </div>
    );
}
