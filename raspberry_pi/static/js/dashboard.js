async function updateDashboard() {
    try {
        const response = await fetch("/api/latest");

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();

        if (data.status === "no_data") {
            setConnection(false);
            return;
        }

        setConnection(true);

        document.getElementById("methane").textContent =
            data.methane_raw ?? "--";

        document.getElementById("fsr").textContent =
            data.force_raw ?? "--";

        document.getElementById("flex").textContent =
            data.flex_raw ?? "--";

        document.getElementById("moisture").textContent =
            data.moisture_raw ?? "--";

        document.getElementById("distance").textContent =
            data.roof_distance_cm >= 0
                ? data.roof_distance_cm.toFixed(2)
                : "--";

        document.getElementById("accel-x").textContent =
            data.accel_x ?? "--";

        document.getElementById("accel-y").textContent =
            data.accel_y ?? "--";

        document.getElementById("accel-z").textContent =
            data.accel_z ?? "--";


        const score = data.risk_score ?? 0;
        const level = data.risk_level ?? "LOW";

        document.getElementById("risk-score").textContent = score;

        let emoji = "🟢";

        if (level === "MEDIUM") {
            emoji = "🟡";
        } else if (level === "HIGH") {
            emoji = "🟠";
        } else if (level === "CRITICAL") {
            emoji = "🔴";
        }

        document.getElementById("risk-level").textContent =
            emoji + " " + level;


        document.getElementById("activity-methane").textContent =
            "Live sensor reading";

        document.getElementById("activity-force").textContent =
            "Live sensor reading";

        document.getElementById("activity-flex").textContent =
            "Live sensor reading";

        document.getElementById("activity-moisture").textContent =
            "Live sensor reading";

        document.getElementById("activity-distance").textContent =
            "Live sensor reading";


        const timestamp = data.timestamp;

        if (timestamp) {
            document.getElementById("last-update").textContent =
                timestamp.replace("T", " ");
        }

    } catch (error) {

        console.error("Dashboard update failed:", error);

        setConnection(false);
    }
}


function setConnection(connected) {

    const dot = document.getElementById("connection-status");
    const text = document.getElementById("connection-text");

    if (connected) {

        dot.style.background = "#48d597";
        dot.style.boxShadow =
            "0 0 10px rgba(72, 213, 151, 0.5)";

        text.textContent = "Connected";

    } else {

        dot.style.background = "#ff5c5c";
        dot.style.boxShadow =
            "0 0 10px rgba(255, 92, 92, 0.5)";

        text.textContent = "Disconnected";
    }
}


updateDashboard();

setInterval(updateDashboard, 1000);