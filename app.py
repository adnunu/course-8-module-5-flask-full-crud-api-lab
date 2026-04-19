from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory data store
events = []
event_counter = 1

# Helper function to find an event by ID
def find_event_by_id(event_id):
    """Find and return an event by its ID."""
    for event in events:
        if event['id'] == event_id:
            return event
    return None

# Home route - Welcome message
@app.route('/', methods=['GET'])
def welcome():
    """Return a JSON welcome message."""
    return jsonify({
        "message": "Welcome to the Event Management API",
        "endpoints": {
            "GET /events": "Retrieve all events",
            "POST /events": "Create a new event",
            "GET /events/<id>": "Retrieve a specific event",
            "PATCH /events/<id>": "Update an existing event",
            "DELETE /events/<id>": "Delete an event"
        }
    }), 200

# GET /events - Retrieve all events
@app.route('/events', methods=['GET'])
def get_events():
    """Return a JSON array of all events."""
    return jsonify(events), 200

# GET /events/<id> - Retrieve a specific event
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Return a specific event by ID."""
    event = find_event_by_id(event_id)
    
    if event is None:
        return jsonify({"error": f"Event with ID {event_id} not found"}), 404
    
    return jsonify(event), 200

# POST /events - Create a new event
@app.route('/events', methods=['POST'])
def create_event():
    """Create a new event from JSON data."""
    global event_counter
    
    # Get JSON data from request
    try:
        data = request.get_json(force=True)
    except:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    # Input validation
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if 'title' not in data:
        return jsonify({"error": "Missing required field: title"}), 400
    
    # Create new event with auto-incrementing ID
    new_event = {
        "id": event_counter,
        "title": data['title'],
        "description": data.get('description', ''),
        "location": data.get('location', ''),
        "date": data.get('date', ''),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    events.append(new_event)
    event_counter += 1
    
    return jsonify(new_event), 201

# PATCH /events/<id> - Update an existing event
@app.route('/events/<int:event_id>', methods=['PATCH'])
def update_event(event_id):
    """Update an existing event partially."""
    event = find_event_by_id(event_id)
    
    if event is None:
        return jsonify({"error": f"Event with ID {event_id} not found"}), 404
    
    # Get JSON data from request
    try:
        data = request.get_json(force=True)
    except:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Update only the fields that are provided
    if 'title' in data:
        event['title'] = data['title']
    if 'description' in data:
        event['description'] = data['description']
    if 'location' in data:
        event['location'] = data['location']
    if 'date' in data:
        event['date'] = data['date']
    
    # Update the timestamp
    event['updated_at'] = datetime.now().isoformat()
    
    return jsonify(event), 200

# DELETE /events/<id> - Delete an event
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event by ID."""
    event = find_event_by_id(event_id)
    
    if event is None:
        return jsonify({"error": f"Event with ID {event_id} not found"}), 404
    
    events.remove(event)
    
    return jsonify({"message": f"Event with ID {event_id} successfully deleted"}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)