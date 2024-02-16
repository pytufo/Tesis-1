import React, { useEffect, useState } from "react";
import { Text, View, Button } from "react-native";
import { useNavigation, useRoute } from "@react-navigation/native";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";
import { toast } from "react-toastify";

import { useUser } from "../../contexts/UserContext";

import AsyncStorage from "@react-native-async-storage/async-storage";
import MaterialServices from "../../services/MaterialServices";

const DetalleMaterialScreen = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { materialId } = route.params;
  const [detalleMaterial, setDetalleMaterial] = useState(null);

  const { userInfo } = useUser();

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

  const handleReservarMaterial = async () => {
    try {
      const access_token = userInfo.access_token;
      const response = await MaterialServices.reservar(
        access_token,
        materialId
      );
      
      if (response && response.message) {
        toast.error(response.message);
      } else {
        toast.success(response.message)
      }
    } catch (error) {
      console.error("Error al realizar la reserva del material", error);
    }
  };
  return (
    <View>
      {detalleMaterial ? (
        <View>
          <Text> Detalles del material:</Text>
          <Text> Titulo: {detalleMaterial.titulo} </Text>
          <Text>
            Editorial:
            {detalleMaterial.editorial.map((editorial) => (
              <Text key={editorial.id}>{editorial.nombre}</Text>
            ))}
          </Text>
          <Text>
            Autor:
            {detalleMaterial.autor.map((autor) => (
              <Text key={autor.id}>
                {autor.nombre}, {autor.apellido}.
              </Text>
            ))}
          </Text>
          <Text>
            carrera:
            {detalleMaterial.carrera.map((carrera) => (
              <Text key={carrera.id}>{carrera.nombre}</Text>
            ))}
          </Text>
          <Text>
            genero:
            {detalleMaterial.genero.map((genero) => (
              <Text key={genero.id}>{genero.nombre}</Text>
            ))}
          </Text>
          {detalleMaterial.estado === "Disponible" ? (
            <View>
              <Button title="Reservar" onPress={handleReservarMaterial} />
            </View>
          ) : (
            <Text>El material no se encuentra disponible...</Text>
          )}
        </View>
      ) : (
        <Text> Cargando detalles...</Text>
      )}
    </View>
  );
};

export default DetalleMaterialScreen;
