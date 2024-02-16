import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  ScrollView,
  TouchableOpacity,
  TextInput,
  StyleSheet,
} from "react-native";
import { useNavigation } from "@react-navigation/native";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";

import { tableStyles } from "../../constants/Colors";

import { useUser } from "../../contexts/UserContext";
import MaterialServices from "../../services/MaterialServices";

const MaterialListScreen = ({ navigation }) => {
  const [material, setMaterial] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const { userInfo } = useUser();

  useEffect(() => {
    const fetchMaterial = async () => {
      try {
        const access_token = userInfo.access_token;
        const response = await MaterialServices.listarMateriales(
          access_token,
          searchQuery
        );
        setMaterial(response);
        console.log(response);
      } catch (error) {
        console.error("Error al obtener material", error);
      }
    };

    fetchMaterial();
  }, [userInfo.access_token, searchQuery]);


  const renderTableHeader = () => (
    <View style={tableStyles.tableHeader}>
      <Text style={tableStyles.headerText}>Titulo</Text>
      <Text style={tableStyles.headerText}>Autor</Text>
      <Text style={tableStyles.headerText}>Estado</Text>
    </View>
  );

  const renderItem = ({ item }) => (
    <TouchableOpacity onPress={() => handleMaterialPress(item.id)}>
      <View style={tableStyles.tableRow}>
        <Text style={tableStyles.cell}>{item.titulo}</Text>
        <Text style={tableStyles.cell}>{item.autor[0].nombre} {item.autor[0].apellido}</Text>
        <Text style={tableStyles.cell}>{item.estado}</Text>
      </View>
    </TouchableOpacity>
  );

  const handleMaterialPress = (materialId) => {
    navigation.navigate("DetalleMaterial", { materialId });
  };
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
        {renderTableHeader()}
        <FlatList
          data={material}
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
export default MaterialListScreen;
