import React, { useEffect, useState } from "react";
import { Text, View, FlatList, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";

const ReservasScreen = ({ navigation }) => {
  const [reserva, setReserva] = useState([]);

  useEffect(() => {
    const fetchReserva = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.RESERVAS}`
        );
        console.log(response);
        setReserva(response.data);
      } catch (error) {
        console.log("Error al obtener los prestamos:", error);
      }
    };
    fetchReserva();
  }, []);
  const handleReservaPress = (prestamoId) => {
    navigation.navigate("DetallePrestamo", { prestamoId });
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
