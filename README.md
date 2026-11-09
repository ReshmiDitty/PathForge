# PathForge – AI Career Guidance & Skills Intelligence Portal

> **"Find your career. Or build your own."**  
> *AI-Powered Career Intelligence, Skill-Gap Radars & Venture Track for Higher Education*

---

## 🚀 1. Executive Summary & Core Innovation

Most traditional placement portals only suggest static job listings. **PathForge is an AI-Enabled Career Guidance Portal with Dual-Path Architecture**: for every student, it takes a single set of academic disciplines, technical competencies, passions, and risk psychometrics to synthesize:
1. **Primary Track: High-Trajectory Career Intelligence** (Top 3–5 careers, skill-gap radar charts, 6-month placement roadmap, curated industry certifications).
2. **Pathway Decision Meter**: Empirical readiness comparison across (a) Corporate & Tech Job, (b) Higher Studies (MS/MBA), and (c) Venture Creation.
3. **Optional Innovation Track: Venture Studio** (Skills-to-startup generator, 5-stage Design Thinking board, Ash Maurya 9-block Lean Canvas, MVP sprint planner, 10-slide investor deck, and Indian grant matching).

---

## 🛠️ 2. Technology Stack & Dual Deployability

- **Web Application Stack**: Python 3.10+ / Flask 3.1, SQLite with SQLAlchemy ORM, Jinja2, Tailwind CSS, Chart.js (v4).
- **Streamlit Deployment Stack**: `streamlit_app.py`, Plotly for interactive radar and trajectory charts. Deployable instantly on Streamlit Community Cloud.
- **AI Engine**: Anthropic Claude API (`claude-3-5-sonnet`) with an **Intelligent Rule-Based Fallback Engine** (`services/fallback_engine.py`) that executes 100% locally when no API key is provided.
- **Payments**: Razorpay in **TEST mode** (INR) with an integrated **1-Click Demo Checkout Simulator** that enables full transaction verification and subscription unlocking without requiring third-party credentials.
- **Security**: Strictly zero hardcoded keys. All secrets read from environment variables via `python-dotenv`. `.env` is ignored by Git, and `.env.example` is provided.

```
venturemicroproj/
├── app.py                      # Flask Application entrypoint
├── streamlit_app.py            # Streamlit Cloud deployment entrypoint
├── config.py                   # Environment configuration loader
├── requirements.txt            # Python dependencies (Flask + Streamlit + Plotly)
├── .env.example                # Template for environment variables
├── .env                        # Local development variables (never commit)
├── .gitignore                  # Git exclusions
├── models/
│   ├── __init__.py             # SQLAlchemy database instance
│   ├── user.py                 # User model, authentication, usage counters
│   ├── assessment.py           # Dual-Path assessment responses & scores
│   ├── venture.py              # Venture ideas, Design Thinking notes, Lean Canvas, MVP, Pitch
│   └── subscription.py         # Subscriptions, Invoices, and Coupon models
├── routes/
│   ├── auth.py                 # Login, Register, Logout
│   ├── main.py                 # Landing page, Dashboard, Business Model
│   ├── assessment.py           # Multi-step assessment form, Compass report, Decision Meter
│   ├── venture.py              # 7 Venture Studio engines & Sticky note APIs
│   ├── subscription.py         # Pricing, Razorpay checkout, Demo pay, Billing
│   ├── api.py                  # AI Mentor Chat endpoint, Coupon validation
│   └── admin.py                # Admin analytics dashboard
├── services/
│   ├── ai_service.py           # Anthropic Claude API caller with auto-fallback
│   ├── fallback_engine.py      # High-fidelity deterministic reasoning engine
│   ├── payment_service.py      # Razorpay client, Demo simulator & @subscription_required decorator
│   └── seed_data.py            # 15+ careers, 10+ startup ideas, plans & coupons
├── static/
│   ├── css/custom.css          # Sticky-note themes, skeleton animations, print mode
│   └── js/main.js              # AI Mentor widget, multi-step form, pricing toggles
└── templates/                  # Modular Jinja2 responsive templates
```

---

## 🌐 3. Website Content & Structural Architecture

