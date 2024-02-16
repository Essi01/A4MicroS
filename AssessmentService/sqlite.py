from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


# Create a new question
new_question = Question(
    text="What is the capital of France?",
    correct_answer='B',  # Assuming 'B' is the correct option
    quiz_id=1  # Assuming the quiz with ID 1 already exists
)

# Create the options for the question
options_data = [
    {'option_text': "A: Berlin", 'option_identifier': 'A'},
    {'option_text': "B: Paris", 'option_identifier': 'B'},  # This is the correct answer
    {'option_text': "C: Rome", 'option_identifier': 'C'},
    {'option_text': "D: Madrid", 'option_identifier': 'D'},
]

# Add the new question to the session
db.session.add(new_question)
db.session.commit()  # Commit to get the question ID

# Now, create and add options for the question
for option_data in options_data:
    option = Option(
        option_text=option_data['option_text'],
        option_identifier=option_data['option_identifier'],
        question_id=new_question.id  # Use the ID of the new question
    )
    db.session.add(option)

# Commit the options to the database
db.session.commit()