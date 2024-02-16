from flask import Flask, jsonify, request, Response, render_template
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://admin:admin@localhost:27017')
db = client['course_management']  # Adjusted database name
courses_collection = db['courses']

# Function to add CORS headers to the response
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Apply CORS headers to all routes
app.after_request(add_cors_headers)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/courses')
def courses_page():
    return render_template('courses.html')

@app.route('/course/<id>')
def course_detail(id):
    # Here you can fetch course details from MongoDB using the provided id
    course = courses_collection.find_one({"_id": ObjectId(id)})
    if course:
        course_details = loads(dumps(course))  # Convert MongoDB BSON to JSON
        return render_template('course-detail.html', course=course_details)
    else:
        return "Course not found", 404

@app.route('/enroll')
def enroll():
    return render_template('enroll.html')

@app.route('/discussions')
def discussions():
    return render_template('discussions.html')

@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = courses_collection.find({})
    return Response(dumps(courses), mimetype='application/json')

@app.route('/api/courses', methods=['POST'])
def add_course():
    data = request.json
    result = courses_collection.insert_one(data)
    return jsonify({'result': 'Course added', 'id': str(result.inserted_id)})

@app.route('/api/courses/<id>', methods=['DELETE'])
def delete_course(id):
    result = courses_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'result': 'Course deleted'})
    else:
        return jsonify({'error': 'Course not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
