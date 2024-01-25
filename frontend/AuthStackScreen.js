import React from "react";
import { createStackNavigator } from "@react-navigation/stack";
import LoginScreen from "./screens/auth/LoginScreen";
import SignUpScreen from "./screens/auth/SignUpScreen";

const Stack = createStackNavigator();

const AuthStackScreen = ({ setIsLoggedIn, setUserData }) => (
  <Stack.Navigator>
    <Stack.Screen
      name="Login"
      children={(props) => (
        <LoginScreen
          {...props}
          setIsLoggedIn={setIsLoggedIn}
          setUserData={setUserData}
        />
      )}
    />
    <Stack.Screen name="Signup" component={SignUpScreen} />
  </Stack.Navigator>
);

export default AuthStackScreen;
