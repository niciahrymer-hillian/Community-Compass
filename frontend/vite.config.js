import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite dev server on :5173 (the origin the backend CORS allows).
export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
});
