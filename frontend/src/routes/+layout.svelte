<script>
  import { onMount } from "svelte";
  import { getMe } from "../api";
  import Footer from "./Footer.svelte";
  import Header from "./Header.svelte";
  import "./styles.css";
  onMount(getMe);
</script>

<div class="app">
  <Header />

  <main>
    <slot />
  </main>

  <Footer />
</div>

<style>
  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  main {
    padding: 20px;
    min-height: 100vh;
    margin-top: var(--nav-height);
  }
</style>
