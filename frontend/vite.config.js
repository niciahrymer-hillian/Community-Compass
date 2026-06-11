import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite dev server on :5173 (the origin the backend CORS allows).
// strictPort so it never silently moves to 5174 — keeps the URL in sync.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, strictPort: true },
});
