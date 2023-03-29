import { writable } from "svelte/store";

export const user = writable(null);

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export function getToken() {
  return getCookie("token");
}

export async function request_json(endpoint, method, body) {
  if (!getToken()) {
    throw new Error("No token found");
  }
  let res = await fetch(endpoint, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + getCookie("token"),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(res.statusText);
  }
  return await res.json();
}

export async function get(endpoint) {
  return await request_json(endpoint, "GET");
}

export async function post(endpoint, body) {
  return await request_json(endpoint, "POST", body);
}

export async function put(endpoint, body) {
  return await request_json(endpoint, "PUT", body);
}

export async function del(endpoint) {
  return await request_json(endpoint, "DELETE");
}

export async function patch(endpoint, body) {
  return await request_json(endpoint, "PATCH", body);
}

export async function getMe() {
  try {
    let data = await get("/api/user/me/");
    user.set(data);
    return data;
  } catch (e) {
    return null;
  }
}

export async function login(username, password) {
  let res = await fetch("/api/auth/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Basic " + btoa(username + ":" + password),
    },
  });
  let data = await res.json();
  const expires = new Date(data.expiry);
  document.cookie =
    "token=" + data.token + "; expires=" + expires.toUTCString() + ";";
  getMe();
}

export async function logout() {
  await fetch("/api/auth/logout/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + getCookie("token"),
    },
  });
  user.set(null);
}
