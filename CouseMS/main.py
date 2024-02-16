from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)


# Function to add CORS headers to the response
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


# Apply CORS headers to all routes
app.after_request(add_cors_headers)

# Connect to your MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client.course_management


def initialize_courses():
    # Pre-populate the database with courses if they don't already exist
    courses_data = [
        {"code": "IKT221", "name": "Chaos Engineering", "description": "Learn the principles of Chaos Engineering..."},
        {"code": "IKT222", "name": "Software Security", "description": "Dive into software security..."},
        {"code": "IKT230", "name": "GPT Coding", "description": "Explore the capabilities of Generative Pretrained Transformers in coding and software generation."},
        {"code": "IKT333", "name": "Disaster Recovery", "description": "Study the strategies for disaster recovery and business continuity in the face of IT outages."},
        {"code": "IKT322", "name": "Criminality and Warfare",
         "description": "Analyze the impact of cyber criminality and information warfare in the digital age."}
    ]

    for course in courses_data:
        db.courses.update_one({'code': course['code']}, {'$setOnInsert': course}, upsert=True)


# Initialize courses when the application starts
initialize_courses()


# Define the route for getting all courses
@app.route('/courses', methods=['GET'])
def get_courses():
    courses = db.courses.find({}, {'_id': 0})  # Exclude the MongoDB id from the results
    return jsonify(list(courses))


# Define the route for adding a new course
@app.route('/courses', methods=['POST'])
def add_course():
    course_data = request.get_json()
    result = db.courses.update_one(
        {'code': course_data['code']},
        {'$setOnInsert': course_data},
        upsert=True
    )
    return jsonify({'inserted_id': str(result.upserted_id)}), 201


# Define the route for deleting a course
@app.route('/courses/<string:course_code>', methods=['DELETE'])
def delete_course(course_code):
    result = db.courses.delete_one({'code': course_code})
    if result.deleted_count:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': 'course not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)

