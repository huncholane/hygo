<script>
  import { get } from "../../api";
  import { onMount } from "svelte";
  let user;
  onMount(async () => {
    user = await get("/api/user/me/");
  });
</script>
