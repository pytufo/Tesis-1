import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createStackNavigator } from "@react-navigation/stack";
import { useUser } from "./contexts/UserContext";
import { Text, Button, StyleSheet } from "react-native";

import MaterialListScreen from "./screens/materiales/MaterialListScreen";
import DetalleMaterialScreen from "./screens/materiales/DetalleMaterialScreen";
import EjemplarListScreen from "./screens/ejemplares/EjemplaresListScreen";
import DetalleEjemplarScreen from "./screens/ejemplares/DetalleEjemplar";
import ReservasScreen from "./screens/movimientos/ReservasScreen";
import PrestamosScreen from "./screens/movimientos/PrestamosScreen";
import LogoutScreen from "./screens/auth/LogoutScreen";
import ProfileScreen from "./screens/users/ProfileScreen";
import UsersListScreen from "./screens/users/UsersListScreen";
import DetalleUsuarioScreen from "./screens/users/DetalleUsuarioScreen";
import DetalleReservaScreen from "./screens/movimientos/DetalleReservaScreen";
import DetallePrestamoScreen from "./screens/movimientos/DetallePrestamoScreen";
import HomeScreen from "./screens/HomeScreen";
import PrestarMaterialScreen from "./screens/materiales/Actions/PrestarMaterialScreen";
import NuevoMaterialScreen from "./screens/materiales/Actions/NuevoMaterialScreen";

const AppTabs = createBottomTabNavigator();
const UsuariosStack = createStackNavigator();
const PrestamosStack = createStackNavigator();
const ReservasStack = createStackNavigator();
const MaterialesStack = createStackNavigator();
const EjemplaresStack = createStackNavigator();

const UsuariosStackNavigator = () => (
  <UsuariosStack.Navigator>
    <UsuariosStack.Screen
      name="Usuarios"
      options={{ headerShown: false }}
      component={UsersListScreen}
    />
    <UsuariosStack.Screen
      name="DetalleUsuario"
      component={DetalleUsuarioScreen}
    />
  </UsuariosStack.Navigator>
);

const PrestamosStackNavigator = () => (
  <PrestamosStack.Navigator>
    <PrestamosStack.Screen
      name="Prestamos"
      options={{ headerShown: false }}
      component={PrestamosScreen}
    />
    <PrestamosStack.Screen
      name="DetallePrestamo"
      component={DetallePrestamoScreen}
    />
  </PrestamosStack.Navigator>
);

const ReservasStackNavigator = () => (
  <ReservasStack.Navigator>
    <ReservasStack.Screen
      name="Reservas"
      options={{ headerShown: false }}
      component={ReservasScreen}
    />
    <ReservasStack.Screen
      name="DetalleReserva"
      component={DetalleReservaScreen}
    />
  </ReservasStack.Navigator>
);

export const MaterialesStackNavigator = () => (
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
    <MaterialesStack.Screen
      name="PrestarMaterial"
      component={PrestarMaterialScreen}
    />
    <MaterialesStack.Screen
      name="NuevoMaterial"
      component={NuevoMaterialScreen}
    />
  </MaterialesStack.Navigator>
);

export const EjemplaresStackNavigator = () => (
  <EjemplaresStack.Navigator>
    <EjemplaresStack.Screen
      name="Ejemplares"
      options={{ headerShown: false }}
      component={EjemplarListScreen}
    />
    <EjemplaresStack.Screen
      name="DetalleEjemplar"
      component={DetalleEjemplarScreen}
    />
  </EjemplaresStack.Navigator>
);
const AppTabsScreen = ({ setIsLoggedIn, setUserData, navigation }) => {
  const { userInfo } = useUser();
  const isAdmin = userInfo && userInfo.user.role === 1;
  return (
    <>
      <AppTabs.Navigator>
        {userInfo && userInfo.user.role === 1 ? (
          <>
            <AppTabs.Screen
              name="Usuarios"
              component={UsuariosStackNavigator}
            />
            {/* <AppTabs.Screen
              name="Ejemplares"
              component={EjemplaresStackNavigator}
            /> */}
          </>
        ) : (
          <>
            <AppTabs.Screen name="Perfil" component={ProfileScreen} />
          </>
        )}

        <AppTabs.Screen
          name="Reservas"
          component={ReservasStackNavigator}
          options={{ tabBarVisibilityAnimationConfig: isAdmin }}
        />
        <AppTabs.Screen name="Prestamos" component={PrestamosStackNavigator} />
        <AppTabs.Screen
          name="Materiales"
          component={MaterialesStackNavigator}
          initialParams={{ setIsLoggedIn }}
        />
        <AppTabs.Screen
          name="Logout"
          children={(props) => (
            <LogoutScreen {...props} setIsLoggedIn={setIsLoggedIn} />
          )}
        />
      </AppTabs.Navigator>
    </>
  );
};

export default AppTabsScreen;
