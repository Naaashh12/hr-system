import { useState } from "react";
import API from "../api";

const ApplyLeave = () => {
  const [form, setForm] = useState({
    leave_type: "",
    start_date: "",
    end_date: "",
    reason: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await API.post("/leaves/", form);
      console.log(res.data);

      alert("Leave applied successfully ✅");

      // reset form
      setForm({
        leave_type: "",
        start_date: "",
        end_date: "",
        reason: "",
      });

    } catch (err) {
      console.log(err.response?.data);
      alert(err.response?.data?.detail || "Error applying leave ❌");
    }
  };

  return (
    <div>
      <h2>Apply Leave</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="leave_type"
          placeholder="Leave Type"
          value={form.leave_type}
          onChange={handleChange}
        />

        <input
          type="date"
          name="start_date"
          value={form.start_date}
          onChange={handleChange}
        />

        <input
          type="date"
          name="end_date"
          value={form.end_date}
          onChange={handleChange}
        />

        <input
          type="text"
          name="reason"
          placeholder="Reason"
          value={form.reason}
          onChange={handleChange}
        />

        <button type="submit">Apply</button>
      </form>
    </div>
  );
};

export default ApplyLeave;