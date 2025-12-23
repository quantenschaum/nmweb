import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte(), tailwindcss()],
  build: {
    minify: false,
  },
  server: {
    // host: "0.0.0.0",
    // allowedHosts: true,
    proxy: {
      "/nm": {
        target: "http://localhost:5005",
        changeOrigin: true,
      },
    },
  },
});
