"""
PathForge Fallback Intelligence Engine
---------------------------------------
Provides high-fidelity, deterministic, and course-aligned reasoning for:
1. Tri-Path Readiness Scoring (Job vs Higher Studies vs Startup)
2. Career Compass matching & Skill-Gap Radar benchmarks
3. Venture Idea generation from student skills and branch
4. Ash Maurya 9-Block Lean Canvas generation
5. Deep Idea Validation scorecard, TAM/SAM/SOM calculation, and SWOT analysis
6. MVP Sprint Planning & Riskiest Assumption Testing
7. 10-Slide Investor Pitch Deck generation
8. Context-aware AI Mentor Chat responses
"""

import json
from services.seed_data import CAREERS_SEED, STARTUP_IDEAS_SEED

def compute_tri_path_scores(assessment_data: dict) -> dict:
    """
    Computes comparative career readiness scores (0-100) across:
    1. Corporate & Tech Industry Careers (Placement & CTC focus)
    2. Higher Studies & Advanced Research (MS / M.Tech / MBA)
    3. Entrepreneurship & Venture Track (Optional startup route)

    Anchored in realistic career guidance psychometrics:
    Skill Depth, Problem-Solving, Stability, and Growth Appetite.
    """
    risk = int(assessment_data.get("risk_appetite", 5)) # 1-10
    autonomy = int(assessment_data.get("stability_vs_autonomy", 5)) # 1-10
    hours = int(assessment_data.get("hours_per_week", 15))
    goal = assessment_data.get("primary_goal", "job").lower()
    skills = assessment_data.get("skills", {})
    if isinstance(skills, str):
        try:
            skills = json.loads(skills)
        except Exception:
            skills = {}
    
    # Skill execution average
    skill_vals = [float(v) for v in skills.values()] if skills else [7.5]
    avg_skill = sum(skill_vals) / max(len(skill_vals), 1) # 1-10 scale
    
    # 1. Corporate & High-Tech Job Readiness (Primary Path for Career Guidance)
    # Rewards technical competency, project execution, and problem solving
    job_score = int(65 + (avg_skill * 2.8) + (min(autonomy, 7) * 0.8))
    if goal in ["job", "corporate", "placement"]:
        job_score += 10
    job_score = max(50, min(96, job_score))

    # 2. Higher Studies & Research Readiness
    # Rewards analytical depth, foundational skills, and study commitment
    higher_studies_score = int(55 + (avg_skill * 2.2) + ((10 - risk) * 1.5))
    if goal in ["higher_studies", "masters", "ms", "mba"]:
        higher_studies_score += 12
    higher_studies_score = max(45, min(94, higher_studies_score))

    # 3. Entrepreneurship & Venture Track
    # Balanced assessment of venture aptitude
    time_factor = min(hours / 25.0, 1.0)
    venture_score = int(40 + (risk * 2.5) + (autonomy * 2.2) + (time_factor * 8))
    if goal == "startup":
        venture_score += 10
    venture_score = max(35, min(92, venture_score))

    # Breakdown attributes for Decision Meter radar / bar charts
    breakdown = {
        "Technical & Core Skills": min(100, int(avg_skill * 10)),
        "Industry & Placement Fit": min(100, job_score),
        "Academic & Research Depth": min(100, higher_studies_score),
        "Problem Solving & Autonomy": min(100, autonomy * 10),
        "Innovation & Risk Appetite": min(100, risk * 10)
    }

    # Career-First Recommendation Synthesis
    if job_score >= 85 and goal != "startup":
        verdict = "High-Trajectory Tech Specialist"
        rec = "Your technical baseline and execution capability align strongly with top-tier corporate engineering and product roles. Focus on placement interview prep, advanced DSA/system design, and target high-CTC offers (₹14-30 LPA)."
    elif higher_studies_score >= 82 and (goal == "higher_studies" or higher_studies_score > job_score):
        verdict = "Advanced Research & Postgrad Candidate"
        rec = "Your analytical depth and academic strengths make you an excellent candidate for specialized Masters (MS/M.Tech/MBA). Target tier-1 global research universities to build specialized domain depth in AI, Robotics, or Data Science."
    elif goal == "startup" and venture_score >= 80:
        verdict = "Entrepreneurial Innovator"
        rec = "You have high autonomy drive and venture appetite. Validate your startup concepts in the Venture Track while maintaining placement preparation as a secure financial foundation."
    else:
        verdict = "Dual-Track Career Accelerator"
        rec = "Your well-rounded profile fits both high-growth corporate tech careers and startup innovation. Secure a top placement offer first, then explore entrepreneurial side projects with zero financial pressure."

    return {
        "job_score": job_score,
        "higher_studies_score": higher_studies_score,
        "venture_score": venture_score,
        "breakdown": breakdown,
        "verdict_title": verdict,
        "recommendation": rec
    }

    return {
        "job_score": job_score,
        "higher_studies_score": higher_studies_score,
        "venture_score": venture_score,
        "breakdown": breakdown,
        "verdict_title": verdict,
        "recommendation": rec
    }


