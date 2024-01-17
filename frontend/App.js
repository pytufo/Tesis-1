import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";

// IMPORTAR PANTALLAS
import LoginScreen from "./screens/auth/LoginScreen";
// import HomeScreen from "./screens/HomeScreen";
import MaterialListScreen from "./screens/materiales/MaterialListScreen";
import DetalleMaterialScreen from "./screens/materiales/DetalleMaterialScreen";

const Stack = createStackNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="MaterialList">
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="MaterialList" component={MaterialListScreen} />
        <Stack.Screen name="DetalleMaterialScreen" component={DetalleMaterialScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;
