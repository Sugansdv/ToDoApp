from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import config

app = Flask(__name__)

# 🔥 CORS SETTINGS: Allow Netlify frontend origin
CORS(app, origins=["https://687b2d9e4eebc9c728ca3bef--mytodoapp-project.netlify.app"],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# 🔧 MySQL Config
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

# ✅ GET all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, task_name, is_completed FROM tasks")
        tasks = [{'id': row[0], 'title': row[1], 'completed': bool(row[2])} for row in cur.fetchall()]
        cur.close()
        return jsonify(tasks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ POST new task
@app.route('/api/tasks', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        task_name = data.get('title')
        if not task_name:
            return jsonify({'error': 'Title is required'}), 400
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (task_name, is_completed) VALUES (%s, %s)", (task_name, False))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Task added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ PUT to update task
@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        data = request.get_json()
        completed = data.get('completed')
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tasks SET is_completed = %s WHERE id = %s", (completed, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Task updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ DELETE task
@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Task deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ✅ Root
@app.route('/')
def index():
    return 'Flask To-Do API is running 🚀'

# ✅ Main
if __name__ == "__main__":
    app.run(debug=True)