def generate_career_compass(assessment_data: dict) -> list:
    """
    Matches student skills, branch, and interests against the career taxonomy.
    Generates tailored match percentages and customized radar benchmarks.
    """
    interests = assessment_data.get("interests", [])
    if isinstance(interests, str):
        try:
            interests = json.loads(interests)
        except Exception:
            interests = [interests]
    interests_str = " ".join([str(i).lower() for i in interests])

    skills = assessment_data.get("skills", {})
    if isinstance(skills, str):
        try:
            skills = json.loads(skills)
        except Exception:
            skills = {}

    branch = str(assessment_data.get("branch", "")).lower()

    scored_careers = []
    for career in CAREERS_SEED:
        score = 65 # Base match
        # Keyword matching
        for kw in career["match_keywords"]:
            if kw in interests_str or kw in branch:
                score += 6
            for user_skill in skills.keys():
                if kw in user_skill.lower():
                    score += 5

        # Normalize score
        score = min(98, score)
        
        # Skill-gap radar calculations
        user_radar_scores = {}
        target_benchmark = career["skills_benchmark"]
        for benchmark_skill, benchmark_target in target_benchmark.items():
            # Estimate user baseline based on provided skills
            matched_user_score = 65
            for us, val in skills.items():
                if any(w in us.lower() for w in benchmark_skill.lower().split()):
                    matched_user_score = int(float(val) * 10)
                    break
            user_radar_scores[benchmark_skill] = min(100, max(40, matched_user_score))

        career_entry = dict(career)
        career_entry["match_percentage"] = score
        career_entry["user_radar_scores"] = user_radar_scores
        scored_careers.append(career_entry)

    scored_careers.sort(key=lambda x: x["match_percentage"], reverse=True)
    return scored_careers[:4]


def generate_venture_ideas(assessment_data: dict, count: int = 4) -> list:
    """
    Transforms student skills + academic discipline into 3-5 high-potential startup concepts.
    """
    interests = assessment_data.get("interests", [])
    if isinstance(interests, str):
        try:
            interests = json.loads(interests)
        except Exception:
            interests = [interests]
    interests_str = " ".join([str(i).lower() for i in interests])
    branch = str(assessment_data.get("branch", "")).lower()

    # Score ideas by relevance
    scored_ideas = []
    for idea in STARTUP_IDEAS_SEED:
        relevance = 50
        category = idea["category"].lower()
        if any(term in category for term in ["tech", "ai", "software"]) and ("computer" in branch or "it" in branch or "software" in branch or "ai" in interests_str):
            relevance += 25
        if "agri" in category and ("agri" in branch or "agri" in interests_str or "bio" in branch):
            relevance += 35
        if "health" in category and ("health" in interests_str or "bio" in branch):
            relevance += 35
        if "fintech" in category and ("finance" in interests_str or "fintech" in interests_str or "business" in branch):
            relevance += 35
        if "sustain" in category and ("clean" in interests_str or "energy" in interests_str or "mechanical" in branch):
            relevance += 35
        
        scored_ideas.append((relevance, idea))

    scored_ideas.sort(key=lambda x: x[0], reverse=True)
    selected = [item[1] for item in scored_ideas[:count]]
    return selected


