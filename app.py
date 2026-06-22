from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request
)
from database.db import db
from database import models

from database.models import Interview

from utils.resume_parser import extract_text_from_pdf
from utils.information_extractor import extract_resume_info

from AI.question_generator import generate_questions

import os

from flask import session



UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///interview.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "harsh_ai_interview"

db.init_app(app)


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

@app.route("/")
def home():

    return render_template(
        "index.html"
    )



@app.route("/dashboard")
def dashboard():

    interviews = Interview.query.all()

    return render_template(
        "dashboard.html",
        interviews=interviews
    )

@app.route(
    "/upload-resume/<int:interview_id>",
    methods=["POST"]
)
def upload_resume(interview_id):


    if "resume" not in request.files:

        return "No File Selected"


    file = request.files["resume"]


    if file.filename == "":

        return "No File Selected"


    if file and allowed_file(file.filename):


        filename = file.filename


        save_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )


        file.save(save_path)


        interview = Interview.query.get(
            interview_id
        )


        if interview:

            interview.resume = save_path

            db.session.commit()


        return redirect(
            url_for("dashboard")
        )


    return "Only PDF files allowed"



# Start Interview

@app.route("/start-interview")
def start_interview():


    new_interview = Interview(

        user_id=1,

        resume="Not Uploaded"

    )


    db.session.add(new_interview)

    db.session.commit()



    return redirect(

        url_for(
            "interview",
            interview_id=new_interview.id
        )

    )





@app.route("/interview/<int:interview_id>")
def interview(interview_id):


    return render_template(

        "interview.html",

        interview_id=interview_id

    )




@app.route("/result")
def result():

    return render_template(
        "result.html"
    )


@app.route("/generate-questions/<int:interview_id>")
def generate_interview_questions(interview_id):

    interview = Interview.query.get_or_404(
        interview_id
    )

    extracted_text = extract_text_from_pdf(
        interview.resume
    )

    resume_info = extract_resume_info(
        extracted_text
    )

    questions = generate_questions(
        resume_info
    )

    question_list = [
        q.strip()
        for q in questions.split("\n")
        if q.strip()
    ]

    session["questions"] = question_list

    session["current_question"] = 0

    return redirect(
        url_for(
            "interview_session",
            interview_id=interview_id
        )
    )


@app.route(
    "/interview-session/<int:interview_id>",
    methods=["GET", "POST"]
)
def interview_session(interview_id):

    questions = session.get(
        "questions",
        []
    )

    current = session.get(
        "current_question",
        0
    )

    if current >= len(questions):

        return redirect(
            url_for(
                "interview_complete",
                interview_id=interview_id
            )
        )

    question = questions[current]

    if request.method == "POST":

        answer_text = request.form.get(
            "answer"
        )

        answer = Answer(

            interview_id=interview_id,

            question=question,

            answer=answer_text

        )

        db.session.add(answer)

        db.session.commit()

        session["current_question"] += 1

        return redirect(
            url_for(
                "interview_session",
                interview_id=interview_id
            )
        )

    return render_template(
        "interview_session.html",
        question=question,
        question_number=current + 1
    )

@app.route(
    "/interview-complete/<int:interview_id>"
)
def interview_complete(interview_id):

    answers = Answer.query.filter_by(
        interview_id=interview_id
    ).all()

    return render_template(
        "interview_complete.html",
        answers=answers
    )


@app.route("/resume-analysis/<int:interview_id>")
def resume_analysis(interview_id):


    interview = Interview.query.get_or_404(
        interview_id
    )


    if not interview.resume:

        return "Resume not uploaded"


    extracted_text = extract_text_from_pdf(
    interview.resume
    )

    resume_info = extract_resume_info(
        extracted_text
    )


    return render_template(
        "resume_analysis.html",
        extracted_text=extracted_text,
        resume_info=resume_info,
        interview=interview
    )





with app.app_context():

    db.create_all()



if __name__=="__main__":

    app.run(debug=True)