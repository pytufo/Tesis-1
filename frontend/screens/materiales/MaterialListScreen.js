import React, { useEffect, useState } from "react";
import { Text, View, FlatList, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";

const MaterialListScreen = () => {
  const navigation = useNavigation();
  const [material, setMaterial] = useState([]);

  useEffect(() => {
    const fetchMaterial = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.MATERIALES}`
        );
        setMaterial(response.data);
      } catch (error) {
        console.error("Error al obtener material", error);
      }
    };

    fetchMaterial();
  }, []);

  const handleMaterialPress = (materialId) => {
    navigation.navigate("DetalleMaterialScreen", { materialId });
  };
  return (
    <View>
      <Text>Listado de Materiales:</Text>
      <FlatList
        data={material}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity onPress={() => handleMaterialPress(item.id)}>
            <View>
              <Text>{item.titulo}</Text>
              {/* Mostrar más detalles del material según sea necesario */}
            </View>
          </TouchableOpacity>
        )}
      />
    </View>
  );
};

export default MaterialListScreen;
