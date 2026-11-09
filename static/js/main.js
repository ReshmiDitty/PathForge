// PathForge Main Interactive Script

document.addEventListener("DOMContentLoaded", function () {
  // 1. Auto dismiss alerts after 6 seconds
  const alerts = document.querySelectorAll(".alert-dismissible");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = "opacity 0.5s ease";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 500);
    }, 6000);
  });

  // 2. AI Mentor Floating Widget Logic
  initMentorChat();

  // 3. Pricing Toggle Logic
  initPricingToggle();

  // 4. Assessment Multi-Step Form Logic
  initAssessmentForm();
});

// AI Mentor Chat
function initMentorChat() {
  const toggleBtn = document.getElementById("mentor-toggle-btn");
  const drawer = document.getElementById("mentor-drawer");
  const closeBtn = document.getElementById("mentor-close-btn");
  const sendBtn = document.getElementById("mentor-send-btn");
  const input = document.getElementById("mentor-input");
  const messagesContainer = document.getElementById("mentor-messages");
  const promptPills = document.querySelectorAll(".mentor-pill");

  if (!toggleBtn || !drawer) return;

  function openDrawer() {
    drawer.classList.remove("translate-x-full", "invisible");
    drawer.classList.add("translate-x-0");
    if (input) input.focus();
  }

  function closeDrawer() {
    drawer.classList.add("translate-x-full");
    setTimeout(() => drawer.classList.add("invisible"), 300);
  }

  toggleBtn.addEventListener("click", openDrawer);
  if (closeBtn) closeBtn.addEventListener("click", closeDrawer);

  // Quick prompt pills
  promptPills.forEach(pill => {
    pill.addEventListener("click", function () {
      if (input) {
        input.value = this.innerText;
        sendMentorMessage();
      }
    });
  });

  if (sendBtn && input) {
    sendBtn.addEventListener("click", sendMentorMessage);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMentorMessage();
      }
    });
  }

  function sendMentorMessage() {
    const text = input.value.trim();
    if (!text) return;

    // Append user message
    appendMessage("user", text);
    input.value = "";

    // Append loading skeleton
    const loadingId = "loading-" + Date.now();
    appendLoading(loadingId);

    // Call API
    fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: text })
    })
      .then(res => res.json())
      .then(data => {
        removeLoading(loadingId);
        appendMessage("assistant", data.reply || "I am here to guide your career and startup ideation!");
      })
      .catch(err => {
        removeLoading(loadingId);
        appendMessage("assistant", "Sorry, I encountered a brief issue. You can ask about viva concepts, market validation, or funding schemes!");
      });
  }

  function appendMessage(role, text) {
    if (!messagesContainer) return;
    const msgDiv = document.createElement("div");
    msgDiv.className = role === "user"
      ? "flex justify-end mb-3"
      : "flex justify-start mb-3";

    const bubble = document.createElement("div");
    bubble.className = role === "user"
      ? "bg-teal-600 text-white rounded-2xl rounded-tr-none px-4 py-2.5 max-w-[85%] text-sm shadow-sm"
      : "bg-slate-100 text-slate-800 rounded-2xl rounded-tl-none px-4 py-2.5 max-w-[85%] text-sm shadow-sm prose prose-sm";

    // Simple markdown formatting for bold and lists
    let formatted = text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/\n\n/g, "<br><br>")
      .replace(/\n- /g, "<br>• ");

    bubble.innerHTML = formatted;
    msgDiv.appendChild(bubble);
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function appendLoading(id) {
    if (!messagesContainer) return;
    const loadDiv = document.createElement("div");
    loadDiv.id = id;
    loadDiv.className = "flex justify-start mb-3";
    loadDiv.innerHTML = `
      <div class="bg-slate-100 rounded-2xl rounded-tl-none px-4 py-3 max-w-[70%]">
        <div class="flex space-x-1.5 items-center">
          <div class="w-2 h-2 rounded-full bg-teal-500 animate-bounce"></div>
          <div class="w-2 h-2 rounded-full bg-teal-500 animate-bounce [animation-delay:0.2s]"></div>
          <div class="w-2 h-2 rounded-full bg-teal-500 animate-bounce [animation-delay:0.4s]"></div>
        </div>
      </div>
    `;
    messagesContainer.appendChild(loadDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function removeLoading(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }
}

// Pricing Monthly / Yearly Switcher
function initPricingToggle() {
  const toggle = document.getElementById("billing-cycle-toggle");
  if (!toggle) return;

  const monthlyPrices = document.querySelectorAll(".price-monthly");
  const yearlyPrices = document.querySelectorAll(".price-yearly");
  const billingCycleInputs = document.querySelectorAll(".billing-cycle-input");

  toggle.addEventListener("change", function () {
    const isYearly = this.checked;
    if (isYearly) {
      monthlyPrices.forEach(el => el.classList.add("hidden"));
      yearlyPrices.forEach(el => el.classList.remove("hidden"));
      billingCycleInputs.forEach(input => input.value = "yearly");
    } else {
      monthlyPrices.forEach(el => el.classList.remove("hidden"));
      yearlyPrices.forEach(el => el.classList.add("hidden"));
      billingCycleInputs.forEach(input => input.value = "monthly");
    }
  });
}

// Assessment Multi-Step Form
function initAssessmentForm() {
  const form = document.getElementById("assessment-form");
  if (!form) return;

  const steps = document.querySelectorAll(".form-step");
  const progressBar = document.getElementById("assessment-progress-bar");
  const progressText = document.getElementById("assessment-progress-text");
  const nextBtns = document.querySelectorAll(".btn-next-step");
  const prevBtns = document.querySelectorAll(".btn-prev-step");
  let currentStep = 0;

  function updateStep(index) {
    steps.forEach((step, idx) => {
      if (idx === index) {
        step.classList.remove("hidden");
        step.classList.add("block");
      } else {
        step.classList.add("hidden");
        step.classList.remove("block");
      }
    });

    const percent = Math.round(((index + 1) / steps.length) * 100);
    if (progressBar) progressBar.style.width = percent + "%";
    if (progressText) progressText.innerText = `Step ${index + 1} of ${steps.length} (${percent}%)`;
    window.scrollTo({ top: 100, behavior: "smooth" });
  }

  nextBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      if (currentStep < steps.length - 1) {
        currentStep++;
        updateStep(currentStep);
      }
    });
  });

  prevBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      if (currentStep > 0) {
        currentStep--;
        updateStep(currentStep);
      }
    });
  });

  updateStep(0);
}

// Global copy-to-clipboard helper
function copyToClipboard(text, btnElement) {
  navigator.clipboard.writeText(text).then(() => {
    const originalText = btnElement.innerHTML;
    btnElement.innerHTML = `
      <svg class="w-4 h-4 inline mr-1 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg> Copied!
    `;
    setTimeout(() => {
      btnElement.innerHTML = originalText;
    }, 2000);
  });
}

