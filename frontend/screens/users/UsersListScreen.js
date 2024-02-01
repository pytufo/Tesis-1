import {
  View,
  Text,
  FlatList,
  ScrollView,
  TouchableOpacity,
  TextInput,
  StyleSheet,
} from "react-native";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { API_BASE_URL, AUTH_ROUTES } from "../../constants/API";
import { tableStyles } from "../../constants/Colors";

import { useUser } from "../../contexts/UserContext";

const UsersListScreen = ({ navigation }) => {
  const [user, setUser] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
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

  const handleSearch = (text) => {
    setSearchQuery(text);
    const filteredUsers = user.filter((item) =>
      item.email.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setUser(filteredUsers);
  };

  const renderTableHeader = () => (
    <View style={tableStyles.tableHeader}>
      <Text style={tableStyles.headerText}>Usuario</Text>
      <Text style={tableStyles.headerText}>Estado de la cuenta</Text>
    </View>
  );

  const renderItem = ({ item }) => (
    <TouchableOpacity onPress={() => handleUserPress(item.id)}>
      <View style={tableStyles.tableRow}>
        <Text style={tableStyles.cell}>{item.email}</Text>
        <Text style={tableStyles.cell}>
          {item.is_active ? (
            <Text> Cuenta activada</Text>
          ) : (
            <Text> Cuenta pendiente de activacion por el administrador</Text>
          )}
        </Text>
      </View>
    </TouchableOpacity>
  );

  const handleUserPress = (userId) => {
    navigation.navigate("DetalleUsuario", { userId });
  };
  return (
    <View style={styles.container}>
      <View style={{ padding: 10 }}>
        <TextInput
          style={styles.searchInput}
          placeholder="Buscar usuarios..."
          value={searchQuery}
          onChangeText={handleSearch}          
        />
      </View>
      <ScrollView>
        {renderTableHeader()}
        <FlatList
          data={user}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderItem}
        />
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  searchBar: {
    padding: 10,
    backgroundColor: "#fff",
    borderBottomWidth: 1,
    borderBottomColor: "#ddd",
  },
  searchInput: {
    height: 40,
    borderColor: "gray",
    borderWidth: 1,
    padding: 10,
  },
});

export default UsersListScreen;
