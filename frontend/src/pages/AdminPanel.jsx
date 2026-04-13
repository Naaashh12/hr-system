import { useState } from "react";
import API from "../api";

function AdminPanel() {
  const [form, setForm] = useState({
    email: "",
    password: "",
    role: "employee",
  });

  const handleCreate = async () => {
    try {
      await API.post("/auth/register", form);
      alert("User created ✅");
    } catch (err) {
      console.log(err.response.data);
    }
  };

  return (
    <div>
      <h2>Create User</h2>

      <input
        placeholder="Email"
        onChange={(e) => setForm({ ...form, email: e.target.value })}
      />

      <input
        placeholder="Password"
        type="password"
        onChange={(e) => setForm({ ...form, password: e.target.value })}
      />

      <select
        onChange={(e) => setForm({ ...form, role: e.target.value })}
      >
        <option value="employee">Employee</option>
        <option value="hr">HR</option>
      </select>

      <button onClick={handleCreate}>Create</button>
    </div>
  );
}

export default AdminPanel;