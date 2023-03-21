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

export default async function request(endpoint, method, body) {
  let res = await fetch(endpoint, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + getCookie("token"),
    },
    body: JSON.stringify(body),
  });
  return await res.json();
}

export async function get(endpoint) {
  return await request(endpoint, "GET");
}

export async function post(endpoint, body) {
  return await request(endpoint, "POST", body);
}

export async function put(endpoint, body) {
  return await request(endpoint, "PUT", body);
}

export async function del(endpoint) {
  return await request(endpoint, "DELETE");
}

export async function patch(endpoint, body) {
  return await request(endpoint, "PATCH", body);
}

export async function getMe() {
  return await get("/api/v1/users/me");
}
