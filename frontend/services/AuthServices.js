import { API_BASE_URL } from "../constants/API";

const AuthServices = {
  login: async (email, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}auth/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });
      const user = await response.json();
      return user;
    } catch (error) {
      console.error("Error al autenticar:", error);
      throw error;
    }
  },
  signup: async (email, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}auth/register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error al registra el usuario", error);
      throw error;
    }
  },
  logout: async (accessToken) => {
    try {
      const response = await fetch(`${API_BASE_URL}auth/logout/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ accessToken: accessToken }),
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error al cerrar sesion:", error);
      throw error;
    }
  },
};

export default AuthServices;
