from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Assessment.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model Definitions
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)

    def serialize(self):
        return {'id': self.id, 'title': self.title, 'questions': [q.serialize() for q in self.questions]}

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    options = db.relationship('Option', backref='question', lazy=True)

    def serialize(self):
        return {'id': self.id, 'text': self.text, 'correct_answer': self.correct_answer, 'options': [o.serialize() for o in self.options]}

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option_text = db.Column(db.String(255), nullable=False)
    option_identifier = db.Column(db.String(1), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def serialize(self):
        return {'id': self.id, 'option_text': self.option_text, 'option_identifier': self.option_identifier}

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {'id': self.id, 'title': self.title, 'description': self.description, 'due_date': self.due_date.isoformat() if self.due_date else None}

# Route Definitions
@app.route('/quizzes', methods=['GET', 'POST'])
def handle_quizzes():
    if request.method == 'GET':
        quizzes = Quiz.query.all()
        return jsonify([quiz.serialize() for quiz in quizzes]), 200
    elif request.method == 'POST':
        data = request.get_json()
        new_quiz = Quiz(title=data['title'])
        db.session.add(new_quiz)
        db.session.commit()
        return jsonify(new_quiz.serialize()), 201

@app.route('/assignments', methods=['GET', 'POST'])
def handle_assignments():
    if request.method == 'GET':
        assignments = Assignment.query.all()
        return jsonify([assignment.serialize() for assignment in assignments]), 200
    elif request.method == 'POST':
        data = request.get_json()
        new_assignment = Assignment(title=data['title'], description=data.get('description'), due_date=datetime.strptime(data['due_date'], '%Y-%m-%d') if data.get('due_date') else None)
        db.session.add(new_assignment)
        db.session.commit()
        return jsonify(new_assignment.serialize()), 201

@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    data = request.get_json()  # Assuming data is {'answers': {'question_id': 'selected_option_identifier', ...}}
    quiz = Quiz.query.get_or_404(quiz_id)
    total = len(quiz.questions)
    correct = sum(1 for q in quiz.questions if data['answers'].get(str(q.id)) == q.correct_answer)
    return jsonify({'total': total, 'correct': correct, 'score': f"{correct}/{total}"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)
