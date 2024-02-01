import React, { useEffect, useState } from "react";
import {
  Text,
  View,
  FlatList,
  ScrollView,
  TouchableOpacity,
} from "react-native";
import { tableStyles } from "../../constants/Colors";

import { useNavigation } from "@react-navigation/native";
import axios from "axios";

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

  const renderTableHeader = () => (
    <View style={tableStyles.tableHeader}>
      <Text style={tableStyles.headerText}>Material</Text>
      <Text style={tableStyles.headerText}>Usuario</Text>
      <Text style={tableStyles.headerText}>Fecha finalizacion</Text>
    </View>
  );

  const renderItem = ({ item }) => (
    <TouchableOpacity onPress={() => handleReservaPress(item.id)}>
      <View style={tableStyles.tableRow}>
        <Text style={tableStyles.cell}>{item.material}</Text>
        <Text style={tableStyles.cell}>{item.owner}</Text>
        <Text style={tableStyles.cell}>{item.fecha_fin}</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <ScrollView>
      <View>
        {renderTableHeader()}
        <FlatList
          data={reserva}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderItem}
        />
      </View>
    </ScrollView>
  );
};

export default ReservasScreen;
