const API_BASE_URL = "http://127.0.0.1:8000";

export function getAccessToken() { return localStorage.getItem("access_token"); }
export function setAccessToken(token) { localStorage.setItem("access_token", token); }
export function removeAccessToken() { localStorage.removeItem("access_token"); }

async function apiRequest(endpoint, options = {}) {
  const token = getAccessToken();
  const headers = { Accept: "application/json", ...options.headers };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers });
  const text = await response.text();
  let data = null;
  if (text) { try { data = JSON.parse(text); } catch { data = text; } }

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    if (typeof data === "object" && data) {
      if (Array.isArray(data.detail)) message = data.detail.map((x) => `${x.loc?.at(-1) || "field"}: ${x.msg}`).join("\n");
      else if (data.detail) message = data.detail;
      else if (data.message) message = data.message;
    }
    throw new Error(message);
  }
  return data;
}

export function registerUser(userData) {
  return apiRequest("/api/v1/users/register", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(userData) });
}
export function sendMobileOTP(mobileNumber) {
  return apiRequest("/api/v1/users/send-mobile-otp", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ mobile_number: mobileNumber }) });
}
export function verifyMobileOTP(verificationId, otp) {
  return apiRequest("/api/v1/users/verify-mobile-otp", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ verification_id: verificationId, otp }) });
}
export function resendMobileOTP(verificationId) {
  return apiRequest("/api/v1/users/resend-mobile-otp", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ verification_id: verificationId }) });
}
export async function login(username, password) {
  const form = new URLSearchParams();
  form.append("grant_type", "password"); form.append("username", username); form.append("password", password);
  form.append("scope", ""); form.append("client_id", ""); form.append("client_secret", "");
  const response = await fetch(`${API_BASE_URL}/api/v1/users/login`, { method: "POST", headers: { Accept: "application/json", "Content-Type": "application/x-www-form-urlencoded" }, body: form.toString() });
  const text = await response.text();
  let data = null; if (text) { try { data = JSON.parse(text); } catch { data = text; } }
  if (!response.ok) throw new Error(data?.detail || "Login failed.");
  if (!data?.access_token) throw new Error("Login response does not contain an access token.");
  setAccessToken(data.access_token); return data;
}
export function getCurrentUser() { return apiRequest("/api/v1/users/me"); }
export function getDashboardSummary() { return apiRequest("/api/v1/dashboard/summary"); }
export function getExpenses({ category = "", search = "", page = 1, limit = 100 } = {}) {
  const params = new URLSearchParams();
  if (category) params.set("category", category);
  if (search) params.set("search", search);
  params.set("page", page); params.set("limit", limit);
  return apiRequest(`/api/v1/expenses?${params.toString()}`);
}
export function createExpense(data) {
  return apiRequest("/api/v1/expenses", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
}
export function updateExpense(id, data) {
  return apiRequest(`/api/v1/expenses/${id}`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
}
export async function deleteExpense(id) {
  return apiRequest(`/api/v1/expenses/${id}`, { method: "DELETE" });
}
export function logout() { removeAccessToken(); }
