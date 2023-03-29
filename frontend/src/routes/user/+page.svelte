<script>
  import { getMe, get } from "../../api";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { user } from "../../api";

  user.subscribe((user) => {
    console.log(user);
  });
</script>
