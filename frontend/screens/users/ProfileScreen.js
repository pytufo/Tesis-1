import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import React,{useEffect, useState} from "react";
import { useUser } from "../../contexts/UserContext";

const ProfileScreen = () => {
  const { userInfo } = useUser();
  console.log(userInfo);

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
                // Manejar la acción del botón "Mis prestamos"
              }}
            >
              <Text style={styles.buttonText}>Notificaciones (0)</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.button}
              onPress={() => { console.log(userInfo)
                // Manejar la acción del botón "Mis reservas"
              }}
            >
              <Text style={styles.buttonText}>Mis reservas</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.button}
              onPress={() => {
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
