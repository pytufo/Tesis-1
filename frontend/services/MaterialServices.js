import { API_BASE_URL, API_ROUTES } from "../constants/API";

const MaterialServices = {
  reservar: async (accessToken, materialId) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ROUTES.MATERIALES}${materialId}/reservar/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify({ accessToken: accessToken }),
        }
      );
      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error al reservar el material:", error);
      throw error;
    }
  },
};

export default MaterialServices;
