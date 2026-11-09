"""
PathForge Seed Data:
- 15+ curated careers with skill-gap radar benchmarks, roadmaps, and venture bridges
- 10+ sample startup ideas mapped to academic branches and student skills
- Subscription plans and coupon codes
"""

CAREERS_SEED = [
    {
        "id": "fullstack_ai_dev",
        "title": "Full-Stack AI Application Engineer",
        "category": "Technology & AI",
        "match_keywords": ["python", "javascript", "machine learning", "web development", "cloud", "apis"],
        "salary_range": "₹12 - ₹28 LPA",
        "market_demand": "Very High (42% YoY growth)",
        "description": "Architects modern responsive applications powered by LLMs, vector search, and scalable cloud microservices.",
        "skills_benchmark": {
            "Python/Backend": 85,
            "Frontend (JS/React)": 80,
            "AI/ML & APIs": 85,
            "System Design": 75,
            "DevOps & Cloud": 70
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Modern Full-Stack Mastery", "details": "Build REST & GraphQL APIs with FastAPI/Flask and clean reactive frontends."},
            {"month": "Month 3-4", "focus": "Applied GenAI & Vector Databases", "details": "Integrate Claude/OpenAI APIs, embeddings, PGVector/Pinecone, and RAG pipelines."},
            {"month": "Month 5", "focus": "Production Deployment & Caching", "details": "Containerize with Docker, deploy to AWS/Render with Redis caching and CI/CD."},
            {"month": "Month 6", "focus": "Portfolio Capstones & System Interviews", "details": "Ship 2 end-to-end fullstack AI SaaS products and solve high-concurrency design problems."}
        ],
        "certifications": [
            "AWS Certified Developer – Associate",
            "DeepLearning.AI: LangChain & LLM Application Development",
            "Full Stack Open – University of Helsinki"
        ],
        "venture_bridge": "Turn these skills into a Vertical AI Micro-SaaS for a niche industry (legal document parsing, regional language customer care, or automated code review tools)."
    },
    {
        "id": "product_manager",
        "title": "Associate Product Manager (APM / Tech PM)",
        "category": "Product & Strategy",
        "match_keywords": ["product management", "ui/ux", "communication", "analytics", "business", "strategy"],
        "salary_range": "₹14 - ₹30 LPA",
        "market_demand": "High (Top choice for tech grads)",
        "description": "Leads cross-functional teams of engineers and designers to define product roadmaps, user stories, and GTM strategy.",
        "skills_benchmark": {
            "Product Strategy": 85,
            "User Research & UX": 80,
            "Data Analytics": 75,
            "Technical Empathy": 70,
            "Stakeholder Leadership": 85
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Product Thinking & Problem Breakdown", "details": "Study tear-downs, write PRDs (Product Requirement Documents), master wireframing with Figma."},
            {"month": "Month 3-4", "focus": "Metrics & Product Analytics", "details": "A/B testing frameworks, funnel optimization, cohort retention using Mixpanel/PostHog."},
            {"month": "Month 5", "focus": "Agile Sprints & Delivery", "details": "Scrum rituals, backlog grooming, cross-functional engineering management."},
            {"month": "Month 6", "focus": "APM Case Studies & Interviews", "details": "Complete 5 end-to-end product case studies on market leaders and startup pivots."}
        ],
        "certifications": [
            "Reforge Product Strategy / Pragmatic Institute PM",
            "Google Project Management Professional Certificate",
            "Scrum Alliance: Certified Scrum Product Owner (CSPO)"
        ],
        "venture_bridge": "APMs possess the exact core toolkit of a Startup CEO: discovery, Lean experimentation, unit economics, and team synchronization."
    },
    {
        "id": "data_scientist_ml",
        "title": "Data Scientist & Predictive Modeler",
        "category": "Data & Analytics",
        "match_keywords": ["python", "data science", "sql", "statistics", "machine learning", "visualization"],
        "salary_range": "₹10 - ₹24 LPA",
        "market_demand": "High (Data-driven decision making)",
        "description": "Transforms structured and unstructured enterprise data into predictive forecasting models and strategic business insights.",
        "skills_benchmark": {
            "Statistics & Math": 85,
            "Python & Pandas": 90,
            "SQL & Data Pipelines": 80,
            "Machine Learning": 75,
            "Data Storytelling": 75
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Advanced SQL & Exploratory Data Analysis", "details": "Window functions, subqueries, Pandas, NumPy, statistical hypothesis testing."},
            {"month": "Month 3-4", "focus": "Supervised & Unsupervised ML", "details": "Scikit-Learn, XGBoost, feature engineering, cross-validation and hyperparameter tuning."},
            {"month": "Month 5", "focus": "Model Serving & Monitoring", "details": "Flask/FastAPI model inference endpoints, MLflow tracking, drift detection."},
            {"month": "Month 6", "focus": "Real-world Kaggle Competitions & Research", "details": "Deploy 2 business analytics apps with interactive Streamlit/Chart dashboards."}
        ],
        "certifications": [
            "IBM Data Science Professional Certificate",
            "Google Data Analytics Certificate",
            "Databricks Certified Data Engineer Associate"
        ],
        "venture_bridge": "Build an AI-powered churn prediction or demand forecasting SaaS for direct-to-consumer (D2C) brands or local retail chains."
    },
    {
        "id": "cybersecurity_analyst",
        "title": "Cybersecurity & Cloud Defense Specialist",
        "category": "Security & Infrastructure",
        "match_keywords": ["cybersecurity", "networking", "linux", "cloud", "security", "ethical hacking"],
        "salary_range": "₹9 - ₹22 LPA",
        "market_demand": "Critical (Severe global talent shortage)",
        "description": "Defends organizational infrastructure against zero-day exploits, conducts penetration testing, and ensures regulatory compliance.",
        "skills_benchmark": {
            "Network Protocols": 85,
            "Penetration Testing": 80,
            "Cloud Security (AWS/Azure)": 75,
            "Incident Response": 80,
            "Compliance & Auditing": 70
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Core Networking & Linux Hardening", "details": "TCP/IP, Wireshark packet capture, Linux system administration and bash scripting."},
            {"month": "Month 3-4", "focus": "Vulnerability Assessment & Web Security", "details": "OWASP Top 10 vulnerabilities, Burp Suite, TryHackMe and HackTheBox labs."},
            {"month": "Month 5", "focus": "SIEM & SOC Operations", "details": "Splunk, Microsoft Sentinel log analysis, incident triage and mitigation playbooks."},
            {"month": "Month 6", "focus": "Industry Certifications & Red/Blue Teaming", "details": "Prepare CompTIA Security+ / CEH and publish detailed vulnerability write-ups."}
        ],
        "certifications": [
            "CompTIA Security+ (SY0-701)",
            "Certified Ethical Hacker (CEH) / eJPT",
            "AWS Certified Security – Specialty"
        ],
        "venture_bridge": "Launch a Cybersecurity Compliance Automation Agency or API Security Audit tool tailored for Indian FinTechs and startups."
    },
    {
        "id": "uiux_designer",
        "title": "Lead UI/UX & Design Systems Architect",
        "category": "Design & Human Experience",
        "match_keywords": ["ui/ux", "design", "figma", "user research", "prototyping", "creative"],
        "salary_range": "₹8 - ₹20 LPA",
        "market_demand": "High (Product differentiation driver)",
        "description": "Crafts intuitive, accessible, and delightful digital user experiences through iterative wireframing, usability tests, and design systems.",
        "skills_benchmark": {
            "Figma & Prototyping": 90,
            "User Research & Personas": 80,
            "Information Architecture": 80,
            "Design Systems & Tokens": 75,
            "Frontend Handoff": 70
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Design Fundamentals & Typography", "details": "Visual hierarchy, layout grids, color psychology, accessibility (WCAG 2.1)."},
            {"month": "Month 3-4", "focus": "User Journey Mapping & Usability Testing", "details": "Conduct 10+ user interviews, synthesize empathy maps, create interactive prototypes."},
            {"month": "Month 5", "focus": "Design Systems & Component Libraries", "details": "Build atomic design systems with Figma auto-layout, variants, and variables."},
            {"month": "Month 6", "focus": "High-Impact Portfolio Launch", "details": "Publish 3 comprehensive case studies on Behance/Dribbble with quantifiable business metrics."}
        ],
        "certifications": [
            "Google UX Design Professional Certificate",
            "Interaction Design Foundation (IxDF) Certified UX Specialist",
            "Figma Professional Designer Certification"
        ],
        "venture_bridge": "Launch a Productized UX Audit & Conversion Rate Optimization (CRO) Studio for fast-growing SaaS startups."
    },
    {
        "id": "fintech_analyst",
        "title": "FinTech Quantitative Analyst & Wealth Strategist",
        "category": "Finance & Quantitative",
        "match_keywords": ["finance", "analytics", "python", "markets", "accounting", "risk"],
        "salary_range": "₹11 - ₹26 LPA",
        "market_demand": "High (Surge in digital financial services)",
        "description": "Builds algorithmic trading models, analyzes credit risk datasets, and crafts next-gen digital banking solutions.",
        "skills_benchmark": {
            "Financial Modeling": 85,
            "Python/R Quant Tools": 80,
            "Risk Assessment": 85,
            "Regulatory Compliance (RBI/SEBI)": 75,
            "Algorithmic Logic": 75
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Corporate Finance & Capital Markets", "details": "Discounted cash flow (DCF), financial statements analysis, ratio analysis."},
            {"month": "Month 3-4", "focus": "Python for Quantitative Finance", "details": "NumPy, Pandas, time-series forecasting, portfolio optimization (Sharpe ratio, VaR)."},
            {"month": "Month 5", "focus": "FinTech Systems & Open Banking APIs", "details": "Account Aggregator framework, UPI architecture, credit underwriting models."},
            {"month": "Month 6", "focus": "Valuation & CFA Level 1 Foundations", "details": "Build automated backtesting models and present simulated investment memos."}
        ],
        "certifications": [
            "CFA Level 1 Candidate / NISM Equity Derivatives",
            "Columbia University: FinTech Innovation on Coursera",
            "Financial Modeling & Valuation Analyst (FMVA) – CFI"
        ],
        "venture_bridge": "Start an automated micro-savings or alternative credit scoring platform for college students and gig workers."
    },
    {
        "id": "growth_marketer",
        "title": "Performance Marketer & Growth Hacker",
        "category": "Marketing & Growth",
        "match_keywords": ["marketing", "growth", "seo", "analytics", "content", "social media"],
        "salary_range": "₹7 - ₹18 LPA",
        "market_demand": "High (Customer acquisition engine)",
        "description": "Drives exponential user acquisition, viral loops, and search engine dominance using rapid experimental marketing.",
        "skills_benchmark": {
            "Paid Ads (Meta/Google)": 85,
            "SEO & Content Loops": 80,
            "Conversion Optimization": 80,
            "Lifecycle Email/SMS Marketing": 75,
            "Data Analytics (GA4)": 80
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Organic Search & Technical SEO", "details": "Keyword research, programmatic SEO, technical site speed, backlink strategies."},
            {"month": "Month 3-4", "focus": "Performance Marketing & Funnel Architecture", "details": "Meta Ads Manager, Google Search/Performance Max campaigns, ROAS optimization."},
            {"month": "Month 5", "focus": "Retention & Marketing Automation", "details": "Klaviyo/CleverTap push notifications, automated onboarding drip sequences."},
            {"month": "Month 6", "focus": "Cold Outreach & B2B Lead Gen", "details": "LinkedIn Sales Navigator, Apollo.io scraping, running live growth campaigns with verifiable ROI."}
        ],
        "certifications": [
            "Google Ads & Google Analytics 4 Certification",
            "HubSpot Inbound Marketing & Growth-Driven Design",
            "Reforge Growth Series"
        ],
        "venture_bridge": "Form a Growth-as-a-Service Agency or Content Engine generating qualified leads for niche B2B services on revenue share."
    },
    {
        "id": "cloud_devops_engineer",
        "title": "Cloud Architect & Site Reliability Engineer (SRE)",
        "category": "Technology & Infrastructure",
        "match_keywords": ["cloud", "devops", "linux", "docker", "kubernetes", "networking"],
        "salary_range": "₹12 - ₹30 LPA",
        "market_demand": "Very High (Cloud modernization)",
        "description": "Maintains high uptime, designs fault-tolerant cloud infrastructures, and automates CI/CD deployment pipelines.",
        "skills_benchmark": {
            "Docker & Kubernetes": 85,
            "AWS/Azure/GCP Cloud": 85,
            "Terraform (IaC)": 80,
            "CI/CD (GitHub Actions)": 85,
            "Monitoring (Prometheus/Grafana)": 75
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Linux Sysadmin & Containerization", "details": "Deep bash scripting, Docker multi-stage builds, networking namespaces."},
            {"month": "Month 3-4", "focus": "Kubernetes Cluster Management", "details": "Pods, Services, Ingress, Helm charts, self-healing architecture."},
            {"month": "Month 5", "focus": "Infrastructure as Code (IaC)", "details": "Terraform modules, AWS VPC, ECS, RDS automated provisioning."},
            {"month": "Month 6", "focus": "Observability & Chaos Engineering", "details": "Deploy Grafana/Prometheus dashboards and execute simulated failover recovery."}
        ],
        "certifications": [
            "Certified Kubernetes Administrator (CKA)",
            "AWS Certified Solutions Architect – Associate",
            "HashiCorp Certified: Terraform Associate"
        ],
        "venture_bridge": "Create a Developer Tooling or Cloud Cost Optimization platform (FinOps) that automatically cuts AWS bills for startups by 30%."
    },
    {
        "id": "embedded_iot_engineer",
        "title": "Embedded Systems & IoT Hardware Engineer",
        "category": "Hardware & Electronics",
        "match_keywords": ["embedded", "iot", "c/c++", "hardware", "electronics", "robotics"],
        "salary_range": "₹8 - ₹20 LPA",
        "market_demand": "Moderate-High (Smart devices, EV, robotics)",
        "description": "Programs microcontrollers, designs custom PCB layouts, and creates connected hardware for automotive, smart cities, and healthcare.",
        "skills_benchmark": {
            "Embedded C/C++": 85,
            "PCB Design (KiCad)": 75,
            "Microcontrollers (STM32/ESP32)": 85,
            "IoT Protocols (MQTT/BLE)": 80,
            "Hardware Debugging": 80
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Embedded C & Registers", "details": "GPIO, Timers, Interrupts, I2C, SPI, and UART protocols on ARM Cortex-M."},
            {"month": "Month 3-4", "focus": "Real-Time Operating Systems (FreeRTOS)", "details": "Tasks, queues, semaphores, memory management in multi-threaded hardware."},
            {"month": "Month 5", "focus": "KiCad Schematic & PCB Layout", "details": "Component selection, 2-layer routing, signal integrity, and fabrication ordering."},
            {"month": "Month 6", "focus": "Connected IoT Mesh Prototype", "details": "Build an ESP32 edge sensor node streaming sensor metrics to an AWS IoT dashboard."}
        ],
        "certifications": [
            "Arm Certified Engineer (Arm Education)",
            "Coursera: Embedded Software Essentials – University of Colorado",
            "IPC-A-610 Electronic Assemblies Standard"
        ],
        "venture_bridge": "Design smart IoT hardware for smart farming (soil sensors), cold storage logistics, or industrial predictive maintenance."
    },
    {
        "id": "biotech_health_analyst",
        "title": "Bioinformatics & Computational Health Specialist",
        "category": "Biotech & Healthcare",
        "match_keywords": ["biotechnology", "python", "research", "healthcare", "data science"],
        "salary_range": "₹8 - ₹22 LPA",
        "market_demand": "Growing rapidly (Personalized medicine)",
        "description": "Applies statistical modeling and sequence analysis algorithms to genomic, clinical, and drug discovery datasets.",
        "skills_benchmark": {
            "Genomics & Biopython": 85,
            "Statistical Genetics": 80,
            "Data Pipeline Engineering": 75,
            "Healthcare Regulatory (FDA/CDSCO)": 70,
            "Clinical Trial Analytics": 75
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Biopython & Sequence Data", "details": "FASTA/FASTQ parsing, BLAST tools, biological databases (NCBI, UniProt)."},
            {"month": "Month 3-4", "focus": "Next-Gen Sequencing (NGS) Pipelines", "details": "Read alignment (BWA), variant calling (GATK), RNA-seq differential expression."},
            {"month": "Month 5", "focus": "Structural Bioinformatics & Docking", "details": "PyMOL, molecular dynamics, AutoDock Vina for ligand-protein binding."},
            {"month": "Month 6", "focus": "Healthcare Predictive Capstone", "details": "Publish an open-source clinical risk stratification predictor on real EHR datasets."}
        ],
        "certifications": [
            "Coursera: Genomic Data Science Specialization – Johns Hopkins",
            "NCBI Bioinformatics Essentials",
            "Good Clinical Practice (GCP) Certification"
        ],
        "venture_bridge": "Launch a Preventive Health Diagnostics or AI-assisted Pathology Screening service partnering with local diagnostic labs."
    },
    {
        "id": "cleantech_energy_engineer",
        "title": "CleanTech & Renewable Energy Systems Engineer",
        "category": "Sustainability & Energy",
        "match_keywords": ["sustainability", "energy", "clean technology", "mechanical", "electrical"],
        "salary_range": "₹8 - ₹20 LPA",
        "market_demand": "High (Net-zero 2070 targets & EV revolution)",
        "description": "Designs grid-scale solar/wind installations, battery storage management systems, and industrial decarbonization models.",
        "skills_benchmark": {
            "Solar/Renewable System Design": 85,
            "Battery Tech & BMS": 80,
            "Energy Auditing & Carbon Accounting": 80,
            "Simulation (MATLAB/HOMER)": 75,
            "Green Building Standards": 70
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Solar PV & Storage System Sizing", "details": "PVSyst software, grid-tied inverter modeling, tilt angles and irradiance data."},
            {"month": "Month 3-4", "focus": "Battery Chemistry & BMS Architecture", "details": "Li-ion cell monitoring, thermal runaway prevention, state of charge (SoC) algorithms."},
            {"month": "Month 5", "focus": "Industrial Carbon Accounting & ESG", "details": "GHG Protocol Scope 1, 2, 3 calculations, energy efficiency audits in commercial buildings."},
            {"month": "Month 6", "focus": "Decarbonization Feasibility Project", "details": "Produce a full bankable techno-commercial report for a 500kW rooftop solar & BESS microgrid."}
        ],
        "certifications": [
            "Certified Energy Auditor (BEE India / AEE CEM)",
            "NABCEP PV Associate Certification",
            "GRIHA Certified Green Building Professional"
        ],
        "venture_bridge": "Start an Energy-as-a-Service company helping MSMEs switch to solar with zero upfront capex via power purchase agreements (PPAs)."
    },
    {
        "id": "blockchain_web3_dev",
        "title": "Smart Contract & Decentralized Protocol Architect",
        "category": "Technology & Web3",
        "match_keywords": ["blockchain", "solidity", "cryptography", "web development", "security"],
        "salary_range": "₹12 - ₹32 LPA",
        "market_demand": "High (Enterprise tokenization & DeFi)",
        "description": "Develops trustless smart contracts, zero-knowledge proofs, and decentralized storage applications on EVM networks.",
        "skills_benchmark": {
            "Solidity & EVM Architecture": 85,
            "Smart Contract Security Audit": 80,
            "Ethers.js / Web3.js Integration": 80,
            "Cryptography & Tokenomics": 75,
            "Decentralized Storage (IPFS)": 70
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Solidity Syntax & EVM Fundamentals", "details": "Gas optimization, storage layout, ERC-20, ERC-721 token standards."},
            {"month": "Month 3-4", "focus": "Hardhat & Foundry Testing Suites", "details": "Fuzz testing, invariant testing, reentrancy attacks, flash loan mechanics."},
            {"month": "Month 5", "focus": "Decentralized Frontend (dApp)", "details": "Wagmi, Viem, Next.js, wallet connection states and signature verification."},
            {"month": "Month 6", "focus": "Security Audit Contest Submissions", "details": "Participate in Code4rena audits and deploy a tested DeFi liquidity staking vault."}
        ],
        "certifications": [
            "Certified Ethereum Developer – Blockchain Council",
            "Cyfrin Updraft Smart Contract Security Certification",
            "ConsenSys Academy Blockchain Developer"
        ],
        "venture_bridge": "Build an on-chain credential verification network for Indian universities to eliminate fake degree certificates."
    },
    {
        "id": "edtech_instructional_designer",
        "title": "EdTech Learning Experience Architect",
        "category": "Education & Design",
        "match_keywords": ["education", "teaching", "communication", "content", "psychology"],
        "salary_range": "₹7 - ₹16 LPA",
        "market_demand": "Moderate-High (Digital upskilling demand)",
        "description": "Designs gamified, pedagogy-backed learning pathways, interactive simulations, and adaptive curriculum platforms.",
        "skills_benchmark": {
            "Pedagogy & Adult Learning Theory": 85,
            "Gamification & Micro-learning": 85,
            "Interactive Authoring Tools": 75,
            "Curriculum Analytics": 75,
            "Instructional Video Production": 70
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "ADDIE & Bloom's Taxonomy", "details": "Formulate learning objectives, formative vs summative assessments, cognitive load theory."},
            {"month": "Month 3-4", "focus": "Interactive Module Authoring", "details": "Articulate Storyline, SCORM packages, gamified badge systems, branch scenarios."},
            {"month": "Month 5", "focus": "LMS Architecture & Learner Telemetry", "details": "Moodle, Canvas LMS configuration, completion rate analytics, drop-off reduction."},
            {"month": "Month 6", "focus": "Cohort-Based Course Launch", "details": "Design, market, and run a live 2-week cohort course for 50+ students with 80%+ completion."}
        ],
        "certifications": [
            "ATD Instructional Design Certificate",
            "Coursera: Learning How to Learn – UC San Diego",
            "Gamification Certification – University of Pennsylvania"
        ],
        "venture_bridge": "Build an AI-native micro-skilling boot camp that guarantees job placement for tier-2/3 college engineers in 90 days."
    },
    {
        "id": "agritech_solutions_lead",
        "title": "AgriTech Supply Chain & Precision Farming Specialist",
        "category": "Agriculture & Supply Chain",
        "match_keywords": ["agriculture", "iot", "supply chain", "robotics", "data science"],
        "salary_range": "₹8 - ₹19 LPA",
        "market_demand": "High (Farm mechanization & cold-chain modernization)",
        "description": "Integrates remote satellite sensing, soil quality analytics, and fair-price market linkages for Indian agricultural producers.",
        "skills_benchmark": {
            "GIS & Remote Sensing (NDVI)": 80,
            "Agricultural Economics & Mandi Systems": 85,
            "Farm IoT Sensors": 75,
            "Cold Chain & Post-Harvest Logistics": 80,
            "Rural Distribution Strategy": 80
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Satellite Imagery & Crop Health Analytics", "details": "Google Earth Engine, Sentinel-2 imagery processing, NDVI vegetation indices."},
            {"month": "Month 3-4", "focus": "Agri-Supply Chain & Farm Economics", "details": "APMC mandi pricing, warehouse receipt financing, post-harvest losses mitigation."},
            {"month": "Month 5", "focus": "Precision Irrigation & Soil Sensors", "details": "Telemetry gateways, solar drip irrigation controllers, moisture threshold alerts."},
            {"month": "Month 6", "focus": "Farmer Producer Org (FPO) Partnership", "details": "Pilot a direct-to-retail produce aggregation model with 20+ local farming families."}
        ],
        "certifications": [
            "ISRO: Remote Sensing and GIS Applications in Agriculture",
            "FAO: Sustainable Agriculture and Rural Development",
            "Supply Chain Operations Professional (APICS / ASCM)"
        ],
        "venture_bridge": "Launch a Farm-to-Fork B2B procurement network that eliminates 3 tiers of middlemen, boosting farmer incomes by 25%."
    },
    {
        "id": "robotics_automation_engineer",
        "title": "Robotics & Warehouse Automation Engineer",
        "category": "Robotics & Automation",
        "match_keywords": ["robotics", "computer vision", "ros", "c++", "mechanical", "electronics"],
        "salary_range": "₹10 - ₹25 LPA",
        "market_demand": "High (E-commerce fulfillment centers & EV manufacturing)",
        "description": "Programs Autonomous Mobile Robots (AMRs), industrial robotic arms, and automated optical inspection systems.",
        "skills_benchmark": {
            "ROS2 (Robot Operating System)": 85,
            "Computer Vision (OpenCV)": 80,
            "Motion Planning (MoveIt)": 80,
            "C++ & Real-time Systems": 85,
            "Kinematics & Dynamics": 75
        },
        "roadmap_6_months": [
            {"month": "Month 1-2", "focus": "Modern C++ & Linear Algebra for Robotics", "details": "Modern C++20, Eigen library, transformation matrices, Euler angles and quaternions."},
            {"month": "Month 3-4", "focus": "ROS2 Navigation & SLAM", "details": "Nav2 stack, LIDAR point cloud processing, Gazebo simulation, Cartographer SLAM."},
            {"month": "Month 5", "focus": "Robotic Vision & Pick-and-Place", "details": "YOLOv8 object detection, eye-in-hand camera calibration, collision-free trajectory planning."},
            {"month": "Month 6", "focus": "Hardware In-the-Loop Simulation", "details": "Simulate and deploy an autonomous patrol or material handling robot in a simulated warehouse."}
        ],
        "certifications": [
            "ROS2 Basics & Navigation – The Construct",
            "Robotics Specialization – University of Pennsylvania (Coursera)",
            "FANUC / ABB Industrial Robotics Programmer Certification"
        ],
        "venture_bridge": "Build affordable robotic sorting arms or automated guided carts for tier-2 Indian logistics hubs and garment factories."
    }
]

