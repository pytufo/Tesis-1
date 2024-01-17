const API_BASE_URL = "http://localhost:8000/";

const API_ROUTES = {
  MATERIALES: "material/",
  DETALLE_MATERIAL: "material/{material_pk/",
  RESERVAR_MATERIAL: "material/{material_pk}/reservar/",
  EJEMPLARES: "ejemplar/",
  PRESTAMOS: "movimientos/prestamo/",
  RESERVAS: "movimientos/reserva/",
};

export { API_BASE_URL, API_ROUTES };
