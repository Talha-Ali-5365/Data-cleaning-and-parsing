from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    answer_a = db.Column(db.Text, nullable=False)
    answer_b = db.Column(db.Text, nullable=False)
    answer_c = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)


db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("quiz"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions = [
        Question(question_text="What does CPU stand for?", answer_a="Central Processing Unit", answer_b="Computer Processing Unit", answer_c="Central Program Unit", correct_answer="Central Processing Unit"),
        Question(question_text="Which of these is not a programming language?", answer_a="Python", answer_b="HTML", answer_c="Java", correct_answer="HTML"),
        Question(question_text="What is the binary equivalent of the decimal number 10?", answer_a="1010", answer_b="1110", answer_c="1001", correct_answer="1010"),
    ]

    if request.method == "POST":
        score = 0
        for question, answer in zip(questions, request.form.getlist("answer")):
            if answer.lower() == question.correct_answer.lower():
            	score += 1
        return render_template("quiz_result.html", score=score, questions_answers=zip(questions, request.form.getlist("answer")))

    db.session.add_all(questions)
    db.session.commit()
    return render_template("quiz.html", questions=questions)



if __name__ == "__main__":
    app.run()

