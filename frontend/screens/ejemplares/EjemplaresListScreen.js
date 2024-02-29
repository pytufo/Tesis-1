import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  ScrollView,
  TouchableOpacity,
  TextInput,
  StyleSheet,
  Button,
} from "react-native";
import { useNavigation } from "@react-navigation/native";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";

import { tableStyles } from "../../constants/Colors";

import { useUser } from "../../contexts/UserContext";
import EjemplarServices from "../../services/EjemplarServices";

const EjemplarListScreen = ({ navigation }) => {
  const [ejemplar, setEjemplar] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const { userInfo } = useUser();

  useEffect(() => {
    const fetchEjemplar = async () => {
      try {
        const access_token = userInfo.access_token;
        const response = await EjemplarServices.listarEjemplares(
          access_token,
          searchQuery
        );
        setEjemplar(response);
        console.log(response);
      } catch (error) {
        console.error("Error al obtener Ejemplar", error);
      }
    };

    fetchEjemplar();
  }, [userInfo.access_token, searchQuery]);

  const renderTableHeader = () => (
    <View style={tableStyles.tableHeader}>
      <Text style={tableStyles.headerText}>Id</Text>
      <Text style={tableStyles.headerText}>Titulo</Text>      
      <Text style={tableStyles.headerText}>Estado</Text>
    </View>
  );

  const renderItem = ({ item }) => (
    <TouchableOpacity onPress={() => handleEjemplarPress(item.id)}>
      <View style={tableStyles.tableRow}>
        <Text style={tableStyles.cell}>{item.id}</Text>
        <Text style={tableStyles.cell}>{item.material.titulo}</Text>        
        <Text style={tableStyles.cell}>{item.estado}</Text>
      </View>
    </TouchableOpacity>
  );

  const handleEjemplarPress = (ejemplarId) => {
    navigation.navigate("DetalleEjemplar", { ejemplarId });
  };
  return (
    <View style={styles.container}>
      <Button>asfd</Button>
      <View style={{ padding: 10 }}>
        <TextInput
          style={styles.searchInput}
          placeholder="Buscar Ejemplar..."
          value={searchQuery}
          onChangeText={(text) => setSearchQuery(text)}
        />
      </View>
      <ScrollView>
        {renderTableHeader()}
        <FlatList
          data={ejemplar}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderItem}
        />
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
export default EjemplarListScreen;
