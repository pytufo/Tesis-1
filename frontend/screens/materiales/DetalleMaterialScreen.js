import React, { useEffect, useState } from "react";
import { Text, View, Button, StyleSheet } from "react-native";
import { useNavigation, useRoute } from "@react-navigation/native";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";
import { toast } from "react-toastify";

import { useUser } from "../../contexts/UserContext";

import AsyncStorage from "@react-native-async-storage/async-storage";
import MaterialServices from "../../services/MaterialServices";

const DetalleMaterialScreen = (props) => {
  const { route } = props;
  const { materialId } = route.params;
  const { isLoggedIn } = props.isLoggedIn || false;
  const [detalleMaterial, setDetalleMaterial] = useState(null);
  const navigation = useNavigation();

  const { userInfo } = useUser();

  console.log(route.parms);
  useEffect(() => {
    const fetchDetalleMaterial = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.MATERIALES}${materialId}/`
        );
        setDetalleMaterial(response.data);
        console.log(response);
      } catch (error) {
        console.error("Error al obtener detales del material", error);
      }
    };
    fetchDetalleMaterial();
  }, [materialId]);

  const handleReservarMaterial = async () => {
    try {
      console.log(userInfo);
      if (!userInfo) {
        // Mostrar un mensaje y redireccionar al login
        toast.warning("Debes iniciar sesión para realizar una reserva.");
        navigation.navigate("Login"); // Asegúrate de que el nombre de la pantalla sea correcto
        return;
      }
      const access_token = userInfo.access_token;
      const owner_id = userInfo.id;

      const response = await MaterialServices.reservar(
        access_token,
        materialId,
        { id: owner_id }
      );

      toast.info(response.message);
    } catch (error) {
      console.error("Error al realizar la reserva del material", error);
    }
  };
  return (
    <View style={styles.container}>
      {detalleMaterial ? (
        <View style={styles.reservaContainer}>
          <Text>Titulo: {detalleMaterial.titulo} </Text>
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
            <View style={styles.entregarContainer}>
              <Button
                style={styles.button}
                title="Reservar"
                onPress={handleReservarMaterial}
              />
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

const styles = StyleSheet.create({
  container: {
    flex: 1,
    /* justifyContent: "center", */
    alignItems: "center",
    paddingHorizontal: 16,
  },
  reservaContainer: {
    width: "100%",
  },
  finalizadaText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "green",
    marginBottom: 10,
  },
  entregarContainer: {
    marginTop: 10,
  },
  label: {
    fontSize: 16,
    marginBottom: 5,
  },
  input: {
    height: 40,
    borderColor: "gray",
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
  },
  flatList: {
    marginBottom: 10,
  },
  ejemplarText: {
    fontSize: 16,
  },
  button: {
    marginTop: 10,
  },
  loadingText: {
    fontSize: 18,
    fontStyle: "italic",
  },
});
export default DetalleMaterialScreen;
