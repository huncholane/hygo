<!--
  Redirects
  https://kit.svelte.dev/docs/modules#$app-navigation
  -->
<script>
  import { login, user, post } from "../../../api";
  import { goto } from "$app/navigation";

  let userVal;
  let username = "";
  let password = "";
  user.subscribe((val) => {
    if (val) goto("/user");
  });
  function handleOnSubmit() {
    login(username, password);
  }
  const sendRedirect = async () => {
    const res = await fetch("/api/spotify/redirect/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await res.json();
    goto(data.redirect);
  };
</script>

<div class="card">
  <h1>Login</h1>
  <form on:submit|preventDefault={handleOnSubmit}>
    <div style="width:100%;text-align:center;padding-bottom:20px;">
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
  <div class="social">
    <button on:click|preventDefault={sendRedirect}>
      <img src="/img/reference/spotify.png" alt="Spotify" />
    </button>
  </div>
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
    padding-bottom: 20px;
    padding-left: 0px;
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
  div.social {
    display: flex;
    justify-content: center;
    padding: 20px 0px;
  }
</style>
