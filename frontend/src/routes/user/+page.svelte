<script>
  import { getMe, get } from "../../api";
  import { onMount } from "svelte";

  onMount(() => {
    get("/api/spotify/redirect/");
  });
</script>
