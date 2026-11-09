import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db
from models.user import User
from models.venture import VentureIdea, DesignThinkingNote, LeanCanvas, MVPPlan, PitchDeck, JourneyTracker
from routes.auth import login_required
from services.payment_service import subscription_required
from services import ai_service, fallback_engine

venture_bp = Blueprint("venture", __name__)

@venture_bp.route("/venture-studio")
@login_required
def hub():
    user = User.query.get(session["user_id"])
    active_idea = user.active_idea
    tracker = user.tracker
    return render_template("venture/hub.html", user=user, active_idea=active_idea, tracker=tracker)


@venture_bp.route("/venture-studio/ideas", methods=["GET", "POST"])
@login_required
def ideas():
    user = User.query.get(session["user_id"])
    assessment = user.latest_assessment
    generated_ideas = []

    # If form submitted to generate new ideas
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "generate":
            if not user.can_generate_ai_ideas:
                flash("You have reached your Free plan limit of 3 AI idea generations this month. Upgrade to Pro for unlimited generations!", "warning")
                return redirect(url_for("subscription.pricing", required_plan="pro"))

            # Build assessment payload or default
            assessment_payload = {
                "branch": assessment.branch if assessment else "General Engineering",
                "year_of_study": assessment.year_of_study if assessment else "3rd Year",
                "interests": assessment.interests if assessment else ["Tech", "SaaS"],
                "skills": assessment.skills if assessment else {"Coding": 8},
                "strengths": assessment.strengths if assessment else ["Problem Solving"],
                "risk_appetite": assessment.risk_appetite if assessment else 7
            }

            user.increment_ai_usage()
            ideas_list = ai_service.generate_ideas_ai(assessment_payload)
            
            # Save generated ideas to database
            first = True
            for i_data in ideas_list:
                v_idea = VentureIdea(
                    user_id=user.id,
                    title=i_data.get("title", "Student Venture"),
                    tagline=i_data.get("tagline", ""),
                    problem_statement=i_data.get("problem_statement", ""),
                    target_customer=i_data.get("target_customer", ""),
                    solution=i_data.get("solution", ""),
                    why_now=i_data.get("why_now", ""),
                    revenue_model=i_data.get("revenue_model", ""),
                    complexity=i_data.get("complexity", "Medium"),
                    is_active_venture=first and not user.active_idea
                )
                db.session.add(v_idea)
                first = False

            # Update tracker badge
            if user.tracker:
                badges = user.tracker.badges
                if "Venture Ideator" not in badges:
                    badges.append("Venture Ideator")
                    user.tracker.badges = badges
                user.tracker.overall_progress = max(user.tracker.overall_progress, 50)

            db.session.commit()
            flash("New venture ideas successfully synthesized from your skills & interests!", "success")
            return redirect(url_for("venture.ideas"))

        elif action == "custom":
            # Add custom idea manually
            title = request.form.get("title", "").strip()
            problem = request.form.get("problem_statement", "").strip()
            customer = request.form.get("target_customer", "").strip()
            solution = request.form.get("solution", "").strip()

            if title and problem and solution:
                v_idea = VentureIdea(
                    user_id=user.id,
                    title=title,
                    tagline=request.form.get("tagline", ""),
                    problem_statement=problem,
                    target_customer=customer,
                    solution=solution,
                    why_now=request.form.get("why_now", ""),
                    revenue_model=request.form.get("revenue_model", ""),
                    complexity=request.form.get("complexity", "Medium"),
                    is_active_venture=True
                )
                # Deactivate others
                for old_idea in user.ideas.all():
                    old_idea.is_active_venture = False
                db.session.add(v_idea)
                db.session.commit()
                flash(f"Custom idea '{title}' created and set as active venture!", "success")
                return redirect(url_for("venture.ideas"))

    saved_ideas = user.ideas.order_by(VentureIdea.created_at.desc()).all()
    # If user has no ideas yet and has completed assessment, auto-generate initial ideas
    if not saved_ideas and assessment:
        init_payload = {
            "branch": assessment.branch,
            "year_of_study": assessment.year_of_study,
            "interests": assessment.interests,
            "skills": assessment.skills,
            "strengths": assessment.strengths,
            "risk_appetite": assessment.risk_appetite
        }
        init_ideas = fallback_engine.generate_venture_ideas(init_payload, count=3)
        for idx, i_data in enumerate(init_ideas):
            v_idea = VentureIdea(
                user_id=user.id,
                title=i_data.get("title"),
                tagline=i_data.get("tagline"),
                problem_statement=i_data.get("problem_statement"),
                target_customer=i_data.get("target_customer"),
                solution=i_data.get("solution"),
                why_now=i_data.get("why_now"),
                revenue_model=i_data.get("revenue_model"),
                complexity=i_data.get("complexity", "Medium"),
                is_active_venture=(idx == 0)
            )
            db.session.add(v_idea)
        db.session.commit()
        saved_ideas = user.ideas.order_by(VentureIdea.created_at.desc()).all()

    return render_template("venture/ideas.html", user=user, ideas=saved_ideas)


