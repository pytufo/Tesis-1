import React, { useEffect, useState } from "react";
import { useFocusEffect } from "@react-navigation/native";
import {
  Text,
  View,
  FlatList,
  ScrollView,
  TouchableOpacity,
  TextInput,
  StyleSheet,
} from "react-native";
import { tableStyles } from "../../constants/Colors";
import moment from "moment";

import { useNavigation } from "@react-navigation/native";
import axios from "axios";

import MovimientosServices from "../../services/MovimientosServices";
import { useUser } from "../../contexts/UserContext";

const ReservasScreen = ({ navigation }) => {
  const [reserva, setReserva] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const { userInfo } = useUser();
  const [refreshing, setRefreshing] = useState(false);

  const fetchReserva = async () => {
    try {
      const access_token = userInfo.access_token;
      if (userInfo && userInfo.user.role === 1) {
        const response = await MovimientosServices.listarReservas(
          access_token,
          searchQuery
        );
        setReserva(response);
        console.log(response);
      } else {
        const response = await MovimientosServices.reservasUsuario(
          access_token,
          searchQuery
        );
        setReserva(response);
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
      fetchReserva();
    }, [userInfo, searchQuery])
  );

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
        <Text style={tableStyles.cell}>{item.material.titulo}</Text>
        <Text style={tableStyles.cell}>{item.owner.email}</Text>
        {item.estado === "Finalizada" ? (
          <Text style={tableStyles.cell}> Finalizada </Text>
        ) : item.fecha_fin === null ? (
          <Text style={tableStyles.cell}>Pendiente: {item.estado}</Text>
        ) : (
          <Text style={tableStyles.cell}>
            Pendiente: {moment(item.fecha_fin).format("YYYY-MM-DD HH:mm:ss")}
          </Text>
        )}
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={{ padding: 10 }}>
        <TextInput
          style={styles.searchInput}
          placeholder="Buscar material..."
          value={searchQuery}
          onChangeText={(text) => setSearchQuery(text)}
        />
      </View>
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
    </View>
  );
};
const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  searchBar: {
    padding: 10,
    backgroundColor: "#fff",
    borderBottomWidth: 1,
    borderBottomColor: "#ddd",
  },
  searchInput: {
    height: 40,
    borderColor: "gray",
    borderWidth: 1,
    padding: 10,
  },
});
export default ReservasScreen;
