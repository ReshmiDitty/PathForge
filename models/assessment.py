import json
from datetime import datetime, timezone
from models import db

def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class Assessment(db.Model):
    __tablename__ = "assessments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    # Academic profile
    branch = db.Column(db.String(100), nullable=False)
    year_of_study = db.Column(db.String(50), nullable=False)
    college = db.Column(db.String(150), default="College of Engineering")
    
    # Student preferences & inputs
    interests_raw = db.Column(db.Text, default="[]")      # JSON string
    skills_raw = db.Column(db.Text, default="{}")         # JSON dict of skill: score (1-10)
    strengths_raw = db.Column(db.Text, default="[]")      # JSON string list
    
    # Venture & Career Readiness psychometrics
    risk_appetite = db.Column(db.Integer, default=5)          # 1 to 10
    stability_vs_autonomy = db.Column(db.Integer, default=5)  # 1 (pure corporate) to 10 (pure founder)
    hours_per_week = db.Column(db.Integer, default=15)
    capital_willing = db.Column(db.String(50), default="Low (₹0 - ₹10,000)")
    primary_goal = db.Column(db.String(50), default="job")   # 'job', 'higher_studies', 'startup'
    
    # Computed Tri-Path Readiness Scores (0 - 100)
    job_readiness_score = db.Column(db.Integer, default=75)
    higher_studies_score = db.Column(db.Integer, default=65)
    venture_readiness_score = db.Column(db.Integer, default=70)
    
    # Cached assessment output
    careers_data = db.Column(db.Text, default="[]")
    
    created_at = db.Column(db.DateTime, default=utc_now)

    user = db.relationship("User", back_populates="assessments")

    @property
    def interests(self):
        try:
            return json.loads(self.interests_raw)
        except Exception:
            return []

    @interests.setter
    def interests(self, value):
        self.interests_raw = json.dumps(value)

    @property
    def skills(self):
        try:
            return json.loads(self.skills_raw)
        except Exception:
            return {}

    @skills.setter
    def skills(self, value):
        self.skills_raw = json.dumps(value)

    @property
    def strengths(self):
        try:
            return json.loads(self.strengths_raw)
        except Exception:
            return []

    @strengths.setter
    def strengths(self, value):
        self.strengths_raw = json.dumps(value)

    @property
    def careers(self):
        try:
            return json.loads(self.careers_data)
        except Exception:
            return []

    @careers.setter
    def careers(self, value):
        self.careers_data = json.dumps(value)