@venture_bp.route("/venture-studio/ideas/set-active/<int:idea_id>", methods=["POST"])
@login_required
def set_active_idea(idea_id):
    user = User.query.get(session["user_id"])
    target_idea = VentureIdea.query.filter_by(id=idea_id, user_id=user.id).first_or_404()
    for idea in user.ideas.all():
        idea.is_active_venture = (idea.id == target_idea.id)
    db.session.commit()
    flash(f"Active venture switched to: {target_idea.title}", "success")
    return redirect(request.referrer or url_for("venture.ideas"))


@venture_bp.route("/venture-studio/design-thinking")
@login_required
def design_thinking():
    user = User.query.get(session["user_id"])
    active_idea = user.active_idea

    # Default starter notes if empty
    notes = user.design_notes.all()
    if not notes and active_idea:
        starter_notes = [
            ("empathize", "User Pain Point", f"Target users ({active_idea.target_customer}) struggle with manual, fragmented workflows daily.", "amber"),
            ("define", "Problem Statement (HMW)", f"How might we empower {active_idea.target_customer} to solve this 10x faster?", "sky"),
            ("ideate", "Core Solution Feature", f"Deploy an automated interface: {active_idea.solution[:80]}...", "emerald"),
            ("prototype", "Interactive Smoke Test", "Build responsive landing page + WhatsApp concierge channel.", "rose"),
            ("test", "Customer Interview Goal", "Interview 10 target users and record willingness-to-pay token amounts.", "purple")
        ]
        for idx, (stg, tit, cont, col) in enumerate(starter_notes):
            n = DesignThinkingNote(
                user_id=user.id,
                idea_id=active_idea.id,
                stage=stg,
                title=tit,
                content=cont,
                color=col,
                order_index=idx
            )
            db.session.add(n)
        db.session.commit()
        notes = user.design_notes.all()

    # Group notes by stage
    stages = {
        "empathize": [n for n in notes if n.stage == "empathize"],
        "define": [n for n in notes if n.stage == "define"],
        "ideate": [n for n in notes if n.stage == "ideate"],
        "prototype": [n for n in notes if n.stage == "prototype"],
        "test": [n for n in notes if n.stage == "test"]
    }

    return render_template("venture/design_thinking.html", user=user, active_idea=active_idea, stages=stages)


@venture_bp.route("/venture-studio/design-thinking/add", methods=["POST"])
@login_required
def add_design_note():
    user = User.query.get(session["user_id"])
    stage = request.form.get("stage", "empathize")
    title = request.form.get("title", "").strip() or "New Note"
    content = request.form.get("content", "").strip() or "Note description..."
    color = request.form.get("color", "amber")

    note = DesignThinkingNote(
        user_id=user.id,
        idea_id=user.active_idea.id if user.active_idea else None,
        stage=stage,
        title=title,
        content=content,
        color=color
    )
    db.session.add(note)
    db.session.commit()
    flash("Sticky note added to design board!", "success")
    return redirect(url_for("venture.design_thinking"))


