import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

const Dashboard = () => {
  const navigate = useNavigate();
  const [role, setRole] = useState("");

  useEffect(() => {
    const storedRole = localStorage.getItem("role");
    setRole(storedRole);
  }, []);

  return (
    <div>
      <h2>Dashboard 🎉</h2>

      {/* 👤 EMPLOYEE */}
      {role === "employee" && (
        <>
          <button onClick={() => navigate("/apply-leave")}>
            Apply Leave
          </button>

          <button onClick={() => navigate("/my-leaves")}>
            My Leaves
          </button>
        </>
      )}

      {/* 👩‍💼 HR */}
      {role === "hr" && (
        <>
          <button onClick={() => navigate("/admin/leaves")}>
            Manage Leaves
          </button>
        </>
      )}

      {/* 🛠 ADMIN */}
      {role === "admin" && (
        <>
          <button onClick={() => navigate("/admin")}>
            Admin Panel
          </button>
        </>
      )}

      <br /><br />

      <button
        onClick={() => {
          localStorage.removeItem("token");
          localStorage.removeItem("role");
          window.location.href = "/";
        }}
      >
        Logout
      </button>
    </div>
  );
};

export default Dashboard;