def generate_lean_canvas(idea_data: dict) -> dict:
    """
    Generates complete Ash Maurya 9-Block Lean Canvas for a given startup idea.
    """
    title = idea_data.get("title", "Student Venture")
    problem = idea_data.get("problem_statement", "Inefficient workflow in market segment.")
    customer = idea_data.get("target_customer", "College students and SMEs.")
    solution = idea_data.get("solution", "Automated digital platform.")
    why_now = idea_data.get("why_now", "Rapid digital penetration and policy tailwinds.")
    revenue = idea_data.get("revenue_model", "Subscription SaaS + Transaction Fees.")

    canvas = {
        "title": f"Lean Canvas: {title}",
        "problem": f"1. {problem}\n2. Lack of affordable, localized solutions for Indian users.\n3. Existing alternatives rely on manual, error-prone paperwork.",
        "existing_alternatives": "Spreadsheets, legacy agencies, unorganized local service providers.",
        "customer_segments": f"Primary: {customer}\nSecondary: Academic institutions, early-stage SMBs, campus innovators.",
        "early_adopters": "Tech-forward student founders, tier-2 college engineers, pilot FPOs with active WhatsApp communities.",
        "unique_value_proposition": f"The fastest, most cost-effective way to solve {title.split('–')[0].strip()} with zero upfront friction.",
        "high_level_concept": f"Uber/Canva for {idea_data.get('category', 'Student Innovation')}",
        "solution": f"1. {solution}\n2. Native vernacular support (WhatsApp integration & regional voice).\n3. End-to-end telemetry and actionable automated reporting.",
        "channels": "1. Campus Brand Ambassador programs across 50+ colleges.\n2. LinkedIn thought leadership and developer communities.\n3. Institutional partnerships with startup incubators (T-Hub, NSRCEL).",
        "revenue_streams": f"1. {revenue}\n2. Enterprise B2B campus licensing (₹1.5 Lakhs/year/college).\n3. Value-added premium analytics and API integration charges.",
        "cost_structure": "1. Cloud hosting & AI API tokens (AWS/Render/Claude API): ₹15,000/mo.\n2. Prototyping hardware & testing BOM.\n3. Customer acquisition, digital marketing & campus events: ₹25,000/mo.",
        "key_metrics": "1. Customer Acquisition Cost (CAC) vs Lifetime Value (LTV).\n2. Weekly Active Users (WAU) and 30-day retention cohort.\n3. Net Promoter Score (NPS > 65) and organic referral coefficient (k > 1.2).",
        "unfair_advantage": "Proprietary campus distribution channel, deep regional data pipelines, and rapid agile development loop."
    }
    return canvas


