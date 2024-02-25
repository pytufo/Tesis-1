import { API_BASE_URL, API_ROUTES } from "../constants/API";

const MovimientosServices = {
  listarReservas: async (accessToken, searchQuery) => {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.RESERVAS}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!response.ok) {
        throw new Error(
          `Error al obtener las reservas: ${response.statusText}`
        );
      }
      const data = await response.json();

      const buscarReserva = data.filter(
        (reserva) =>
          reserva.material &&
          reserva.material.titulo
            .toLowerCase()
            .includes(searchQuery.toLowerCase())
      );
      console.log(buscarReserva);
      console.log(data);
      return buscarReserva;
    } catch (error) {
      console.error("Error al obtener las reservas");
      throw error;
    }
  },
  entregarEjemplarReserva: async (accessToken, reservaId, prestamoData) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ROUTES.RESERVAS}${reservaId}/entregar_ejemplar/`,
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
      console.log(data);
      return data;
    } catch (error) {
      console.error("Error al entregar el ejemplar de la reserva");
      throw error;
    }
  },
  finalizarPrestamo: async (accessToken, prestamoId) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ROUTES.PRESTAMOS}${prestamoId}/devolucion/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      const data = await response.json();
      console.log(data);
      return data, response;
    } catch (error) {
      console.error("Error al entregar el ejemplar de la reserva");
      throw error;
    }
  },
};

export default MovimientosServices;
