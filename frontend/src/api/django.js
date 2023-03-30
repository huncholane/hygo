import { CookieHandler } from "./cookies";
import { user } from "./user";

class DjangoHandler extends CookieHandler {
  getCSRFToken() {
    const csrfToken = this.getCookie("csrftoken");
    return csrfToken;
  }

  getHeaders() {
    const csrfToken = this.getCSRFToken();
    console.log(csrfToken);
    return {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    };
  }

  async request(url, method, body) {
    const headers = this.getHeaders();
    const response = await fetch(url, {
      method: method,
      headers: headers,
      body: JSON.stringify(body),
    });
    try {
      return await response.json();
    } catch {
      return response;
    }
  }

  async get(url) {
    const response = await this.request(url, "GET");
    return response;
  }

  async post(url, body) {
    const response = await this.request(url, "POST", body);
    return response;
  }

  async put(url, body) {
    const response = await this.request(url, "PUT", body);
    return response;
  }

  async delete(url) {
    const response = await this.request(url, "DELETE");
    return response;
  }

  async patch(url, body) {
    const response = await this.request(url, "PATCH", body);
    return response;
  }

  async login(username, password) {
    const url = "/api/auth/login/";
    await this.get(url);
    let response = await this.get(url);
    response = await this.post(url, { username, password });
    const userVal = await this.get("/api/user/me/");
    console.log(userVal);
    user.set(userVal);
  }

  async logout() {
    const url = "/api/auth/logout/";
    console.log("logging out");
    const response = await this.post(url, {});
    user.set(null);
  }
}

export default new DjangoHandler();
