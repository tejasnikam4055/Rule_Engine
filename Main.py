from flask import Flask, request, jsonify, render_template
import mysql.connector
from ast12 import Node, create_rule, evaluate_rule 

app = Flask(__name__)

# Connect to the database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='tejas',
            database='rule_engine'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/')
def index():
    return render_template('index2.html')  

# Add or get rules
@app.route('/rules', methods=['GET', 'POST'])
def add_rule():
    if request.method == 'POST':
        if request.content_type != 'application/json':
            return jsonify({"error": "Content-Type must be application/json"}), 415

        rule_data = request.json.get('rule')
        if not rule_data:
            return jsonify({"error": "Invalid JSON or rule field missing"}), 400

        try:
            ast = create_rule(rule_data)  # Create AST from rule
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO rules(rule_string) VALUES (%s)", (rule_data,))
            conn.commit()
            return jsonify({"message": "Rule added successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # Handle GET request to fetch all rules
    elif request.method == 'GET':
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rules")
            rules = cursor.fetchall()
            return jsonify({"rules": rules}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate():
    if request.method == 'POST':
        if request.content_type != 'application/json':
            return jsonify({"error": "Content-Type must be application/json"}), 415

        rule_id = request.json.get('rule_id')
        data = request.json.get('data')
        if not rule_id or not data:
            return jsonify({"error": "rule_id or data is missing"}), 400

    elif request.method == 'GET':
        # Use query parameters for GET request
        rule_id = request.args.get('rule_id')
        data = request.args.get('data')
        if not rule_id or not data:
            return jsonify({"error": "rule_id or data is missing"}), 400

    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT rule_string FROM rules WHERE id = %s", (rule_id,))
        rule = cursor.fetchone()

        if rule:
            rule_string = rule[0]
            ast = create_rule(rule_string)

            # Convert data from JSON string if necessary
            if isinstance(data, str):
                import json
                data = json.loads(data)

            result = evaluate_rule(ast, data)
            return jsonify({"result": result}), 200
        else:
            return jsonify({"error": "Rule not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete rule
@app.route('/rules/<int:id>', methods=["DELETE"])
def delete_rule(id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rules WHERE id = %s", (id,))
        conn.commit()

        if cursor.rowcount > 0:
            return jsonify({'message': "Rule deleted successfully"}), 200
        else:
            return jsonify({"error": "Rule not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
