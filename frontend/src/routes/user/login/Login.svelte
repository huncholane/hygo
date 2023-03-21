<div class="card">
  <h1>Login</h1>
  <form action="">
    <div style="width:100%;text-align:center;">The Old Fashion</div>
    <label for="">Username</label>
    <input type="text" />
    <label for="">Password</label>
    <input type="password" />
  </form>
  <div style="height:10px" />
  <div style="width:100%;text-align:center;">The cool way</div>
  <form style="display:flex;justify-content:space-around;" action="">
    <button>social</button>
    <button>social</button>
    <button>social</button>
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
</style>
