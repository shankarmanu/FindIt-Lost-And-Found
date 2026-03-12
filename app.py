from flask import Flask, jsonify, request, render_template

import database

app = Flask(__name__)

# Initialize the database
database.init_db()

@app.route('/')
def index():
    # Serve the main HTML page
    return render_template('index.html')

@app.route('/api/items', methods=['GET'])
def get_items():
    items = database.get_all_items()
    return jsonify(items)

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.json
    try:
        new_id = database.add_item(data)
        data['id'] = new_id
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
