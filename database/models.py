from database.db import db
from datetime import datetime



class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(
        db.String(200)
    )



class Interview(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer
    )

    resume = db.Column(
        db.String(200)
    )

    date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



class Question(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    interview_id = db.Column(
        db.Integer
    )

    question_text = db.Column(
        db.Text
    )



class Answer(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    interview_id = db.Column(
        db.Integer
    )

    question = db.Column(
        db.Text
    )

    answer = db.Column(
        db.Text
    )



class Score(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    interview_id = db.Column(
        db.Integer
    )

    technical_score = db.Column(
        db.Integer
    )

    communication_score = db.Column(
        db.Integer
    )