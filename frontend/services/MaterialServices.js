import { API_BASE_URL, API_ROUTES } from "../constants/API";

const MaterialServices = {
  listarMateriales: async (searchQuery) => {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.MATERIALES}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
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
  crearMaterial: async (accessToken, nuevoMaterial) => {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.MATERIALES}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(nuevoMaterial),
      });
      const data = await response.json();
      console.log(response);
      console.log(data);
      return data;
    } catch (error) {
      console.error("Error al crear el material:", error);
      throw error;
    }
  },
  DetaleMateriales: async (searchQuery) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ROUTES.MATERIALES}${materialId}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
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

  // Listar los campos del material (genero, autor, etc....)
  listarTipoMaterial: async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}tipo/`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error("Error al obtener los materiales");
      throw error;
    }
  },
  listarEditoriales: async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}editorial/`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error("Error al obtener los materiales");
      throw error;
    }
  },
  listarAutores: async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}autor/`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error("Error al obtener los materiales");
      throw error;
    }
  },
  listarCarreras: async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}carrera/`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error("Error al obtener los materiales");
      throw error;
    }
  },listarGeneros: async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}genero/`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error("Error al obtener los materiales");
      throw error;
    }
  },
  
};

export default MaterialServices;
