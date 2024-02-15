from flask import Blueprint, jsonify, request
from . import mongo

course_blueprint = Blueprint('course', __name__)

@course_blueprint.route('/courses', methods=['GET'])
def get_courses():
    courses = mongo.db.courses.find()  # Assuming your MongoDB collection is named 'courses'
    return jsonify([course for course in courses])

@course_blueprint.route('/courses', methods=['POST'])
def add_course():
    course_data = request.get_json()
    mongo.db.courses.insert_one(course_data)
    return jsonify(course_data), 201
