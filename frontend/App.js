import React, { useState, useEffect, useCallback } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import { UserProvider } from "./contexts/UserContext";

import AsyncStorage from "@react-native-async-storage/async-storage";
import AuthStackScreen from "./AuthStackScreen";
import AppTabsScreen from "./AppTabsScreens";

const Stack = createStackNavigator();
const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);
  useEffect(() => {
    const checkAuthentication = async () => {
      try {
        const token = await AsyncStorage.getItem("access_token");
        setIsLoggedIn(!!token);
      } catch (error) {
        console.error("error al autenticar", error);
      }
    };
    checkAuthentication();
  }, []);

  return (
    <UserProvider>
      <NavigationContainer>
        <Stack.Navigator headerMode="none">
          {isLoggedIn ? (
            <Stack.Screen
              name="AppTabs"
              children={(props) => (
                <AppTabsScreen {...props} setIsLoggedIn={setIsLoggedIn} />
              )}
            />
          ) : (
            <Stack.Screen
              name="AuthStack"
              children={(props) => (
                <AuthStackScreen
                  {...props}
                  setIsLoggedIn={setIsLoggedIn}
                  setUserData={setUserData}
                />
              )}
            />
          )}
        </Stack.Navigator>
        <ToastContainer />
      </NavigationContainer>
    </UserProvider>
  );
};

export default App;
