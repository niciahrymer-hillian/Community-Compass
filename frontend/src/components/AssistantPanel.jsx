import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";
import { getSaved, toggleSaved } from "../saved";

// Persistent panel from the prototype (index.html floating-panel): three tabs —
// AI assistant (mini chat), My Notes (localStorage + email), Saved Items.
const NOTES_KEY = "cc_notes";

export default function AssistantPanel() {
  const [open, setOpen] = useState(true);
  const [tab, setTab] = useState("assistant");

  return (
    <aside className={`panel ${open ? "" : "collapsed"}`} aria-label="Assistant panel">
      <button className="panel-toggle" onClick={() => setOpen((o) => !o)}>
        {open ? "▸" : "💬"}
      </button>
      {open && (
        <>
          <div className="panel-tabs">
            <button className={tab === "assistant" ? "active" : ""} onClick={() => setTab("assistant")}>Assistant</button>
            <button className={tab === "notes" ? "active" : ""} onClick={() => setTab("notes")}>Notes</button>
            <button className={tab === "saved" ? "active" : ""} onClick={() => setTab("saved")}>Saved</button>
          </div>
          <div className="panel-body">
            {tab === "assistant" && <MiniChat />}
            {tab === "notes" && <Notes />}
            {tab === "saved" && <Saved />}
          </div>
        </>
      )}
    </aside>
  );
}

function MiniChat() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Tell me what you need and I'll find matches." },
  ]);
  const [input, setInput] = useState("");
  const [suggestions, setSuggestions] = useState({});
  const nav = useNavigate();

  async function send(e) {
    e.preventDefault();
    if (!input.trim()) return;
    const convo = [...messages, { role: "user", content: input }];
    setMessages(convo);
    setInput("");
    try {
      const res = await api.assistantChat(convo);
      setMessages((m) => [...m, { role: "assistant", content: res.reply }]);
      const clean = Object.fromEntries(Object.entries(res.suggestions || {}).filter(([, v]) => v != null));
      setSuggestions((s) => ({ ...s, ...clean }));
    } catch {
      setMessages((m) => [...m, { role: "assistant", content: "(assistant offline)" }]);
    }
  }

  return (
    <div className="mini-chat">
      <div className="chat">
        {messages.map((m, i) => <div key={i} className={`bubble ${m.role}`}>{m.content}</div>)}
      </div>
      {Object.keys(suggestions).length > 0 && (
        <button className="btn small" onClick={() => { localStorage.setItem("cc_intake_prefill", JSON.stringify(suggestions)); nav("/intake"); }}>
          Use in intake →
        </button>
      )}
      <form onSubmit={send} className="mini-form">
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="I need a ride…" />
        <button className="btn small" type="submit">Send</button>
      </form>
    </div>
  );
}

function Notes() {
  const [text, setText] = useState(localStorage.getItem(NOTES_KEY) || "");
  return (
    <div className="notes">
      <textarea value={text} onChange={(e) => setText(e.target.value)} rows="6" placeholder="Type notes as you go…" />
      <div className="row">
        <button className="btn small" onClick={() => localStorage.setItem(NOTES_KEY, text)}>Save</button>
        <a className="btn small outline" href={`mailto:?subject=My Community Compass notes&body=${encodeURIComponent(text)}`}>Email to myself</a>
      </div>
    </div>
  );
}

function Saved() {
  const [items, setItems] = useState(getSaved());
  useEffect(() => {
    const refresh = () => setItems(getSaved());
    window.addEventListener("cc-saved-changed", refresh);
    return () => window.removeEventListener("cc-saved-changed", refresh);
  }, []);

  if (items.length === 0) return <p className="muted">No saved items yet. Tap “Save” on a card.</p>;
  return (
    <ul className="saved-list">
      {items.map((it) => (
        <li key={it.id}>
          <span>{it.label}</span>
          <button className="link-btn" onClick={() => toggleSaved(it)}>remove</button>
        </li>
      ))}
    </ul>
  );
}
