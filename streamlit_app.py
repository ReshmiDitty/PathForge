"""
PathForge – AI-Enabled Career Guidance & Skills Intelligence Portal
Streamlit Cloud Entrypoint Application
"""

import streamlit as st
import json
import plotly.graph_objects as go
from services.seed_data import CAREERS_SEED, STARTUP_IDEAS_SEED, PLANS_INFO, COUPONS_SEED
from services import fallback_engine, ai_service

# Page Configuration
st.set_page_config(
    page_title="PathForge – AI Career Guidance Portal",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    :root {
        --primary: #0d9488;
        --navy: #0f172a;
    }
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-teal {
        background-color: #ccfbf1;
        color: #0f766e;
        padding: 0.2rem 0.6rem;
        border-radius: 0.5rem;
        font-weight: 700;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "student_profile" not in st.session_state:
    st.session_state.student_profile = {
        "name": "Aarav Sharma",
        "branch": "Computer Science & Engineering",
        "year_of_study": "3rd Year",
        "college": "Indian Institute of Information Technology",
        "interests": ["Artificial Intelligence / GenAI", "SaaS & Cloud Web Apps"],
        "skills": {
            "Python & Backend Architecture": 8.5,
            "Frontend & Web Development": 8.0,
            "Data Analysis & Machine Learning": 7.5,
            "Product Thinking & User Empathy": 7.0,
            "System Design & Cloud Basics": 6.5,
            "Verbal Communication & Pitching": 8.0
        },
        "strengths": ["Rapid Prototyping", "Critical Thinking", "Product Empathy"],
        "risk_appetite": 5,
        "stability_vs_autonomy": 6,
        "hours_per_week": 18,
        "primary_goal": "job"
    }

if "active_idea_idx" not in st.session_state:
    st.session_state.active_idea_idx = 0

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your **PathForge AI Career Mentor**. How can I help with your campus placement preparation, skill-gap analysis, or target career roles today?"}
    ]

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/fluency/96/compass.png", width=50)
st.sidebar.markdown("### **PathForge**\n*AI Career Guidance Portal*")
st.sidebar.markdown("---")

nav = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Home & Overview",
        "🧭 AI Career Assessment",
        "📊 Career Compass & Radars",
        "⚖️ Pathway Decision Meter",
        "💼 Explore In-Demand Careers",
        "🚀 Optional Venture Track",
        "💬 AI Career Mentor",
        "🏛️ Platform Architecture",
        "💳 Student Pricing"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Logged in:** {st.session_state.student_profile['name']}")
st.sidebar.markdown(f"**Major:** {st.session_state.student_profile['branch']}")

# ==========================================
# PAGE 1: HOME & OVERVIEW
# ==========================================
if nav == "🏠 Home & Overview":
    st.markdown('<div class="main-title">Discover Your Ideal Career. Powered by Precision AI.</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">PathForge is an AI-Enabled Career Guidance Portal that maps your academic discipline, technical skills, and passions into personalized high-trajectory career pathways.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <span class="badge-teal">Step 1</span>
            <h4 style="margin-top:0.5rem; margin-bottom:0.2rem;">AI Aptitude & Skill Mapping</h4>
            <p style="font-size:0.85rem; color:#64748b;">Multi-step assessment rating your core technical skills, passion domains, and risk preferences.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <span class="badge-teal">Step 2</span>
            <h4 style="margin-top:0.5rem; margin-bottom:0.2rem;">Career Compass & Radars</h4>
            <p style="font-size:0.85rem; color:#64748b;">Diagnostic skill-gap radar charts benchmarking your baseline against hiring requirements (₹12-28 LPA CTC).</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <span class="badge-teal">Step 3</span>
            <h4 style="margin-top:0.5rem; margin-bottom:0.2rem;">6-Month Placement Roadmaps</h4>
            <p style="font-size:0.85rem; color:#64748b;">Curated industry certifications, portfolio capstones, and 24/7 AI mentor guidance.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Featured Career Pathway Match")
    careers = fallback_engine.generate_career_compass(st.session_state.student_profile)
    top_c = careers[0]

    fc1, fc2 = st.columns([3, 2])
    with fc1:
        st.markdown(f"### {top_c['title']}")
        st.markdown(f"**Match:** `{top_c['match_percentage']}% Profile Fit` &bull; **Category:** {top_c['category']}")
        st.markdown(f"**Industry Demand:** {top_c['market_demand']}")
        st.markdown(f"**Typical India CTC:** `{top_c['salary_range']}`")
        st.write(top_c['description'])
        st.info(f"💡 **Venture Bridge:** {top_c['venture_bridge']}")

    with fc2:
        # Radar preview
        labels = list(top_c['skills_benchmark'].keys())
        target_vals = list(top_c['skills_benchmark'].values())
        user_vals = [top_c['user_radar_scores'].get(k, 70) for k in labels]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=user_vals, theta=labels, fill='toself', name='Your Baseline', line_color='#0d9488'))
        fig.add_trace(go.Scatterpolar(r=target_vals, theta=labels, fill='toself', name='Target Benchmark', line_color='#94a3b8'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), showlegend=True, margin=dict(l=20, r=20, t=20, b=20), height=300)
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# PAGE 2: AI CAREER ASSESSMENT
# ==========================================
elif nav == "🧭 AI Career Assessment":
    st.markdown('<div class="main-title">AI Career Assessment & Skills Mapping</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Update your competencies and career ambitions to recalculate your skill-gap radars.</div>', unsafe_allow_html=True)

    with st.form("assessment_form"):
        st.markdown("#### 1. Academic Background")
        c1, c2 = st.columns(2)
        with c1:
            branch = st.selectbox(
                "Academic Branch / Major",
                [
                    "Computer Science & Engineering",
                    "Information Technology / AI & Data Science",
                    "Electronics & Communication (ECE)",
                    "Electrical & Electronics (EEE)",
                    "Mechanical & Mechatronics",
                    "Biotechnology & Biomedical",
                    "Business Administration & Management (BBA/MBA)",
                    "Commerce & Financial Markets"
                ],
                index=0
            )
        with c2:
            year = st.selectbox("Year of Study", ["1st Year", "2nd Year", "3rd Year", "4th Year / Final Year", "Post-Graduate"], index=2)

        st.markdown("#### 2. Domain Interests")
        interests = st.multiselect(
            "Select Passion Domains",
            [
                "Artificial Intelligence / GenAI",
                "SaaS & Cloud Web Apps",
                "FinTech & Quantitative",
                "HealthTech & Bio",
                "CleanTech & Decarbonization",
                "EdTech & Skill Building",
                "Hardware, Robotics & IoT"
            ],
            default=["Artificial Intelligence / GenAI", "SaaS & Cloud Web Apps"]
        )

        st.markdown("#### 3. Core Technical & Professional Skills (1 to 10)")
        sk_cols = st.columns(3)
        skills = {}
        skill_names = [
            "Python & Backend Architecture",
            "Frontend & Web Development",
            "Data Analysis & Machine Learning",
            "Product Thinking & User Empathy",
            "System Design & Cloud Basics",
            "Verbal Communication & Pitching"
        ]
        for i, sk in enumerate(skill_names):
            with sk_cols[i % 3]:
                cur_val = st.session_state.student_profile["skills"].get(sk, 7.5)
                skills[sk] = st.slider(sk, min_value=1.0, max_value=10.0, value=float(cur_val), step=0.5)

        st.markdown("#### 4. Career Ambition & Preferences")
        c_goal1, c_goal2 = st.columns(2)
        with c_goal1:
            goal = st.radio("Primary Post-College Goal", ["High-CTC Tech Job (Corporate)", "Higher Studies (MS/MBA)", "Venture Creation (Startup)"], index=0)
        with c_goal2:
            hours = st.slider("Available Upskilling Hours per Week", 5, 40, 18)

        submitted = st.form_submit_button("🚀 Save & Recalculate AI Career Guidance Report", use_container_width=True)
        if submitted:
            goal_key = "job" if "Job" in goal else ("higher_studies" if "Higher" in goal else "startup")
            st.session_state.student_profile.update({
                "branch": branch,
                "year_of_study": year,
                "interests": interests,
                "skills": skills,
                "hours_per_week": hours,
                "primary_goal": goal_key
            })
            st.success("Profile saved! Open 'Career Compass & Radars' or 'Pathway Decision Meter' in the menu.")

