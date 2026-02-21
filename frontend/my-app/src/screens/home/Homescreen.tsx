import React, { useContext } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { AuthContext } from "../../context/AuthContext";
import { useNavigation } from "@react-navigation/native";

export default function HomeScreen() {
  const { rol, logout } = useContext(AuthContext);
  const navigation = useNavigation<any>();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Panel Principal</Text>
      <Text style={styles.subtitle}>Rol: {rol}</Text>

      {/* VENTAS (Admin y Cajero) */}
      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.navigate("Ventas")}
      >
        <Text style={styles.buttonText}>Ventas</Text>
      </TouchableOpacity>

      {/* MEDIOS DE PAGO (solo Admin) */}
      {rol === "Administrador" && (
        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.navigate("MediosPago")}
        >
          <Text style={styles.buttonText}>Medios de Pago</Text>
        </TouchableOpacity>
      )}

      {/* CATEGORIAS (solo Admin) */}
      {rol === "Administrador" && (
        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.navigate("Categorias")}
        >
          <Text style={styles.buttonText}>Categorias</Text>
        </TouchableOpacity>
      )}

      {/* PRODUCTOS (solo Admin) */}
      {rol === "Administrador" && (
        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.navigate("Productos")}
        >
          <Text style={styles.buttonText}>Productos</Text>
        </TouchableOpacity>
      )}

      {/* CERRAR SESIÓN */}
      <TouchableOpacity style={[styles.button, styles.logout]} onPress={logout}>
        <Text style={styles.buttonText}>Cerrar Sesión</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: "center",
    backgroundColor: "#f2f4f8",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    textAlign: "center",
    marginBottom: 5,
  },
  subtitle: {
    textAlign: "center",
    marginBottom: 25,
    color: "#666",
  },
  button: {
    backgroundColor: "#4a90e2",
    padding: 15,
    borderRadius: 12,
    marginBottom: 15,
    alignItems: "center",
  },
  logout: {
    backgroundColor: "#e74c3c",
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 16,
  },
});