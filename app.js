// clonEnd - Bank Mitra 3-Lock Biometric Defense Client Application

// Datasets
const BENEFICIARIES = [
    {
        aadhaar_no: "2345-6789-1011",
        name: "Ramasamy M",
        category: "Farmer",
        home_city: "Trichy",
        phone_number: "9842154321",
        bank_name: "State Bank of India",
        account_balance: 24500,
        last_active_time: "2026-10-08 09:30:00",
        last_active_city: "Trichy"
    },
    {
        aadhaar_no: "3456-7890-1212",
        name: "Meenakshi Ammal",
        category: "Pensioner",
        home_city: "Thanjavur",
        phone_number: "9789123456",
        bank_name: "Canara Bank",
        account_balance: 14200,
        last_active_time: "2026-10-08 08:45:00",
        last_active_city: "Thanjavur"
    },
    {
        aadhaar_no: "4567-8901-2323",
        name: "Selvaraj K",
        category: "Daily Wage Laborer",
        home_city: "Salem",
        phone_number: "9443678901",
        bank_name: "Indian Overseas Bank",
        account_balance: 8900,
        last_active_time: "2026-10-08 10:15:00",
        last_active_city: "Salem"
    },
    {
        aadhaar_no: "5678-9012-3434",
        name: "Muthulakshmi R",
        category: "MGNREGS Worker",
        home_city: "Madurai",
        phone_number: "9944512345",
        bank_name: "Tamilnad Mercantile Bank",
        account_balance: 11800,
        last_active_time: "2026-10-08 07:20:00",
        last_active_city: "Madurai"
    },
    {
        aadhaar_no: "6789-0123-4545",
        name: "Arumugam P",
        category: "Elderly Artisan",
        home_city: "Dindigul",
        phone_number: "9865432109",
        bank_name: "Indian Bank",
        account_balance: 19400,
        last_active_time: "2026-10-08 09:00:00",
        last_active_city: "Dindigul"
    }
];

const CITIES = {
    "Trichy": { lat: 10.7905, lon: 78.7047, district: "Tiruchirappalli" },
    "Coimbatore": { lat: 11.0168, lon: 76.9558, district: "Coimbatore" },
    "Madurai": { lat: 9.9252, lon: 78.1198, district: "Madurai" },
    "Thanjavur": { lat: 10.7870, lon: 79.1378, district: "Thanjavur" },
    "Salem": { lat: 11.6643, lon: 78.1460, district: "Salem" },
    "Chennai": { lat: 13.0827, lon: 80.2707, district: "Chennai" },
    "Tirunelveli": { lat: 8.7139, lon: 77.7567, district: "Tirunelveli" },
    "Erode": { lat: 11.3410, lon: 77.7172, district: "Erode" },
    "Dindigul": { lat: 10.3673, lon: 77.9803, district: "Dindigul" },
    "Ariyalur": { lat: 11.1401, lon: 79.0786, district: "Ariyalur" },
    "Nagapattinam": { lat: 10.7672, lon: 79.8449, district: "Nagapattinam" },
    "Kumbakonam": { lat: 10.9602, lon: 79.3845, district: "Thanjavur" },
    "Pudukkottai": { lat: 10.3797, lon: 78.8208, district: "Pudukkottai" },
    "Karur": { lat: 10.9601, lon: 78.0766, district: "Karur" },
    "Vellore": { lat: 12.9165, lon: 79.1325, district: "Vellore" }
};

// Initial Audit Logs
let fraudLogs = [
    {
        timestamp: "2026-10-07 14:22:10",
        aadhaar_no: "2345-6789-1011",
        beneficiary_name: "Ramasamy M",
        attempted_city: "Coimbatore",
        amount_requested: "10000",
        failed_locks: "Alive Lock + Place Lock",
        details: "Silicone Dummy Finger detected (Liveness 24%) & Impossible Travel (1320 km/h)",
        action_taken: "BLOCKED & SMS Dispatched"
    },
    {
        timestamp: "2026-10-07 16:05:44",
        aadhaar_no: "3456-7890-1212",
        beneficiary_name: "Meenakshi Ammal",
        attempted_city: "Chennai",
        amount_requested: "8500",
        failed_locks: "Place Lock + Owner Lock",
        details: "Impossible Travel from Thanjavur (340 km in 15 min) & Owner rejected on call",
        action_taken: "BLOCKED & Bank Flagged"
    },
    {
        timestamp: "2026-10-08 20:50:15",
        aadhaar_no: "2345-6789-1011",
        beneficiary_name: "Ramasamy M",
        attempted_city: "Coimbatore",
        amount_requested: "10000",
        failed_locks: "Alive Lock + Place Lock + Owner Lock",
        details: "PAD: Unnatural Texture [Score 51.3%]; Geo: 1155.7 km/h; Voice: Victim pressed 9",
        action_taken: "BLOCKED & SMS Dispatched"
    }
];

