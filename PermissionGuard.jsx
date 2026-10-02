import { useEffect, useState } from "react";
import { checkPermission } from "../services/permissionService";
import AccessDenied from "../pages/AccessDenied";

function PermissionGuard({
  patientId,
  permissionType,
  children,
}) {
  const [allowed, setAllowed] = useState(null);

  useEffect(() => {
    async function checkAccess() {
      try {
        const data = await checkPermission(
          patientId,
          permissionType
        );

        setAllowed(data.has_permission);
      } catch (error) {
        setAllowed(false);
      }
    }

    checkAccess();
  }, [patientId, permissionType]);

  if (allowed === null) {
    return <p>Checking permission...</p>;
  }

  if (!allowed) {
    return <AccessDenied />;
  }

  return children;
}

export default PermissionGuard;