<script>
  export let value;
  export let title;
  export let classes = "badge-soft";

  let text, color;
  $: {
    text = value ? "yes" : "no";
    color = value ? "badge-success" : "badge-error";
  }
</script>

<div class="badge {color} {classes}" {title}>{text}</div>
