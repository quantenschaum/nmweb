<script context="module">
  import { writable } from "svelte/store";
  const data = writable({});
  export function info(title, msg) {
    data.set({ title, msg });
  }
</script>

<script>
  let dialog;
  $: if ($data.msg) dialog.showModal();
</script>

<dialog bind:this={dialog} class="modal">
  <div class="modal-box max-w-3/4">
    <h3 class="text-lg font-bold">{$data.title}</h3>
    {@html $data.msg}
  </div>
  <form method="dialog" class="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
