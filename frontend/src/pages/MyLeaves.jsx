import { useEffect, useState } from "react";
import API from "../api";

const MyLeaves = () => {
  const [leaves, setLeaves] = useState([]);

  useEffect(() => {
    const fetchLeaves = async () => {
      try {
        const res = await API.get("/leaves/my-leaves");
        setLeaves(res.data);
      } catch (err) {
        console.log(err.response.data); // already there

        // ✅ ADD THIS LINE
        alert(JSON.stringify(err.response.data));
      }
    };

    fetchLeaves();
  }, []);

  return (
    <div>
      <h2>My Leaves</h2>

      {leaves.length === 0 ? (
        <p>No leaves found</p>
      ) : (
        leaves.map((leave) => (
          <div
            key={leave.id}
            style={{
              border: "1px solid gray",
              margin: "10px",
              padding: "10px",
            }}
          >
            <p>
              <b>Type:</b> {leave.leave_type}
            </p>
            <p>
              <b>From:</b> {leave.start_date}
            </p>
            <p>
              <b>To:</b> {leave.end_date}
            </p>
            <p>
              <b>Status:</b> {leave.status}
            </p>
            <p>
              <b>Reason:</b> {leave.reason}
            </p>
            <p>
              Status:{" "}
              <span
                style={{
                  color:
                    leave.status === "approved"
                      ? "green"
                      : leave.status === "rejected"
                        ? "red"
                        : "orange",
                }}
              >
                {leave.status}
              </span>
            </p>
          </div>
        ))
      )}
    </div>
  );
};

export default MyLeaves;
