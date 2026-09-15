const DEVICE_ID = "trailer-001";
const POLL_INTERVAL_MS = 1000;

async function fetchDeviceState(){
    const response = await fetch(
        `api/device/${DEVICE_ID}/state`
    );

    if(!response.ok){
        throw new Error('Failed to retrieve device state: ${response.status}');
    }

    return response.json();
}

function updateDashboard(state) {
    document.getElementById("device-id").textContent = state.device_id;
    document.getElementById("speed").textContent = state.speed_mph.toFixed(1);
    document.getElementById("lateral-acceleration").textContent = state.accelerometer.y.toFixed(3);
    document.getElementById("yaw-rate").textContent = state.gyroscope.yaw_rate.toFixed(2);
    
    const timestamp = new Date(state.timestamp);

    document.getElementById("last-telemetry").textContent = timestamp.toLocaleTimeString();

}

function setConnectionStatus(connected){
    const indicator = document.getElementById("connection-indicator");

    const status = document.getElementById("connection-status");

    if(connected){
        indicator.style.background = "#22c55e";
        status.textContent = "Online";
    } else{
        indicator.style.background = "#ef4444";
        status.textContent = "Offline";
    }
}

async function refreshDashboard() {
    try {
        const state = await fetchDeviceState();

        updateDashboard(state);
        setConnectionStatus(true);
    }catch (error) {
        console.error(error);
        setConnectionStatus(false);
    }
}

refreshDashboard();

setInterval(
    refreshDashboard,
    POLL_INTERVAL_MS
);