```
                                  [ LANDING PAGE (/) ]
                     Hero • 3-Step Methodology • Feature Cards • Pricing
                                            │
               ┌────────────────────────────┴───────────────────────────┐
               ▼                                                        ▼
      [ STUDENT AUTH ]                                         [ EXPLORE CAREERS ]
    Register / Login / Quick-fill                             15+ In-Demand Tech Roles
               │
               ▼
   [ AI CAREER ASSESSMENT ]  ──►  4-Stage Diagnostic Form
               │                  (Branch, Interests, 6 Core Skills, Goals)
               │
        ┌──────┴───────────────────────────────────┐
        ▼                                          ▼
[ CAREER COMPASS ]                       [ PATHWAY DECISION METER ]
• Top Matched Role & Match %             • Path 1: Corporate Job (92/100 - Primary)
• Chart.js Skill-Gap Radar               • Path 2: Higher Studies (80/100)
• 6-Month Placement Roadmap              • Path 3: Venture Track (75/100 - Optional)
• Industry Certifications & CTC          • Strategic Placement Advisory Synthesis
        │
        ▼
[ STUDENT DASHBOARD ]
• Placement Readiness Gauge
• Active Target Roles & Roadmaps
• Plan Status & Usage Limits
        │
        ├──────────────────────────────────────────┐
        ▼                                          ▼
[ OPTIONAL VENTURE TRACK ]                [ MONETIZATION & PLATFORM ]
• Idea Generator (Skills-to-Startup)     • Pricing (Free / Pro / Founder)
• 5-Stage Design Thinking Board          • Checkout (Razorpay Test + 1-Click Demo)
• Idea Validator (100-pt Scorecard)      • Billing & Invoices
• Lean Canvas Builder (9-Block + PDF)    • "Our Business Model" (CAC/LTV Analysis)
• MVP Planner & Pitch Deck Builder       • Admin Telemetry Analytics (/admin)
• Founder Toolkit (SISFS, BIRAC Grants)
```

### Detailed Section Breakdown

#### 1. Top-Level Layout & Global Elements
- **Sticky Navigation Bar (`components/navbar.html`)**: Direct access to AI Career Assessment, Career Compass, Decision Meter, Explore Careers, and the Optional Venture Track. Dynamic profile dropdown with user plan badges (*Free*, *Pro*, or *Founder*) and 1-click logout.
- **24/7 AI Career Mentor (`components/mentor_widget.html`)**: Persistent bottom-right drawer with quick-prompt pills (*"Analyze my skill gap"*, *"Top 3 placement interview tips"*, *"Should I do MS or take a job?"*). Powered by Claude 3.5 Sonnet with local deterministic fallback.
- **Platform Footer (`components/footer.html`)**: Career guidance platform info, university placement links, and ethical AI disclosures.

#### 2. Core Career Guidance Engine (Primary Pillar)
- **AI Diagnostic Assessment (`/assessment`)**: 4-stage progressive intake: Academic Background, Domain Passions, Core Competencies (Python, Frontend, Data/ML, Product, System Design, Communication), and Career Ambition (defaults to *High-CTC Corporate Job*).
- **Career Compass Report (`/career-compass`)**: Top Matched Role (e.g. *Full-Stack AI Application Engineer*, 94% match, ₹12–28 LPA), interactive Chart.js polar radar comparing student vs industry benchmark, actionable 6-month placement roadmap, curated certifications, and a Venture Bridge showing how these technical skills can also create a startup.
- **Pathway Decision Meter (`/decision-meter`)**: Empirical 3-way trajectory evaluation:
  - **Pathway 1 (Corporate & Tech Job - 92/100)**: Highlighted primary card focusing on structured career growth, immediate cash flow, and campus placement readiness.
  - **Pathway 2 (Higher Studies - 80/100)**: Specialization for MS/M.Tech/MBA.
  - **Pathway 3 (Venture Creation - 75/100)**: Optional startup innovation route.
  - **Comparative Breakdown Chart & Strategic Placement Verdict**: Placement-first strategy advisory.
- **Explore In-Demand Careers (`/careers`)**: 15+ curated tech roles with CTC packages, top recruiters, and required skills.

#### 3. Student Dashboard (`/dashboard`)
- Placement Readiness Gauge tracking overall profile strength.
- Active target role summary and next upcoming roadmap milestone.
- Saved assessment reports and remaining AI generations for current plan.

#### 4. Optional Venture Track (`/venture-studio/*`)
- **Idea Generator (`/ideas`)**: 4 practical startup concepts mapped to student's branch and skills.
- **Design Thinking Board (`/design-thinking`)**: 5-stage interactive board (*Empathize $\rightarrow$ Define $\rightarrow$ Ideate $\rightarrow$ Prototype $\rightarrow$ Test*) with sticky notes.
- **Idea Validator (`/validator`)**: 100-pt scorecard, TAM/SAM/SOM market sizing, and SWOT matrix with GO/PIVOT verdict.
- **Lean Canvas Builder (`/lean-canvas`)**: Ash Maurya's 9-block grid with 1-click AI autofill and clean PDF/print export.
- **MVP Sprint Planner (`/mvp-planner`)**: Smallest testable prototype, riskiest assumptions, and target metrics.
- **Pitch Deck Builder (`/pitch-builder`)**: 10-slide investor outline with speaker notes and 60-second elevator speech.
- **Founder Toolkit (`/toolkit`)**: Directory of Indian student grants (*SISFS, NIDHI-PRAYAS, BIRAC*) and IPR basics (*Patents, Trademarks, Copyrights*).