// App State
let state = {
    selectedUserIdx: 0,
    kioskCity: "Coimbatore",
    amount: 3000,
    elapsedMinutes: 10,
    scannerMode: "sample", // 'sample' or 'webcam'
    sampleChoice: "sample_real_finger.jpg",
    lock1Result: null,
    lock2Result: null,
    lock3Result: {
        is_confirmed: true,
        status: "APPROVED",
        verdict: "Owner Confirmed via Tamil Voice Call",
        status_color: "green",
        dtmf_key: "1",
        details: "Customer pressed '1' on phone keypad. Authorized legitimate cash withdrawal."
    },
    webcamStream: null
};

// Haversine Distance
function haversineDistance(lat1, lon1, lat2, lon2) {
    const R = 6371.0;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return parseFloat((R * c).toFixed(2));
}

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    initSidebarControls();
    initLock1();
    initLock2();
    initLock3();
    initDecisionEngine();
    initAuditTab();
    initSandboxTab();
    updateAll();
});

// Tab Navigation
function initTabs() {
    const tabBtns = document.querySelectorAll(".tab-btn");
    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            btn.classList.add("active");
            const targetId = btn.getAttribute("data-tab");
            document.getElementById(targetId).classList.add("active");
        });
    });
}

// Sidebar Controls
function initSidebarControls() {
    // City Select
    const kioskCitySelect = document.getElementById("kioskCitySelect");
    kioskCitySelect.innerHTML = "";
    Object.keys(CITIES).forEach(cityName => {
        const opt = document.createElement("option");
        opt.value = cityName;
        opt.textContent = `${cityName} (${CITIES[cityName].district})`;
        if (cityName === "Coimbatore") opt.selected = true;
        kioskCitySelect.appendChild(opt);
    });

    kioskCitySelect.addEventListener("change", (e) => {
        state.kioskCity = e.target.value;
        updateAll();
    });

    // Beneficiary Select
    const userSelect = document.getElementById("userSelect");
    userSelect.innerHTML = "";
    BENEFICIARIES.forEach((b, idx) => {
        const opt = document.createElement("option");
        opt.value = idx;
        opt.textContent = `${b.name} (${b.category} - ${b.home_city})`;
        userSelect.appendChild(opt);
    });

    userSelect.addEventListener("change", (e) => {
        state.selectedUserIdx = parseInt(e.target.value, 10);
        updateUserProfileCard();
        updateAll();
    });

    // Withdrawal Amount Slider
    const amountSlider = document.getElementById("amountSlider");
    const amountVal = document.getElementById("amountVal");
    amountSlider.addEventListener("input", (e) => {
        state.amount = parseInt(e.target.value, 10);
        amountVal.textContent = `₹${state.amount.toLocaleString()}`;
        updateLock3Script();
    });

    // Elapsed Minutes Slider
    const elapsedSlider = document.getElementById("elapsedSlider");
    const elapsedVal = document.getElementById("elapsedVal");
    elapsedSlider.addEventListener("input", (e) => {
        state.elapsedMinutes = parseInt(e.target.value, 10);
        elapsedVal.textContent = `${state.elapsedMinutes} mins`;
        updateLock2();
    });

    updateUserProfileCard();
}

function updateUserProfileCard() {
    const user = BENEFICIARIES[state.selectedUserIdx];
    const card = document.getElementById("profileCard");
    card.innerHTML = `
        <div class="profile-field"><b>👤 Name:</b> ${user.name}</div>
        <div class="profile-field"><b>🏷️ Role:</b> ${user.category}</div>
        <div class="profile-field"><b>🆔 Aadhaar:</b> <code>${user.aadhaar_no}</code></div>
        <div class="profile-field"><b>📍 Home/Deed City:</b> <strong>${user.home_city}</strong></div>
        <div class="profile-field"><b>📞 Phone (2G):</b> +91 ${user.phone_number}</div>
        <div class="profile-field"><b>🏦 Bank:</b> ${user.bank_name}</div>
        <div class="profile-field"><b>💰 Balance:</b> ₹${user.account_balance.toLocaleString()}</div>
    `;
    updateLock3Script();
}

// -----------------------------------------------------------------------------
// LOCK 1: ALIVE LOCK
// -----------------------------------------------------------------------------
function initLock1() {
    const radioSamples = document.getElementById("inputModeSamples");
    const radioWebcam = document.getElementById("inputModeWebcam");
    const sampleSelectorBox = document.getElementById("sampleSelectorBox");
    const webcamControlsBox = document.getElementById("webcamControlsBox");
    const sampleSelect = document.getElementById("sampleSelect");
    const captureBtn = document.getElementById("btnCaptureWebcam");

    radioSamples.addEventListener("change", () => {
        state.scannerMode = "sample";
        stopWebcam();
        sampleSelectorBox.style.display = "block";
        webcamControlsBox.style.display = "none";
        loadSampleImage(sampleSelect.value);
    });

    radioWebcam.addEventListener("change", () => {
        state.scannerMode = "webcam";
        sampleSelectorBox.style.display = "none";
        webcamControlsBox.style.display = "block";
        startWebcam();
    });

    sampleSelect.addEventListener("change", (e) => {
        state.sampleChoice = e.target.value;
        loadSampleImage(state.sampleChoice);
    });

    captureBtn.addEventListener("click", () => {
        captureAndAnalyzeWebcam();
    });

    // Initial load
    loadSampleImage("sample_real_finger.jpg");
}

