import os
import json
from datetime import datetime, timezone
from flask import Flask, render_template, session
from config import config
from models import db
from models.user import User
from models.subscription import Subscription, PaymentInvoice, Coupon
from models.assessment import Assessment
from models.venture import VentureIdea, DesignThinkingNote, LeanCanvas, MVPPlan, PitchDeck, JourneyTracker
from services.seed_data import COUPONS_SEED, STARTUP_IDEAS_SEED, CAREERS_SEED
from services import fallback_engine

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize Database
    db.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.assessment import assessment_bp
    from routes.venture import venture_bp
    from routes.subscription import subscription_bp
    from routes.api import api_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(venture_bp)
    app.register_blueprint(subscription_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    # Global Context Processor
    @app.context_processor
    def inject_global_context():
        user = None
        if "user_id" in session:
            user = User.query.get(session["user_id"])
        return {
            "current_user": user,
            "now": datetime.now(timezone.utc),
            "is_anthropic_live": config.has_anthropic_key,
            "is_razorpay_live": config.has_razorpay_keys
        }

    # Custom Jinja Filters
    @app.template_filter("currency_inr")
    def currency_inr(val):
        try:
            return f"₹{float(val):,.0f}"
        except (ValueError, TypeError):
            return f"₹{val}"

    # Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template("index.html", error_message="The requested page could not be found."), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("index.html", error_message="An internal server error occurred."), 500

    # Auto-initialize and seed DB on start
    with app.app_context():
        db.create_all()
        seed_initial_database()

    return app


def seed_initial_database():
    """Seeds coupons, demo admin, and starter student data if database is fresh."""
    # 1. Seed Coupons
    if Coupon.query.count() == 0:
        for c in COUPONS_SEED:
            coupon = Coupon(
                code=c["code"],
                discount_percentage=c["discount_percentage"],
                max_uses=c.get("max_uses", 500)
            )
            db.session.add(coupon)
        db.session.commit()

    # 2. Seed Admin User
    admin = User.query.filter_by(email="admin@pathforge.edu").first()
    if not admin:
        admin = User(name="PathForge Admin", email="admin@pathforge.edu", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.flush()

        admin_sub = Subscription(
            user_id=admin.id,
            plan="founder",
            billing_cycle="yearly",
            status="active",
            amount_paid=4499.0,
            payment_id="pay_admin_seed",
            order_id="order_admin_seed"
        )
        db.session.add(admin_sub)
        db.session.commit()

    # 3. Seed Demo Student User for instant viva testing
    demo_student = User.query.filter_by(email="student@pathforge.edu").first()
    if not demo_student:
        demo_student = User(name="Aarav Sharma", email="student@pathforge.edu", role="student")
        demo_student.set_password("student123")
        db.session.add(demo_student)
        db.session.flush()

        # Seed Journey Tracker
        tracker = JourneyTracker(
            user_id=demo_student.id,
            overall_progress=65,
            badges_raw=json.dumps(["Compass Explorer", "Compass Navigator", "Venture Ideator", "Lean Architect"])
        )
        db.session.add(tracker)

        # Seed initial completed assessment
        payload = {
            "branch": "Computer Science & Engineering",
            "year_of_study": "3rd Year",
            "college": "Indian Institute of Information Technology",
            "interests": ["Artificial Intelligence", "SaaS & Web Applications", "CleanTech"],
            "skills": {
                "Python & Backend": 8.5,
                "Web Development": 8.0,
                "Machine Learning": 7.5,
                "Product Design": 7.0,
                "Communication": 8.0
            },
            "strengths": ["Rapid Prototyping", "Critical Thinking", "Product Empathy"],
            "risk_appetite": 6,
            "stability_vs_autonomy": 6,
            "hours_per_week": 18,
            "capital_willing": "Low (₹0 - ₹10,000)",
            "primary_goal": "job"
        }
        tri_scores = fallback_engine.compute_tri_path_scores(payload)
        top_careers = fallback_engine.generate_career_compass(payload)

        assessment = Assessment(
            user_id=demo_student.id,
            branch=payload["branch"],
            year_of_study=payload["year_of_study"],
            college=payload["college"],
            risk_appetite=6,
            stability_vs_autonomy=6,
            hours_per_week=18,
            capital_willing=payload["capital_willing"],
            primary_goal="job",
            job_readiness_score=tri_scores["job_score"],
            higher_studies_score=tri_scores["higher_studies_score"],
            venture_readiness_score=tri_scores["venture_score"]
        )
        assessment.interests = payload["interests"]
        assessment.skills = payload["skills"]
        assessment.strengths = payload["strengths"]
        assessment.careers = top_careers
        db.session.add(assessment)
        db.session.flush()

        # Seed 2 Venture Ideas
        idea1 = VentureIdea(
            user_id=demo_student.id,
            title="KisanSense – Autonomous IoT Soil & Microclimate Intelligence",
            tagline="Solar-powered IoT probe giving Indian smallholders hyper-local irrigation advice via WhatsApp.",
            problem_statement="Smallholder farmers lose up to 35% of crops due to erratic watering and over-fertilization, while commercial soil testing labs take 3 weeks and cost ₹1,500 per test.",
            target_customer="Marginal farmers (2-5 acres) and Farmer Producer Organizations (FPOs) across Maharashtra and Andhra Pradesh.",
            solution="A ₹2,499 solar-powered plug-and-play soil sensor that sends voice & text advisory in 8 Indian regional languages directly via WhatsApp, saving 40% water and 25% fertilizer expense.",
            why_now="Rapid expansion of 4G/5G in rural India + Government push for digital agriculture (Digital Agriculture Mission 2024-25) + falling sensor BOM costs.",
            revenue_model="Hardware sale (₹2,499 one-time) + ₹99/month seasonal crop advisory subscription.",
            complexity="Medium",
            is_active_venture=True,
            validation_score=86,
            validation_verdict="GO"
        )
        db.session.add(idea1)
        db.session.flush()

        # Seed Lean Canvas for Idea 1
        canvas_data = fallback_engine.generate_lean_canvas({
            "title": idea1.title,
            "problem_statement": idea1.problem_statement,
            "target_customer": idea1.target_customer,
            "solution": idea1.solution,
            "why_now": idea1.why_now,
            "revenue_model": idea1.revenue_model
        })
        canvas = LeanCanvas(
            user_id=demo_student.id,
            idea_id=idea1.id,
            title=canvas_data["title"],
            problem=canvas_data["problem"],
            customer_segments=canvas_data["customer_segments"],
            unique_value_proposition=canvas_data["unique_value_proposition"],
            solution=canvas_data["solution"],
            channels=canvas_data["channels"],
            revenue_streams=canvas_data["revenue_streams"],
            cost_structure=canvas_data["cost_structure"],
            key_metrics=canvas_data["key_metrics"],
            unfair_advantage=canvas_data["unfair_advantage"],
            early_adopters=canvas_data["early_adopters"],
            existing_alternatives=canvas_data["existing_alternatives"],
            high_level_concept=canvas_data["high_level_concept"]
        )
        db.session.add(canvas)

        # Seed Design Thinking starter notes
        starter_notes = [
            ("empathize", "Farmer Discovery Note", "Farmers in Nashik district rely on visual finger-feel for soil moisture, leading to severe root rot during humid weeks.", "amber"),
            ("define", "How Might We (HMW)", "How might we give non-English speaking farmers real-time soil moisture alerts without requiring smartphone app installations?", "sky"),
            ("ideate", "WhatsApp Voice Bot Solution", "Direct WhatsApp audio notes in Marathi that speak out: 'Bhaurao, your north field needs 2 hours of drip today.'", "emerald"),
            ("prototype", "Pilot Probe Hardware", "Constructed ESP32 capacitive sensor with solar lithium cell enclosed in IP67 PVC tube for ₹850 BOM.", "rose"),
            ("test", "Initial Field Pilot", "Deployed 5 units with Baramati Grape Growers; 100% reported water saving and asked to purchase 10 more.", "purple")
        ]
        for idx, (stg, tit, cont, col) in enumerate(starter_notes):
            n = DesignThinkingNote(
                user_id=demo_student.id,
                idea_id=idea1.id,
                stage=stg,
                title=tit,
                content=cont,
                color=col,
                order_index=idx
            )
            db.session.add(n)

        # Seed sample invoice
        inv = PaymentInvoice(
            user_id=demo_student.id,
            invoice_number=f"INV-{datetime.now().strftime('%Y%m')}-DEMO01",
            plan="Free",
            billing_cycle="Monthly",
            amount=0.0,
            currency="INR",
            payment_method="Free Starter Plan",
            status="paid"
        )
        db.session.add(inv)
        db.session.commit()

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

