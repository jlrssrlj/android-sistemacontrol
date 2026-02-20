import { useEffect, useState } from "react";
import { getGastos, Gasto } from "../services/gastoservice";


import {
  View,
  Text,
  FlatList,
  ActivityIndicator,
  StyleSheet,
} from "react-native";

export default function GastosList() {
  const [gastos, setGastos] = useState<Gasto[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    cargarGastos();
  }, []);

  const cargarGastos = async () => {
    try {
      const data = await getGastos();
      setGastos(data);
    } catch (error) {
      console.error("Error cargando gastos", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <ActivityIndicator size="large" />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Lista de Gastos</Text>

      <FlatList
        data={gastos}
        keyExtractor={(item) => item.id?.toString() ?? ""}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.descripcion}>{item.descripcion}</Text>
            <Text style={styles.valor}>${item.valor}</Text>
            <Text style={styles.fecha}>{item.fecha}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 12,
  },
  card: {
    padding: 12,
    borderWidth: 1,
    borderRadius: 8,
    marginBottom: 10,
  },
  descripcion: {
    fontSize: 16,
    fontWeight: "600",
  },
  valor: {
    fontSize: 14,
  },
  fecha: {
    fontSize: 12,
    color: "gray",
  },
});
