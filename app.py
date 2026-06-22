from flask import Flask, render_template, redirect, url_for

from database.db import db
from database import models

from database.models import Interview



app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///interview.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)



@app.route("/")
def home():

    return render_template(
        "index.html"
    )



@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html"
    )



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





with app.app_context():

    db.create_all()



if __name__=="__main__":

    app.run(debug=True)