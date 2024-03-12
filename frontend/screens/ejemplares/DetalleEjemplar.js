import React, { useEffect, useState } from "react";
import {
  Text,
  View,
  FlatList,
  TouchableOpacity,
  Keyboard,
  StyleSheet,
} from "react-native";
import {
  Button,
  Dialog,
  PaperProvider,
  Paragraph,
  Portal,
  TextInput,
  Snackbar,
} from "react-native-paper";
import { useNavigation, useRoute } from "@react-navigation/native";
import axios from "axios";
import { API_BASE_URL, API_ROUTES } from "../../constants/API";
import { toast } from "react-toastify";

import { useUser } from "../../contexts/UserContext";

import AsyncStorage from "@react-native-async-storage/async-storage";
import EjemplarServices from "../../services/EjemplarServices";
import AuthServices from "../../services/AuthServices";

const DetalleEjemplarScreen = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { ejemplarId } = route.params;
  const [detalleEjemplar, setDetalleEjemplar] = useState({});
  const [selectedUser, setSelectedUser] = useState(null);
  const [users, setUsers] = useState([]);

  const [dialogVisible, setDialogVisible] = useState(false);

  const [snackbarVisible, setSnackbarVisible] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [searchText, setSearchText] = useState("");
  const [filteredUsers, setFilteredUsers] = useState([]);

  const { userInfo } = useUser();
  const accessToken = userInfo.access_token;

  useEffect(() => {
    const fetchDetalleEjemplar = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${API_ROUTES.EJEMPLARES}${ejemplarId}/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        setDetalleEjemplar(response.data);
        console.log(response);
      } catch (error) {
        console.error("Error al obtener detales del ejemplar", error);
      }
    };

    const fetchUsers = async () => {
      try {
        const usersResponse = await AuthServices.listarUsuariosNoAdmin(
          accessToken,
          ""
        );
        console.log(usersResponse);
        setUsers(usersResponse);
      } catch (error) {
        console.error("Error al obtener la lista de usuarios", error);
      }
    };
    fetchUsers();
    fetchDetalleEjemplar();
  }, [ejemplarId, accessToken]);
  const handleConfirmar = async () => {
    setDialogVisible(true);
  };
  const handleCancel = () => {
    // Cerrar el diálogo de confirmación
    setDialogVisible(false);
  };
  const handlePrestarEjemplar = async () => {
    try {
      const access_token = userInfo.access_token;
      const owner_id = selectedUser;

      if (!selectedUser) {
        setSnackbarMessage("Selecciona un usuario para el prestamo");
        setSnackbarVisible(true);
        return;
      }
      const prestamoData = {
        created_by: userInfo.user.id,
        owner: owner_id,
        ejemplar: ejemplarId,
      };
      const response = await EjemplarServices.prestar(
        access_token,
        ejemplarId,
        prestamoData
      );
      if (response) {
        setSnackbarMessage(response.message);
        setSnackbarVisible(true);
        
      } else {
        setSnackbarMessage(response.message);
      }
    } catch (error) {
      console.error("Error al realizar el prestamo del ejemplar", error);
    }
  };

  const handleSearchChange = (text) => {
    setSearchText(text);
    const filtered = users.filter((user) =>
      user.email.toLowerCase().includes(text.toLowerCase())
    );
    setFilteredUsers(filtered);
  };
  const handleUserSelect = (userId) => {
    setSelectedUser(userId);
    const selectedUser = users.find((user) => user.id === userId);
    setSearchText(selectedUser?.email.toLowerCase() || "");
  };
  const handleKeyboardDismiss = () => {
    Keyboard.dismiss();
  };

  const handleKeyPress = ({ nativeEvent }) => {
    const { key } = nativeEvent;
    if (key === "ArrowDown" || key == "ArrowUp") {
      const currentIndex = filteredUsers.findIndex(
        (user) => user.id === selectedUser?.id
      );
      const newIndex =
        key === "ArrowDown"
          ? (currentIndex + 1) % filteredUsers.length
          : (currentIndex - 1 + filteredUsers.length) % filteredUsers.length;

      handleUserSelect(filteredUsers[newIndex]?.id);
    }
  };

  return (
    <Portal.Host>
      <Snackbar
        visible={snackbarVisible}
        onDismiss={() => setSnackbarVisible(false)}
      >
        {snackbarMessage}
      </Snackbar>
      <View style={styles.container} onTouchStart={handleKeyboardDismiss}>
        {detalleEjemplar ? (
          <View>
            <Text>Id: {detalleEjemplar.id} </Text>
            <Text>Titulo: {detalleEjemplar.material?.titulo} </Text>
            <Text>
              Editorial:
              {detalleEjemplar.material?.editorial?.map((editorial) => (
                <Text key={editorial.id}>{editorial.nombre}</Text>
              ))}
            </Text>
            <Text>
              Autor:
              {detalleEjemplar.material?.autor?.map((autor) => (
                <Text key={autor.id}>
                  {autor.nombre}, {autor.apellido}.
                </Text>
              ))}
            </Text>
            <Text>
              carrera:
              {detalleEjemplar.material?.carrera?.map((carrera) => (
                <Text key={carrera.id}>{carrera.nombre}</Text>
              ))}
            </Text>
            <Text>
              genero:
              {detalleEjemplar.material?.genero?.map((genero) => (
                <Text key={genero.id}>{genero.nombre}</Text>
              ))}
            </Text>
            {detalleEjemplar.estado === "Disponible" ? (
              <View style={styles.entregarContainer}>
                <Text style={styles.label}>Buscar usuario: </Text>
                <TextInput
                  style={styles.input}
                  value={searchText}
                  onChangeText={handleSearchChange}
                  placeholder="Ingresa el correo del usuario"
                  onKeyPress={handleKeyPress}
                />
                <FlatList
                  style={styles.flatList}
                  data={filteredUsers}
                  keyExtractor={(item) => item.id.toString()}
                  renderItem={({ item }) => (
                    <TouchableOpacity
                      onPress={() => handleUserSelect(item.id)}
                      style={[
                        styles.ejemplarItem,
                        item.id === selectedUser?.id && styles.selectedItem,
                      ]}
                    >
                      <Text style={styles.ejemplarText}>{item.email}</Text>
                    </TouchableOpacity>
                  )}
                />
                <Button onPress={handleConfirmar}>
                  <Text>Entregar ejemplar</Text>
                </Button>
                <Portal>
                  <Dialog visible={dialogVisible} onDismiss={handleConfirmar}>
                    <Dialog.Content>
                      <Paragraph>¿Estas seguro realizar el prestamo?</Paragraph>
                    </Dialog.Content>
                    <Dialog.Actions>
                      <Button onPress={handleCancel}>Cancelar</Button>
                      <Button onPress={handlePrestarEjemplar}>Aceptar</Button>
                    </Dialog.Actions>
                  </Dialog>
                </Portal>
              </View>
            ) : (
              <Text>El material no se encuentra disponible...</Text>
            )}
          </View>
        ) : (
          <Text> Cargando detalles...</Text>
        )}
      </View>
    </Portal.Host>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 16,
  },
  reservaContainer: {
    width: "100%",
  },
  finalizadaText: {
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
  ejemplarItem: {
    padding: 10,
    borderBottomWidth: 1,
    borderColor: "#ccc",
  },
  selectedItem: {
    backgroundColor: "#e0e0e0",
  },
});

export default DetalleEjemplarScreen;
