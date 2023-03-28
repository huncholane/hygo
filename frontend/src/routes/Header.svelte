<script>
  let open = false;
</script>

<header>
  <nav>
    <a href="/">
      <img src="/img/brand/inverted.png" height="40" alt="" />
    </a>
    <button on:click={() => (open = !open)}>
      <img
        class="avatar"
        src="/img/avatars/hygo_ghost.png"
        height="40"
        alt=""
      />
    </button>
  </nav>
</header>
<nav />
{#if open}
  <nav class="container">
    <!-- content here -->
    <nav class="flex">
      <a href="/about">About</a>
      <a href="/contact">Contact</a>
      <a href="/login">Login</a>
      <a href="/register">Register</a>
    </nav>
  </nav>
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
  nav {
    margin: auto 10px;
    display: flex;
    justify-content: space-between;
    width: 100%;
  }
  button {
    background: none;
    border: none;
    cursor: pointer;
  }
  nav.container {
    width: 100%;
    height: 100vh;
    background-color: black;
    position: fixed;
    top: var(--nav-height);
    padding: 0px;
    margin: 0px;
  }
  nav.flex {
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: center;
    height: 100%;
    gap: var(--nav-spacing);
    padding-top: var(--nav-spacing);
  }
</style>
