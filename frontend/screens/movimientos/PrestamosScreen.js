import { View, Text, TouchableOpacity, FlatList } from "react-native";
import React, { useEffect, useState } from "react";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";
import axios from "axios";

const PrestamosScreen = ({ navigation }) => {
  const [prestamo, setPrestamo] = useState([]);

  useEffect(() => {
    const fetchPrestamo = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.PRESTAMOS}`
        );
        console.log(response);
        setPrestamo(response.data);
      } catch (error) {
        console.log("Error al obtener los prestamos:", error);
      }
    };
    fetchPrestamo();
  }, []);
  const handlePrestamoPress = (prestamoId) => {
    navigation.navigate("DetallePrestamo", { prestamoId });
  };
  return (
    <View>
      <Text>Listado de Prestamos:</Text>
      <FlatList
        data={prestamo}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity onPress={() => handlePrestamoPress(item.id)}>
            <View>
              <Text>Ejemplar: {item.ejemplar}</Text>
              <Text>Usuario: {item.owner}</Text>
              <Text>Fecha finalizacion: {item.fecha_fin}</Text>
            </View>
          </TouchableOpacity>
        )}
      />
    </View>
  );
};

export default PrestamosScreen;
