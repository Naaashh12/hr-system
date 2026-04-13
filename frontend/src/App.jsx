import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ApplyLeave from "./pages/ApplyLeave";
import MyLeaves from "./pages/MyLeaves";
import AdminPanel from "./pages/AdminPanel";
import AdminLeaves from "./pages/AdminLeaves";
function App() {
  const isAuthenticated = () => {
  return !!localStorage.getItem("token");
};
  const getRole = () => {
  return localStorage.getItem("role");
};
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
  path="/dashboard"
  element={isAuthenticated() ? <Dashboard /> : <Login />}
/>

<Route
  path="/apply-leave"
  element={isAuthenticated() ? <ApplyLeave /> : <Login />}
/>

<Route
  path="/my-leaves"
  element={isAuthenticated() ? <MyLeaves /> : <Login />}
/>

<Route
  path="/admin"
  element={
    isAuthenticated() ? (
      getRole() === "admin" ? (
        <AdminPanel />
      ) : (
        <h2>❌ Access Denied (Admin only)</h2>
      )
    ) : (
      <Login />
    )
  }
/>

<Route
  path="/admin/leaves"
  element={
    isAuthenticated() ? (
      getRole() === "hr" ? (
        <AdminLeaves />
      ) : (
        <h2>❌ Access Denied (HR only)</h2>
      )
    ) : (
      <Login />
    )
  }
/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
