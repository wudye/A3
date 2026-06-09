"use client";
import { useRequireAuth } from "@/core/auth/AuthProvider"; 

export default function tempbPage() {
  const { user, logout } = useRequireAuth();


  return (
    <div>
      <h1>tempb</h1>
      <p>Welcome back, {user?.name}!</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
