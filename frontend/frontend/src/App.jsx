import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [data, setData] = useState([]);
  const [name, setName] = useState("");

  const fetchData = async () => {
    const res = await fetch(`${API_URL}/api/data`);
    const result = await res.json();
    setData(result);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const addItem = async () => {
    await fetch(`${API_URL}/api/data`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });

    setName("");
    fetchData();
  };

  const deleteItem = async (id) => {
    await fetch(`${API_URL}/api/data/${id}`, {
      method: "DELETE",
    });

    fetchData();
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Fullstack App 🚀</h1>

      <p>Student: Anzhelika | ID: 123456</p>

      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter item"
      />
      <button onClick={addItem}>Add</button>

      <ul>
        {data.map((item) => (
          <li key={item.id}>
            {item.name}
            <button onClick={() => deleteItem(item.id)}>❌</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;