import PermissionManagement from "./pages/PermissionManagement";
import { useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import MyQR from "./pages/MyQR";
import { getToken } from "./services/authService";

function App() {
  const [page, setPage] = useState(
    getToken() ? "dashboard" : "login"
  );

  function handleLoginSuccess() {
    setPage("dashboard");
  }

  if (page === "login") {
    return (
      <Login
        onLoginSuccess={handleLoginSuccess}
      />
    );
  }

  return (
    <div>
      <nav>
        <button onClick={() => setPage("dashboard")}>
          Dashboard
        </button>

        <button onClick={() => setPage("qr")}>
          My QR
        </button>
        <button onClick={() => setPage("permissions")}>
  Permissions
</button>
      </nav>

      <hr />

      {page === "dashboard" && <Dashboard />}

      {page === "qr" && <MyQR />}
      {page === "permissions" && <PermissionManagement />}
    </div>
  );
}

export default App;