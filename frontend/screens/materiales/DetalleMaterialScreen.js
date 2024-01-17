import React, { useEffect, useState } from "react";
import { Text, View, FlatList, TouchableOpacity } from "react-native";
import { useNavigation, useRoute } from "@react-navigation/native";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";

const DetalleMaterialScreen = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { materialId } = route.params;
  const [detalleMaterial, setDetalleMaterial] = useState(null);

  useEffect(() => {
    const fetchDetalleMaterial = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.MATERIALES}${materialId}/`
        );
        setDetalleMaterial(response.data);
      } catch (error) {
        console.error("Error al obtener detales del material", error);
      }
    };
    fetchDetalleMaterial();
  }, [materialId]);
  return (
    <View>
      {detalleMaterial ? (
        <View>
          <Text> Detalles del material:</Text>
          <Text> Titulo: {detalleMaterial.titulo} </Text>
          <Text> Autor: {detalleMaterial.autor} </Text>
          <Text> Genero: {detalleMaterial.genero} </Text>
          <Text> estado: {detalleMaterial.estado} </Text>
        </View>
      ) : (
        <Text> Cargando detalles...</Text>
      )}
    </View>
  );
};

export default DetalleMaterialScreen;
