import { useEffect, useState } from "react";
import AuthContext from "./AuthContext";
import { getAccessToken, getCurrentUser, login as loginRequest, logout as logoutRequest } from "../services/api";
export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null); const [loading, setLoading] = useState(true);
  useEffect(() => { (async () => { const token = getAccessToken(); if (!token) return setLoading(false); try { setUser(await getCurrentUser()); } catch { logoutRequest(); setUser(null); } finally { setLoading(false); } })(); }, []);
  async function login(username, password) { await loginRequest(username, password); const current = await getCurrentUser(); setUser(current); return current; }
  function logout() { logoutRequest(); setUser(null); }
  return <AuthContext.Provider value={{ user, loading, isAuthenticated: !!user, login, logout }}>{children}</AuthContext.Provider>;
}
