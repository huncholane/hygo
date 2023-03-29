<script>
  import { getMe, get } from "../../api";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { user } from "../../api";
  let spotify = null;

  user.subscribe((user) => {
    spotify = user?.spotify;
  });
</script>

{#if spotify}
  <h1 class="connected">Spotify Connected</h1>
{:else}
  <h1>Spotify</h1>
  <p>Spotify is not connected</p>
  <button on:click={() => goto("/user/spotify/connect")}> Connect </button>
{/if}

<style>
  h1.connected {
    font-size: 2rem;
    color: var(--color-theme-2);
  }
</style>
