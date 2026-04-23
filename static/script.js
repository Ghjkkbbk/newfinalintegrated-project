// 🌍 Global Mode
let mode = "dashboard";


// 📄 Upload PDF
document.getElementById("pdfFile").addEventListener("change", async () => {
    const fileInput = document.getElementById("pdfFile");
    if (!fileInput.files[0]) return;

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const status = document.getElementById("uploadStatus");
    status.innerText = "⏳ Uploading...";

    try {
        const res = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        status.innerText = data.message;

    } catch {
        status.innerText = "❌ Upload failed!";
    }
});


// 💬 Send Message
async function sendMessage() {
    const input = document.getElementById("userInput");
    const msg = input.value.trim();

    if (!msg) return;

    addMessage(msg, "user");
    input.value = "";
    input.disabled = true;

    let loader;
    if (mode === "research" || mode === "hybrid") {
        addMessage("🔍 Searching...\n📊 Analyzing...\n🧠 Generating...", "bot");
    } else {
        loader = addLoader();
    }

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg, mode: mode })
        });

        const data = await res.json();
        if (loader) loader.remove();

        typeMessage(formatResponse(data.response));

    } catch {
        if (loader) loader.remove();
        addMessage("❌ Error getting response", "bot");
    }

    input.disabled = false;
    input.focus();
}


// ✨ Add Message
function addMessage(text, sender) {
    const chatBox = document.getElementById("chatBox");

    const div = document.createElement("div");
    div.classList.add("message", sender);
    div.innerHTML = formatText(text);

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}


// ⌨️ Typing Effect
function typeMessage(text) {
    const chatBox = document.getElementById("chatBox");

    const div = document.createElement("div");
    div.classList.add("message", "bot");
    chatBox.appendChild(div);

    let i = 0;
    const interval = setInterval(() => {
        div.innerHTML = formatText(text.substring(0, i));
        i++;

        if (i > text.length) clearInterval(interval);

        chatBox.scrollTop = chatBox.scrollHeight;
    }, 15);
}


// 🔄 Loader
function addLoader() {
    const chatBox = document.getElementById("chatBox");

    const div = document.createElement("div");
    div.classList.add("message", "bot");

    const loader = document.createElement("div");
    loader.classList.add("loader");

    div.appendChild(loader);
    chatBox.appendChild(div);

    return div;
}


// 🎯 Format Text
function formatText(text) {
    if (!text) return "";

    return text
        .replace(/\n/g, "<br>")
        .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")
        .replace(/\* (.*?)(<br>|$)/g, "• $1<br>")
        .replace(/`(.*?)`/g, "<code>$1</code>");
}


// ⚡ Format Response
function formatResponse(text) {
    if (mode === "hybrid") {
        return `
📄 <b>From Documents:</b><br>
${text.substring(0, 150)}...<br><br>

🌐 <b>From Research:</b><br>
${text.substring(150, 300)}...<br><br>

⚡ <b>Final Answer:</b><br>
${text}
`;
    }

    if (mode === "research") {
        return `
🌐 <b>Research Insights:</b><br>
${text}
`;
    }

    return text;
}


// 🧠 Mode Switch
function switchMode(newMode, element) {

    mode = newMode;

    const titles = {
        dashboard: "🏠 Dashboard",
        chat: "💬 Chat Mode",
        doc: "📄 Document Mode",
        research: "🌐 Research Mode",
        hybrid: "⚡ Hybrid Mode"
    };

    document.getElementById("modeTitle").innerText = titles[newMode];

    const uploadSection = document.getElementById("uploadSection");
    const chatBox = document.getElementById("chatBox");
    const dashboard = document.getElementById("dashboardSection");

    // Reset UI
    dashboard.style.display = "none";
    chatBox.style.display = "block";
    chatBox.innerHTML = "";

    uploadSection.style.display =
        (mode === "doc" || mode === "hybrid") ? "block" : "none";

    // Active button
    document.querySelectorAll(".sidebar button")
        .forEach(btn => btn.classList.remove("active"));

    element.classList.add("active");

    // Mode UI
    if (mode === "research") showResearchUI();
    if (mode === "hybrid") showHybridUI();
    if (mode === "doc") showDocumentUI();

    if (mode === "dashboard") {
        chatBox.style.display = "none";
        dashboard.style.display = "block";
    }

    const inputBox = document.querySelector(".input-box");

if (mode === "dashboard") {
    inputBox.style.display = "none";
} else {
    inputBox.style.display = "flex";
}
}


// 🌐 Research UI
function showResearchUI() {
    document.getElementById("chatBox").innerHTML = `
        <div style="padding:20px; color:#94a3b8;">
            <h3>🌐 Research Agent</h3>
            <p>Enter a topic below to generate a detailed research report.</p>
        </div>
    `;
}


// ⚡ Hybrid UI
function showHybridUI() {
    document.getElementById("chatBox").innerHTML = `
        <div style="padding:20px; color:#94a3b8;">
            <h3>⚡ Hybrid Mode</h3>
            <p>Upload documents and ask questions to combine document knowledge with live research.</p>
        </div>
    `;
}


// 📄 Document UI
function showDocumentUI() {
    document.getElementById("chatBox").innerHTML = `
        <div style="padding:20px; color:#94a3b8;">
            <h3>📄 Document Mode</h3>
            <p>Upload your PDFs and ask questions based on your documents.</p>
        </div>
    `;
}


// ⌨️ Enter key
document.getElementById("userInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
}


);



window.onload = () => {
    const dashboardBtn = document.querySelector(".sidebar button");

    // Activate first button (Dashboard)
    dashboardBtn.classList.add("active");

    // Show dashboard
    switchMode("dashboard", dashboardBtn);
};