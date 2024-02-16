import { View, Text, Button } from "react-native";
import React, { useEffect, useState } from "react";
import { useRoute } from "@react-navigation/native";
import { toast } from "react-toastify";


import axios from "axios";

import { API_BASE_URL, AUTH_ROUTES } from "../../constants/API";
import { useUser } from "../../contexts/UserContext";

const DetalleUsuarioScreen = () => {
  const route = useRoute();
  const { userId } = route.params;
  const [detalleUsuario, setDetalleUsuario] = useState(null);

  const {userInfo} = useUser()
  const accessToken = userInfo.access_token;

  useEffect(() => {
    const fethDetalleUsuario = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${AUTH_ROUTES.USUARIOS}${userId}/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        console.log("usuario:", response);
        setDetalleUsuario(response.data);
      } catch (error) {
        console.error("Error al obtener los datos del usuario.", error);
      }
    };
    fethDetalleUsuario();
  }, [userId]);

  const handleActivarCuenta = async () => {
    try {
      await axios.put(
        `${API_BASE_URL}${AUTH_ROUTES.USUARIOS}${userId}/activar/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      setDetalleUsuario((prevUsuario) => ({
        ...prevUsuario,
        is_active: true,
      }));
      toast.success("El la cuenta ha sido activada exitosamente");
    } catch (error) {
      console.error("Error al activar la cuenta", error);
    }
  };

  return (
    <View>
      {detalleUsuario ? (
        <View>
          <Text>Detalles del usuario </Text>
          <Text> Nombre: {detalleUsuario.username}</Text>
          <Text> Apellido: {detalleUsuario.last_name}</Text>
          <Text> E-Moil: {detalleUsuario.email}</Text>
          <Text> role: {detalleUsuario.role}</Text>
          {detalleUsuario.is_active ? (
            <Text> Cuenta activada</Text>
          ) : (
            <View>
              <Text> Cuenta pendiente de activacion por el administrador</Text>
              <Button title="Activar Cuenta" onPress={handleActivarCuenta} />
            </View>
          )}
        </View>
      ) : (
        <Text>DetalleUsuarioScreen</Text>
      )}
    </View>
  );
};

export default DetalleUsuarioScreen;