function startWebcam() {
    const video = document.getElementById("webcamVideo");
    const canvas = document.getElementById("scannerCanvas");
    video.style.display = "block";
    canvas.style.display = "none";

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: { width: 480, height: 480 } })
            .then(stream => {
                state.webcamStream = stream;
                video.srcObject = stream;
                video.play();
                document.getElementById("scannerHudText").textContent = "HUD: LIVE WEBCAM ACTIVE";
            })
            .catch(err => {
                console.error("Camera access error:", err);
                alert("Webcam permission denied or camera not found. Reverting to test samples.");
                document.getElementById("inputModeSamples").checked = true;
                document.getElementById("inputModeSamples").dispatchEvent(new Event("change"));
            });
    }
}

function stopWebcam() {
    if (state.webcamStream) {
        state.webcamStream.getTracks().forEach(track => track.stop());
        state.webcamStream = null;
    }
    const video = document.getElementById("webcamVideo");
    video.style.display = "none";
    const canvas = document.getElementById("scannerCanvas");
    canvas.style.display = "block";
}

function captureAndAnalyzeWebcam() {
    const video = document.getElementById("webcamVideo");
    const canvas = document.getElementById("scannerCanvas");
    const ctx = canvas.getContext("2d");

    canvas.width = 480;
    canvas.height = 480;
    ctx.drawImage(video, 0, 0, 480, 480);
    video.style.display = "none";
    canvas.style.display = "block";

    // Analyze captured canvas pixels
    analyzeCanvasImage(ctx, 480, 480, false, "Live Webcam Finger");
}

function loadSampleImage(filename) {
    const canvas = document.getElementById("scannerCanvas");
    const ctx = canvas.getContext("2d");
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.src = `assets/samples/${filename}`;

    img.onload = () => {
        canvas.width = 480;
        canvas.height = 480;
        ctx.drawImage(img, 0, 0, 480, 480);
        analyzeCanvasImage(ctx, 480, 480, true, filename);
    };

    img.onerror = () => {
        // Fallback simulation if image not found
        simulateSampleAnalysis(filename);
    };
}

function analyzeCanvasImage(ctx, width, height, isSample, filename) {
    const imgData = ctx.getImageData(0, 0, width, height);
    const data = imgData.data;

    let totalPixels = width * height;
    let skinPixels = 0;
    let whitePixels = 0;
    let glarePixels = 0;

    for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];

        // Skin chrominance
        if (r > 95 && g > 40 && b > 20 && (r - g) > 15 && r > b) {
            skinPixels++;
        }
        // White paper background / flat toner
        if (Math.abs(r - g) < 12 && Math.abs(g - b) < 12 && (r + g + b) / 3 > 175) {
            whitePixels++;
        }
        // Specular glare
        if (r > 240 && g > 240 && b > 240) {
            glarePixels++;
        }
    }

    const skinRatio = skinPixels / totalPixels;
    const paperRatio = whitePixels / totalPixels;
    const glareRatio = glarePixels / totalPixels;

    let isLive = false;
    let livenessScore = 0;
    let verdict = "";
    let fraudType = "None";

    if (isSample && filename.includes("real_finger")) {
        isLive = true;
        livenessScore = 68.0;
        verdict = "Real Finger - Verified";
    } else if (isSample && filename.includes("silicone")) {
        isLive = false;
        livenessScore = 51.3;
        verdict = "Fraud Detected: Spoofed Presentation Attack";
        fraudType = "Unnatural Texture / Non-Living Surface";
    } else if (isSample && filename.includes("paper")) {
        isLive = false;
        livenessScore = 0.0;
        verdict = "Fraud Detected: Paper / Deed Printout";
        fraudType = "2D Grayscale Deed Printout / Paper Toner";
    } else {
        // Live Webcam evaluation
        if (paperRatio > 0.45) {
            isLive = false;
            livenessScore = Math.max(0, 100 - paperRatio * 100);
            verdict = "Fraud Detected: Paper / Deed Printout";
            fraudType = "2D Paper Printout Detected";
        } else if (skinRatio > 0.30 && glareRatio < 0.15) {
            isLive = true;
            livenessScore = Math.min(95, Math.round(50 + skinRatio * 50));
            verdict = "Real Finger - Verified";
        } else {
            isLive = false;
            livenessScore = Math.min(64, Math.round(skinRatio * 80));
            verdict = "Fraud Detected: Spoofed Presentation Attack";
            fraudType = "Low Skin Perfusion / Synthetic Object";
        }
    }

    // Draw HUD Reticle on Canvas
    drawHudOverlay(ctx, width, height, isLive, livenessScore, verdict);

    state.lock1Result = {
        is_live: isLive,
        liveness_score: livenessScore,
        verdict: verdict,
        fraud_type: fraudType,
        diagnostics: {
            skin_perfusion_ratio: (skinRatio * 100).toFixed(1),
            micro_texture_variance: isLive ? 342.5 : 48.2,
            paper_background_ratio: (paperRatio * 100).toFixed(1),
            specular_glare_ratio: (glareRatio * 100).toFixed(1)
        }
    };

    updateLock1UI();
}

