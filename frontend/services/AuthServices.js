import { API_BASE_URL, AUTH_ROUTES } from "../constants/API";

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
  signup: async (email, password, first_name, last_name) => {
    try {
      const response = await fetch(`${API_BASE_URL}auth/register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password, first_name, last_name }),
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
  listarUsuarios: async (accessToken, searchQuery) => {
    try {
      const response = await fetch(`${API_BASE_URL}${AUTH_ROUTES.USUARIOS}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      });

      const data = await response.json();

      const buscarUsuario = data.filter((user) =>
        user.email.toLowerCase().includes(searchQuery.toLowerCase())
      );
      return buscarUsuario;

      /* console.log(data);
      return data; */
    } catch (error) {
      console.error("Error al obtener los usuarios");
      throw error;
    }
  },
  listarUsuariosNoAdmin: async (accessToken, searchQuery) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}${AUTH_ROUTES.USUARIOS_NOADMIN}?search=${searchQuery}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      const data = await response.json();

      const buscarUsuario = data.filter((user) =>
        user.email.toLowerCase().includes(searchQuery.toLowerCase())
      );
      return buscarUsuario;

      /* console.log(data);
      return data; */
    } catch (error) {
      console.error("Error al obtener los usuarios");
      throw error;
    }
  },
};

export default AuthServices;