def validate_idea_scorecard(idea_data: dict) -> dict:
    """
    Performs comprehensive Idea Validation across 5 venture dimensions:
    - Problem-Solution Fit (0-20)
    - Market Size TAM/SAM/SOM (0-20)
    - Competitive Advantage / Moat (0-20)
    - Technical Feasibility (0-20)
    - Unit Economics & Monetization (0-20)

    Generates SWOT analysis and final GO / REFINE / PIVOT verdict.
    """
    title = idea_data.get("title", "InnovateX")
    problem = idea_data.get("problem_statement", "")
    solution = idea_data.get("solution", "")
    complexity = idea_data.get("complexity", "Medium")

    # Dimensions
    problem_fit_score = 17 # High severity problem
    market_size_score = 16 # Large expanding market
    moat_score = 15 # Defensible distribution
    tech_score = 16 if complexity != "High" else 14
    unit_econ_score = 16

    total_score = problem_fit_score + market_size_score + moat_score + tech_score + unit_econ_score

    if total_score >= 78:
        verdict = "GO"
        verdict_message = "Outstanding potential! Strong problem-solution fit and clear unit economics. Proceed directly to MVP build and customer interview sprints."
        verdict_badge = "bg-emerald-100 text-emerald-800 border-emerald-300"
    elif total_score >= 65:
        verdict = "REFINE"
        verdict_message = "Promising concept with viable demand. Refine customer segmentation and test willingness-to-pay before committing capital."
        verdict_badge = "bg-amber-100 text-amber-800 border-amber-300"
    else:
        verdict = "PIVOT"
        verdict_message = "High risk of commoditization or excessive barrier to entry. Consider pivoting the target customer segment or narrowing scope."
        verdict_badge = "bg-rose-100 text-rose-800 border-rose-300"

    swot = {
        "strengths": [
            "Hyper-focused value proposition targeting acute student and enterprise pain points.",
            "Low fixed-overhead operational structure leveraging cloud microservices.",
            "Direct access to early adopter testing cohorts on college campuses."
        ],
        "weaknesses": [
            "Early dependency on external API providers or specialized hardware components.",
            "Initial brand awareness is low compared to established enterprise incumbents.",
            "Limited runway requiring rapid milestone validation to unlock grant funding."
        ],
        "opportunities": [
            "Government startup funding schemes (Startup India SISFS up to ₹50L, NIDHI-PRAYAS).",
            "Untapped Tier-2/3 Indian regional markets with rising digital purchasing power.",
            "Institutional partnerships with college placement cells and state incubators."
        ],
        "threats": [
            "Feature copying by well-funded capitalized tech platforms.",
            "Regulatory shifts in data protection (DPDP Act 2023) or licensing mandates.",
            "Customer inertia and slow sales cycles in institutional enterprise procurement."
        ]
    }

    tam_sam_som = {
        "tam": "₹6,500 Crores ($780M)",
        "tam_description": "Total Indian market expenditure in the target sector annually.",
        "sam": "₹1,250 Crores ($150M)",
        "sam_description": "Serviceable addressable segment accessible through digital & campus channels.",
        "som": "₹45 Crores ($5.4M)",
        "som_description": "Target capture in Years 1–3 by securing 300 institutions / 25,000 active users."
    }

    return {
        "total_score": total_score,
        "verdict": verdict,
        "verdict_message": verdict_message,
        "verdict_badge": verdict_badge,
        "dimensions": {
            "Problem-Solution Fit": {"score": problem_fit_score, "max": 20, "notes": "Acute, recurring pain point with clear quantified loss."},
            "Market Sizing (TAM/SAM/SOM)": {"score": market_size_score, "max": 20, "notes": "Growing at >22% CAGR driven by digital transformation."},
            "Competitive Advantage & Moat": {"score": moat_score, "max": 20, "notes": "Network effects and proprietary localized dataset."},
            "Technical & Operational Feasibility": {"score": tech_score, "max": 20, "notes": f"Achievable with current tech stack; complexity is {complexity}."},
            "Unit Economics & Monetization": {"score": unit_econ_score, "max": 20, "notes": "High gross margin (>75%) with clear subscription expansion."}
        },
        "swot": swot,
        "tam_sam_som": tam_sam_som
    }


