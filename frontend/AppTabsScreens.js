import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import MaterialListScreen from "./screens/materiales/MaterialListScreen";
import DetalleMaterialScreen from "./screens/materiales/DetalleMaterialScreen";
import ReservasScreen from "./screens/movimientos/ReservasScreen";
import PrestamosScreen from "./screens/movimientos/PrestamosScreen";
import LogoutScreen from "./screens/auth/LogoutScreen";
import ProfileScreen from "./screens/users/ProfileScreen";
import { useUser } from "./contexts/UserContext";
import UsersListScreen from "./screens/users/UsersListScreen";
import DetalleUsuarioScreen from "./screens/users/DetalleUsuarioScreen";
import DetalleReservaScreen from "./screens/movimientos/DetalleReservaScreen";
import DetallePrestamoScreen from "./screens/movimientos/DetallePrestamoScreen";

import Ionicons from 'react-native-vector-icons/Ionicons'

const AppTabs = createBottomTabNavigator();

const AppTabsScreen = ({ setIsLoggedIn, setUserData }) => {
  const { userInfo } = useUser();
  
  return (
    <AppTabs.Navigator>
      {userInfo.user && userInfo.user.role === 1 ? (
        <>
          <AppTabs.Screen name="Reservas" component={ReservasScreen} />
          <AppTabs.Screen name="Prestamos" component={PrestamosScreen} />
          <AppTabs.Screen name="Usuarios" component={UsersListScreen} />
        </>
      ) : (
        <>
          <AppTabs.Screen name="Perfil" component={ProfileScreen} />
          <AppTabs.Screen name="Materiales" component={MaterialListScreen} />
        </>
      )}

      {userInfo.user && userInfo.user.role === 1 && (
        <>
          <AppTabs.Screen
            name="DetalleUsuario"
            component={DetalleUsuarioScreen}
            options={{ tabBarVisible: false }}
          />
          <AppTabs.Screen
            name="DetallePrestamo"
            component={DetallePrestamoScreen}
            options={{ tabBarVisible: false }}
          />
          <AppTabs.Screen
            name="DetalleMaterial"
            component={DetalleMaterialScreen}
            options={{ tabBarVisible: false }}
          />
          <AppTabs.Screen
            name="DetalleReserva"
            component={DetalleReservaScreen}
            options={{ tabBarVisible: false }}
          />
        </>
      )}

      <AppTabs.Screen
        name="Logout"
        children={(props) => (
          <LogoutScreen {...props} setIsLoggedIn={setIsLoggedIn} />
        )}
      />
    </AppTabs.Navigator>
  );
};

export default AppTabsScreen;
