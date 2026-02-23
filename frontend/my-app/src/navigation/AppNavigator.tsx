import React, { useContext } from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { AuthContext } from "../context/AuthContext";

import LoginScreen from "../screens/auth/LoginScreen";
import HomeScreen from "../screens/home/Homescreen";
import VentasScreen from "../screens/ventas/VentasScreen";
import MedioPagoScreen from "../screens/mediospago/MedioPagoScreens";
import CategoriasScreen from "../screens/categorias/CategoriasScreens";
import ArqueoScreen from "../screens/arqueo/arqueoScreens";

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  const { userToken } = useContext(AuthContext);

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {!userToken ? (
          <Stack.Screen name="Login" component={LoginScreen} />
        ) : (
          <>
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="arqueo" component={ArqueoScreen} />            
            <Stack.Screen name="Ventas" component={VentasScreen} />
            <Stack.Screen name="MediosPago" component={MedioPagoScreen} />
            <Stack.Screen name="Categorias" component={CategoriasScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}