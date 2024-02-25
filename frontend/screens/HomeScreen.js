import React from "react";
import { View, Text, Button, StyleSheet, TouchableOpacity } from "react-native";
import { useNavigation } from "@react-navigation/native";

import MaterialesStackNavigator from '../AppTabsScreens'
import { useUser } from "../contexts/UserContext";

const HomeScreen = () => {
  const navigation = useNavigation();
  const { userInfo, logout } = useUser();

  return (
    <View style={styles.container}>
      {/* Barra de navegación */}    

      {/* Contenido principal */}
      <MaterialesStackNavigator />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  navBar: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 10,
    backgroundColor: "#3498db", // Puedes cambiar el color según tus preferencias
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#fff", // Color del texto
  },
});

export default HomeScreen;
