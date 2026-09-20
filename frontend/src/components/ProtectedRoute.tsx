import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute() {
  const { user, loading } = useAuth();
  if (loading) {
    return <div className="min-h-screen bg-[#0b0b0b] grid place-items-center text-slate-300">Loading NutriCoach...</div>;
  }
  return user ? <Outlet /> : <Navigate to="/login" replace />;
}