#### 5. Monetization, Platform Economics & Admin
- **Pricing (`/pricing`)**: 3 tiers (Free @ ₹0, Pro @ ₹199/mo, Founder @ ₹499/mo) with monthly/annual switch.
- **Checkout (`/checkout/<tier>`)**: Razorpay Test Mode + instant 1-Click Demo Checkout Simulator and coupon system (`STUDENT20`).
- **Billing (`/billing`)**: Invoice history and cancellation.
- **"Our Business Model" (`/business-model`)**: Platform unit economics (CAC: ₹140, LTV: ₹890, LTV:CAC: 6.35x).
- **Admin Analytics (`/admin`)**: Real-time KPI telemetry and Chart.js distribution charts.

---

## ⚡ 4. Quick Setup & Run Instructions

### Option A: Run as Flask Web Application
```bash
pip install -r requirements.txt
python app.py
```
Open your browser at: **`http://localhost:5000`**

### Option B: Run as Streamlit Web Application
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Open your browser at: **`http://localhost:8501`**

---

## ☁️ 5. Deploying to Streamlit Cloud

To deploy PathForge on Streamlit Community Cloud:
1. Push this repository to GitHub: `https://github.com/ReshmiDitty/PathForge`
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"Create app"** (or **"New app"**).
4. Select:
   - **Repository:** `ReshmiDitty/PathForge`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
5. Click **"Deploy!"** — Streamlit Cloud will automatically install dependencies from `requirements.txt` and launch the portal with live interactive charts!

---

## 🔑 6. Demo & Test Credentials

The database automatically seeds two pre-configured accounts on initial launch for instant viva testing:

| Role | Email | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Demo Student** | `student@pathforge.edu` | `student123` | Student with completed assessment & sample KisanSense venture |
| **Admin User** | `admin@pathforge.edu` | `admin123` | Full access to Admin Analytics & all features |

*(Note: The Sign In page has **1-Click Quick-Fill buttons** for both accounts).*

---

## 💳 7. Payment Testing & Demo Checkout Guide

PathForge supports two modes of payment processing:
1. **Live Razorpay Test Mode**: When `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` are present in `.env`, the Razorpay Test modal opens.
2. **Built-in 1-Click Demo Checkout**: Always available! Even if no Razorpay keys are configured, click **"⚡ Instant Demo Checkout"** on the checkout page. The system will:
   - Simulate a verified INR payment
   - Apply active coupon discounts
   - Generate an official invoice (`INV-YYYYMM-XXXXXX`)
   - Unlock Pro or Founder tier features on the backend using the `@subscription_required` decorator.

### Available Student Coupons:
- `STUDENT20` &rarr; **20% instant discount**
- `STARTUP50` &rarr; **50% instant discount**
- `CAMPUSFREE` &rarr; **100% waiver** for sponsored campus pilots

---

## 🎬 8. Step-by-Step Viva Demo Script

Follow this 5-minute walkthrough during your project demonstration or viva examination:

### Step 1: Landing Page (`/`)
- Showcase the hero headline: *"Find your career. Or build your own."*
- Highlight the **Dual-Path visualizer** showing how one student profile splits into (1) Corporate Career and (2) Startup Venture.
- Explain the 3-step pedagogical methodology.

### Step 2: Student Login & Dashboard (`/login` &rarr; `/dashboard`)
- Click **"Demo Student"** quick-fill button (`student@pathforge.edu` / `student123`).
- Point out the active venture (*KisanSense IoT*), plan badge (*Free* or *Pro*), and formation progress tracker (*65%*).

### Step 3: Dual-Path Assessment & Career Compass (`/career-compass`)
- Review the matched career: **Full-Stack AI Application Engineer (94% match, ₹12 - ₹28 LPA)**.
- Observe the **Skill-Gap Radar Chart** dynamically generated using Chart.js.
- Point out **The Venture Bridge**: how these exact software engineering skills can be monetized into an AI SaaS micro-startup.

### Step 4: Decision Meter (`/decision-meter`)
- Review the comparative readiness score:
  - Corporate Job: 75/100
  - Higher Studies: 65/100
  - Startup Venture: 86/100
- Explain the **Hybrid Model Recommendation**: Secure campus placement in 7th semester, build MVP in 15 hrs/week, then apply for Indian grants.

### Step 5: Venture Studio – Idea Generator (`/venture-studio/ideas`)
- Show the 4 synthesized ideas customized to the student's branch and skills.
- Show how the student can click **"Set as Active Venture"** to propagate the idea across the entire studio.

