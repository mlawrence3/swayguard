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

async function fetchDeviceSettings(){
    const response = await fetch(
        `/api/devices/${DEVICE_ID}/settings`
    );

    if(!response.ok){
        throw new Error(
            `Failed to retrieve device settings: ${response.status}`
        );
    }
    return response.json();
}
async function loadSettings() {
    try {
        const settings = await fetchDeviceSettings();

        document.getElementById("warning-threshold").value =
            settings.warning_threshold_g;

        document.getElementById("alert-threshold").value =
            settings.alert_threshold_g;

        document.getElementById("brake-force").value =
            settings.brake_force_percent;
    } catch (error) {
        console.error(error);
    }
}
async function saveSettings(settings) {
    
    const response = await fetch(
        `/api/devices/${DEVICE_ID}/settings`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(settings)
        }
    );

    if (!response.ok) {
        throw new Error(
            `Failed to save device settings: ${response.status}`
        );
    }

    return response.json();
}
document
    .getElementById("save-settings")
    .addEventListener("click", async () => {
        const status =
            document.getElementById("settings-status");

        const settings = getSettingsFromForm();
        const validationError = validateSettings(settings);

        if (validationError) {
            status.textContent = validationError;
            return;
        }

        try {
            await saveSettings(settings);
            status.textContent = "Settings saved";
        } catch (error) {
            console.error(error);
            status.textContent = "Failed to save settings";
        }
    });

function validateSettings(settings) {
    if (settings.warning_threshold_g >= settings.alert_threshold_g) {
        return "Warning threshold must be less than alert threshold";
    }

    if (
        settings.brake_force_percent < 0 ||
        settings.brake_force_percent > 100
    ) {
        return "Brake force must be between 0 and 100 percent";
    }

    return null;
}

function getSettingsFromForm() {
    return {
        warning_threshold_g: parseFloat(
            document.getElementById("warning-threshold").value
        ),
        alert_threshold_g: parseFloat(
            document.getElementById("alert-threshold").value
        ),
        brake_force_percent: parseInt(
            document.getElementById("brake-force").value
        )
    };
}

refreshDashboard();
loadSettings();

setInterval(
    refreshDashboard,
    POLL_INTERVAL_MS
);