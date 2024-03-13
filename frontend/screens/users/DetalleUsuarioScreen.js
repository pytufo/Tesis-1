import React, { useEffect, useState } from "react";
import { toast } from "react-toastify";
import {
  View,
  Text,
  Button,
  TextInput,
  StyleSheet,
  FlatList,
} from "react-native";
import { useNavigation, useRoute } from "@react-navigation/native";

import axios from "axios";

import { API_BASE_URL, AUTH_ROUTES } from "../../constants/API";
import { useUser } from "../../contexts/UserContext";

const DetalleUsuarioScreen = () => {
  const route = useRoute();
  const { userId } = route.params;
  const [detalleUsuario, setDetalleUsuario] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredRoles, setFilteredRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState(null);

  const { userInfo } = useUser();
  const accessToken = userInfo.access_token;
  const navigation = useNavigation();

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
  React.useEffect(() => {
    navigation.setOptions({
      title: "Detalles del usuario",
    });
  }, [userInfo]);
  const handleActivarCuenta = async () => {
    if (!selectedRole) {
      toast.error("Por favor seleccione un rol.");
      return;
    }
    try {
      await axios.put(
        `${API_BASE_URL}${AUTH_ROUTES.USUARIOS}${userId}/activar/`,
        { role: selectedRole },
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
      toast.success("La cuenta ha sido activada exitosamente");
    } catch (error) {
      console.error("Error al activar la cuenta", error);
    }
  };

  const ROLES = [
    { label: "Administrador", value: 1 },
    { label: "Bibliotecario", value: 2 },
    { label: "Profesor", value: 3 },
    { label: "Tesorero", value: 4 },
    { label: "Alumno", value: 5 },
    { label: "Invitado", value: 6 },
  ];
  const filterRoles = () => {
    if (!searchTerm) {
      setFilteredRoles([]);
      return;
    }
    const filtered = ROLES.filter((role) =>
      role.label.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredRoles(filtered);
  };

  const selectRole = (role) => {
    setSelectedRole(role.value);
    setFilteredRoles([]);
  };

  return (
    <View>
      {detalleUsuario ? (
        <View style={styles.container}>
          <Text> Nombre: {detalleUsuario.username}</Text>
          <Text> Apellido: {detalleUsuario.last_name}</Text>
          <Text> E-Mail: {detalleUsuario.email}</Text>
          <Text> Rol: {detalleUsuario.role}</Text>
          {detalleUsuario.is_active ? (
            <Text> Cuenta activada</Text>
          ) : (
            <View>
              <Text> Cuenta pendiente de activacion por el administrador</Text>
              <View style={styles.searchContainer}>
                <TextInput
                  style={styles.input}
                  placeholder="Buscar Rol"
                  value={searchTerm}
                  onChangeText={(text) => setSearchTerm(text)}
                  onBlur={filterRoles}
                />
                <FlatList
                  data={filteredRoles}
                  renderItem={({ item }) => (
                    <Text
                      style={styles.roleItem}
                      onPress={() => selectRole(item)}
                    >
                      {item.label}
                    </Text>
                  )}
                  keyExtractor={(item) => item.value.toString()}
                />
              </View>
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

const styles = {
  container: {
    flex: 1,
    /* justifyContent: "center", */
    paddingTop: 20,
    paddingHorizontal: 16,
  },
};
export default DetalleUsuarioScreen;
