import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

// CC-04: guided resident intake → POST /intake → dashboard.
const EMPTY = {
  age: "", location: "", household_size: "", housing_status: "", income_range: "",
  employment_status: "", education_status: "", document_status: "",
  housing_assistance_type: "", notes: "",
  transportation_need: false, food_access_need: false,
  health_wellness_need: false, safety_concern: false,
};

export default function Intake() {
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState("");
  const nav = useNavigate();

  const set = (k) => (e) => {
    const v = e.target.type === "checkbox" ? e.target.checked : e.target.value;
    setForm((f) => ({ ...f, [k]: v }));
  };

  async function submit(e) {
    e.preventDefault();
    setError("");
    // Drop empty strings so optional fields stay null; coerce numbers.
    const payload = {};
    for (const [k, v] of Object.entries(form)) {
      if (v === "" || v === null) continue;
      payload[k] = k === "age" || k === "household_size" ? Number(v) : v;
    }
    try {
      await api.createIntake(payload);
      nav("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="card">
      <h1>Tell us about your situation</h1>
      <p className="muted">This helps us match you to housing and resources. Everything is optional.</p>
      <form onSubmit={submit} className="grid">
        <label>Age<input type="number" min="0" max="120" value={form.age} onChange={set("age")} /></label>
        <label>Location (city or ZIP)<input value={form.location} onChange={set("location")} placeholder="Wilmington, DE" /></label>
        <label>Household size<input type="number" min="1" value={form.household_size} onChange={set("household_size")} /></label>
        <label>Housing status
          <select value={form.housing_status} onChange={set("housing_status")}>
            <option value="">—</option>
            <option value="stable">Stable</option>
            <option value="at_risk">At risk</option>
            <option value="unstable">Unstable</option>
            <option value="homeless">Homeless</option>
          </select>
        </label>
        <label>Income range<input value={form.income_range} onChange={set("income_range")} placeholder="e.g. under $20k" /></label>
        <label>Employment status<input value={form.employment_status} onChange={set("employment_status")} placeholder="unemployed / part-time / …" /></label>
        <label>Education status<input value={form.education_status} onChange={set("education_status")} placeholder="no_diploma / GED / …" /></label>
        <label>Document status
          <select value={form.document_status} onChange={set("document_status")}>
            <option value="">—</option>
            <option value="has_id">Has ID</option>
            <option value="partial">Partial</option>
            <option value="missing_id">Missing ID</option>
          </select>
        </label>
        <label>Housing assistance
          <select value={form.housing_assistance_type} onChange={set("housing_assistance_type")}>
            <option value="">—</option>
            <option value="section8">Section 8</option>
            <option value="srap">SRAP</option>
            <option value="senior_55plus">55+</option>
            <option value="income_restricted">Income-restricted</option>
            <option value="none">None</option>
          </select>
        </label>
        <fieldset className="needs">
          <legend>Needs</legend>
          <label className="check"><input type="checkbox" checked={form.transportation_need} onChange={set("transportation_need")} /> Transportation</label>
          <label className="check"><input type="checkbox" checked={form.food_access_need} onChange={set("food_access_need")} /> Food access</label>
          <label className="check"><input type="checkbox" checked={form.health_wellness_need} onChange={set("health_wellness_need")} /> Health / wellness</label>
          <label className="check"><input type="checkbox" checked={form.safety_concern} onChange={set("safety_concern")} /> Safety concern</label>
        </fieldset>
        <label className="full">Anything else?<textarea value={form.notes} onChange={set("notes")} rows="3" /></label>
        {error && <p className="error full">{error}</p>}
        <button type="submit" className="btn full">See my matches</button>
      </form>
    </div>
  );
}
