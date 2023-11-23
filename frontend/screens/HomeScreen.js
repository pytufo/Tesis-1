import { Button, Text, View } from "react-native";
import React from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";

const HomeScreen = ({ navigation }) => {
  const handleLogout = async () => {
    await AsyncStorage.removeItem(jwtToken);
    navigation.navigate("Login");
  };
  return (
    <View>
      <Text>Bienbenido a Sys-Bib</Text>
      <Button title="Cerrar sesión" onPress={handleLogout} />
    </View>
  );
};

export default HomeScreen;
