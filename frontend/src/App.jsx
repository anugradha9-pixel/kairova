import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./auth/Login";
import Dashboard from "./pages/Dashboard";

function ProtectedRoute({ children }) {
  const token = localStorage.getItem("access_token");

  // SAFE CHECK (prevents empty string / invalid token issues)
  const isAuthenticated = token && token !== "null" && token !== "undefined";

  return isAuthenticated ? children : <Navigate to="/" replace />;
}

export default function App() {
  return (
    <Routes>
      {/* Login Route */}
      <Route path="/" element={<Login />} />

      {/* Protected Dashboard Route */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      {/* Fallback route (prevents blank page on bad URLs) */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}