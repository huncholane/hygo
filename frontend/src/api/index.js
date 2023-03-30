import { writable } from "svelte/store";
import cookies from "./cookies";
import django from "./django";
import { user } from "./user";

export { django, user };

export async function request_json(endpoint, method, body) {
  if (!getToken()) {
    throw new Error("No token found");
  }
  let res = await fetch(endpoint, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + cookies.getCookie("token"),
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
      Authorization: "Bearer " + cookies.getCookie("token"),
    },
  });
  cookies.deleteCookie("token");
  user.set(null);
}
