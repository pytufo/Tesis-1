// components/Navbar.js
import React, { useContext } from "react";
import { View, Text, TouchableOpacity } from "react-native";
import { useUser } from "../contexts/UserContext";
import { useNavigation } from "@react-navigation/native";

const Navbar = () => {
  const { userInfo, clearUserInfo } = useUser();
  const navigation = useNavigation();

  const handleLogout = () => {
    // Lógica para cerrar sesión
    navigation.navigate("Logout");
  };

  return (
    <View
      style={{
        flexDirection: "row",
        justifyContent: "space-between",
        padding: 16,
        backgroundColor: "lightblue",
      }}
    >
      <Text style={{ fontSize: 18, fontWeight: "bold" }}>SysBib</Text>
      <View style={{ flexDirection: "row" }}>
        {userInfo ? (
          <TouchableOpacity onPress={handleLogout}>
            <Text style={{ marginRight: 10 }}>Logout</Text>
          </TouchableOpacity>
        ) : (
          <TouchableOpacity
            onPress={() => {
              /* Implementar la lógica de login */
            }}
          >
            <Text style={{ marginRight: 10 }}>Login</Text>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
};

export default Navbar;