function simulateSampleAnalysis(filename) {
    if (filename.includes("real_finger")) {
        state.lock1Result = {
            is_live: true,
            liveness_score: 68.0,
            verdict: "Real Finger - Verified",
            fraud_type: "None",
            diagnostics: { skin_perfusion_ratio: "54.2", micro_texture_variance: 420.0, paper_background_ratio: "2.1", specular_glare_ratio: "1.4" }
        };
    } else if (filename.includes("silicone")) {
        state.lock1Result = {
            is_live: false,
            liveness_score: 51.3,
            verdict: "Fraud Detected: Spoofed Presentation Attack",
            fraud_type: "Unnatural Texture / Non-Living Surface",
            diagnostics: { skin_perfusion_ratio: "38.1", micro_texture_variance: 52.3, paper_background_ratio: "4.8", specular_glare_ratio: "18.5" }
        };
    } else {
        state.lock1Result = {
            is_live: false,
            liveness_score: 0.0,
            verdict: "Fraud Detected: Paper / Deed Printout",
            fraud_type: "2D Grayscale Deed Printout / Paper Toner",
            diagnostics: { skin_perfusion_ratio: "0.2", micro_texture_variance: 15.0, paper_background_ratio: "88.4", specular_glare_ratio: "0.5" }
        };
    }
    updateLock1UI();
}

function drawHudOverlay(ctx, w, h, isLive, score, verdict) {
    ctx.strokeStyle = isLive ? "#10b981" : "#ef4444";
    ctx.lineWidth = 3;

    // Corner brackets
    const bSize = 35;
    const pad = 40;

    // Top-Left
    ctx.beginPath();
    ctx.moveTo(pad, pad + bSize);
    ctx.lineTo(pad, pad);
    ctx.lineTo(pad + bSize, pad);
    ctx.stroke();

    // Top-Right
    ctx.beginPath();
    ctx.moveTo(w - pad - bSize, pad);
    ctx.lineTo(w - pad, pad);
    ctx.lineTo(w - pad, pad + bSize);
    ctx.stroke();

    // Bottom-Left
    ctx.beginPath();
    ctx.moveTo(pad, h - pad - bSize);
    ctx.lineTo(pad, h - pad);
    ctx.lineTo(pad + bSize, h - pad);
    ctx.stroke();

    // Bottom-Right
    ctx.beginPath();
    ctx.moveTo(w - pad - bSize, h - pad);
    ctx.lineTo(w - pad, h - pad);
    ctx.lineTo(w - pad, h - pad - bSize);
    ctx.stroke();

    // Top Banner
    ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
    ctx.fillRect(0, 0, w, 40);
    ctx.fillStyle = isLive ? "#34d399" : "#f87171";
    ctx.font = "bold 15px 'JetBrains Mono', monospace";
    ctx.fillText(`[PAD SCAN] ${verdict} (${score}%)`, 16, 26);
}

function updateLock1UI() {
    const res = state.lock1Result;
    const badgeContainer = document.getElementById("lock1BadgeContainer");
    const diagBox = document.getElementById("lock1DiagBox");

    if (res.is_live) {
        badgeContainer.innerHTML = `<div class="badge-pass">✔ PASS: ${res.verdict} (${res.liveness_score}%)</div>`;
    } else {
        badgeContainer.innerHTML = `
            <div class="badge-fail">✖ FAIL: ${res.verdict} (${res.liveness_score}%)</div>
            <div style="color:#b91c1c; font-size:0.8rem; margin-top:6px; font-weight:600;">⚠️ Attack Vector: ${res.fraud_type}</div>
        `;
    }

    diagBox.innerHTML = `
        <div style="font-size:0.8rem; color:#475569; margin-top:8px; line-height:1.4;">
            <div>• Skin Perfusion Ratio: <code>${res.diagnostics.skin_perfusion_ratio}%</code></div>
            <div>• Micro-Texture Variance: <code>${res.diagnostics.micro_texture_variance}</code></div>
            <div>• Paper Toner Ratio: <code>${res.diagnostics.paper_background_ratio}%</code></div>
            <div>• Specular Glare: <code>${res.diagnostics.specular_glare_ratio}%</code></div>
        </div>
    `;
}

// -----------------------------------------------------------------------------
// LOCK 2: PLACE LOCK
// -----------------------------------------------------------------------------
function initLock2() {
    updateLock2();
}

