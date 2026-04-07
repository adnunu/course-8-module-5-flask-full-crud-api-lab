from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database (simulated)
events = []
event_id_counter = 1

# Helper function to find event by ID
def find_event_by_id(event_id):
    return next((event for event in events if event['id'] == event_id), None)

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
    return jsonify(events), 200

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
    
    # Create new event
    new_event = {
        "id": event_id_counter,
        "title": data['title'],
        "description": data.get('description', ''),  # Optional field
        "date": data.get('date', ''),  # Optional field
        "location": data.get('location', '')  # Optional field
    }
    
    # Add to "database"
    events.append(new_event)
    event_id_counter += 1
    
    # Return 201 Created status code with the created event
    return jsonify(new_event), 201

# Task 4: PATCH update existing event
@app.route('/events/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
    # Find the event
    event = find_event_by_id(event_id)
    
    # Resource not found check
    if not event:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404
    
    # Get JSON data from request
    data = request.get_json()
    
    # Input validation
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Update only the fields that are provided
    if 'title' in data:
        event['title'] = data['title']
    if 'description' in data:
        event['description'] = data['description']
    if 'date' in data:
        event['date'] = data['date']
    if 'location' in data:
        event['location'] = data['location']
    
    # Return updated event with 200 OK status
    return jsonify(event), 200

# Task 5: DELETE remove an event
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    # Find the event
    event = find_event_by_id(event_id)
    
    # Resource not found check
    if not event:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404
    
    # Remove event from list
    events.remove(event)
    
    # Return 204 No Content status (no response body)
    return '', 204

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5000)