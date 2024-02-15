from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Connect to your MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client.course_management

# Define the route for getting all courses
@app.route('/courses', methods=['GET'])
def get_courses():
    courses = db.courses.find({}, {'_id': 0})  # Exclude the MongoDB id from the results
    return jsonify(list(courses))

# Define the route for adding a new course
@app.route('/courses', methods=['POST'])
def add_course():
    course_data = request.get_json()
    result = db.courses.insert_one(course_data)
    # Return the new ID of the inserted course
    return jsonify(str(result.inserted_id)), 201

# Define the route for deleting a course
@app.route('/courses/<string:course_code>', methods=['DELETE'])
def delete_course(course_code):
    result = db.courses.delete_one({'code': course_code})
    if result.deleted_count:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': 'course not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
# In this example, we have a simple Flask application that connects to a MongoDB database and provides a REST API for managing courses.
# The application has three routes: one for getting all courses, one for adding a new course, and one for deleting a course.
# The routes use the Flask request object to access the JSON data sent by the client, and the jsonify function to return JSON responses.
# We also use the Flask-CORS extension to enable Cross-Origin Resource Sharing (CORS) for all routes, allowing the API to be accessed from different domains.
# The application connects to a MongoDB database using the MongoClient class from the pymongo library.
# The get_courses route retrieves all courses from the MongoDB collection and returns them as a JSON array.
# The add_course route inserts a new course into the MongoDB collection and returns the ID of the newly inserted document.
# The delete_course route deletes a course from the MongoDB collection based on its course code and returns a success message or an error if the course is not found.