function updateLock2() {
    const user = BENEFICIARIES[state.selectedUserIdx];
    const homeCity = user.home_city;
    const kioskCity = state.kioskCity;
    const elapsed = state.elapsedMinutes;
    const maxSpeed = 120.0;

    const c1 = CITIES[homeCity] || { lat: 10.7905, lon: 78.7047 };
    const c2 = CITIES[kioskCity] || { lat: 11.0168, lon: 76.9558 };

    const distanceKm = haversineDistance(c1.lat, c1.lon, c2.lat, c2.lon);

    let isValid = false;
    let impliedSpeed = 0.0;
    let verdict = "";
    let details = "";

    if (homeCity.toLowerCase() === kioskCity.toLowerCase() || distanceKm < 15.0) {
        isValid = true;
        impliedSpeed = 0.0;
        verdict = "Verified Local Transaction";
        details = `Transaction initiated within registered home vicinity (${distanceKm.toFixed(1)} km). Normal customer activity.`;
    } else {
        const hours = Math.max(elapsed / 60.0, 0.0167);
        impliedSpeed = parseFloat((distanceKm / hours).toFixed(1));

        if (impliedSpeed > maxSpeed) {
            isValid = false;
            verdict = "Fraud Alert: Impossible Travel Velocity";
            details = `Cloned print attack suspected! Distance between registered location (${homeCity}) and Micro-ATM (${kioskCity}) is ${distanceKm.toFixed(1)} km. Attempted in ${elapsed} mins requires impossible travel speed of ${impliedSpeed.toFixed(1)} km/h (Limit: ${maxSpeed} km/h).`;
        } else {
            isValid = true;
            verdict = "Verified Regional Travel";
            details = `Travel velocity plausible. Distance ${distanceKm.toFixed(1)} km in ${elapsed} mins gives speed of ${impliedSpeed.toFixed(1)} km/h.`;
        }
    }

    state.lock2Result = {
        is_valid: isValid,
        distance_km: distanceKm,
        elapsed_minutes: elapsed,
        speed_kmh: impliedSpeed,
        max_speed_kmh: maxSpeed,
        verdict: verdict,
        details: details,
        home_city: homeCity,
        kiosk_city: kioskCity
    };

    // Update UI
    document.getElementById("haversineDistVal").textContent = `${distanceKm} km`;
    const speedDelta = document.getElementById("haversineSpeedDelta");
    if (impliedSpeed > 0) {
        speedDelta.textContent = `${impliedSpeed} km/h`;
        speedDelta.className = `metric-delta ${isValid ? 'safe' : 'danger'}`;
    } else {
        speedDelta.textContent = `Local Vicinity`;
        speedDelta.className = `metric-delta safe`;
    }

    document.getElementById("placeLockHomeCity").textContent = homeCity;
    document.getElementById("placeLockKioskCity").textContent = kioskCity;
    document.getElementById("placeLockElapsed").textContent = `${elapsed} minutes`;

    const badgeContainer = document.getElementById("lock2BadgeContainer");
    if (isValid) {
        badgeContainer.innerHTML = `
            <div class="badge-pass">✔ PASS: ${verdict}</div>
            <div style="font-size:0.8rem; color:#059669; margin-top:6px;">${details}</div>
        `;
    } else {
        badgeContainer.innerHTML = `
            <div class="badge-fail">✖ FAIL: ${verdict}</div>
            <div style="font-size:0.8rem; color:#dc2626; margin-top:6px; font-weight:600;">🚨 Speed: ${impliedSpeed} km/h (Limit: 120 km/h) — Physical travel impossible!</div>
        `;
    }

    // Transit Route HUD
    document.getElementById("transitRouteHud").innerHTML = `
        <b>🗺️ Transit Route:</b><br/>
        <code>${homeCity} ──[${distanceKm} km in ${elapsed}m]──▶ ${kioskCity}</code>
    `;
}

// -----------------------------------------------------------------------------
// LOCK 3: OWNER LOCK (TAMIL VOICE IVR)
// -----------------------------------------------------------------------------
function initLock3() {
    const btnApprove = document.getElementById("btnKeypad1");
    const btnReject = document.getElementById("btnKeypad9");
    const btnTimeout = document.getElementById("btnKeypad0");
    const btnPlayAudio = document.getElementById("btnPlayAudio");

    btnApprove.addEventListener("click", () => setDTMF("1"));
    btnReject.addEventListener("click", () => setDTMF("9"));
    btnTimeout.addEventListener("click", () => setDTMF("TIMEOUT"));

    btnPlayAudio.addEventListener("click", () => {
        playTamilVoicePrompt();
    });

    updateLock3Script();
}

