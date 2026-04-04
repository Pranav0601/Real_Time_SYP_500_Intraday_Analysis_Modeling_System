async function updateUI() {
    const data = await fetchPrediction();

    if (data.error) {
        document.getElementById("signal").innerText = data.error;
        return;
    }

    document.getElementById("timestamp").innerText = data.timestamp;
    document.getElementById("low").innerText = Number(data.low_so_far).toFixed(2);

    let prob = Number(data.probability);
    let probEl = document.getElementById("prob");

    probEl.innerText = prob.toFixed(3);

    if (prob > 0.75) {
        document.getElementById("signal").innerText = "LOW LIKELY SET";
        probEl.className = "value prob-high";
    } else if (prob > 0.55) {
        document.getElementById("signal").innerText = "UNCERTAIN";
        probEl.className = "value prob-medium";
    } else {
        document.getElementById("signal").innerText = "LOW NOT SET";
        probEl.className = "value prob-low";
    }

    if (data.status === "LIVE") {
        document.getElementById("status").innerText = "LIVE";
        document.getElementById("status").className = "value status-live";
    } else {
        document.getElementById("status").innerText = "MARKET CLOSED / STALE";
        document.getElementById("status").className = "value status-stale";
    }
}

async function updateCharts() {
    const history = await fetchHistory();
    if (history) {
        updateModelChart(history.timestamps, history.lows, history.probs);
    }

    const market = await fetchMarketData();
    if (market) {
        updateMarketChart(market.timestamps, market.prices);
    }
}

// INIT
updateUI();
updateCharts();

// REFRESH LOOP
setInterval(() => {
    updateUI();
    updateCharts();
}, 10000);