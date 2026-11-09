import json
from datetime import datetime, timezone
from models import db

def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class VentureIdea(db.Model):
    __tablename__ = "venture_ideas"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    title = db.Column(db.String(150), nullable=False)
    tagline = db.Column(db.String(255), nullable=True)
    problem_statement = db.Column(db.Text, nullable=False)
    target_customer = db.Column(db.String(200), nullable=False)
    solution = db.Column(db.Text, nullable=False)
    why_now = db.Column(db.Text, nullable=True)
    revenue_model = db.Column(db.String(150), nullable=True)
    complexity = db.Column(db.String(50), default="Medium")  # Low, Medium, High
    
    # Selection status
    is_active_venture = db.Column(db.Boolean, default=False)
    
    # Validation Scorecard & SWOT
    validation_score = db.Column(db.Integer, default=0) # 0 to 100
    validation_verdict = db.Column(db.String(50), default="Pending") # "GO", "REFINE", "PIVOT", "Pending"
    validation_details_raw = db.Column(db.Text, default="{}")
    
    created_at = db.Column(db.DateTime, default=utc_now)

    user = db.relationship("User", back_populates="ideas")
    canvases = db.relationship("LeanCanvas", back_populates="idea", cascade="all, delete-orphan", lazy="dynamic")
    design_notes = db.relationship("DesignThinkingNote", back_populates="idea", cascade="all, delete-orphan", lazy="dynamic")
    mvp_plans = db.relationship("MVPPlan", back_populates="idea", cascade="all, delete-orphan", lazy="dynamic")
    pitch_decks = db.relationship("PitchDeck", back_populates="idea", cascade="all, delete-orphan", lazy="dynamic")

    @property
    def validation_details(self):
        try:
            return json.loads(self.validation_details_raw)
        except Exception:
            return {}

    @validation_details.setter
    def validation_details(self, value):
        self.validation_details_raw = json.dumps(value)


class DesignThinkingNote(db.Model):
    """
    Sticky-note cards across the 5 Stanford d.school Design Thinking stages:
    1. Empathize
    2. Define
    3. Ideate
    4. Prototype
    5. Test
    """
    __tablename__ = "design_thinking_notes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey("venture_ideas.id"), nullable=True)
    
    stage = db.Column(db.String(50), nullable=False) # 'empathize', 'define', 'ideate', 'prototype', 'test'
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(30), default="amber") # amber, sky, emerald, rose, purple
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utc_now)

    user = db.relationship("User", back_populates="design_notes")
    idea = db.relationship("VentureIdea", back_populates="design_notes")


class LeanCanvas(db.Model):
    """
    The Ash Maurya 9-Block Lean Canvas for startup validation.
    """
    __tablename__ = "lean_canvases"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey("venture_ideas.id"), nullable=True)

    title = db.Column(db.String(150), default="My Venture Lean Canvas")
    
    # 9 Lean Canvas Blocks
    problem = db.Column(db.Text, default="")
    customer_segments = db.Column(db.Text, default="")
    unique_value_proposition = db.Column(db.Text, default="")
    solution = db.Column(db.Text, default="")
    channels = db.Column(db.Text, default="")
    revenue_streams = db.Column(db.Text, default="")
    cost_structure = db.Column(db.Text, default="")
    key_metrics = db.Column(db.Text, default="")
    unfair_advantage = db.Column(db.Text, default="")
    
    # Sub-blocks / Context
    early_adopters = db.Column(db.Text, default="")
    existing_alternatives = db.Column(db.Text, default="")
    high_level_concept = db.Column(db.Text, default="")
    
    last_updated = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    user = db.relationship("User", back_populates="canvases")
    idea = db.relationship("VentureIdea", back_populates="canvases")


class MVPPlan(db.Model):
    """
    Minimum Viable Product (MVP) specification and testing sprint.
    """
    __tablename__ = "mvp_plans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey("venture_ideas.id"), nullable=True)

    mvp_type = db.Column(db.String(80), default="Landing Page Smoke Test")
    scope_description = db.Column(db.Text, default="")
    riskiest_assumptions_raw = db.Column(db.Text, default="[]")
    success_metrics_raw = db.Column(db.Text, default="[]")
    sprint_tasks_raw = db.Column(db.Text, default="[]")
    created_at = db.Column(db.DateTime, default=utc_now)

    user = db.relationship("User", back_populates="mvp_plans")
    idea = db.relationship("VentureIdea", back_populates="mvp_plans")

    @property
    def riskiest_assumptions(self):
        try:
            return json.loads(self.riskiest_assumptions_raw)
        except Exception:
            return []

    @riskiest_assumptions.setter
    def riskiest_assumptions(self, val):
        self.riskiest_assumptions_raw = json.dumps(val)

    @property
    def success_metrics(self):
        try:
            return json.loads(self.success_metrics_raw)
        except Exception:
            return []

    @success_metrics.setter
    def success_metrics(self, val):
        self.success_metrics_raw = json.dumps(val)

    @property
    def sprint_tasks(self):
        try:
            return json.loads(self.sprint_tasks_raw)
        except Exception:
            return []

    @sprint_tasks.setter
    def sprint_tasks(self, val):
        self.sprint_tasks_raw = json.dumps(val)


class PitchDeck(db.Model):
    """
    Pitch deck outline and executive 1-page summary.
    """
    __tablename__ = "pitch_decks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    idea_id = db.Column(db.Integer, db.ForeignKey("venture_ideas.id"), nullable=True)

    elevator_pitch_60s = db.Column(db.Text, default="")
    one_page_pitch = db.Column(db.Text, default="")
    slides_raw = db.Column(db.Text, default="[]") # 10 slides JSON
    created_at = db.Column(db.DateTime, default=utc_now)

    user = db.relationship("User", back_populates="pitch_decks")
    idea = db.relationship("VentureIdea", back_populates="pitch_decks")

    @property
    def slides(self):
        try:
            return json.loads(self.slides_raw)
        except Exception:
            return []

    @slides.setter
    def slides(self, val):
        self.slides_raw = json.dumps(val)


class JourneyTracker(db.Model):
    """
    Gamified tracking of the student's venture formation journey.
    """
    __tablename__ = "journey_trackers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    
    # Stored as JSON lists
    completed_milestones_raw = db.Column(db.Text, default="[]")
    badges_raw = db.Column(db.Text, default='["Compass Explorer"]')
    overall_progress = db.Column(db.Integer, default=15) # 0 to 100%

    user = db.relationship("User", back_populates="tracker")

    @property
    def completed_milestones(self):
        try:
            return json.loads(self.completed_milestones_raw)
        except Exception:
            return []

    @completed_milestones.setter
    def completed_milestones(self, val):
        self.completed_milestones_raw = json.dumps(val)

    @property
    def badges(self):
        try:
            return json.loads(self.badges_raw)
        except Exception:
            return []

    @badges.setter
    def badges(self, val):
        self.badges_raw = json.dumps(val)