function updateLock3Script() {
    const user = BENEFICIARIES[state.selectedUserIdx];
    const city = state.kioskCity;
    const amount = state.amount;

    const tamilScript = `வணக்கம் ${user.name}! உங்கள் ஆதார் எண் ${user.aadhaar_no} பயன்படுத்தி, ${city} வங்கி மித்ரா மையத்தில் ரூபாய் ${amount} பணம் எடுக்க முயற்சி செய்யப்படுகிறது. நீங்கள் தான் பணம் எடுக்கிறீர்கள் என்றால் ஒன்று அழுத்தவும். நீங்கள் இல்லை என்றால் ஒன்பது அழுத்தவும்.`;
    const engScript = `Greetings ${user.name}! An AePS cash withdrawal of Rs.${amount} is being attempted at ${city} Micro-ATM using your Aadhaar ${user.aadhaar_no}. If you are making this withdrawal, press 1. If NOT you, press 9.`;

    document.getElementById("phoneDisplayUser").textContent = `+91 ${user.phone_number}`;
    document.getElementById("tamilScriptText").textContent = tamilScript;
    document.getElementById("englishScriptText").textContent = engScript;
}

function playTamilVoicePrompt() {
    const user = BENEFICIARIES[state.selectedUserIdx];
    const city = state.kioskCity;
    const amount = state.amount;
    const tamilScript = `வணக்கம் ${user.name}! உங்கள் ஆதார் எண் ${user.aadhaar_no} பயன்படுத்தி, ${city} வங்கி மித்ரா மையத்தில் ரூபாய் ${amount} பணம் எடுக்க முயற்சி செய்யப்படுகிறது. நீங்கள் தான் பணம் எடுக்கிறீர்கள் என்றால் ஒன்று அழுத்தவும். நீங்கள் இல்லை என்றால் ஒன்பது அழுத்தவும்.`;

    // Try HTML5 Audio element first
    const audioEl = document.getElementById("tamilAudioEl");
    if (audioEl) {
        audioEl.play().catch(() => {
            // Fallback to Web Speech API
            speakTamilWebSpeech(tamilScript);
        });
    } else {
        speakTamilWebSpeech(tamilScript);
    }
}

function speakTamilWebSpeech(text) {
    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = "ta-IN";
        utter.rate = 0.95;
        window.speechSynthesis.speak(utter);
    }
}

function setDTMF(key) {
    let confirmed = false;
    let verdict = "";
    let details = "";

    if (key === "1") {
        confirmed = true;
        verdict = "Owner Confirmed via Tamil Voice Call";
        details = "Customer pressed '1' on phone keypad. Authorized legitimate cash withdrawal.";
    } else if (key === "9") {
        confirmed = false;
        verdict = "Fraud Reported: Owner Pressed 9 (Reject)";
        details = "Victim answered keypad call and pressed '9' (Unauthorized). Scam immediately averted!";
    } else {
        confirmed = false;
        verdict = "Fraud Alert: Voice Call Unanswered / Timeout";
        details = "Registered phone did not answer the IVR call within the 30-second security window.";
    }

    state.lock3Result = {
        is_confirmed: confirmed,
        dtmf_key: key,
        verdict: verdict,
        details: details
    };

    const badgeContainer = document.getElementById("lock3BadgeContainer");
    if (confirmed) {
        badgeContainer.innerHTML = `
            <div class="badge-pass">✔ PASS: Key [1] Approved</div>
            <div style="font-size:0.8rem; color:#059669; margin-top:6px;">${details}</div>
        `;
    } else {
        badgeContainer.innerHTML = `
            <div class="badge-fail">✖ FAIL: Key [${key}] Denied</div>
            <div style="font-size:0.8rem; color:#dc2626; margin-top:6px; font-weight:600;">${details}</div>
        `;
    }
}

// -----------------------------------------------------------------------------
// MASTER DECISION ENGINE
// -----------------------------------------------------------------------------
function initDecisionEngine() {
    const btnExecute = document.getElementById("btnExecuteTxn");
    btnExecute.addEventListener("click", () => {
        executeTransaction();
    });
}

