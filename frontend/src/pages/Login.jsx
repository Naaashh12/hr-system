import { useState } from "react";
import { loginUser } from "../api";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const handleLogin = async (e) => {
    e.preventDefault();

    const data = { email, password };

    try {
      const res = await loginUser(data);

      // ✅ save token
      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("role", res.data.role); // ✅ real role from backend; 
      // ✅ show success
      alert("Login successful ✅");

      // ✅ redirect

     window.location.href = "/dashboard";
    } catch (err) {
      console.log(err.response?.data);

      // ❌ show error
      alert(err.response?.data?.detail || "Login failed ❌");
    }
  };

  return (
    <div style={{ padding: "50px" }}>
      <h2>Login</h2>

      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />
        <br />
        <br />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <br />
        <br />

        <button type="submit">Login</button>
      </form>
    </div>
  );
}
