import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [tasks, setTasks] = useState([]);
  const [text, setText] = useState("");
  const [error, setError] = useState(null);

  const loadTasks = () => {
    axios
      .get("http://localhost:5000/api/tasks")
      .then((res) => {
        setTasks(res.data);
        setError(null);
      })
      .catch(() => setError("Failed to load tasks"));
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const addTask = () => {
    if (text.trim() === "") return;
    axios
      .post("http://localhost:5000/api/tasks", { title: text })
      .then(() => {
        setText("");
        loadTasks();
      })
      .catch(() => setError("Failed to add task"));
  };

  const toggleComplete = (task) => {
    axios
      .put(`http://localhost:5000/api/tasks/${task.id}`, {
        completed: !task.completed,
      })
      .then(loadTasks)
      .catch(() => setError("Failed to update task"));
  };

  const deleteTask = (id) => {
    axios
      .delete(`http://localhost:5000/api/tasks/${id}`)
      .then(loadTasks)
      .catch(() => setError("Failed to delete task"));
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="bg-white w-full max-w-md rounded shadow p-6">
        <h1 className="text-2xl font-bold mb-4">My To-Do List</h1>

        {error && <p className="text-red-500 mb-2">{error}</p>}

        <div className="flex gap-2 mb-4">
          <input
            className="border rounded w-full p-2"
            placeholder="Add Task..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button
            className="bg-blue-500 text-white px-4 rounded"
            onClick={addTask}
          >
            Add
          </button>
        </div>

        <ul>
          {tasks.length === 0 ? (
            <p className="text-gray-400">No tasks found.</p>
          ) : (
            tasks.map((task) => (
              <li
                key={task.id}
                className="flex justify-between items-center mb-2 border-b pb-2"
              >
                <span
                  className={task.completed ? "line-through text-gray-400" : ""}
                >
                  {task.title}
                </span>
                <div className="flex gap-2">
                  <button
                    className="text-green-600"
                    onClick={() => toggleComplete(task)}
                  >
                    {task.completed ? "Undo" : "Done"}
                  </button>
                  <button
                    className="text-red-600"
                    onClick={() => deleteTask(task.id)}
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
}

export default App;
