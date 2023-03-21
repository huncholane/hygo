<script>
  import Header from "./Header.svelte";
  import "./styles.css";
</script>

<div class="app">
  <Header />

  <main>
    <slot />
  </main>

  <footer>
    <div class="footer-flex">
      <div class="footer-left">
        <div class="footer-left-info">
          Hygo Since 2022,
          <a href="https://ghostystems.io">Ghost Systems LLC</a> -
          <a href="mailto:huncho@ghostsystems.io">huncho@ghostystems.io</a>
        </div>
      </div>
      <img class="icon" src="https://github.com/favicon.ico" alt="" />
      <img
        class="icon"
        src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png"
        alt="Discord"
      />
    </div>
  </footer>
</div>

<style>
  .app {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  main {
    display: flex;
    min-height: 700px;
    height: 100%;
    padding: 20px;
  }

  footer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 12px;
    background-color: rgba(24, 24, 25, 0.13);
  }

  .footer-flex {
    display: flex;
    flex-direction: row;
    justify-content: end;
    width: 100%;
    height: 40px;
  }

  img.icon {
    height: 30px;
    margin: auto 10px;
  }

  .footer-left {
    display: flex;
    flex-direction: row;
    justify-content: start;
    width: 100%;
    height: 40px;
  }

  .footer-left-info {
    margin: auto 10px;
  }

  @media (min-width: 480px) {
    footer {
      padding: 12px 0;
    }
  }
</style>
