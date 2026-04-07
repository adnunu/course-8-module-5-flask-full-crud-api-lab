from flask import Flask, request, jsonify

app = Flask(__name__)

# Event class for better structure
class Event:
    def __init__(self, id, title, description='', date='', location=''):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.location = location
    
    def to_dict(self):
        """Convert Event object to dictionary for JSON response"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'location': self.location
        }

# In-memory database (simulated)
events = []
event_id_counter = 1

# Helper function to find event by ID
def find_event_by_id(event_id):
    return next((event for event in events if event.id == event_id), None)

# Task 1: Welcome message at root route
@app.route('/', methods=['GET'])
def welcome():
    return jsonify({
        "message": "Welcome to the Events API",
        "version": "1.0",
        "endpoints": {
            "GET /": "Welcome message",
            "GET /events": "Get all events",
            "POST /events": "Create a new event",
            "PATCH /events/<id>": "Update an existing event",
            "DELETE /events/<id>": "Delete an event"
        }
    })

# Task 2: GET all events
@app.route('/events', methods=['GET'])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# Task 3: POST create new event
@app.route('/events', methods=['POST'])
def create_event():
    global event_id_counter
    
    # Get JSON data from request
    data = request.get_json()
    
    # Input validation: check if data exists and has required fields
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    if 'title' not in data:
        return jsonify({"error": "Missing required field: title"}), 400
    
    # Create new event object
    new_event = Event(
        id=event_id_counter,
        title=data['title'],
        description=data.get('description', ''),
        date=data.get('date', ''),
        location=data.get('location', '')
    )
    
    # Add to "database"
    events.append(new_event)
    event_id_counter += 1
    
    # Return 201 Created status code with the created event
    return jsonify(new_event.to_dict()), 201

# Task 4: PATCH update existing event
@app.route('/events/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
    # Find the event
    event = find_event_by_id(event_id)
    
    # Resource not found check
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404
    
    # Get JSON data from request
    data = request.get_json()
    
    # Input validation
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Update only the fields that are provided
    if 'title' in data:
        event.title = data['title']
    if 'description' in data:
        event.description = data['description']
    if 'date' in data:
        event.date = data['date']
    if 'location' in data:
        event.location = data['location']
    
    # Return updated event with 200 OK status
    return jsonify(event.to_dict()), 200

# Task 5: DELETE remove an event
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    global events
    
    # Find the event
    event = find_event_by_id(event_id)
    
    # Resource not found check
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404
    
    # Remove event from list
    events = [e for e in events if e.id != event_id]
    
    # Return 204 No Content status (no response body)
    return '', 204

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5000)