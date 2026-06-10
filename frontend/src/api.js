// Thin fetch wrapper around the Python API. Token lives in localStorage; in
// production it comes from Supabase, in dev from POST /auth/dev-login.

const BASE = import.meta.env.VITE_PYTHON_API_URL || "http://localhost:8000";

export const getToken = () => localStorage.getItem("cc_token");
export const setToken = (t) => localStorage.setItem("cc_token", t);
export const getUser = () => {
  const u = localStorage.getItem("cc_user");
  return u ? JSON.parse(u) : null;
};
export const setUser = (u) => localStorage.setItem("cc_user", JSON.stringify(u));
export const logout = () => {
  localStorage.removeItem("cc_token");
  localStorage.removeItem("cc_user");
};

async function request(path, { method = "GET", body, auth = false } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth && getToken()) headers.Authorization = `Bearer ${getToken()}`;
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    // FastAPI errors come back as {detail: ...}; surface a readable message.
    const err = await res.json().catch(() => ({}));
    const detail = typeof err.detail === "string" ? err.detail : `Request failed (${res.status})`;
    throw new Error(detail);
  }
  return res.status === 204 ? null : res.json();
}

export const api = {
  devLogin: (email, role) => request("/auth/dev-login", { method: "POST", body: { email, role } }),
  createIntake: (data) => request("/intake", { method: "POST", body: data, auth: true }),
  recommendations: () => request("/recommendations/me", { auth: true }),
  risk: () => request("/risk/me", { auth: true }),
  housing: (qs = "") => request(`/housing${qs}`),
  resources: (qs = "") => request(`/resources${qs}`),
  assistantChat: (messages) => request("/assistant/chat", { method: "POST", body: { messages } }),
  // Consolidated newsfeed (FirstStep items + HomeMatch HUD/DSHA) — Python service.
  news: () => request("/news"),
  // Caseworker / navigator dashboard.
  caseworkerSummary: () => request("/caseworker/summary", { auth: true }),
  residents: (risk = "") => request(`/caseworker/residents${risk ? `?risk=${risk}` : ""}`, { auth: true }),
  resident: (id) => request(`/caseworker/residents/${id}`, { auth: true }),
  // Admin resource management (CC-22).
  createResource: (data) => request("/resources", { method: "POST", body: data, auth: true }),
  updateResource: (id, data) => request(`/resources/${id}`, { method: "PUT", body: data, auth: true }),
  deactivateResource: (id) => request(`/resources/${id}/deactivate`, { method: "POST", auth: true }),
};