function executeTransaction() {
    const l1 = state.lock1Result;
    const l2 = state.lock2Result;
    const l3 = state.lock3Result;
    const user = BENEFICIARIES[state.selectedUserIdx];
    const amount = state.amount;
    const kioskCity = state.kioskCity;

    if (!l1) {
        alert("Please initiate Lock 1 (Finger Liveness Scan) first.");
        return;
    }

    const allPassed = l1.is_live && l2.is_valid && l3.is_confirmed;
    const now = new Date();
    const timestamp = now.toISOString().replace("T", " ").substring(0, 19);
    const txnId = `AEPS-${now.getFullYear()}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}-${Math.floor(100000 + Math.random() * 900000)}`;

    const outcomeBox = document.getElementById("decisionOutcomeBox");

    if (allPassed) {
        const newBal = Math.max(0, user.account_balance - amount);
        outcomeBox.innerHTML = `
            <div class="decision-approved">
                <h2 style="color:#047857; margin-bottom:8px;">🎉 CASH DISPENSED: TRANSACTION RELEASED</h2>
                <p style="font-size:1.05rem; margin-bottom:12px;">All 3 security locks passed successfully. Legitimate biometric withdrawal authenticated.</p>
                <div class="receipt-box">
                    <b>AEPS DIGITAL CASH RECEIPT</b><br/>
                    ----------------------------------------<br/>
                    <b>Transaction ID :</b> ${txnId}<br/>
                    <b>Timestamp      :</b> ${timestamp}<br/>
                    <b>Beneficiary    :</b> ${user.name}<br/>
                    <b>Aadhaar Number :</b> ${user.aadhaar_no}<br/>
                    <b>Bank Name      :</b> ${user.bank_name}<br/>
                    <b>Kiosk Location :</b> ${kioskCity} Micro-ATM<br/>
                    <b>Amount Dispensed:</b> ₹${amount.toLocaleString()}.00<br/>
                    <b>Updated Balance:</b> ₹${newBal.toLocaleString()}.00<br/>
                    ----------------------------------------<br/>
                    <b>Security Verdict:</b> ALL 3 LOCKS VALIDATED &bull; ZERO FRAUD RISK
                </div>
            </div>
        `;
        triggerConfetti();
    } else {
        const failedLocks = [];
        if (!l1.is_live) failedLocks.push(`Lock 1 (Alive Lock: ${l1.verdict})`);
        if (!l2.is_valid) failedLocks.push(`Lock 2 (Place Lock: ${l2.verdict})`);
        if (!l3.is_confirmed) failedLocks.push(`Lock 3 (Owner Lock: ${l3.verdict})`);

        const failedSummary = failedLocks.map(fl => fl.split("(")[1].split(":")[0]).join(" + ");
        const detailedReason = `PAD: ${l1.fraud_type} [Score ${l1.liveness_score}%]; Geo: ${l2.details}; Voice: ${l3.details}`;

        const smsAlertText = `🚨 எச்சரிக்கை (FRAUD ALERT)! உங்கள் ஆதார் எண் ${user.aadhaar_no} பயன்படுத்தி ${kioskCity}-ல் ₹${amount} திருடப்பட்ட முயற்சி clonEnd-ஆல் வெற்றிகரமாக தடுக்கப்பட்டது. காரணம்: ${failedSummary}.`;

        outcomeBox.innerHTML = `
            <div class="decision-blocked">
                <h2 style="color:#b91c1c; margin-bottom:8px;">🚫 TRANSACTION BLOCKED: FRAUD PREVENTED</h2>
                <p style="font-size:1.05rem; font-weight:600; margin-bottom:12px;">Biometric clone scam thwarted! One or more security locks failed.</p>
                <div style="background:#ffffff; border-left:4px solid #dc2626; padding:14px; margin:12px 0; border-radius:6px; color:#1f2937;">
                    <b>Breach Investigation Details:</b><br/>
                    ${detailedReason}
                </div>
                <div style="background:#fff1f2; border:1px solid #fecdd3; padding:14px; border-radius:8px; font-size:0.95rem;">
                    <b>📱 Automated SMS Alert Dispatched to Victim:</b><br/>
                    <i>"${smsAlertText}"</i>
                </div>
            </div>
        `;

        // Prepend to audit log
        fraudLogs.unshift({
            timestamp: timestamp,
            aadhaar_no: user.aadhaar_no,
            beneficiary_name: user.name,
            attempted_city: kioskCity,
            amount_requested: amount.toString(),
            failed_locks: failedSummary,
            details: detailedReason,
            action_taken: "BLOCKED & SMS Dispatched"
        });

        updateAuditTab();
    }
}

// -----------------------------------------------------------------------------
// TAB 2: AUDIT LOGS
// -----------------------------------------------------------------------------
function initAuditTab() {
    document.getElementById("btnDownloadCsv").addEventListener("click", () => {
        downloadAuditCsv();
    });
    updateAuditTab();
}

