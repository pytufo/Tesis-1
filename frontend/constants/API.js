const API_BASE_URL = "http://localhost:8000/";

const API_ROUTES = {
  MATERIALES: "material/",  
  RESERVAR_MATERIAL: "material/{material_pk}/reservar/",
  EJEMPLARES: "ejemplar/",
  PRESTAMOS: "movimientos/prestamo/",
  RESERVAS: "movimientos/reservas/",
};

const AUTH_ROUTES = {
  USUARIOS: "auth/users/",
  DETALLE_USUARIO: "auth/users/{account_pk}/",
};

export { API_BASE_URL, API_ROUTES, AUTH_ROUTES };