# ==========================================
# PAGE 3: CAREER COMPASS & RADARS
# ==========================================
elif nav == "📊 Career Compass & Radars":
    st.markdown('<div class="main-title">Career Compass & Skill-Gap Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">AI diagnostics benchmarking your competencies against top industry positions.</div>', unsafe_allow_html=True)

    careers = fallback_engine.generate_career_compass(st.session_state.student_profile)
    top_c = careers[0]

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(f"## 🏆 Top Recommendation: {top_c['title']}")
        st.markdown(f"**Profile Match:** `{top_c['match_percentage']}%` | **Salary:** `{top_c['salary_range']}`")
        st.write(top_c['description'])

        st.markdown("#### 📅 6-Month Actionable Upskilling Roadmap")
        for step in top_c['roadmap_6_months']:
            st.markdown(f"- **{step['month']} ({step['focus']}):** {step['details']}")

        st.markdown("#### 🎓 Curated Industry Certifications")
        for cert in top_c['certifications']:
            st.markdown(f"- 🏅 {cert}")

    with col2:
        st.markdown("### 📡 Diagnostic Skill-Gap Radar")
        labels = list(top_c['skills_benchmark'].keys())
        target_vals = list(top_c['skills_benchmark'].values())
        user_vals = [top_c['user_radar_scores'].get(k, 70) for k in labels]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=user_vals, theta=labels, fill='toself', name='Your Baseline', line_color='#0d9488'))
        fig.add_trace(go.Scatterpolar(r=target_vals, theta=labels, fill='toself', name='Industry Benchmark', line_color='#64748b'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=380)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🔎 Alternate High-Match Career Pathways")
    alt_cols = st.columns(len(careers[1:4]))
    for idx, c in enumerate(careers[1:4]):
        with alt_cols[idx]:
            st.markdown(f"**{c['title']}**")
            st.caption(f"Match: {c['match_percentage']}% | {c['salary_range']}")
            st.write(c['description'][:140] + "...")
            st.caption(f"Cert: {c['certifications'][0]}")

# ==========================================
# PAGE 4: DECISION METER
# ==========================================
elif nav == "⚖️ Pathway Decision Meter":
    st.markdown('<div class="main-title">Career Pathway & Readiness Decision Meter</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">AI evaluation balancing your readiness for Corporate Roles, Higher Studies, and Entrepreneurship.</div>', unsafe_allow_html=True)

    decision = fallback_engine.compute_tri_path_scores(st.session_state.student_profile)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Corporate & Tech Career", value=f"{decision['job_score']} / 100", delta="Primary Placement Route")
    with m2:
        st.metric(label="Higher Studies (MS/MBA)", value=f"{decision['higher_studies_score']} / 100", delta="Specialization")
    with m3:
        st.metric(label="Venture Track", value=f"{decision['venture_score']} / 100", delta="Optional Startup Route")

    st.markdown("---")
    c_chart, c_adv = st.columns([3, 2])
    with c_chart:
        st.markdown("### 📊 Comparative Pathway Scores")
        bar_fig = go.Figure(go.Bar(
            x=['Corporate Tech Job', 'Higher Studies (MS/MBA)', 'Venture Creation'],
            y=[decision['job_score'], decision['higher_studies_score'], decision['venture_score']],
            marker_color=['#0d9488', '#4f46e5', '#10b981'],
            text=[f"{decision['job_score']}%", f"{decision['higher_studies_score']}%", f"{decision['venture_score']}%"],
            textposition='auto'
        ))
        bar_fig.update_layout(yaxis=dict(range=[0, 100]), height=320, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(bar_fig, use_container_width=True)

    with c_adv:
        st.markdown(f"### 💡 Synthesis: {decision['verdict_title']}")
        st.write(decision['recommendation'])
        st.info("📌 **Placement Strategy:** Prioritize technical placement prep to lock down an early offer, while pursuing innovation projects with zero financial pressure.")

# ==========================================
# PAGE 5: EXPLORE IN-DEMAND CAREERS
# ==========================================
elif nav == "💼 Explore In-Demand Careers":
    st.markdown('<div class="main-title">Explore 15+ In-Demand Tech & Engineering Careers</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Comprehensive labor market benchmarks, compensation ranges (CTC), and required skills.</div>', unsafe_allow_html=True)

    search = st.text_input("🔍 Search careers by keyword (e.g. AI, Cloud, Python, Design, Finance):", "")
    filtered = [c for c in CAREERS_SEED if search.lower() in c['title'].lower() or any(search.lower() in kw for kw in c['match_keywords'])]

    for c in filtered:
        with st.expander(f"💼 {c['title']} ({c['salary_range']}) – {c['category']}"):
            st.write(c['description'])
            st.markdown(f"**Industry Demand:** `{c['market_demand']}`")
            st.markdown("**Core Skills Benchmark:**")
            st.json(c['skills_benchmark'])
            st.markdown(f"**Curated Certifications:** {', '.join(c['certifications'])}")
            st.caption(f"💡 Venture Bridge: {c['venture_bridge']}")

# ==========================================
# PAGE 6: OPTIONAL VENTURE TRACK
# ==========================================
elif nav == "🚀 Optional Venture Track":
    st.markdown('<div class="main-title">Optional Innovation & Venture Track</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Turn your career competencies into an entrepreneurial startup venture using Design Thinking and Lean Canvas frameworks.</div>', unsafe_allow_html=True)

    v_tab1, v_tab2, v_tab3, v_tab4 = st.tabs(["1. Idea Generator", "2. Lean Canvas", "3. Idea Validator", "4. Grants Toolkit"])

    with v_tab1:
        st.markdown("### Synthesized Startup Concepts from Your Skills")
        ideas = fallback_engine.generate_venture_ideas(st.session_state.student_profile, count=4)
        for idx, item in enumerate(ideas):
            with st.container():
                st.markdown(f"#### {item['title']}")
                st.caption(f"Target: {item['target_customer']} | Model: {item['revenue_model']}")
                st.write(f"**Problem:** {item['problem_statement']}")
                st.write(f"**Solution:** {item['solution']}")
                st.caption(f"Why Now: {item['why_now']}")
                st.markdown("---")

    with v_tab2:
        st.markdown("### Ash Maurya 9-Block Lean Canvas")
        canvas = fallback_engine.generate_lean_canvas(ideas[0])
        col_l1, col_l2, col_l3 = st.columns(3)
        with col_l1:
            st.text_area("1. Problem", canvas['problem'], height=130)
            st.text_area("4. Solution", canvas['solution'], height=130)
        with col_l2:
            st.text_area("3. Unique Value Proposition", canvas['unique_value_proposition'], height=130)
            st.text_area("9. Unfair Advantage", canvas['unfair_advantage'], height=130)
        with col_l3:
            st.text_area("2. Customer Segments", canvas['customer_segments'], height=130)
            st.text_area("5. Channels", canvas['channels'], height=130)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.text_area("7. Cost Structure", canvas['cost_structure'], height=90)
        with col_b2:
            st.text_area("6. Revenue Streams", canvas['revenue_streams'], height=90)

    with v_tab3:
        st.markdown("### Deep Idea Validation Scorecard")
        val = fallback_engine.validate_idea_scorecard(ideas[0])
        st.metric(label="Validation Score", value=f"{val['total_score']} / 100", delta=val['verdict'])
        st.write(val['verdict_message'])
        st.markdown("#### Indian Market Sizing (TAM/SAM/SOM)")
        st.write(f"- **TAM:** {val['tam_sam_som']['tam']} ({val['tam_sam_som']['tam_description']})")
        st.write(f"- **SAM:** {val['tam_sam_som']['sam']} ({val['tam_sam_som']['sam_description']})")
        st.write(f"- **SOM (3-Yr):** {val['tam_sam_som']['som']} ({val['tam_sam_som']['som_description']})")

    with v_tab4:
        st.markdown("### Indian Startup Schemes & Grants")
        st.markdown("""
        - 🏛️ **Startup India Seed Fund Scheme (SISFS):** Up to **₹20 Lakhs** grant for validation/MVP, and up to **₹50 Lakhs** convertible debt.
        - 🔬 **NIDHI-PRAYAS (DST):** Up to **₹10 Lakhs** non-dilutive prototype grant for hardware & IoT.
        - 🧬 **BIRAC BIG:** Up to **₹50 Lakhs** for healthcare, biotech, and bio-agriculture innovations.
        - 🏢 **Premier Incubators:** T-Hub Hyderabad, NSRCEL IIM Bangalore, SINE IIT Bombay.
        """)

# ==========================================
# PAGE 7: AI CAREER MENTOR
# ==========================================
elif nav == "💬 AI Career Mentor":
    st.markdown('<div class="main-title">24/7 AI Career & Placement Mentor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Ask about placement interview prep, closing skill gaps, salary negotiations, or career pivots.</div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a career or placement question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        reply = fallback_engine.ai_mentor_respond(prompt, st.session_state.student_profile)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

# ==========================================
# PAGE 8: PLATFORM ARCHITECTURE
# ==========================================
elif nav == "🏛️ Platform Architecture":
    st.markdown('<div class="main-title">PathForge Platform Architecture & Unit Economics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Sustainable business model for an AI-Enabled Career Guidance Portal.</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Customer Acq Cost (CAC)", "₹140")
    with c2: st.metric("Lifetime Value (LTV)", "₹890")
    with c3: st.metric("LTV : CAC Ratio", "6.35x")
    with c4: st.metric("Gross Margin", "82%")

    st.markdown("---")
    st.markdown("""
    #### Business Engine & Scaling Strategy
    - **B2C Student Subscriptions:** Free tier (1 assessment), Pro (₹199/mo), Founder (₹499/mo).
    - **B2B Campus Placement Partnerships:** Institutional licenses for college Training & Placement Offices (TPOs) at ₹1.5 Lakhs/year.
    - **Cloud Microservices:** Lightweight Python inference + SQLite/Postgres. Low server cost of ₹0.08 per generation.
    """)

# ==========================================
# PAGE 9: STUDENT PRICING
# ==========================================
elif nav == "💳 Student Pricing":
    st.markdown('<div class="main-title">Student-Friendly Transparent Pricing</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Start free. Upgrade to unlock unlimited multi-scenario assessments and deep validation.</div>', unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("### Free Starter\n**₹0** / forever")
        st.markdown("- 1 AI Career Assessment\n- Top 3 Career Matches\n- Basic Skill-Gap Radar\n- 3 AI generations / mo")
    with p2:
        st.markdown("### Pro Career (Popular)\n**₹199** / month")
        st.markdown("- **Unlimited** Assessments\n- Full Diagnostic Radars\n- 6-Month Upskilling Roadmap\n- Complete Venture Track\n- Lean Canvas PDF export")
    with p3:
        st.markdown("### Elite Founder\n**₹499** / month")
        st.markdown("- Everything in Pro\n- Deep Idea Validator & SWOT\n- 10-Slide Investor Deck\n- Priority AI Placement Mentor\n- Indian Grant Matcher")

    st.markdown("---")
    st.markdown("💡 **Student Discount:** Enter coupon code `STUDENT20` for an instant 20% discount!")
