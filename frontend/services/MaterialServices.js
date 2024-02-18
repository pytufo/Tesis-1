import { API_BASE_URL, API_ROUTES } from "../constants/API";

const MaterialServices = {
  listarMateriales: async (accessToken, searchQuery) => {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.MATERIALES}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      });
      const data = await response.json();

      const buscarMaterial = data.filter((material) =>
        material.titulo.toLowerCase().includes(searchQuery.toLowerCase())
      );
      return buscarMaterial;

      /* console.log(data);
      return data; */
    } catch (error) {
      console.error("Error al obtener los materiales");
      throw error;
    }
  },
  reservar: async (accessToken, materialId, userId) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ROUTES.MATERIALES}${materialId}/reservar/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify({
            material: { id: materialId },
            owner: { id: userId },
          }),
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

export default MaterialServices;