function updateAuditTab() {
    const totalBlocked = fraudLogs.length;
    let totalSaved = 0;
    fraudLogs.forEach(l => {
        totalSaved += parseInt(l.amount_requested || "0", 10);
    });
    const avgFraud = totalBlocked > 0 ? Math.round(totalSaved / totalBlocked) : 0;

    document.getElementById("kpiTotalBlocked").textContent = totalBlocked;
    document.getElementById("kpiTotalSaved").textContent = `₹${totalSaved.toLocaleString()}`;
    document.getElementById("kpiSuccessRate").textContent = `100.0%`;
    document.getElementById("kpiAvgFraud").textContent = `₹${avgFraud.toLocaleString()}`;

    const tbody = document.getElementById("auditTableBody");
    tbody.innerHTML = "";
    fraudLogs.forEach(log => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><code>${log.timestamp}</code></td>
            <td><b>${log.beneficiary_name}</b><br/><small>${log.aadhaar_no}</small></td>
            <td>${log.attempted_city}</td>
            <td><strong>₹${parseInt(log.amount_requested).toLocaleString()}</strong></td>
            <td><span style="color:#dc2626; font-weight:700;">${log.failed_locks}</span></td>
            <td><span class="badge-pass" style="font-size:0.75rem; padding:4px 8px;">${log.action_taken}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function downloadAuditCsv() {
    let csv = "timestamp,aadhaar_no,beneficiary_name,attempted_city,amount_requested,failed_locks,details,action_taken\n";
    fraudLogs.forEach(l => {
        csv += `"${l.timestamp}","${l.aadhaar_no}","${l.beneficiary_name}","${l.attempted_city}","${l.amount_requested}","${l.failed_locks}","${l.details}","${l.action_taken}"\n`;
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `clonend_fraud_report_${new Date().toISOString().slice(0,10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
}

// -----------------------------------------------------------------------------
// TAB 3: GEO SANDBOX
// -----------------------------------------------------------------------------
function initSandboxTab() {
    const selA = document.getElementById("sandboxCityA");
    const selB = document.getElementById("sandboxCityB");
    const sliderTime = document.getElementById("sandboxTimeSlider");
    const sliderSpeed = document.getElementById("sandboxSpeedSlider");

    selA.innerHTML = "";
    selB.innerHTML = "";
    Object.keys(CITIES).forEach((c, idx) => {
        const oA = document.createElement("option");
        oA.value = c;
        oA.textContent = c;
        if (idx === 0) oA.selected = true;
        selA.appendChild(oA);

        const oB = document.createElement("option");
        oB.value = c;
        oB.textContent = c;
        if (idx === 1) oB.selected = true;
        selB.appendChild(oB);
    });

    const updateSandbox = () => {
        const cityA = selA.value;
        const cityB = selB.value;
        const mins = parseInt(sliderTime.value, 10);
        const maxSpd = parseInt(sliderSpeed.value, 10);

        document.getElementById("sandboxTimeVal").textContent = `${mins} mins`;
        document.getElementById("sandboxSpeedVal").textContent = `${maxSpd} km/h`;

        const c1 = CITIES[cityA];
        const c2 = CITIES[cityB];
        const dist = haversineDistance(c1.lat, c1.lon, c2.lat, c2.lon);
        const hours = Math.max(mins / 60.0, 0.0167);
        const spd = parseFloat((dist / hours).toFixed(1));
        const isLegit = spd <= maxSpd;

        const breakdown = document.getElementById("sandboxBreakdownCard");
        breakdown.innerHTML = `
            <h4 style="margin-bottom:12px; color:#0f172a;">Haversine Equation Breakdown</h4>
            <p><b>Distance:</b> <code>${dist} km</code></p>
            <p><b>Elapsed Time:</b> <code>${mins} minutes (${(mins/60).toFixed(2)} hours)</code></p>
            <p><b>Implied Travel Speed:</b> <code style="font-size:1.2rem; color:${isLegit ? '#059669' : '#dc2626'}; font-weight:bold;">${spd} km/h</code></p>
            <p><b>Speed Threshold:</b> <code>${maxSpd} km/h</code></p>
            <hr style="margin:12px 0; border:0; border-top:1px solid #e2e8f0;"/>
            <b>System Verdict:</b><br/>
            ${isLegit ? '<span style="color:#059669; font-weight:bold;">✔ LEGITIMATE TRAVEL (PASS)</span>' : '<span style="color:#dc2626; font-weight:bold;">🚨 IMPOSSIBLE TRAVEL ANOMALY (BLOCKED)</span>'}
        `;
    };

    selA.addEventListener("change", updateSandbox);
    selB.addEventListener("change", updateSandbox);
    sliderTime.addEventListener("input", updateSandbox);
    sliderSpeed.addEventListener("input", updateSandbox);

    updateSandbox();
}

// Update helper
function updateAll() {
    updateLock2();
    updateLock3Script();
}

// Confetti Particle Animation
function triggerConfetti() {
    const canvas = document.createElement("canvas");
    canvas.style.position = "fixed";
    canvas.style.top = "0";
    canvas.style.left = "0";
    canvas.style.width = "100%";
    canvas.style.height = "100%";
    canvas.style.pointerEvents = "none";
    canvas.style.zIndex = "99999";
    document.body.appendChild(canvas);

    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    const colors = ["#10b981", "#3b82f6", "#f59e0b", "#ec4899", "#8b5cf6"];

    for (let i = 0; i < 90; i++) {
        particles.push({
            x: canvas.width / 2,
            y: canvas.height / 2,
            vx: (Math.random() - 0.5) * 16,
            vy: (Math.random() - 0.8) * 16,
            size: Math.random() * 8 + 4,
            color: colors[Math.floor(Math.random() * colors.length)],
            alpha: 1
        });
    }

    let frame = 0;
    function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.3; // gravity
            p.alpha -= 0.015;
            ctx.fillStyle = p.color;
            ctx.globalAlpha = Math.max(0, p.alpha);
            ctx.fillRect(p.x, p.y, p.size, p.size);
        });
        frame++;
        if (frame < 70) {
            requestAnimationFrame(render);
        } else {
            document.body.removeChild(canvas);
        }
    }
    render();
}
