import React, { useEffect, useState } from "react";
import { Text, View, FlatList, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";
import MovimientosServices from "../../services/MovimientosServices";
import { useUser } from "../../contexts/UserContext";

const ReservasScreen = ({ navigation }) => {
  const [reserva, setReserva] = useState([]);
  const { userInfo } = useUser();
  useEffect(() => {
    const fetchReserva = async () => {
      try {
        const access_token = userInfo.access_token;
        const response = await MovimientosServices.listarReservas(access_token);        
        setReserva(response);
      } catch (error) {
        console.log("Error al obtener las reservas:", error);
      }
    };
    fetchReserva();
  }, [userInfo.access_token]);
  const handleReservaPress = (reservaId) => {
    navigation.navigate("DetalleReserva", { reservaId });
  };
  return (
    <View>
      <Text>Listado de Reservas:</Text>
      <FlatList
        data={reserva}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity onPress={() => handleReservaPress(item.id)}>
            <View>
              <Text>Material: {item.material}</Text>
              <Text>Usuario: {item.owner}</Text>
              <Text>Fecha finalizacion: {item.fecha_fin}</Text>
            </View>
          </TouchableOpacity>
        )}
      />
    </View>
  );
};

export default ReservasScreen;
