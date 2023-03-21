<script>
  import Login from "./Login.svelte";
</script>

<div class="left">
  <!-- <img class="soundwaves" src="/brand/reduced/soundwaves.png" alt="" /> -->
  <img class="soundwaves" src="/stock/johnwick2.png" alt="" />
  <div class="info-container">
    <a href="https://www.spotify.com/us/premium/">
      <img
        class="premium-required"
        src="https://gamecardsdirect.com/content/image/00_alle-logos/handleidingen%20logos/spotify-premium-logo-klein.png"
        alt="Premium Required"
      />
    </a>
    <div class="info">
      Hygo requires <a href="https://www.spotify.com/us/premium/"
        >Spotify Premium</a
      >
    </div>
  </div>
  <div class="top-song-container">
    <div class="top-song">Top Song</div>
  </div>
</div>
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
