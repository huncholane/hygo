<!--
  Redirects
  https://kit.svelte.dev/docs/modules#$app-navigation
  -->
<script>
  import login from "./login.js";
  import { redirect } from "@sveltejs/kit";
  import { goto } from "$app/navigation";
  let username = "";
  let password = "";
  function handleOnSubmit() {
    login(username, password).then((res) => {
      if (res.status === 200) {
        goto("/user");
      }
    });
  }
</script>

<div class="card">
  <h1>Login</h1>
  <form on:submit|preventDefault={handleOnSubmit}>
    <div style="width:100%;text-align:center;">
      The Good Ol' Username and Password
    </div>
    <label for="">Username</label>
    <input placeholder="Username or email" type="text" bind:value={username} />
    <label for="">Password</label>
    <input placeholder="Password" type="password" bind:value={password} />
    <div class="flex">
      <input id="submit" type="submit" />
    </div>
  </form>
  <div style="height:10px" />
  <div style="width:100%;text-align:center;">
    Login or Register with Social Media
  </div>
  <form style="display:flex;justify-content:space-around;" action="">
    <a href="https://google.com">
      <img
        src="https://cdn.freebiesupply.com/logos/large/2x/google-icon-logo-png-transparent.png"
        alt="Google"
      />
    </a>
    <a href="https://facebook.com">
      <img
        src="https://www.edigitalagency.com.au/wp-content/uploads/Facebook-logo-blue-circle-large-transparent-png.png"
        alt="Facebook"
      />
    </a>
    <a href="https://spotify.com">
      <img
        src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/1982px-Spotify_icon.svg.png"
        alt="Spotify"
      />
    </a>
  </form>
  <div class="needs-account">
    <div>
      Want to sign up the old school way?
      <br /><br />
      <a href="register">Click Here</a> to register.
    </div>
  </div>
</div>

<style>
  img {
    height: 50px;
  }
  .needs-account {
    text-align: center;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .card {
    display: flex;
    flex-direction: column;
  }

  .flex {
    display: flex;
    justify-content: center;
  }
  #submit {
    margin: 10px auto;
    width: 200px;
    background-color: #203582;
    height: 45px;
    color: white;
  }
  #submit:hover {
    background-color: #203582;
    color: white;
    cursor: pointer;
  }
</style>