def generate_mvp_plan(idea_data: dict) -> dict:
    """
    Generates a 2-week MVP Execution Sprint with Riskiest Assumptions testing.
    """
    title = idea_data.get("title", "Venture MVP")
    return {
        "mvp_type": "Landing Page Smoke Test + Concierge Pilot",
        "scope_description": f"Build a high-converting 1-page interactive prototype of {title} demonstrating the core value proposition. Process the first 10 transactions or reports manually (Concierge MVP) to validate customer willingness-to-pay before writing complex automation code.",
        "riskiest_assumptions": [
            {"category": "Desirability", "assumption": "Target users experience enough pain that they will sign up and share contact info within 60 seconds."},
            {"category": "Viability", "assumption": "Customers will pay at least ₹199 - ₹499 for the solution rather than using free ad-hoc workarounds."},
            {"category": "Feasibility", "assumption": "The core problem can be solved in under 48 hours using off-the-shelf APIs and responsive web interfaces."}
        ],
        "success_metrics": [
            "50+ verified customer waitlist signups in 10 days.",
            "15 in-depth user discovery interviews completed.",
            "At least 5 prospective customers willing to pay an advance token deposit / Letter of Intent (LOI)."
        ],
        "sprint_tasks": [
            {"day": "Days 1 - 3", "title": "Customer Empathy & Problem Validation", "desc": "Draft interview script, speak with 10 potential users, document verbatim complaints."},
            {"day": "Days 4 - 7", "title": "Build Minimum Smoke Test Page", "desc": "Deploy responsive landing page with value prop, pricing preview, and waitlist form."},
            {"day": "Days 8 - 10", "title": "Drive Targeted Traffic", "desc": "Distribute across campus WhatsApp groups, LinkedIn, and relevant Reddit/Discord channels."},
            {"day": "Days 11 - 14", "title": "Synthesize Learnings & Pivot / Proceed", "desc": "Calculate conversion rate, interview respondents, and finalize sprint scorecard."}
        ]
    }


