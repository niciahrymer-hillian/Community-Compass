import { Navigate, Route, Routes } from "react-router-dom";
import Nav from "./components/Nav.jsx";
import { getToken } from "./api";
import Login from "./pages/Login.jsx";
import Intake from "./pages/Intake.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import HousingMap from "./pages/HousingMap.jsx";
import Resources from "./pages/Resources.jsx";
import Assistant from "./pages/Assistant.jsx";
import Caseworker from "./pages/Caseworker.jsx";

// Gate pages that need a signed-in resident; bounce to /login otherwise.
function RequireAuth({ children }) {
  return getToken() ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <>
      <Nav />
      <main className="container">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/intake" element={<RequireAuth><Intake /></RequireAuth>} />
          <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
          <Route path="/caseworker" element={<RequireAuth><Caseworker /></RequireAuth>} />
          {/* Map + resources + assistant are public (no auth needed to browse). */}
          <Route path="/housing" element={<HousingMap />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/assistant" element={<Assistant />} />
          <Route path="*" element={<Navigate to={getToken() ? "/dashboard" : "/login"} replace />} />
        </Routes>
      </main>
    </>
  );
}