STARTUP_IDEAS_SEED = [
    {
        "title": "KisanSense – Autonomous IoT Soil & Microclimate Intelligence",
        "tagline": "Solar-powered IoT probe giving Indian smallholders hyper-local irrigation and fertilizer advice via WhatsApp.",
        "category": "AgriTech & Hardware",
        "problem_statement": "Smallholder farmers lose up to 35% of crops due to erratic watering and over-fertilization, while commercial soil testing labs take 3 weeks and cost ₹1,500 per test.",
        "target_customer": "Marginal farmers (2-5 acres) and Farmer Producer Organizations (FPOs) across Maharashtra, Punjab, and Andhra Pradesh.",
        "solution": "A ₹2,499 solar-powered plug-and-play soil sensor that sends voice & text advisory in 8 Indian regional languages directly via WhatsApp, saving 40% water and 25% fertilizer expense.",
        "why_now": "Rapid expansion of 4G/5G in rural India + Government push for digital agriculture (Digital Agriculture Mission 2024-25) + falling sensor BOM costs.",
        "revenue_model": "Hardware sale (₹2,499 one-time) + ₹99/month seasonal crop advisory subscription.",
        "complexity": "Medium"
    },
    {
        "title": "VeriSkill – Cryptographic Proof-of-Competence Network",
        "tagline": "Tamper-proof verifiable skills portfolio for engineering students verified by automated code audits.",
        "category": "EdTech & Web3 / HRTech",
        "problem_statement": "Resumes are flooded with exaggerated claims and AI-generated buzzwords; campus recruiters spend ₹4,000 per candidate just filtering unqualified applicants.",
        "target_customer": "Tech recruiters at high-growth startups and engineering students seeking merit-based job placement.",
        "solution": "Students complete live sandbox coding challenges and real GitHub project audits; their verified performance is minted as a tamper-proof digital credential recruiters can trust instantly.",
        "why_now": "AI-generated resumes have made traditional CV screening obsolete; companies demand verifiable proof-of-work over paper degrees.",
        "revenue_model": "Freemium for students; B2B subscription for recruiters (₹9,999/month for unlimited candidate verifications).",
        "complexity": "Medium"
    },
    {
        "title": "MediTransit – Zero-Dwell Cold Chain for Temperature-Sensitive Vaccines",
        "tagline": "Phase-change material portable smart coolers with real-time IoT temperature telemetry for rural vaccine logistics.",
        "category": "HealthTech & CleanTech",
        "problem_statement": "Over 20% of temperature-sensitive vaccines and biologics spoil before reaching rural primary health centres (PHCs) due to unreliable ice-pack coolers.",
        "target_customer": "State health missions, vaccine distributors, veterinary pharmaceutical companies, and diagnostic chains.",
        "solution": "Lightweight insulated carriers utilizing non-electric phase change materials (PCM) that hold 2°C–8°C for 72 hours, paired with a BLE-enabled data logger that sends breach alerts.",
        "why_now": "Stricter CDSCO temperature guidelines + rapid expansion of expensive biologics and mRNA treatments requiring unbroken cold chains.",
        "revenue_model": "B2B hardware sales to state health logistics + recurring SaaS dashboard fee for cold-chain compliance certificates.",
        "complexity": "High"
    },
    {
        "title": "FinSetu – Alternative Credit Scoring for Campus Gig Freelancers",
        "tagline": "Turning freelance GitHub commits, Upwork reviews, and UPI flow into bankable credit scores for student founders.",
        "category": "FinTech",
        "problem_statement": "India has 15 million college freelancers and creators earning real income, yet traditional banks reject them for credit cards, laptops, or equipment financing due to zero CIBIL history.",
        "target_customer": "Student freelancers, gig coders, designers, and campus micro-entrepreneurs aged 18-24.",
        "solution": "A machine-learning risk engine that connects to UPI transaction logs, freelance platforms, and GitHub activity to issue a verified 'SetuScore' with pre-approved hardware micro-loans.",
        "why_now": "RBI's Account Aggregator (AA) framework makes financial data sharing instantaneous and secure; exponential rise in campus freelancing.",
        "revenue_model": "1.5% loan origination fee from NBFC lending partners + zero-cost EMI merchant subsidies.",
        "complexity": "High"
    },
    {
        "title": "EcoPack Studio – Agricultural Residue Compostable Packaging",
        "tagline": "Transforming stubble and sugarcane bagasse into molded pulp packaging to replace styrofoam in Indian e-commerce.",
        "category": "Sustainability & Circular Economy",
        "problem_statement": "North India burns 20 million tons of crop stubble every winter causing severe smog, while e-commerce generates 1.2 million tons of non-biodegradable plastic and thermocol cushions.",
        "target_customer": "D2C electronics, cosmetics, and food brands committed to plastic-free shipments.",
        "solution": "Decentralized mini-pulping units in farming clusters that purchase stubble directly from farmers and press it into custom shock-absorbent packaging inserts that biodegrade in 45 days.",
        "why_now": "Single-use plastic bans across Indian states + ESG mandates on top e-commerce players + stubble burning penalties.",
        "revenue_model": "B2B per-unit sales of custom molded packaging at price parity with high-grade expanded polystyrene (₹12 - ₹45 per insert).",
        "complexity": "Medium"
    },
    {
        "title": "DocuPulse AI – Vernacular Medical Discharge Explainer",
        "tagline": "Translates complex hospital discharge summaries into WhatsApp voice notes and visual medication schedules in regional languages.",
        "category": "HealthTech & AI",
        "problem_statement": "68% of hospital readmissions in tier-2/3 cities occur because patients and caregivers misunderstand complex English discharge summaries and medicine timings.",
        "target_customer": "Mid-tier private hospitals, nursing homes, and health insurance providers wanting to reduce 30-day readmissions.",
        "solution": "Hospitals upload the doctor's discharge summary; our HIPAA/ABDM-compliant OCR & LLM engine creates a simplified 2-minute voice note in Hindi, Tamil, Telugu, or Marathi with an illustrated pill schedule.",
        "why_now": "Ayushman Bharat Digital Mission (ABDM) digitization + state-of-the-art multilingual speech synthesis models.",
        "revenue_model": "B2B hospital subscription (₹15,000 to ₹50,000/month per hospital) or ₹30 per processed discharge.",
        "complexity": "Low"
    },
    {
        "title": "CampusHive – Micro-Subletting & Equipment Sharing for Students",
        "tagline": "Peer-to-peer rental marketplace for engineering lab kits, drafting boards, cameras, and festival clothing on campus.",
        "category": "Consumer Marketplace & Sharing Economy",
        "problem_statement": "Students spend thousands buying lab kits, scientific calculators, Arduino boards, and blazers used only for 1 semester, which then sit idle in hostel rooms.",
        "target_customer": "College students living in campus hostels and surrounding PGs.",
        "solution": "Hyper-local peer-to-peer marketplace inside verified college domains with integrated UPI security deposits and locker pickups.",
        "why_now": "High inflation in student textbook and hardware costs + strong Gen Z preference for circular economy and sharing.",
        "revenue_model": "10% commission on peer rentals + campus brand sponsorships.",
        "complexity": "Low"
    },
    {
        "title": "EnerGrid – Micro-Solar Peer-to-Peer Energy Trading",
        "tagline": "Enabling rooftop solar homes to sell excess kilowatt-hours directly to neighbors across local distribution transformers.",
        "category": "CleanTech & Smart Grid",
        "problem_statement": "Rooftop solar owners receive low feed-in tariffs from state DISCOMs with long settlement delays, while commercial shops nearby pay peak commercial tariffs.",
        "target_customer": "Independent bungalow owners with rooftop solar and nearby small commercial establishments.",
        "solution": "Smart IoT energy meters installed at both ends that log energy transactions and execute local peer-to-peer netting with automated UPI billing.",
        "why_now": "National Green Energy Open Access Rules 2023 allow sub-100kW open access + PM Surya Ghar Muft Bijli Yojana installing 10M rooftop solar units.",
        "revenue_model": "₹0.50 facilitation fee per kilowatt-hour traded on the local network.",
        "complexity": "High"
    },
    {
        "title": "CivicWatch – AI-Powered Road Hazard & Municipal Pothole Mapper",
        "tagline": "Crowdsourced dashcam telemetry turning delivery driver bikes into real-time municipal road inspection sensors.",
        "category": "Smart Cities & Mobility",
        "problem_statement": "Municipal corporations spend millions on slow manual road surveys, leaving hazardous potholes unrepaired for months resulting in accidents.",
        "target_customer": "Municipal corporations (Smart Cities Mission) and road maintenance concessionaires (NHAI).",
        "solution": "Delivery drivers (Zomato/Swiggy/Zepto) mount an AI smartphone app that detects potholes and road cracks automatically using edge computer vision, earning micro-rewards for every road scanned.",
        "why_now": "Ultra-fast edge AI inference on sub-₹10,000 smartphones + India's 100 Smart Cities Mission mandate for digital infrastructure auditing.",
        "revenue_model": "SaaS annual subscription sold to municipal corporations (₹10 Lakhs/city/year) for live road health dashboards.",
        "complexity": "Medium"
    },
    {
        "title": "SkillSprint – AI Roleplay Simulator for Campus Placement Interviews",
        "tagline": "Realistic voice-based AI interviewers that grill students on their specific branch and provide instant speech & technical feedback.",
        "category": "EdTech & Career Readiness",
        "problem_statement": "Over 75% of engineering graduates fail company interviews not due to lack of technical know-how, but because of poor verbal articulation and interview anxiety.",
        "target_customer": "Final and pre-final year college students preparing for campus recruitment drives.",
        "solution": "Hyper-realistic voice AI that simulates technical panel interviews for software, mechanical, finance, and consulting roles with real-time feedback on filler words, accuracy, and confidence.",
        "why_now": "Breakthroughs in low-latency voice AI + intensely competitive campus placement environment.",
        "revenue_model": "Freemium (2 free mock interviews) + Pro tier at ₹299 for unlimited interviews + Institutional B2B campus license.",
        "complexity": "Medium"
    }
]

