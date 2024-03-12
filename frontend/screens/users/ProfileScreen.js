import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import React, { useEffect, useState } from "react";
import { useUser } from "../../contexts/UserContext";
import MovimientosServices from "../../services/MovimientosServices";

const ProfileScreen = ({ navigation }) => {
  const [userReservas, setUserReserva] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const { userInfo } = useUser();
  console.log(userInfo);
  useEffect(() => {
    const fetchReservaUsuario = async () => {
      try {
        const access_token = userInfo.access_token;
        const response = await MovimientosServices.reservasUsuario(
          access_token,
          searchQuery
        );
        setUserReserva(response);
        console.log(response);
      } catch (error) {
        console.log("Error al obtener las reservas del usuario: ", error);
      }
    };
    fetchReservaUsuario();
  }, [userInfo]);

  return (
    <View style={styles.container}>
      {userInfo && (
        <>
          <Text>Email: {userInfo.user.email}</Text>
          <Text>Rol: {userInfo.user.role}</Text>
          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={styles.button}
              onPress={() => {
                navigation;
              }}
            >
              <Text style={styles.buttonText}>Notificaciones (0)</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.button}
              onPress={() => {
                navigation.navigate("Reservas");
                // Manejar la acción del botón "Mis reservas"
              }}
            >
              <Text style={styles.buttonText}>Mis reservas</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.button}
              onPress={() => {
                navigation.navigate("Prestamos");
                // Manejar la acción del botón "Mis prestamos"
              }}
            >
              <Text style={styles.buttonText}>Mis prestamos</Text>
            </TouchableOpacity>
          </View>
        </>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  buttonContainer: {
    flexDirection: "column",
    marginTop: 10,
  },
  button: {
    backgroundColor: "#3498db", // Puedes ajustar el color de fondo según tu diseño
    padding: 15,
    marginBottom: 10,
    borderRadius: 5,
  },
  buttonText: {
    color: "#fff", // Puedes ajustar el color del texto según tu diseño
    textAlign: "center",
    fontWeight: "bold",
  },
});

export default ProfileScreen;
