import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set up database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///verification.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Import routes after app initialization to avoid circular imports
from models import Claim
from fact_checker import verify_claim
from ai_verification import classify_text

@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")

@app.route("/verify", methods=["POST"])
def verify():
    """Process the user's submitted claim or article and verify it."""
    claim_text = request.form.get("claim_text", "").strip()
    
    if not claim_text:
        flash("Please enter a claim or article to verify.", "warning")
        return redirect(url_for("index"))
    
    # Store in session temporarily to display on results page
    session['claim_text'] = claim_text
    
    # Step 1: AI model classification
    ai_classification, ai_confidence = classify_text(claim_text)
    session['ai_classification'] = ai_classification
    session['ai_confidence'] = f"{ai_confidence:.1%}"  # Format as percentage
    
    # Step 2: Check against fact-checking sources
    verification_results = verify_claim(claim_text)
    session['verification_results'] = verification_results
    
    # Save to database
    try:
        new_claim = Claim(
            text=claim_text,
            ai_classification=ai_classification,
            ai_confidence=ai_confidence
        )
        db.session.add(new_claim)
        db.session.commit()
        flash("Your claim has been verified.", "success")
    except Exception as e:
        logging.error(f"Database error: {e}")
        db.session.rollback()
        flash("There was an issue saving your claim.", "danger")
    
    return redirect(url_for("results"))

@app.route("/results")
def results():
    """Display verification results."""
    # Check if we have results to display
    if 'claim_text' not in session:
        flash("No verification results found.", "warning")
        return redirect(url_for("index"))
    
    return render_template(
        "results.html", 
        claim_text=session.get('claim_text'),
        ai_classification=session.get('ai_classification'),
        ai_confidence=session.get('ai_confidence'),
        verification_results=session.get('verification_results', [])
    )

@app.route("/about")
def about():
    """About page with information on how the tool works."""
    return render_template("about.html")

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return render_template("500.html"), 500

# Initialize the database
with app.app_context():
    db.create_all()
