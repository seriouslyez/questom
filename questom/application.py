import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///questom.db")


@app.route("/")
@login_required
def index():
    """homepage"""

    # show answered questions for students
    if session["type"] == "False":
        answers = []

        # Query database for questions and answers for student
        rows = db.execute("SELECT questions.question, answers.answer, answers.posted_date FROM questions JOIN answers WHERE questions.question_id=answers.question_id AND questions.student_id=:sid",
                          sid=session["user_id"])

        # if no questions have been answered yet:
        if len(rows) == 0:
            return render_template("no_answers.html")

        return render_template("indexS.html", rows=rows)
    # show unanswered questions for pros
    else:
        # Query database for unanswered questions
        rows = db.execute("SELECT question_id, question, posted_date FROM questions WHERE answered=:answered", answered="False")

        #if no unanswered questions exist:
        if len(rows) == 0:
            return render_template("no_questions.html")

        return render_template("unanswered.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Remember type of user
        session["type"] = rows[0]["professional"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if request.form.get("userType") == "S":
            return render_template("registerS.html")

        elif request.form.get("userType") == "P":
            return render_template("registerP.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/registerS", methods=["GET", "POST"])
def registerS():
    """Register student"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must enter email", 403)

        # Query database for email
        rows2=db.execute("SELECT email FROM users WHERE email=:email",
                        email=request.form.get("email"))

        # Ensure email hasn't been used
        if len(rows2) > 0:
            return apology("An account already exists under this email")

        # Ensure username was submitted
        elif not request.form.get("username"):
            return apology("must choose username", 403)

        # Query database for usernames
        rows1=db.execute("SELECT username FROM users WHERE username=:username",
                        username=request.form.get("username"))

        # Ensure username does not already exist
        if len(rows1) > 0:
            return apology("username is not available", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must choose password", 403)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        # Ensure terms accepted
        elif not request.form.get("terms"):
            return apology("must accept terms", 403)

        # Ensure privacy policy accepted
        elif not request.form.get("privacy"):
            return apology("must accept privacy policy", 403)
        # Register user
        rows = db.execute("INSERT INTO users (username, hash, email) VALUES(:username, :hashp, :email)",
                          username=request.form.get("username"),
                          hashp=generate_password_hash(request.form.get("password")),
                          email=request.form.get("email"))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("registerS.html")


@app.route("/registerP", methods=["GET", "POST"])
def registerP():
    """Register professional"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure first name was submitted
        if not request.form.get("first"):
            return apology("must enter first name", 403)

        # Ensure last name was submitted
        elif not request.form.get("last"):
            return apology("must enter last name", 403)

        # Ensure email was submitted
        elif not request.form.get("email"):
            return apology("must enter email", 403)

        # Query database for email
        rows2=db.execute("SELECT email FROM users WHERE email=:email",
                        email=request.form.get("email"))

        # Ensure email hasn't been used
        if len(rows2) > 0:
            return apology("An account already exists under this email", 403)

        # Ensure years were submitted
        if not request.form.get("years"):
            return apology("must enter years of experience", 403)

        # Ensure username was submitted
        elif not request.form.get("username"):
            return apology("must choose username", 403)

        # Query database for usernames
        rows1=db.execute("SELECT username FROM users WHERE username=:username",
                        username=request.form.get("username"))

        # Ensure username does not already exist
        if len(rows1) > 0:
            return apology("username is not available", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must choose password", 403)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        # Ensure terms accepted
        elif not request.form.get("terms"):
            return apology("must accept terms", 403)

        # Ensure privacy policy accepted
        elif not request.form.get("privacy"):
            return apology("must accept privacy policy", 403)

        # Register user
        rows = db.execute("INSERT INTO users (username, hash, email, first_name, last_name, xp_years, professional) VALUES(:username, :hash, :email, :first, :last, :xp, :pro)",
                          username=request.form.get("username"),
                          hash=generate_password_hash(request.form.get("password")),
                          email=request.form.get("email"),
                          first=request.form.get("first"),
                          last=request.form.get("last"),
                          xp=request.form.get("years"),
                          pro="True")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("registerP.html")


@app.route("/about", methods=["GET"])
def about():
    """Shows about us page"""

    return render_template("about.html")


@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    """Posts a new question from the student"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure a symbol was submitted
        if not request.form.get("symptoms"):
            return apology("must enter at least one symptom", 403)

        # Post question
        rows = db.execute("INSERT INTO questions (student_id, question) VALUES(:id, :symptoms)",
                          id=session['user_id'],
                          symptoms=request.form.get("symptoms"))

        # Redirect user to home page
        return redirect("/pending_questions")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("new.html")


@app.route("/pending_questions", methods=["GET"])
@login_required
def pending_questions():
    """student can see questions yet to be answered"""

    # Query database for unanswered questions of current student
    rows=db.execute("SELECT question, posted_date FROM questions WHERE student_id=:sid AND answered=:answered",
                    sid=session["user_id"],
                    answered="False")
    return render_template("pending_questions.html", rows=rows)


@app.route("/pending_answers", methods=["POST"])
@login_required
def pending_answers():
    """Let professional respond to symptoms"""

    # User reached route via POST (as by submitting a form via POST)
    qid = request.form.get("qid")
    symptoms = request.form.get("symptoms")
    return render_template("respond.html", symptoms=symptoms, qid=qid)


@app.route("/answer", methods=["POST"])
@login_required
def answer():
    """Record professional's answer"""

    # Ensure suggestion is present
    if not request.form.get("response"):
        return apology("must enter at least one suggestion", 403)

    # Insert answer into database
    rows = db.execute("INSERT INTO answers (question_id, pro_id, answer) VALUES(:qid, :pro_id, :answer)",
                          qid=request.form.get("qid"),
                          pro_id=session["user_id"],
                          answer=request.form.get("response"))

    # Update questions table answered column
    rows1 = db.execute("UPDATE questions SET answered=:answered WHERE question_id=:qid",
                            answered="True",
                            qid=request.form.get("qid"))
    return redirect("/")


@app.route("/history", methods=["GET"])
@login_required
def history():
    """professionals can see previously answered questions"""

    # Query database for questions and answers for student
    rows = db.execute("SELECT questions.question, answers.answer, answers.posted_date FROM questions JOIN answers WHERE questions.question_id=answers.question_id AND answers.pro_id=:pid",
                          pid=session["user_id"])
    return render_template("history.html", rows=rows)


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    """professionals can see what their profile entails"""

    # Query database for profile details
    rows=db.execute("SELECT username, first_name, last_name, email, xp_years FROM users WHERE id=:id", id=session["user_id"])
    return render_template("profile.html", rows=rows)


@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    """Posts a new question from the student"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure user submitted rating
        if not request.form.get("rating"):
            return apology("please enter rating", 403)

        # Enter response into database
        rows = db.execute("INSERT INTO feedback (rating, pros, improvements, comments) VALUES(:rating, :pros, :improvements, :comments)",
                          rating=request.form.get("rating"),
                          pros=request.form.get("pros"),
                          improvements=request.form.get("improvements"),
                          comments=request.form.get("comments"))
        return render_template("thanks.html")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("feedback.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
