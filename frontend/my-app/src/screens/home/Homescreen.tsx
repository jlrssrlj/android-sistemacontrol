import React, { useContext, useEffect, useState } from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { AuthContext } from "../../context/AuthContext";

export default function HomeScreen() {
  const { logout } = useContext(AuthContext);

  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const getToken = async () => {
      const storedToken = await AsyncStorage.getItem("token");
      setToken(storedToken);
    };

    getToken();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Bienvenido al Sistema</Text>

      <Text style={styles.subtitle}>Token activo:</Text>
      <Text numberOfLines={1} style={styles.token}>
        {token}
      </Text>

      <View style={{ marginTop: 20 }}>
        <Button title="Cerrar Sesión" onPress={logout} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: "center",
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    marginTop: 10,
  },
  token: {
    fontSize: 12,
    color: "gray",
  },
});
