from datetime import datetime
from app import db

class Claim(db.Model):
    """Model to store verified claims and their results."""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    ai_classification = db.Column(db.String(20), nullable=False)  # true, false, or unclear
    ai_confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Claim {self.id}: {self.ai_classification}>'

class Source(db.Model):
    """Model to store sources used for verification."""
    id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('claim.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255))
    source_type = db.Column(db.String(50))  # fact-check, news, etc.
    stance = db.Column(db.String(20))  # supports, refutes, or neutral
    
    claim = db.relationship('Claim', backref=db.backref('sources', lazy=True))
    
    def __repr__(self):
        return f'<Source {self.id}: {self.stance}>'
