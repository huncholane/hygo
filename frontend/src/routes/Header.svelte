<script>
  import { page } from "$app/stores";
  import logo from "$lib/images/svelte-logo.svg";
  import github from "$lib/images/github.svg";
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
      </ul>
    </nav>
  </div>
</header>

<style>
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
    height: 60%;
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
