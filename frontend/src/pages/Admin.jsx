import { useEffect, useState } from "react";
import { api } from "../api";

// CC-22: admin resource management — add, edit, (de)activate resources.
const CATEGORIES = [
  "housing", "clothing", "household", "food", "transportation", "employment", "wellness",
  "education", "documents", "safety", "youth_services", "financial_literacy", "legal_aid", "mentorship",
];
const EMPTY = {
  name: "", category: "housing", description: "", contact_phone: "", website: "",
  city: "", state: "DE", eligibility_notes: "", need_tags: "",
};

export default function Admin() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");

  function load() {
    api.resources("?active_only=false").then(setItems).catch((e) => setError(e.message));
  }
  useEffect(() => { load(); }, []);

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  function reset() {
    setForm(EMPTY);
    setEditingId(null);
  }

  async function submit(e) {
    e.preventDefault();
    setError("");
    setMsg("");
    // need_tags is a comma-separated input → array.
    const payload = {
      ...form,
      need_tags: form.need_tags ? form.need_tags.split(",").map((t) => t.trim()).filter(Boolean) : [],
    };
    try {
      if (editingId) {
        await api.updateResource(editingId, payload);
        setMsg("Resource updated.");
      } else {
        await api.createResource(payload);
        setMsg("Resource added.");
      }
      reset();
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  function edit(r) {
    setEditingId(r.id);
    setForm({
      name: r.name || "", category: r.category || "housing", description: r.description || "",
      contact_phone: r.contact_phone || "", website: r.website || "", city: r.city || "",
      state: r.state || "DE", eligibility_notes: r.eligibility_notes || "",
      need_tags: (r.need_tags || []).join(", "),
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function toggleActive(r) {
    setError("");
    try {
      if (r.is_active) await api.deactivateResource(r.id);
      else await api.updateResource(r.id, { is_active: true });
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h1>Admin · resources</h1>

      <form className="card" onSubmit={submit}>
        <h2>{editingId ? "Edit resource" : "Add resource"}</h2>
        <div className="grid">
          <label>Name<input value={form.name} onChange={set("name")} required /></label>
          <label>Category
            <select value={form.category} onChange={set("category")}>
              {CATEGORIES.map((c) => <option key={c} value={c}>{c.replace("_", " ")}</option>)}
            </select>
          </label>
          <label>City<input value={form.city} onChange={set("city")} /></label>
          <label>State<input value={form.state} onChange={set("state")} /></label>
          <label>Phone<input value={form.contact_phone} onChange={set("contact_phone")} /></label>
          <label>Website<input value={form.website} onChange={set("website")} /></label>
          <label className="full">Description<textarea rows="2" value={form.description} onChange={set("description")} /></label>
          <label className="full">Eligibility notes<input value={form.eligibility_notes} onChange={set("eligibility_notes")} /></label>
          <label className="full">Need tags (comma-separated)<input value={form.need_tags} onChange={set("need_tags")} placeholder="food, housing" /></label>
        </div>
        {error && <p className="error">{error}</p>}
        {msg && <p className="muted">{msg}</p>}
        <div className="row">
          <button className="btn" type="submit">{editingId ? "Save changes" : "Add resource"}</button>
          {editingId && <button type="button" className="btn outline" onClick={reset}>Cancel</button>}
        </div>
      </form>

      <h2>All resources ({items.length})</h2>
      <ul className="resident-list">
        {items.map((r) => (
          <li key={r.id}>
            <div className="resident-row" style={{ cursor: "default" }}>
              <span>
                {r.name} <span className="muted">· {r.category}{!r.is_active && " · inactive"}</span>
              </span>
              <span className="row">
                <button className="btn small outline" onClick={() => edit(r)}>Edit</button>
                <button className="btn small" onClick={() => toggleActive(r)}>
                  {r.is_active ? "Deactivate" : "Reactivate"}
                </button>
              </span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