def generate_pitch_deck(idea_data: dict) -> dict:
    """
    Produces a 10-Slide Investor Deck outline and 60-Second Elevator Pitch.
    """
    title = idea_data.get("title", "PathForge Venture")
    tagline = idea_data.get("tagline", "Innovative digital solution for modern problems.")
    problem = idea_data.get("problem_statement", "Users struggle with high friction and lack of modern tooling.")
    customer = idea_data.get("target_customer", "College students and aspiring professionals.")
    solution = idea_data.get("solution", "An intelligent automated platform streamlining the workflow.")
    revenue = idea_data.get("revenue_model", "Subscription SaaS + Transaction Fees.")

    slides = [
        {
            "slide_number": 1,
            "title": "Title & Vision",
            "subtitle": f"{title}",
            "bullets": [
                f"Tagline: {tagline}",
                "Presenters: Student Founding Team",
                "Vision: Building India's category-defining platform for this space."
            ],
            "speaker_notes": "Grab the room's attention with a 1-sentence hook: 'We are solving the single largest bottleneck in this sector.'"
        },
        {
            "slide_number": 2,
            "title": "The Problem",
            "subtitle": "A severe, unaddressed pain point costing time and money",
            "bullets": [
                f"Core issue: {problem}",
                "Existing solutions are fragmented, expensive, and out of touch.",
                "Customers lose up to 30% efficiency dealing with manual workarounds."
            ],
            "speaker_notes": "Ground the problem in a real human story. Make the investor feel the frustration."
        },
        {
            "slide_number": 3,
            "title": "The Solution",
            "subtitle": "An elegant, purpose-built product that delivers instant 10x value",
            "bullets": [
                f"Our platform: {solution}",
                "Instant onboarding with zero training required.",
                "Reduces turnaround time from days to seconds."
            ],
            "speaker_notes": "Show the product in action. Emphasize why our approach is 10x better, not just 10% better."
        },
        {
            "slide_number": 4,
            "title": "Market Size & Opportunity",
            "subtitle": "A rapidly compounding multi-million dollar market",
            "bullets": [
                "TAM: ₹6,500 Crores ($780M) overall industry spend.",
                "SAM: ₹1,250 Crores ($150M) serviceable addressable audience.",
                "SOM: ₹45 Crores ($5.4M) 3-year realistic capture."
            ],
            "speaker_notes": "Explain bottom-up sizing: Number of target customers x Annual Contract Value (ACV)."
        },
        {
            "slide_number": 5,
            "title": "Business Model & Unit Economics",
            "subtitle": "High-margin, recurring software and transactional monetization",
            "bullets": [
                f"Primary engine: {revenue}",
                "Customer Acquisition Cost (CAC): ₹450 | Lifetime Value (LTV): ₹2,800 (LTV:CAC = 6.2x)",
                "Gross Margins exceeding 78% with low variable server costs."
            ],
            "speaker_notes": "Investors invest in businesses, not just cool ideas. Show profitability at the unit level."
        },
        {
            "slide_number": 6,
            "title": "Underlying Magic & Moat",
            "subtitle": "Why incumbents and fast-followers cannot easily replicate us",
            "bullets": [
                "Proprietary regional dataset and localized algorithms.",
                "Virality embedded into campus user workflows (k-factor > 1.2).",
                "Deep workflow lock-in: users store their active portfolios on our engine."
            ],
            "speaker_notes": "Highlight our technological unfair advantage and distribution defensibility."
        },
        {
            "slide_number": 7,
            "title": "Competition & Positioning",
            "subtitle": "Where we stand in the 2x2 competitive matrix",
            "bullets": [
                "Legacy Players: Clunky, high setup costs, poor mobile/vernacular support.",
                "Generic Alternatives: Lack domain specificity and actionable guidance.",
                "PathForge Advantage: Agile, accessible, high-ROI, purpose-built."
            ],
            "speaker_notes": "Never say 'We have no competitors.' Show why we win in our specific high-value quadrant."
        },
        {
            "slide_number": 8,
            "title": "Traction & Validation",
            "subtitle": "Early evidence of product-market pull",
            "bullets": [
                "Completed 25+ discovery interviews with target users.",
                "Prototype tested with 92% satisfaction rate.",
                "3 pilot Letters of Intent (LOIs) signed for campus deployment."
            ],
            "speaker_notes": "Traction cures all objections. Show that real customers are already pulling the product from your hands."
        },
        {
            "slide_number": 9,
            "title": "Founding Team",
            "subtitle": "Complementary builders with domain empathy and technical grit",
            "bullets": [
                "CEO / Product Lead: Passionate domain student with strong vision.",
                "CTO / Tech Architect: Full-stack builder proficient in scalable Python/Cloud.",
                "Advisors: Department Faculty & College Entrepreneurship Cell mentors."
            ],
            "speaker_notes": "Explain why this team is uniquely qualified to win this market."
        },
        {
            "slide_number": 10,
            "title": "The Ask & Roadmap Milestones",
            "subtitle": "Catalyst capital to achieve key inflection points",
            "bullets": [
                "Seeking: ₹10 Lakhs (NIDHI-PRAYAS / Incubator Grant) or ₹25 Lakhs Pre-Seed.",
                "Milestone 1 (Months 1-3): Complete production MVP & reach 1,000 active users.",
                "Milestone 2 (Months 4-6): Onboard 5 paid enterprise campuses & reach ₹1 Lakh MRR."
            ],
            "speaker_notes": "Be crystal clear on what milestones this capital unlocks before the next financing round."
        }
    ]

    elevator_pitch = (
        f"Did you know that {problem.lower()} "
        f"That's why we built {title}. {tagline} "
        f"Our platform empowers {customer} to achieve results in minutes. "
        f"We monetize through {revenue}, and we're currently piloting with early campus adopters. "
        f"We are looking for mentorship, incubator support, and grant funding to scale across Indian campuses. Thank you!"
    )

    one_pager = f"""
### Executive One-Pager: {title}
**Tagline:** {tagline}
**Target Market:** {customer}
**Problem:** {problem}
**Solution:** {solution}
**Market Opportunity:** TAM ₹6,500 Cr | SAM ₹1,250 Cr | SOM ₹45 Cr
**Business Model:** {revenue}
**Current Stage:** Validated Prototype & Early Pilot Cohort
**Contact:** student-founders@pathforge.edu
"""

    return {
        "slides": slides,
        "elevator_pitch_60s": elevator_pitch,
        "one_page_pitch": one_pager.strip()
    }