### Step 6: Design Thinking Board (`/venture-studio/design-thinking`)
- Demonstrate the 5 columns: **Empathize &bull; Define &bull; Ideate &bull; Prototype &bull; Test**.
- Click **"+ Add Sticky Note"** to add a new observation note with custom sticky colors (amber, sky, emerald, rose, purple).

### Step 7: Lean Canvas Builder (`/venture-studio/lean-canvas`)
- Display Ash Maurya's 9-block layout.
- Click **"✨ AI Auto-Fill Canvas"** to observe intelligent, contextual population of all 9 blocks.
- Click **"Export to PDF / Print"** to demonstrate the clean print-ready stylesheet.

### Step 8: Upgrade Flow (`/pricing` &rarr; `/checkout/founder`)
- Navigate to Pricing, demonstrate the **Monthly / Yearly toggle** (with 25% annual discount indicator).
- Click **"Get Founder Suite"**.
- In the coupon box, enter `STUDENT20` and click **"Apply"** &rarr; Observe the 20% price deduction.
- Click **"⚡ Instant Demo Checkout"** &rarr; Notice immediate redirect to Dashboard with a success alert and Founder badge!

### Step 9: Founder Features: Idea Validator & Pitch Builder
- Visit **`/venture-studio/validator`**: Show the 100-point scorecard, Indian TAM/SAM/SOM sizing (₹6,500 Cr TAM), and 4-quadrant SWOT with the **GO Verdict**.
- Visit **`/venture-studio/pitch-builder`**: Show the 10-slide investor presentation outline, speaker notes, and 60-second elevator speech script.

### Step 10: "Our Business Model" Page (`/business-model`)
- Explain to the examiner how PathForge applies the course syllabus to itself:
  - CAC: ₹140, LTV: ₹890, LTV:CAC: 6.35x, Gross Margin: 82%.
  - Ash Maurya 9-block Lean Canvas for PathForge as a scalable EdTech platform.

### Step 11: Admin Analytics (`/admin`)
- Log in as `admin@pathforge.edu` / `admin123`.
- Inspect platform KPIs: Total Users, Active Subscribers, Total Revenue (INR), Conversion Rate %, Subscriber Doughnut chart, and Revenue Bar chart.

---

## 🎓 9. Academic Viva & Course Q&A Cheat Sheet

Prepare for these common professor questions:

### Q1: What is the difference between Alexander Osterwalder's Business Model Canvas (BMC) and Ash Maurya's Lean Canvas?
> **Answer:** Osterwalder's BMC was created for established enterprises and includes *Key Partners, Key Activities, Key Resources, and Customer Relationships*. For early-stage startups with high uncertainty, these are unknown guesses. Ash Maurya replaced those four blocks with **Problem, Solution, Key Metrics, and Unfair Advantage**, anchoring the model around *Problem-Solution Fit* and rapid falsification.

### Q2: How does Effectuation Theory (Prof. Saras Sarasvathy) apply to PathForge?
> **Answer:** Effectuation states that expert entrepreneurs do not start with fixed end goals; they start with **Means** (*Bird-in-Hand: who I am, what I know, and whom I know*) and practice **Affordable Loss**. PathForge embodies this by deriving startup ideas directly from the student's existing skills, college network, and branch, rather than asking them to pursue arbitrary high-risk concepts.

### Q3: How is TAM, SAM, and SOM calculated?
> **Answer:**
> - **TAM (Total Addressable Market):** Total annual market expenditure across the whole sector (e.g., ₹6,500 Crores).
> - **SAM (Serviceable Addressable Market):** The segment accessible through our target channels and geography (e.g., ₹1,250 Crores).
> - **SOM (Serviceable Obtainable Market):** The realistic portion we can capture in Years 1–3 (e.g., ₹45 Crores).

### Q4: What are the main Indian government grant schemes available for student founders?
> **Answer:**
> - **Startup India Seed Fund Scheme (SISFS):** Up to ₹20 Lakhs grant for validation/MVP, and up to ₹50 Lakhs convertible debenture via DPIIT incubators.
> - **NIDHI-PRAYAS (DST):** Up to ₹10 Lakhs non-dilutive grant for physical/IoT prototypes.
> - **BIRAC BIG:** Up to ₹50 Lakhs for healthcare, biotech, and bio-agriculture innovations.

---

## 🔒 10. Security & Ethical AI Notice
- All secrets are isolated strictly in `.env`.
- Passwords are encrypted using Werkzeug PBKDF2/SHA-256 salts.
- Feature gating is enforced on backend Python route decorators (`@subscription_required`), preventing unauthorized URL tampering.

---
*Developed with ❤️ for Venture Ideation and Entrepreneurship Course Evaluation.*

