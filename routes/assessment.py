import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from models.assessment import Assessment
from routes.auth import login_required
from services import fallback_engine

assessment_bp = Blueprint("assessment", __name__)

@assessment_bp.route("/assessment", methods=["GET", "POST"])
@login_required
def start_assessment():
    user = User.query.get(session["user_id"])

    if request.method == "POST":
        branch = request.form.get("branch", "Computer Science & Engineering")
        year_of_study = request.form.get("year_of_study", "3rd Year")
        college = request.form.get("college", "Engineering Institute")

        interests = request.form.getlist("interests")
        if not interests:
            interests = ["Artificial Intelligence / Machine Learning", "SaaS & Web Applications"]

        # Parse skills dictionary
        skill_names = request.form.getlist("skill_name")
        skill_ratings = request.form.getlist("skill_rating")
        skills_dict = {}
        for name, rating in zip(skill_names, skill_ratings):
            if name.strip():
                try:
                    skills_dict[name.strip()] = float(rating)
                except ValueError:
                    skills_dict[name.strip()] = 7.0

        if not skills_dict:
            skills_dict = {
                "Python / Programming": 8,
                "Web Development": 7,
                "Problem Solving": 8,
                "Communication": 7
            }

        strengths = request.form.getlist("strengths")
        if not strengths:
            strengths = ["Rapid Prototyping", "Critical Thinking", "Product Empathy"]

        try:
            risk_appetite = int(request.form.get("risk_appetite", 6))
            stability_vs_autonomy = int(request.form.get("stability_vs_autonomy", 7))
            hours_per_week = int(request.form.get("hours_per_week", 15))
        except ValueError:
            risk_appetite = 6
            stability_vs_autonomy = 7
            hours_per_week = 15

        capital_willing = request.form.get("capital_willing", "Low (₹0 - ₹10,000)")
        primary_goal = request.form.get("primary_goal", "startup")

        assessment_payload = {
            "branch": branch,
            "year_of_study": year_of_study,
            "college": college,
            "interests": interests,
            "skills": skills_dict,
            "strengths": strengths,
            "risk_appetite": risk_appetite,
            "stability_vs_autonomy": stability_vs_autonomy,
            "hours_per_week": hours_per_week,
            "capital_willing": capital_willing,
            "primary_goal": primary_goal
        }

        # Compute Tri-Path Readiness Scores
        tri_scores = fallback_engine.compute_tri_path_scores(assessment_payload)
        # Compute Top Careers
        top_careers = fallback_engine.generate_career_compass(assessment_payload)

        # Save to database
        assessment = Assessment(
            user_id=user.id,
            branch=branch,
            year_of_study=year_of_study,
            college=college,
            risk_appetite=risk_appetite,
            stability_vs_autonomy=stability_vs_autonomy,
            hours_per_week=hours_per_week,
            capital_willing=capital_willing,
            primary_goal=primary_goal,
            job_readiness_score=tri_scores["job_score"],
            higher_studies_score=tri_scores["higher_studies_score"],
            venture_readiness_score=tri_scores["venture_score"]
        )
        assessment.interests = interests
        assessment.skills = skills_dict
        assessment.strengths = strengths
        assessment.careers = top_careers

        db.session.add(assessment)

        # Update Journey Tracker
        if user.tracker:
            badges = user.tracker.badges
            if "Compass Navigator" not in badges:
                badges.append("Compass Navigator")
                user.tracker.badges = badges
            user.tracker.overall_progress = max(user.tracker.overall_progress, 35)

        db.session.commit()
        flash("Assessment successfully analyzed! Here is your Dual-Path Career Compass & Venture Report.", "success")
        return redirect(url_for("assessment.career_compass"))

    return render_template("assessment/form.html", user=user)


@assessment_bp.route("/career-compass")
@login_required
def career_compass():
    user = User.query.get(session["user_id"])
    assessment = user.latest_assessment
    if not assessment:
        flash("Please complete your Dual-Path Assessment first.", "info")
        return redirect(url_for("assessment.start_assessment"))

    careers = assessment.careers
    top_career = careers[0] if careers else None

    # Prepare radar chart JSON for the top career match
    radar_labels = []
    user_scores = []
    target_scores = []
    if top_career:
        for skill_name, target_val in top_career.get("skills_benchmark", {}).items():
            radar_labels.append(skill_name)
            target_scores.append(target_val)
            user_val = top_career.get("user_radar_scores", {}).get(skill_name, 70)
            user_scores.append(user_val)

    return render_template(
        "assessment/career_compass.html",
        user=user,
        assessment=assessment,
        careers=careers,
        top_career=top_career,
        radar_labels=json.dumps(radar_labels),
        user_scores=json.dumps(user_scores),
        target_scores=json.dumps(target_scores)
    )


@assessment_bp.route("/decision-meter")
@login_required
def decision_meter():
    """
    Career vs Venture Decision Meter:
    Scores and chart comparing student's readiness for Job, Higher Studies, and Startup.
    """
    user = User.query.get(session["user_id"])
    assessment = user.latest_assessment
    if not assessment:
        flash("Please complete your assessment first.", "info")
        return redirect(url_for("assessment.start_assessment"))

    payload = {
        "risk_appetite": assessment.risk_appetite,
        "stability_vs_autonomy": assessment.stability_vs_autonomy,
        "hours_per_week": assessment.hours_per_week,
        "primary_goal": assessment.primary_goal,
        "skills": assessment.skills
    }
    decision_data = fallback_engine.compute_tri_path_scores(payload)

    return render_template(
        "assessment/decision_meter.html",
        user=user,
        assessment=assessment,
        decision=decision_data
    )

