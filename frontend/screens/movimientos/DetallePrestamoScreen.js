import { View, Text } from "react-native";
import React, { useEffect, useState } from "react";
import { useRoute } from "@react-navigation/native";
import { useUser } from "../../contexts/UserContext";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";
const DetallePrestamoScreen = () => {
  const route = useRoute();
  const [detallePrestamo, setDetallePrestamo] = useState(null);
  const { prestamoId } = route.params;

  const { userInfo } = useUser();
  const accessToken = userInfo.access_token;

  useEffect(() => {
    const fetchDetallePrestamo = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.PRESTAMOS}${prestamoId}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        setDetallePrestamo(response.data);
      } catch (error) {
        console.error("Error al obtener los datos del prestamo");
      }
    };
    fetchDetallePrestamo();
  }, [prestamoId, accessToken]);
  return (
    <View>
      {detallePrestamo ? (
        <View>
          <Text>Entregado por: {detallePrestamo
          .created_by}</Text>
          <Text>Usuario: {detallePrestamo.owner}</Text>
          <Text>Ejemplar: {detallePrestamo.ejemplar}</Text>
          <Text>Finalizacion: {detallePrestamo.fecha_fin}</Text>
        </View>
      ) : (
        <Text>Cargando prestamo...</Text>
      )}
    </View>
  );
};

export default DetallePrestamoScreen;
