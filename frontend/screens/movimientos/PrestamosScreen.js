import {
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  FlatList,
} from "react-native";
import React, { useEffect, useState } from "react";
import { tableStyles } from "../../constants/Colors";

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

  const renderTableHeader = () => (
    <View style={tableStyles.tableHeader}>
      <Text style={tableStyles.headerText}>ID_Ejemplar</Text>
      <Text style={tableStyles.headerText}>Material</Text>
      <Text style={tableStyles.headerText}>Usuario</Text>
      <Text style={tableStyles.headerText}>Fecha finalizacion</Text>
    </View>
  );

  const renderItem = ({ item }) => (
    <TouchableOpacity onPress={() => handlePrestamoPress(item.id)}>
      <View style={tableStyles.tableRow}>
      <Text style={tableStyles.cell}>{item.id}</Text>
        <Text style={tableStyles.cell}>{item.ejemplar.material.titulo}</Text>
        <Text style={tableStyles.cell}>{item.owner.email}</Text>
        <Text style={tableStyles.cell}>{item.fecha_fin}</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <ScrollView>
      <View>
        {renderTableHeader()}
        <FlatList
          data={prestamo}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderItem}
        />
      </View>
    </ScrollView>
  );
};

export default PrestamosScreen;
