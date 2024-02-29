import {
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  FlatList,
} from "react-native";
import React, { useEffect, useState } from "react";
import { tableStyles } from "../../constants/Colors";
import { useFocusEffect } from "@react-navigation/native";

import { API_BASE_URL, API_ROUTES } from "../../constants/API";
import axios from "axios";

import moment from "moment";
import MovimientosServices from "../../services/MovimientosServices";
import { useUser } from "../../contexts/UserContext";

const PrestamosScreen = ({ navigation }) => {
  const [prestamo, setPrestamo] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const { userInfo } = useUser();
  const [refreshing, setRefreshing] = useState(false);

  const fetchPrestamo = async () => {
    try {
      const access_token = userInfo.access_token;
      if (userInfo && userInfo.user.role === 1) {
        const response = await MovimientosServices.listarPrestamos(
          access_token,
          searchQuery
        );
        setPrestamo(response);
        console.log(response);
      } else {
        const response = await MovimientosServices.prestamosUsuario(
          access_token,
          searchQuery
        );
        setPrestamo(response);
        console.log(response);
      }
    } catch (error) {
      console.log("Error al obtener las reservas:", error);
    } finally {
      setRefreshing(false);
    }
  };

  useFocusEffect(
    React.useCallback(() => {
      fetchPrestamo();
    }, [userInfo, searchQuery])
  );

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
        <Text style={tableStyles.cell}>{item.ejemplar?.material?.titulo}</Text>
        <Text style={tableStyles.cell}>{item.owner.email}</Text>
        {item.estado === "Finalizado" ? (
          <Text style={tableStyles.cell}>Finalizado</Text>
        ) : (
          <Text style={tableStyles.cell}>
            {moment(item.fecha_fin).format("YYYY-MM-DD HH:mm:ss")}
          </Text>
        )}
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
