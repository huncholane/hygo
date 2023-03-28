<script>
  import Login from "./Login.svelte";
</script>

<Login />

<style>
  .info-container {
    background-color: var(--background-card);
    margin: 10px 0 0 0;
    bottom: 0;
    border-radius: 10px;
    height: 100px;
    display: flex;
  }
  .top-song-container {
    background-color: var(--background-card);
    margin: 10px 0 0 0;
    bottom: 0;
    border-radius: 10px;
    height: 100%;
    display: flex;
  }
  .top-song {
    margin: auto;
  }
  .info {
    margin: auto;
  }
  .premium-required {
    margin: auto 5px;
    height: 100px;
  }
  .left {
    padding: 0 20px 0 0;
    display: flex;
    flex-direction: column;
  }
  .soundwaves {
    width: 550px;
    border-radius: 10px;
  }
</style>
