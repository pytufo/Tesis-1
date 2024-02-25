import React from "react";
import { createStackNavigator } from "@react-navigation/stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

import LoginScreen from "./screens/auth/LoginScreen";
import SignUpScreen from "./screens/auth/SignUpScreen";

import MaterialListScreen from "./screens/materiales/MaterialListScreen";
import DetalleMaterialScreen from "./screens/materiales/DetalleMaterialScreen";

const Stack = createBottomTabNavigator();
const MaterialesStack = createStackNavigator();
const MaterialesStackNavigator = () => (
  <MaterialesStack.Navigator>
    <MaterialesStack.Screen
      name="Materiales"
      options={{ headerShown: false }}
      component={MaterialListScreen}
    />
    <MaterialesStack.Screen
      name="DetalleMaterial"
      component={DetalleMaterialScreen}
    />
  </MaterialesStack.Navigator>
);
const AuthStackScreen = ({ setIsLoggedIn, setUserData, isLoggedIn }) => (
  <Stack.Navigator>
    <Stack.Screen
      name="Materiales"
      component={MaterialesStackNavigator}
      options={{ isLoggedIn }}
    />
    <Stack.Screen
      name="Login"
      children={(props) => (
        <LoginScreen
          {...props}
          setIsLoggedIn={setIsLoggedIn}
          setUserData={setUserData}
          isLoggedIn={isLoggedIn}
        />
      )}
    />
    <Stack.Screen name="Signup" component={SignUpScreen} />
  </Stack.Navigator>
);

export default AuthStackScreen;
