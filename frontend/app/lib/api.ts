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