COUPONS_SEED = [
    {"code": "STUDENT20", "discount_percentage": 20, "max_uses": 1000},
    {"code": "STARTUP50", "discount_percentage": 50, "max_uses": 200},
    {"code": "CAMPUSFREE", "discount_percentage": 100, "max_uses": 50}
]

PLANS_INFO = {
    "free": {
        "name": "Free Starter",
        "price_monthly": 0,
        "price_yearly": 0,
        "description": "Essential career guidance and starter venture preview for every student.",
        "features": [
            "1 Dual-Path Assessment",
            "Top 3 Career matches with salary range",
            "Basic Career Roadmap",
            "3 AI Startup Idea generations per month",
            "Venture Studio preview access",
            "Public Business Model and Founder Toolkit"
        ],
        "badge": "Free Forever"
    },
    "pro": {
        "name": "Pro Student",
        "price_monthly": 199,
        "price_yearly": 1799, # ~25% discount
        "description": "For students serious about mastering career pivots and building early-stage prototypes.",
        "features": [
            "Unlimited Dual-Path Assessments",
            "Complete Career Compass & Skill-gap Radar chart",
            "Unlimited AI Startup Idea generations",
            "Interactive Design Thinking Sticky-Note Board",
            "Ash Maurya 9-Block Lean Canvas Builder",
            "Lean Canvas PDF & Clean Print Export",
            "MVP Planner with testable assumptions checklist",
            "Founder Journey Gamified Tracker & Badges"
        ],
        "badge": "Most Popular"
    },
    "founder": {
        "name": "Founder Suite",
        "price_monthly": 499,
        "price_yearly": 4499,
        "description": "The complete venture studio for student entrepreneurs launching real startups.",
        "features": [
            "Everything included in Pro",
            "Deep Idea Validator with TAM/SAM/SOM scorecard",
            "Comprehensive SWOT analysis & GO/REFINE/PIVOT verdict",
            "10-Slide Investor Pitch Deck Builder & One-Pager",
            "60-second Elevator Pitch AI Speech Script",
            "Indian Startup Support Scheme & Incubator Matcher (SISFS, NIDHI-PRAYAS)",
            "Priority AI Mentor Chat with custom contextual memory",
            "Direct Viva & Entrepreneurship Competition Preparation Kit"
        ],
        "badge": "Ultimate Venture"
    }
}

