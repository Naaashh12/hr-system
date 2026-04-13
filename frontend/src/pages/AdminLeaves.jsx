import { useEffect, useState } from "react";
import API from "../api";

function AdminLeaves() {
  const [leaves, setLeaves] = useState([]);

  const fetchLeaves = async () => {
    try {
      const res = await API.get("/leaves/pending");
      setLeaves(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  const updateStatus = async (id, status) => {
    try {
      await API.put(`/leaves/${id}/status`, { status });
      fetchLeaves(); // refresh
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    fetchLeaves();
  }, []);

  return (
    <div>
      <h2>Pending Leaves</h2>

      {leaves.map((leave) => (
        <div key={leave.id} style={{ border: "1px solid gray", margin: 10, padding: 10 }}>
          <p>{leave.leave_type}</p>
          <p>{leave.start_date} → {leave.end_date}</p>
          <p>{leave.reason}</p>

          <button onClick={() => updateStatus(leave.id, "approved")}>
            Approve
          </button>

          <button onClick={() => updateStatus(leave.id, "rejected")}>
            Reject
          </button>
        </div>
      ))}
    </div>
  );
}

export default AdminLeaves;