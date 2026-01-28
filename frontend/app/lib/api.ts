export const API_BASE_URL = 'http://localhost:8000/api/v1';

export type VixData = {
    symbol: string;
    price: number;
    status: 'Normal' | 'Caution' | 'Crisis';
    thresholds: {
        caution: number;
        crisis: number;
    };
};

export type Holding = {
    id: number;
    symbol: string;
    name?: string;
    quantity: number;
    avg_price: number;
    current_price?: number;
    asset_type: string;
};

export async function fetchVixData(): Promise<VixData | null> {
    try {
        const res = await fetch(`${API_BASE_URL}/vix`);
        if (!res.ok) {
            console.error('Failed to fetch VIX data', res.status);
            return null;
        }
        return await res.json();
    } catch (error) {
        console.error('Error fetching VIX data', error);
        return null;
    }
}

export async function fetchHoldings(): Promise<Holding[]> {
    try {
        const res = await fetch(`${API_BASE_URL}/portfolio/holdings`);
        if (!res.ok) return [];
        return await res.json();
    } catch (error) {
        console.error('Error fetching holdings', error);
        return [];
    }
}

export async function addHolding(symbol: string, quantity: number, price: number): Promise<boolean> {
    try {
        const res = await fetch(`${API_BASE_URL}/portfolio/holdings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol, quantity, avg_price: price, asset_type: 'Stock' })
        });
        return res.ok;
    } catch (error) {
        console.error('Error adding holding', error);
        return false;
    }
}

export type ScanResult = {
    symbol: string;
    price: number;
    rsi_14: number;
    sma_50: number;
    sma_200: number;
    momentum_score: number;
};

export async function runScan(): Promise<ScanResult[]> {
    try {
        const res = await fetch(`${API_BASE_URL}/scanner/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({}) // Use defaults
        });
        if (!res.ok) return [];
        return await res.json();
    } catch (error) {
        console.error('Error running scan', error);
        return [];
    }
}

export type RedditTrend = {
    symbol: string;
    mentions: number;
    sentiment: number;
};

export async function fetchRedditTrends(): Promise<RedditTrend[]> {
    try {
        const res = await fetch(`${API_BASE_URL}/social/trends`);
        if (!res.ok) return [];
        return await res.json();
    } catch (error) {
        console.error('Error fetching Reddit trends', error);
        return [];
    }
}

export type InsiderTrade = {
    symbol: string;
    insider: string;
    relation: string;
    trade_type: 'Buy' | 'Sell';
    price: number;
    quantity: number;
    value: string | number;
    date: string;
};

export async function fetchInsiderTrades(): Promise<InsiderTrade[]> {
    try {
        const res = await fetch(`${API_BASE_URL}/social/insider-trades`);
        if (!res.ok) return [];
        return await res.json();
    } catch (error) {
        console.error('Error fetching insider trades', error);
        return [];
    }
}

export type AlertRule = {
    id: number;
    metric: string;
    symbol?: string;
    operator: string;
    value: number;
    contact: string;
    active: boolean;
};

export async function fetchAlerts(): Promise<AlertRule[]> {
    try {
        const res = await fetch(`${API_BASE_URL}/alerts`);
        if (!res.ok) return [];
        return await res.json();
    } catch (error) {
        console.error('Error fetching alerts', error);
        return [];
    }
}

export async function createAlert(rule: Omit<AlertRule, 'id'>): Promise<AlertRule | null> {
    try {
        const res = await fetch(`${API_BASE_URL}/alerts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...rule, id: 0 }) // ID handled by backend
        });
        if (!res.ok) return null;
        return await res.json();
    } catch (error) {
        console.error('Error creating alert', error);
        return null;
    }
}

export async function deleteAlert(id: number): Promise<boolean> {
    try {
        const res = await fetch(`${API_BASE_URL}/alerts/${id}`, {
            method: 'DELETE'
        });
        return res.ok;
    } catch (error) {
        console.error('Error deleting alert', error);
        return false;
    }
}

export type OptionFlow = {
    symbol: string;
    type: 'Call' | 'Put';
    strike: number;
    expiration: string;
    volume: number;
    open_interest: number;
    vol_oi_ratio: number;
    last_price: number;
};

export async function fetchUnusualOptions(): Promise<OptionFlow[]> {
    try {
        const res = await fetch(`${API_BASE_URL}/options/unusual`);
        if (!res.ok) return [];
        return await res.json();
    } catch (error) {
        console.error('Error fetching options', error);
        return [];
    }
}
