import { View, Text } from "react-native";
import React, { useEffect, useState } from "react";
import { useRoute } from "@react-navigation/native";
import { useUser } from "../../contexts/UserContext";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";
import { Button } from "react-native";
import MovimientosServices from "../../services/MovimientosServices";
import { toast } from "react-toastify";
import moment from "moment";
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
          `${API_BASE_URL}${API_ROUTES.PRESTAMOS}${prestamoId}/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        setDetallePrestamo(response.data || {});
        console.log(response.data);
      } catch (error) {
        console.error("Error al obtener los datos del prestamo");
      }
    };
    fetchDetallePrestamo();
  }, [prestamoId, accessToken]);
  const handleFinalizarPrestamo = async () => {
    try {
      const access_token = userInfo.access_token;

      const response = await MovimientosServices.finalizarPrestamo(
        access_token,
        prestamoId
      );
      console.log(response);

      if (response.ok) {
        toast.info("Devolucion exitosa");
      } else {
        toast.error("Error al realizar la devolucion");
      }
    } catch (error) {
      toast.error("Error al finalizar el prestamo");
    }
  };
  return (
    <View>
      {detallePrestamo ? (
        <View>
          <Text> Entregado por: {detallePrestamo.created_by}</Text>
          <Text> Usuario: {detallePrestamo.owner?.email}</Text>
          <Text> Ejemplar: {detallePrestamo.ejemplar?.id} </Text>

          <Text> Material: </Text>
          <Text> {detallePrestamo.ejemplar?.material.titulo} </Text>
          <Text> Finalizacion: {moment(detallePrestamo.fecha_fin).format("YYYY-MM-DD HH:mm:ss")}</Text>
          {detallePrestamo.estado === "Finalizado" ? (
            <Text>Prestamo Finalizado</Text>
          ) : (
            <Button title="Finalizar" onPress={handleFinalizarPrestamo} />
          )}
        </View>
      ) : (
        <Text>Cargando prestamo...</Text>
      )}
    </View>
  );
};

export default DetallePrestamoScreen;
