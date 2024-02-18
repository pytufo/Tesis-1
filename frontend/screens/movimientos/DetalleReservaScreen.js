import { View, Text, Picker, Button } from "react-native";
import React, { useEffect, useState } from "react";
import { useRoute } from "@react-navigation/native";
import { useUser } from "../../contexts/UserContext";
import MovimientosServices from "../../services/MovimientosServices";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";
import axios from "axios";
import { toast } from "react-toastify";

const DetalleReservaScreen = () => {
  const route = useRoute();
  const [detalleReserva, setDetalleReserva] = useState({});
  const [ejemplaresDisponibles, setEjemplaresDisponibles] = useState([]);
  const [selectedEjemplar, setSelectedEjemplar] = useState();
  const { reservaId } = route.params;

  const { userInfo } = useUser();
  const accessToken = userInfo.access_token;
  useEffect(() => {
    const fetchDetalleReserva = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.RESERVAS}${reservaId}/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        setDetalleReserva(response.data || {});        
        console.log(response.data);
      } catch (error) {
        console.error("Error al obtener los datos de la reserva");
      }
    };

    const fetchEjemplaresDisponibles = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.RESERVAS}${reservaId}/entregar_ejemplar/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );        
        setEjemplaresDisponibles(response.data.ejemplares_disponibles);
        console.log(response.data);
      } catch (error) {
        console.error("Error al obtener los ejemplares disponibles");
      }
    };
    fetchEjemplaresDisponibles();
    fetchDetalleReserva();
  }, [reservaId, accessToken]);

  const handleEntregarEjemplar = async () => {
    try {      
      const access_token = userInfo.access_token;
      
      if (!selectedEjemplar) {
        console.error("Seleccciona un ejemplar a entregar");
        return;
      }

      const owner_id = detalleReserva.owner.id;

      const prestamoData = {
        created_by: userInfo.user.id,
        owner: owner_id,
        ejemplar: selectedEjemplar,
      };
      const response = await MovimientosServices.entregarEjemplarReserva(
        access_token,
        reservaId,
        prestamoData
      );
      toast.success("El prestamo ha sido creado exitosamente");
      console.log(response);
      console.log(prestamoData);
    } catch (error) {
      console.error("Error al entregar el ejemplar");
    }
  };

  return (
    <View>
      {detalleReserva ? (
        <View>
          <Text>Detalles de la reserva</Text>
          <Text>Solicitante:{detalleReserva.owner?.email}</Text>
          <Text>Material: {detalleReserva.material?.titulo}</Text>
          <Text>Finalizacion: {detalleReserva.fecha_fin}</Text>

          <Text>Selecciona un ejemplar: </Text>
          <Picker
            selectedValue={(selectedEjemplar)}
            onValueChange={(itemValue) => setSelectedEjemplar(Number(itemValue))}
          >
            {ejemplaresDisponibles.map((ejemplar, index) => (
              <Picker.Item
                key={index}
                label={`ID: ${ejemplar.id}, Estado: ${ejemplar.estado}`}
                value={ejemplar.id}
              />
            ))}
          </Picker>

          <Button title="Entregar ejemplar" onPress={handleEntregarEjemplar} />
        </View>
      ) : (
        <Text>Cargando reserva...</Text>
      )}
    </View>
  );
};

export default DetalleReservaScreen;
