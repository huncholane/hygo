export default async function login(username, password) {
  let res = await fetch("/api/auth/login/", {
    method: "POST",
    headers: {
      Authorization: "Basic " + btoa(username + ":" + password),
    },
  });
  let data = await res.json();
  const expires = new Date(data.expiry);
  document.cookie =
    "token=" + data.token + "; expires=" + expires.toUTCString() + ";";
}
