import { useState } from "react";
import { grantPermission } from "../services/permissionService";

function PermissionManagement() {
  const [doctorId, setDoctorId] = useState("");
  const [permissionType, setPermissionType] = useState("medical");
  const [message, setMessage] = useState("");

  async function handleGrantPermission(event) {
    event.preventDefault();

    try {
      const data = await grantPermission(
        doctorId,
        permissionType
      );

      setMessage(
        data.message || "Permission granted successfully."
      );
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <div>
      <h1>Permission Management</h1>

      <form onSubmit={handleGrantPermission}>
        <div>
          <label>Doctor User ID</label>
          <br />

          <input
            type="text"
            value={doctorId}
            onChange={(event) =>
              setDoctorId(event.target.value)
            }
            placeholder="Enter doctor user ID"
            required
          />
        </div>

        <br />

        <div>
          <label>Permission Type</label>
          <br />

          <select
            value={permissionType}
            onChange={(event) =>
              setPermissionType(event.target.value)
            }
          >
            <option value="medical">Medical</option>
            <option value="emergency">Emergency</option>
            <option value="profile">Profile</option>
          </select>
        </div>

        <br />

        <button type="submit">
          Grant Permission
        </button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default PermissionManagement;