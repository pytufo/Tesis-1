import { View, TextInput, Button } from "react-native";
import React, { useState } from "react";
import { toast } from "react-toastify";

import AuthServices from "../../services/AuthServices";

const SignUpScreen = ({ setIsLoggedIn, navigation }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const handleSignup = async () => {
    try {
      const response = await AuthServices.signup(email, password);
      if (response.email) {
        toast.success("Usuario registrado correctamente");
        setIsLoggedIn(false);
        navigation.navigate("AuthStack");
      }
    } catch (error) {
      console.log("error al registrarse: ", error);
    }
  };

  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <TextInput placeholder="Email" onChangeText={setEmail} />
      <TextInput
        placeholder="Password"
        secureTextEntry={true}
        onChangeText={setPassword}
      />
      <Button title="Registrase" onPress={handleSignup} />
    </View>
  );
};

export default SignUpScreen;
