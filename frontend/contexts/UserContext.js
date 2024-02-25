import { View, Text } from "react-native";
import React, { createContext, useContext, useState, useEffect } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";

const UserContext = createContext();

const UserProvider = ({ children }) => {
  const [userInfo, setUserInfo] = useState(null);

  const storeUserInfo = async (user) => {
    try {
      await AsyncStorage.setItem("user_info", JSON.stringify(user));
      setUserInfo(user);
    } catch (error) {
      console.error("Error al obtener la informacion del usuario;  ", error);
    }
  };
  const clearUserInfo = async () => {
    try {
      await AsyncStorage.removeItem("user_info");      
      setUserInfo(null);
    } catch (error) {
      console.error("Error al limpiar la información del usuario:", error);
    }
  };

  useEffect(() => {
    const loadUserInfo = async () => {
      try {
        const storedUserInfo = await AsyncStorage.getItem("user_info");
        if (storedUserInfo) {
          setUserInfo(JSON.parse(storedUserInfo));
        }
      } catch (error) {
        console.error("Error al cargar la información del usuario:", error);
      }
    };    
    loadUserInfo();
  }, []);

  return (
    <UserContext.Provider value={{ userInfo, storeUserInfo, clearUserInfo }}>
      {children}
    </UserContext.Provider>
  );
};

const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUser debe ser utilizado dentro de userprovider");
  }
  return context;
};
export { UserProvider, useUser };
