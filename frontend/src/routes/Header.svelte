<script>
  import { getMe } from "../api";
  import { user, logout } from "../api";
  let isOpen = false;
  let userVal;
  user.subscribe((val) => {
    userVal = val;
  });
</script>

<header>
  <nav>
    <a href="/" on:click={() => (isOpen = false)}>
      <img src="/img/brand/inverted.png" height="40" alt="" />
    </a>
    <img
      class="avatar"
      src="/img/avatars/hygo_ghost.png"
      height="40"
      alt="user-icon"
      on:click={() => (isOpen = !isOpen)}
      on:keydown={() => (isOpen = !isOpen)}
    />
  </nav>
</header>
{#if isOpen}
  <div class="container">
    <!-- content here -->
    <div class="flex">
      {#if userVal}
        <!-- content here -->
        <a href="/user" on:click={() => (isOpen = !isOpen)}
          >Welcome back, {userVal.username}</a
        >
      {:else}
        <!-- else content here -->
        <a href="/user/login" on:click={() => (isOpen = false)}>Login</a>
      {/if}
      {#if userVal}
        <!-- content here -->
        <button on:click={logout}>Logout</button>
      {/if}
    </div>
  </div>
{/if}

<style>
  :root {
    --nav-height: 60px;
    --nav-spacing: 15px;
  }
  header {
    background: var(--color-bg-0);
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: var(--nav-height);
    position: fixed;
    width: 100%;
  }
  img.avatar {
    border-radius: 50%;
    border: 1px solid #000000;
  }
  img.avatar:hover {
    cursor: pointer;
  }
  nav {
    margin: auto 10px;
    display: flex;
    justify-content: space-between;
    width: 100%;
    /* height: 48px; */
  }
  button {
    background: none;
    border: none;
    cursor: pointer;
  }
  div.container {
    width: 100%;
    height: 100vh;
    background-color: var(--global-theme);
    position: fixed;
    top: var(--nav-height);
    padding: 0px;
    margin: 0px;
  }
  div.flex {
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
    height: 100%;
    gap: var(--nav-spacing);
    padding-top: var(--nav-spacing);
  }
</style>
