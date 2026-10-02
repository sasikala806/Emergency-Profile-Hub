import { useState } from "react";
import { getCurrentUser, logout } from "../services/authService";

function Dashboard() {
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState("");

  async function loadUser() {
    try {
      const data = await getCurrentUser();
      setUser(data.user);
      setMessage("");
    } catch (error) {
      setMessage(error.message);
    }
  }

  function handleLogout() {
    logout();
    setUser(null);
    setMessage("Logged out successfully.");
  }

  return (
    <div>
      <h1>Emergency Profile Hub</h1>

      <h2>Dashboard</h2>

      <button onClick={loadUser}>
        Load My Profile
      </button>

      {" "}

      <button onClick={handleLogout}>
        Logout
      </button>

      {message && <p>{message}</p>}

      {user && (
        <div>
          <h3>User Information</h3>

          <p>
            <strong>Name:</strong> {user.name || "Not available"}
          </p>

          <p>
            <strong>Email:</strong> {user.email}
          </p>

          <p>
            <strong>Role:</strong> {user.role}
          </p>

          <p>
            <strong>User ID:</strong> {user.user_id}
          </p>
        </div>
      )}
    </div>
  );
}

export default Dashboard;