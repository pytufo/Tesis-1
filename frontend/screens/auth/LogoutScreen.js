import React, { useEffect } from "react";
import { View, Text, Button } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import AuthServices from "../../services/AuthServices";

const LogoutScreen = ({ setIsLoggedIn }) => {
  const handleLogout = async () => {
    try {
      const access_token = await AsyncStorage.getItem("access_token");
      await AuthServices.logout(access_token);
      await AsyncStorage.removeItem("access_token");
      setIsLoggedIn(false);      
    } catch (error) {
      console.error("Error en el cierre de sesión:", error);
    }
  };

  useEffect(() => {
    handleLogout();
  }, []);

  return (
    <View>
      <Text>Cerrando la sesion..</Text>
    </View>
  );
};

export default LogoutScreen;
