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

    // Call API with intelligent client-side fallback for static/Streamlit environments
    fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: text })
    })
      .then(res => {
        if (!res.ok) throw new Error("Fallback to client mentor");
        return res.json();
      })
      .then(data => {
        removeLoading(loadingId);
        appendMessage("assistant", data.reply || getClientMentorReply(text));
      })
      .catch(() => {
        setTimeout(() => {
          removeLoading(loadingId);
          appendMessage("assistant", getClientMentorReply(text));
        }, 350);
      });
  }

  function getClientMentorReply(query) {
    const q = query.toLowerCase();
    if (q.includes("skill") || q.includes("gap") || q.includes("radar")) {
      return "**Skill-Gap Analysis (Full-Stack AI Engineer):**\n- **Strengths:** Python/Backend (85%) and Frontend (80%) are at industry benchmark.\n- **Primary Gap:** DevOps, Docker & Cloud Deployment (currently ~65% vs 75% target) and System Design.\n- **Action Plan:** Build 1 containerized RAG microservice on AWS/Render and complete AWS Certified Developer Associate in Months 3–4.";
    }
    if (q.includes("interview") || q.includes("placement") || q.includes("ctc") || q.includes("job")) {
      return "**Top 3 Placement & High-CTC Interview Strategies:**\n- **1. DSA & Problem Solving:** Master 150 curated patterns (Graphs, DP, Trees, Sliding Window) for Day-1 coding rounds.\n- **2. Production AI Capstones:** Replace generic academic projects with deployed end-to-end applications featuring latency metrics and CI/CD.\n- **3. System Design Readiness:** Practice High-Level Design (caching, rate-limiting, vector search indexing) to stand out in ₹15–28 LPA technical rounds.";
    }
    if (q.includes("ms") || q.includes("higher") || q.includes("mba") || q.includes("study") || q.includes("studies")) {
      return "**Corporate Job vs. Higher Studies (MS/MBA) Framework:**\n- **Pathway 1 (Corporate Job - 90/100):** Immediate financial independence, real-world production engineering experience, zero student debt.\n- **Pathway 2 (Higher Studies - 75/100):** Ideal if targeting deep R&D roles (AI Research Scientist, Quantitative Modeling) or global mobility.\n- **Recommendation:** Secure a top campus placement offer first; gaining 1–2 years of industry experience strengthens both your MS/MBA admits and career trajectory.";
    }
    if (q.includes("startup") || q.includes("venture") || q.includes("grant") || q.includes("fund")) {
      return "**Student Venture & Grant Strategy:**\n- Use **Effectuation (Bird-in-Hand)** to build a micro-SaaS from your existing CSE/AI skills.\n- Validate problem-solution fit with 20 customer interviews before writing heavy code.\n- **Top Indian Grants:** NIDHI-PRAYAS (up to ₹10L prototype grant) and Startup India Seed Fund Scheme (SISFS up to ₹20L grant via campus incubators).";
    }
    return "**PathForge AI Career Advisor:**\nBased on your profile (**Computer Science, 3rd Year**), your highest-readiness trajectory is **Full-Stack AI Application Engineer (94% Match, ₹12–28 LPA)**.\n- Focus on **System Design & Cloud Deployment** over the next 8 weeks.\n- Ship 2 production portfolio projects and practice mock technical rounds.";
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

  const steps = form.querySelectorAll(".form-step");
  const progressBar = document.getElementById("assessment-progress-bar");
  const progressText = document.getElementById("assessment-progress-text");
  const nextBtns = form.querySelectorAll(".btn-next-step");
  const prevBtns = form.querySelectorAll(".btn-prev-step");
  let currentStep = 0;

  function updateStep(index, doScroll = true) {
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
    if (doScroll) {
      window.scrollTo({ top: 100, behavior: "smooth" });
    }
  }

  window.resetAssessmentStep = function () {
    currentStep = 0;
    updateStep(0, false);
  };

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

  // Highlight selected primary_goal radio card
  const goalRadios = form.querySelectorAll('input[name="primary_goal"]');
  goalRadios.forEach(radio => {
    radio.addEventListener("change", () => {
      goalRadios.forEach(r => {
        const lbl = r.closest("label");
        if (!lbl) return;
        if (r.checked) {
          lbl.className = "flex flex-col items-center justify-center p-3 rounded-xl border-2 border-teal-500 bg-teal-50/20 text-center cursor-pointer transition";
        } else {
          lbl.className = "flex flex-col items-center justify-center p-3 rounded-xl border border-slate-200 text-center cursor-pointer hover:border-teal-500 transition";
        }
      });
    });
  });

  updateStep(0, false);
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

