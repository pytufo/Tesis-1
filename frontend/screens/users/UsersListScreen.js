import { View, Text, FlatList, TouchableOpacity } from "react-native";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { API_BASE_URL, AUTH_ROUTES } from "../../constants/API";
import { useUser } from "../../contexts/UserContext";

const UsersListScreen = ({ navigation }) => {
  const [user, setUser] = useState([]);
  const { userInfo } = useUser();
  const accessToken = userInfo.access_token;

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}${AUTH_ROUTES.USUARIOS}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        setUser(response.data);
      } catch (error) {
        console.log("Error al obtener los usuarios", error);
      }
    };
    fetchUser();
  }, []);

  const handleUserPress = (userId) => {
    navigation.navigate("DetalleUsuario", { userId });
  };
  return (
    <View>
      <Text>Lista de usuarios: </Text>
      <FlatList
        data={user}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity onPress={() => handleUserPress(item.id)}>
            <View>
              <Text>
                {item.email}.{" "}
                {item.is_active ? (
                  <Text> Cuenta activada</Text>
                ) : (
                  <Text>
                    {" "}
                    Cuenta pendiente de activacion por el administrador
                  </Text>
                )}
              </Text>
            </View>
          </TouchableOpacity>
        )}
      />
    </View>
  );
};

export default UsersListScreen;
