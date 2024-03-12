import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  ScrollView,
  TouchableOpacity,
  TextInput,
  StyleSheet,
  Modal,
} from "react-native";

import {
  Button,
  Dialog,
  PaperProvider,
  Paragraph,
  Portal,
} from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import { MaterialesStackNavigator } from "../../AppTabsScreens";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";

import { tableStyles } from "../../constants/Colors";

import MaterialServices from "../../services/MaterialServices";
import { useUser } from "../../contexts/UserContext";

const MaterialListScreen = () => {
  const [material, setMaterial] = useState([]);
  const [isMaterialModalVisible, setIsMaterialModalVisible] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  const navigation = useNavigation();
  const { userInfo } = useUser();

  useEffect(() => {
    const fetchMaterial = async () => {
      try {
        const response = await MaterialServices.listarMateriales(searchQuery);
        setMaterial(response);
        console.log(response);
      } catch (error) {
        console.error("Error al obtener material", error);
      }
    };

    fetchMaterial();
  }, [searchQuery]);

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
        <Text style={tableStyles.cell}>
          {item.autor[0].nombre} {item.autor[0].apellido}
        </Text>
        <Text style={tableStyles.cell}>{item.estado}</Text>
      </View>
    </TouchableOpacity>
  );

  const handleMaterialPress = (materialId) => {
    navigation.navigate("DetalleMaterial", { materialId });
  };
  return (
    <View style={styles.container}>
      {userInfo && userInfo.user.role === 1 && (
        <View style={styles.buttonContainer}>
          <Button
            style={[styles.button, { marginRight: 10 }]}
            onPress={() =>
              navigation.navigate("NuevoMaterial", { isEditar: false })
            }
          >
            <Text style={[styles.buttonText, { color: "#FFFFFF" }]}>
              Nuevo material
            </Text>
          </Button>
          <Button style={styles.button}>
            <Text style={[styles.buttonText, { color: "#FFFFFF" }]}>
              Nuevo ejemplar
            </Text>
          </Button>
        </View>
      )}

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
  buttonContainer: {
    flexDirection: "row",
    marginBottom: 10,
  },
  button: {
    backgroundColor: "#2471A3",
    marginTop: 10,
    paddingHorizontal: 12,
    borderRadius: 4,
  },
});
export default MaterialListScreen;
