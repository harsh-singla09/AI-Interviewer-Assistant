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

import os



UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///interview.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


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


    return render_template(
        "resume_analysis.html",
        extracted_text=extracted_text,
        interview=interview
    )





with app.app_context():

    db.create_all()



if __name__=="__main__":

    app.run(debug=True)