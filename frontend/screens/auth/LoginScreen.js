import { Text, Button, TextInput, View } from "react-native";
import React, { useState, useEffect } from "react";
import AuthServices from "../../services/AuthServices";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useUser } from "../../contexts/UserContext";
import { toast } from "react-toastify";

const LoginScreen = ({ setIsLoggedIn, navigation }) => {
  const { storeUserInfo } = useUser();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const user = await AuthServices.login(email, password);
      console.log("Respuesta: ", user);
      if (user.access_token) {
        await AsyncStorage.setItem("access_token", user.access_token);
        storeUserInfo(user);
        setIsLoggedIn(true);
      } else {
        toast.error("usuario o contraseña incorrectos");
        console.log("Token null o invalido");
      }
    } catch (error) {
      console.log("error al autenticar: ", error);
    }
  };

  const navigateToSignup = () => {
    navigation.navigate("Signup");
  };

  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <TextInput placeholder="Email" onChangeText={setEmail} />
      <TextInput
        placeholder="Password"
        secureTextEntry={true}
        onChangeText={setPassword}
      />
      <Button title="Login" onPress={handleLogin} />
      <Text onPress={navigateToSignup}>¿No tienes cuenta? Regístrate aquí</Text>
    </View>
  );
};

export default LoginScreen;
