import { API_BASE_URL, API_ROUTES } from "../constants/API";

const EjemplarServices = {
  listarEjemplares: async (accessToken, searchQuery) => {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.EJEMPLARES}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      });
      const data = await response.json();
      console.log(data);

      const buscarEjemplar = data.filter((ejemplar) =>
        ejemplar.material.titulo
          .toLowerCase()
          .includes(searchQuery.toLowerCase())
      );
      return buscarEjemplar;
    } catch (error) {
      console.error("Error al obtener los ejemplares");
      throw error;
    }
  },
  prestar: async (accessToken, ejemplarId, prestamoData) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ROUTES.EJEMPLARES}${ejemplarId}/prestar/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify(prestamoData),
        }
      );
      const data = await response.json();
      console.log(response);
      console.log(data);
      return data;
    } catch (error) {
      console.error("Error al reservar el material:", error);
      throw error;
    }
  },
};

export default EjemplarServices;
