import { mount } from "svelte";
import App from "./App.svelte";
// import "./app.scss";
// import "@picocss/pico/css/pico.min.css";
import "./style.css";

const app = mount(App, {
  target: document.getElementById("app"),
});

export default app;
