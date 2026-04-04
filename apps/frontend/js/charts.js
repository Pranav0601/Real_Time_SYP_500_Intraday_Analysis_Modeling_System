let modelChart = null;
let marketChart = null;

function updateModelChart(timestamps, lows, probs) {
    const ctx = document.getElementById("modelChart");

    if (modelChart) modelChart.destroy();

    modelChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: timestamps,
            datasets: [
                { label: "Low So Far", data: lows },
                { label: "Probability", data: probs, yAxisID: 'y1' }
            ]
        },
        options: {
            scales: {
                y: { position: 'left' },
                y1: { position: 'right' }
            }
        }
    });
}

function updateMarketChart(timestamps, prices) {
    const ctx = document.getElementById("marketChart");

    if (marketChart) marketChart.destroy();

    marketChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: timestamps,
            datasets: [
                {
                    label: "SPY Price",
                    data: prices,
                    borderWidth: 2,
                    tension: 0.2
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false
            }
        }
    });
}