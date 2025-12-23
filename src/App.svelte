<script>
  import Devs from "./Devs.svelte";
  import Cons from "./Cons.svelte";
  import Aps from "./Aps.svelte";
  import State from "./State.svelte";
  import Menu from "./Menu.svelte";
</script>

<div class="p-5 w-min">
  <h1 class="p-3">Status</h1>
  <div class="rounded-box border border-base-content/5 bg-base-100">
    <State />
  </div>
</div>

<div class="p-5">
  <h1 class="p-3">Devices</h1>
  <div class="rounded-box border border-base-content/5 bg-base-100">
    <Devs />
  </div>
</div>

<div class="p-5">
  <h1 class="p-3">Connections</h1>
  <div class="rounded-box border border-base-content/5 bg-base-100">
    <Cons />
  </div>
</div>

<div class="p-5">
  <h1 class="p-3">Access Points</h1>
  <div class="rounded-box border border-base-content/5 bg-base-100">
    <Aps />
  </div>
</div>

<Menu />
