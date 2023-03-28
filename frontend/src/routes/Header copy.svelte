<script>
  export let user;
</script>

<header>
  <a class="brand" href="/">
    <div class="brand" />
  </a>
  <div class="cluster">
    <nav>
      <ul>
        <li><a href="/about">About</a></li>
        <li><a href="/blog">Blog</a></li>
        <li><a href="/contact">Contact</a></li>
        <li>
          {#if user}
            <!-- content here -->
            <a href="/user">
              <img
                class="avatar"
                src="https://static.vecteezy.com/system/resources/thumbnails/005/545/335/small/user-sign-icon-person-symbol-human-avatar-isolated-on-white-backogrund-vector.jpg"
                alt="User"
              />
            </a>
          {:else}
            <a href="/user/login">Login</a>
          {/if}
        </li>
      </ul>
    </nav>
  </div>
</header>

<style>
  .avatar {
    height: 40px;
    width: 40px;
    border-radius: 50%;
  }
  .cluster {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  .brand {
    background-image: url("/brand/inverted.png");
    background-size: contain;
    background-repeat: no-repeat;
    margin-left: 4px;
    width: 120px;
  }
  a.brand {
    height: 40px;
    margin-top: auto;
    margin-bottom: auto;
  }
  header {
    display: flex;
    justify-content: space-between;
    height: 80px;
    background-color: var(--color-bg-0);
  }

  nav {
    display: flex;
  }

  ul {
    position: relative;
    padding: 0;
    margin: 0;
    height: 3em;
    display: flex;
    justify-content: center;
    align-items: center;
    list-style: none;
    background: var(--background);
    background-size: contain;
  }

  li {
    position: relative;
    height: 100%;
  }

  nav a {
    display: flex;
    height: 100%;
    align-items: center;
    padding: 0 0.5rem;
    color: var(--color-text);
    font-weight: 700;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-decoration: none;
    transition: color 0.2s linear;
  }

  a:hover {
    color: var(--color-theme-1);
  }
</style>
