<script>
  import { getMe, get, post } from "../../api";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { user } from "../../api";
  let spotify = null;

  user.subscribe((user) => {
    spotify = user?.spotify;
    spotify = false;
  });

  const sendAuth = async () => {
    const res = await post("/api/spotify/redirect/");
    goto(res.redirect);
  };
</script>

<div class="main">
  {#if spotify}
    <div class="connected">Spotify Connected</div>
  {:else}
    <button on:click={sendAuth}>Link Spotify</button>
  {/if}
</div>

<style>
  div.connected {
    font-size: 2rem;
    color: var(--color-theme-2);
  }
  .main {
    text-align: center;
    font-size: 1.5rem;
  }
  button:hover {
    cursor: pointer;
  }
  button {
    all: unset;
    cursor: pointer;
    background-color: var(--color-theme-2);
    height: 50px;
    color: white;
    border-radius: 10px;
    padding: 0 20px;
  }
</style>