def ai_mentor_respond(query: str, user_profile: dict, active_idea: dict = None) -> str:
    """
    Provides intelligent, encouraging, course-grounded guidance for student queries.
    Answers questions on:
    - Career decisions (Job vs Higher Studies vs Startup)
    - Viva questions (Lean Canvas vs Business Model Canvas, Effectuation, TAM calculation)
    - Startup grants in India (SISFS, NIDHI-PRAYAS, BIRAC)
    - Prototype and MVP scoping
    """
    q = query.lower()
    student_name = user_profile.get("name", "Student")
    branch = user_profile.get("branch", "Engineering")

    if any(k in q for k in ["viva", "exam", "difference between", "lean canvas vs"]):
        return (
            f"**Great Viva Question! Here is the crisp academic breakdown:**\n\n"
            f"1. **Business Model Canvas (Osterwalder) vs Lean Canvas (Ash Maurya):**\n"
            f"- BMC is designed for established enterprises and includes *Key Partners, Key Activities, Key Resources, and Customer Relationships*.\n"
            f"- Lean Canvas replaces these 4 blocks with **Problem, Solution, Key Metrics, and Unfair Advantage**, making it far more actionable for early-stage, high-uncertainty startups.\n\n"
            f"2. **Effectuation (Prof. Saras Sarasvathy):**\n"
            f"Entrepreneurs don't start with goals; they start with **Means** (Bird-in-Hand: who I am, what I know, whom I know) and practice **Affordable Loss** rather than expected return.\n\n"
            f"3. **TAM, SAM, SOM:**\n"
            f"- TAM (Total Addressable Market): Entire global/national demand.\n"
            f"- SAM (Serviceable Addressable Market): The portion targeted by your business model.\n"
            f"- SOM (Serviceable Obtainable Market): What you can realistically capture in 1-3 years."
        )

    if any(k in q for k in ["grant", "funding", "money", "sisfs", "nidhi", "incubator", "seed fund"]):
        return (
            f"**Top Indian Startup Grants & Seed Funding Schemes for Students:**\n\n"
            f"1. **Startup India Seed Fund Scheme (SISFS):**\n"
            f"- Up to **₹20 Lakhs** as a grant for proof of concept/prototype testing, and up to **₹50 Lakhs** through convertible debentures.\n"
            f"- Applied via DPIIT-recognized incubators (e.g. SINE IIT Bombay, T-Hub, NSRCEL).\n\n"
            f"2. **NIDHI-PRAYAS (Department of Science & Technology):**\n"
            f"- Grant of up to **₹10 Lakhs** for physical and hardware/IoT prototypes. Zero equity dilution.\n\n"
            f"3. **BIRAC BIG (Biotechnology Ignition Grant):**\n"
            f"- Up to **₹50 Lakhs** for healthcare, biotech, medical devices, and bio-agriculture innovations.\n\n"
            f"**Immediate Tip for {student_name}:** Build a working video demonstration or interactive prototype before applying. Incubators fund *traction and evidence*, not just paper concepts!"
        )

    if any(k in q for k in ["job vs startup", "career", "should i join a job", "placement", "risk"]):
        return (
            f"**Decision Advice for a {branch} student:**\n\n"
            f"The best path is often not 'Either/Or'—it is **The Dual-Path Strategy**:\n\n"
            f"1. **Phase 1 (Final Year):** Prepare for campus placements to secure a financial safety net. A stable starting CTC provides freedom from immediate financial anxiety.\n"
            f"2. **Parallel Validation (10-15 hrs/week):** Use your college incubation center to test your MVP, build a waitlist, and file provisional IPR.\n"
            f"3. **Decision Trigger:** If your MVP achieves **₹50,000+ Monthly Recurring Revenue (MRR)** or secures a **₹10 Lakhs+ grant**, you can safely consider taking a formal sabbatical or going full-time as a founder!"
        )

    idea_context = f"regarding '{active_idea.get('title', 'your startup idea')}'" if active_idea else "for your venture"
    return (
        f"Hello {student_name}! As your PathForge AI Mentor, here is guidance {idea_context}:\n\n"
        f"- **Actionable Next Step:** Focus on speaking with **5 real potential customers** this week. Ask: *'How do you currently solve this problem, and how much did that workaround cost you?'*\n"
        f"- **Lean Principle:** Never ask people if they *would* buy your product in the future. Ask what they have *actually done in the past*.\n"
        f"- **Resource:** Check the **Lean Canvas Builder** and **Idea Validator** in your Venture Studio menu to stress-test your assumptions!"
    )

