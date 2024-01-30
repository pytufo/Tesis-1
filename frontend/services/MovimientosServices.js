import { API_BASE_URL, API_ROUTES } from "../constants/API";

const MovimientosServices = {
  listarReservas: async (accessToken) => {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.RESERVAS}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      });
      const data = await response.json();
      console.log(data);
      return data;
    } catch (error) {
      console.error("Error al obtener las reservas");
      throw error;
    }
  },
  entregarEjemplarReserva: async (accessToken, reservaId) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ROUTES.RESERVAS}${reservaId}/entregar_ejemplar/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify({ reservaId: reservaId }),
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
};

export default MovimientosServices;
