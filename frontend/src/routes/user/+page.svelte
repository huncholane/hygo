<script>
  import { getMe, get } from "../../api";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  onMount(async () => {
    let { redirect } = await (
      await fetch("/api/spotify/redirect/", {
        method: "POST",
      })
    ).json();
    goto(redirect);
  });
</script>