@venture_bp.route("/venture-studio/design-thinking/delete/<int:note_id>", methods=["POST"])
@login_required
def delete_design_note(note_id):
    user = User.query.get(session["user_id"])
    note = DesignThinkingNote.query.filter_by(id=note_id, user_id=user.id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    flash("Note removed.", "info")
    return redirect(url_for("venture.design_thinking"))


@venture_bp.route("/venture-studio/validator")
@login_required
@subscription_required("founder")
def validator():
    """
    Idea Validator: Deep scorecard, TAM/SAM/SOM sizing, SWOT, and GO/REFINE/PIVOT verdict.
    Backend feature-gated to Founder plan.
    """
    user = User.query.get(session["user_id"])
    active_idea = user.active_idea
    if not active_idea:
        flash("Please select or generate a venture idea first.", "info")
        return redirect(url_for("venture.ideas"))

    idea_payload = {
        "title": active_idea.title,
        "problem_statement": active_idea.problem_statement,
        "target_customer": active_idea.target_customer,
        "solution": active_idea.solution,
        "complexity": active_idea.complexity
    }

    validation_result = ai_service.validate_idea_ai(idea_payload)

    # Cache validation result on the idea
    active_idea.validation_score = validation_result["total_score"]
    active_idea.validation_verdict = validation_result["verdict"]
    active_idea.validation_details = validation_result
    db.session.commit()

    return render_template(
        "venture/validator.html",
        user=user,
        active_idea=active_idea,
        validation=validation_result
    )


@venture_bp.route("/venture-studio/lean-canvas", methods=["GET", "POST"])
@login_required
def lean_canvas():
    """
    Ash Maurya 9-Block Lean Canvas Builder.
    Allows editing, AI auto-fill, and clean PDF/print export.
    """
    user = User.query.get(session["user_id"])
    active_idea = user.active_idea

    # Check if a canvas exists for active idea or user
    canvas = None
    if active_idea:
        canvas = LeanCanvas.query.filter_by(user_id=user.id, idea_id=active_idea.id).first()
    if not canvas:
        canvas = LeanCanvas.query.filter_by(user_id=user.id).order_by(LeanCanvas.last_updated.desc()).first()

    # If POST action: Save or AI Auto-fill
    if request.method == "POST":
        action = request.form.get("action")

        if action == "autofill":
            if not active_idea:
                flash("Please select an active idea first.", "warning")
                return redirect(url_for("venture.ideas"))
            
            payload = {
                "title": active_idea.title,
                "problem_statement": active_idea.problem_statement,
                "target_customer": active_idea.target_customer,
                "solution": active_idea.solution,
                "why_now": active_idea.why_now,
                "revenue_model": active_idea.revenue_model
            }
            ai_data = ai_service.generate_lean_canvas_ai(payload)

            if not canvas:
                canvas = LeanCanvas(user_id=user.id, idea_id=active_idea.id)
                db.session.add(canvas)

            canvas.title = ai_data.get("title", f"Lean Canvas: {active_idea.title}")
            canvas.problem = ai_data.get("problem", "")
            canvas.customer_segments = ai_data.get("customer_segments", "")
            canvas.unique_value_proposition = ai_data.get("unique_value_proposition", "")
            canvas.solution = ai_data.get("solution", "")
            canvas.channels = ai_data.get("channels", "")
            canvas.revenue_streams = ai_data.get("revenue_streams", "")
            canvas.cost_structure = ai_data.get("cost_structure", "")
            canvas.key_metrics = ai_data.get("key_metrics", "")
            canvas.unfair_advantage = ai_data.get("unfair_advantage", "")
            canvas.early_adopters = ai_data.get("early_adopters", "")
            canvas.existing_alternatives = ai_data.get("existing_alternatives", "")
            canvas.high_level_concept = ai_data.get("high_level_concept", "")

            # Update tracker
            if user.tracker:
                badges = user.tracker.badges
                if "Lean Architect" not in badges:
                    badges.append("Lean Architect")
                    user.tracker.badges = badges
                user.tracker.overall_progress = max(user.tracker.overall_progress, 75)

            db.session.commit()
            flash("Lean Canvas auto-filled with intelligent venture structure!", "success")
            return redirect(url_for("venture.lean_canvas"))

        elif action == "save":
            if not canvas:
                canvas = LeanCanvas(user_id=user.id, idea_id=active_idea.id if active_idea else None)
                db.session.add(canvas)

            canvas.title = request.form.get("title", "My Venture Lean Canvas")
            canvas.problem = request.form.get("problem", "")
            canvas.customer_segments = request.form.get("customer_segments", "")
            canvas.unique_value_proposition = request.form.get("unique_value_proposition", "")
            canvas.solution = request.form.get("solution", "")
            canvas.channels = request.form.get("channels", "")
            canvas.revenue_streams = request.form.get("revenue_streams", "")
            canvas.cost_structure = request.form.get("cost_structure", "")
            canvas.key_metrics = request.form.get("key_metrics", "")
            canvas.unfair_advantage = request.form.get("unfair_advantage", "")
            canvas.early_adopters = request.form.get("early_adopters", "")
            canvas.existing_alternatives = request.form.get("existing_alternatives", "")
            canvas.high_level_concept = request.form.get("high_level_concept", "")

            db.session.commit()
            flash("Lean Canvas changes successfully saved to your portfolio!", "success")
            return redirect(url_for("venture.lean_canvas"))

    # Initial default canvas if none exists
    if not canvas and active_idea:
        initial_data = fallback_engine.generate_lean_canvas({
            "title": active_idea.title,
            "problem_statement": active_idea.problem_statement,
            "target_customer": active_idea.target_customer,
            "solution": active_idea.solution,
            "why_now": active_idea.why_now,
            "revenue_model": active_idea.revenue_model
        })
        canvas = LeanCanvas(
            user_id=user.id,
            idea_id=active_idea.id,
            title=initial_data["title"],
            problem=initial_data["problem"],
            customer_segments=initial_data["customer_segments"],
            unique_value_proposition=initial_data["unique_value_proposition"],
            solution=initial_data["solution"],
            channels=initial_data["channels"],
            revenue_streams=initial_data["revenue_streams"],
            cost_structure=initial_data["cost_structure"],
            key_metrics=initial_data["key_metrics"],
            unfair_advantage=initial_data["unfair_advantage"],
            early_adopters=initial_data["early_adopters"],
            existing_alternatives=initial_data["existing_alternatives"],
            high_level_concept=initial_data["high_level_concept"]
        )
        db.session.add(canvas)
        db.session.commit()

    is_print = request.args.get("print") == "true"
    return render_template("venture/lean_canvas.html", user=user, active_idea=active_idea, canvas=canvas, is_print=is_print)


@venture_bp.route("/venture-studio/mvp-planner")
@login_required
def mvp_planner():
    user = User.query.get(session["user_id"])
    active_idea = user.active_idea
    if not active_idea:
        flash("Please select an active idea first.", "info")
        return redirect(url_for("venture.ideas"))

    mvp_data = fallback_engine.generate_mvp_plan({
        "title": active_idea.title,
        "problem_statement": active_idea.problem_statement,
        "solution": active_idea.solution
    })

    return render_template("venture/mvp_planner.html", user=user, active_idea=active_idea, mvp=mvp_data)


@venture_bp.route("/venture-studio/pitch-builder")
@login_required
@subscription_required("founder")
def pitch_builder():
    """
    10-Slide Investor Deck outline & One-Pager Pitch.
    Feature-gated to Founder plan.
    """
    user = User.query.get(session["user_id"])
    active_idea = user.active_idea
    if not active_idea:
        flash("Please select an active idea first.", "info")
        return redirect(url_for("venture.ideas"))

    pitch_data = fallback_engine.generate_pitch_deck({
        "title": active_idea.title,
        "tagline": active_idea.tagline,
        "problem_statement": active_idea.problem_statement,
        "target_customer": active_idea.target_customer,
        "solution": active_idea.solution,
        "revenue_model": active_idea.revenue_model
    })

    # Save to database
    deck = PitchDeck.query.filter_by(user_id=user.id, idea_id=active_idea.id).first()
    if not deck:
        deck = PitchDeck(
            user_id=user.id,
            idea_id=active_idea.id,
            elevator_pitch_60s=pitch_data["elevator_pitch_60s"],
            one_page_pitch=pitch_data["one_page_pitch"]
        )
        deck.slides = pitch_data["slides"]
        db.session.add(deck)
        db.session.commit()

    # Update tracker
    if user.tracker:
        badges = user.tracker.badges
        if "Pitch Master" not in badges:
            badges.append("Pitch Master")
            user.tracker.badges = badges
        user.tracker.overall_progress = max(user.tracker.overall_progress, 90)
        db.session.commit()

    return render_template("venture/pitch_builder.html", user=user, active_idea=active_idea, pitch=pitch_data)


@venture_bp.route("/venture-studio/founder-toolkit")
@login_required
def founder_toolkit():
    """
    Course content:
    - Funding stages: Bootstrapping, Angels, VCs, Grants
    - Indian support schemes: SISFS (Startup India), NIDHI-PRAYAS, BIRAC, AIM
    - IPR basics: Patents, Trademarks, Copyrights, Trade Secrets
    """
    user = User.query.get(session["user_id"])
    return render_template("venture/founder_toolkit.html", user=user)


@venture_bp.route("/venture-studio/tracker")
@login_required
def tracker():
    """
    Gamified Founder Journey Tracker.
    """
    user = User.query.get(session["user_id"])
    tr = user.tracker
    if not tr:
        tr = JourneyTracker(user_id=user.id, overall_progress=20, badges_raw='["Compass Explorer"]')
        db.session.add(tr)
        db.session.commit()

    # Calculate actual progress dynamically
    progress = 20
    if user.assessments.count() > 0:
        progress += 20
    if user.ideas.count() > 0:
        progress += 20
    if user.canvases.count() > 0:
        progress += 20
    if user.active_idea and user.active_idea.validation_score > 0:
        progress += 20
    tr.overall_progress = min(100, progress)
    db.session.commit()

    return render_template("venture/tracker.html", user=user, tracker=tr)

