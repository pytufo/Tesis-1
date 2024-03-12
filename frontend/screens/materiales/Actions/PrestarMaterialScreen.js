import { View, Text, StyleSheet, ScrollView } from "react-native";
import React, { useState, useEffect } from "react";
import { TextInput, List, Button, Snackbar } from "react-native-paper";
import axios from "axios";
import MaterialServices from "../../../services/MaterialServices";
import MovimientosServices from "../../../services/MovimientosServices";
import AuthServices from "../../../services/AuthServices";
import { useUser } from "../../../contexts/UserContext";
const PrestarMaterialScreen = ({ route, navigation }) => {
  const { detalleMaterial, ejemplares } = route.params;
  const [users, setUsers] = useState([]);
  const { userInfo } = useUser();
  const accessToken = userInfo ? userInfo.access_token : null;

  const [filteredUsers, setFilteredUsers] = useState([]);
  const [searchUserText, setSearchUserText] = useState("");

  const [filteredEjemplares, setFilteredEjemplares] = useState([]);

  const [selectedUser, setSelectedUser] = useState(null);
  const [selectedEjemplar, setSelectedEjemplar] = useState("");

  const [snackbarVisible, setSnackbarVisible] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");

  console.log(detalleMaterial);
  console.log(ejemplares);

  useEffect(() => {
    navigation.setOptions(
      {
        title: detalleMaterial.titulo,
      },
      [userInfo]
    );
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
  }, [detalleMaterial, ejemplares, accessToken]);

  const handleEntregarMaterial = async () => {
    const accessToken = userInfo ? userInfo.access_token : null;
    try {
      console.log(selectedUser);
      if (!selectedUser) {
        setSnackbarMessage("Selecciona un usuario para el prestamo");
        setSnackbarVisible(true);
        return;
      }
      if (!selectedEjemplar) {
        setSnackbarMessage("El ejemplar seleccionado no existe");
        setSnackbarVisible(true);
        return;
      }
      const prestamoData = {
        created_by: userInfo.user.id,
        owner: selectedUser,
        ejemplar: selectedEjemplar,
      };
      const response = await MovimientosServices.crearPrestamo(
        accessToken,
        prestamoData
      );
      if (response) {
        console.log(selectedEjemplar, selectedUser);
        setSnackbarMessage(response.message);
        setSnackbarVisible(true);
      } else {
        setSnackbarMessage(response.message);
      }
    } catch (error) {
      console.error("Error al realizar el prestamo del ejemplar", error);
    }
  };

  const filterItems = (text, items) => {
    return text
      ? items.filter((item) => item.id.toString().includes(text))
      : [];
  };

  const selectUser = (selectedUser) => {
    setSelectedUser(selectedUser.id);
    setSearchUserText(selectedUser.email);
    setFilteredUsers([]);
    console.log(selectedUser);
  };

  const filterUsers = async (text) => {
    setSearchUserText(text);
    try {
      const filtered = await AuthServices.listarUsuariosNoAdmin(
        accessToken,
        text
      );
      setFilteredUsers(filtered);
    } catch (error) {
      console.error("Error al filtrar usuarios", error);
    }
  };

  const selectEjemplar = (selectedEjemplar) => {
    setSelectedEjemplar(selectedEjemplar.id);
    setFilteredEjemplares([]);
    console.log(selectedEjemplar);
  };
  const filterEjemplares = (text) => {
    const filtered = filterItems(text, ejemplares);
    setFilteredEjemplares(filtered);
  };
  return (
    <ScrollView>
      <Snackbar
        visible={snackbarVisible}
        onDismiss={() => setSnackbarVisible(false)}
      >
        {snackbarMessage}
      </Snackbar>
      <TextInput
        label="Ingrese el Id del ejemplar a prestar"
        value={selectedEjemplar}
        onChangeText={(text) => {
          setSelectedEjemplar(text);
          filterEjemplares(text);
        }}
      />
      <List.Section>
        {filteredEjemplares.map((item) => (
          <List.Item
            key={item.id}
            title={`ID: ${item.id} - ${item.estado}`}
            onPress={() => selectEjemplar(item)}
          />
        ))}
      </List.Section>

      <TextInput
        label="Ingrese el correo electrónico del usuario"
        value={searchUserText}
        onChangeText={(text) => {
          filterUsers(text);
        }}
      />
      <List.Section>
        {filteredUsers.map((user) => (
          <List.Item
            key={user.id}
            title={`Email: ${user.email}`}
            onPress={() => selectUser(user)}
          />
        ))}
      </List.Section>
      <View style={styles.buttonContainer}>
        <Button style={styles.button} onPress={handleEntregarMaterial}>
          Entregar Material
        </Button>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 16,
  },
  button: {
    backgroundColor: "#2471A3",
    marginTop: 10,
    paddingHorizontal: 12,
    borderRadius: 4,
  },
  buttonContainer: {
    flexDirection: "row",
    marginBottom: 10,
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
});

export default PrestarMaterialScreen;
