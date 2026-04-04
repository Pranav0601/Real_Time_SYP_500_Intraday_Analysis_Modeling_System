const API_BASE = "http://127.0.0.1:8000";

async function fetchPrediction() {
    const res = await fetch(`${API_BASE}/predict`);
    return await res.json();
}

async function fetchHistory(limit = 100) {
    const res = await fetch(`${API_BASE}/history?limit=${limit}`);
    const data = await res.json();

    if (!data.data) return null;

    return {
        timestamps: data.data.map(d => d.timestamp).reverse(),
        lows: data.data.map(d => d.low_so_far).reverse(),
        probs: data.data.map(d => d.probability).reverse()
    };
}

async function fetchMarketData() {
    const res = await fetch(`${API_BASE}/market`);
    const data = await res.json();

    if (!data.data) return null;

    return {
        timestamps: data.data.map(d => d.timestamp),
        prices: data.data.map(d => d.close)
    };
}