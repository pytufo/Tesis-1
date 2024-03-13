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
import { tableStyles } from "../../constants/Colors";

import { useUser } from "../../contexts/UserContext";
import AuthServices from "../../services/AuthServices";

const UsersListScreen = ({ navigation }) => {
  const [user, setUser] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const { userInfo } = useUser();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const access_token = userInfo.access_token;
        const response = await AuthServices.listarUsuarios(
          access_token,
          searchQuery
        );
        setUser(response);
        console.log(response);
      } catch (error) {
        console.log("Error al obtener los usuarios", error);
      }
    };
    fetchUser();
  }, [userInfo.access_token, searchQuery]);

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
            <Text> Limite: {item.limite}</Text>
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
          onChangeText={(text) => setSearchQuery(text)}
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
