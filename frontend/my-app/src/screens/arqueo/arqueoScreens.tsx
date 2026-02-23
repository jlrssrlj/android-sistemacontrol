import React, { useContext, useEffect, useState } from "react";
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  TextInput,
  StyleSheet,
  Alert,
} from "react-native";
import { AuthContext } from "../../context/AuthContext";
import {
  Arqueo,
  getArqueo,
  abrirarqueo,
  cerrarArqueo,
} from "../services/arqueoservice";

export default function ArqueoScreen() {
  const { rol } = useContext(AuthContext);

  const [arqueos, setArqueos] = useState<Arqueo[]>([]);
  const [montoInicial, setMontoInicial] = useState("");
  const [montoFinal, setMontoFinal] = useState("");

  const [cerrarId, setCerrarId] = useState<number | null>(null);

  const cargarArqueos = async () => {
    try {
      const data = await getArqueo();
      setArqueos(data);
    } catch {
      Alert.alert("Error", "No se pudieron cargar los arqueos");
    }
  };

  useEffect(() => {
    cargarArqueos();
  }, []);

  /* ================= ABRIR ARQUEO ================= */
  const handleAbrir = async () => {
    if (!montoInicial.trim()) return;

    try {
      await abrirarqueo(montoInicial);
      setMontoInicial("");
      cargarArqueos();
    } catch {
      Alert.alert("Error", "No se pudo abrir el arqueo");
    }
  };

  /* ================= CERRAR ARQUEO ================= */
  const handleCerrar = async () => {
    if (!montoFinal.trim() || cerrarId === null) return;

    try {
      await cerrarArqueo(cerrarId, montoFinal);
      setCerrarId(null);
      setMontoFinal("");
      cargarArqueos();
    } catch {
      Alert.alert("Error", "No se pudo cerrar el arqueo");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Arqueo de Caja</Text>

      {/* ABRIR ARQUEO */}
      {(rol === "Administrador" || rol === "Cajero") && (
        <View style={styles.form}>
          <TextInput
            placeholder="Monto inicial"
            value={montoInicial}
            onChangeText={setMontoInicial}
            keyboardType="numeric"
            style={styles.input}
          />
          <TouchableOpacity style={styles.button} onPress={handleAbrir}>
            <Text style={styles.buttonText}>Abrir Arqueo</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* CERRAR ARQUEO */}
      {(rol === "Administrador" || rol === "Cajero") && cerrarId !== null && (
        <View style={styles.form}>
          <TextInput
            placeholder="Monto final"
            value={montoFinal}
            onChangeText={setMontoFinal}
            keyboardType="numeric"
            style={styles.input}
          />
          <TouchableOpacity style={styles.button} onPress={handleCerrar}>
            <Text style={styles.buttonText}>Cerrar Arqueo</Text>
          </TouchableOpacity>

          <TouchableOpacity
            onPress={() => {
              setCerrarId(null);
              setMontoFinal("");
            }}
          >
            <Text style={styles.cancel}>Cancelar</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* LISTA DE ARQUEOS */}
      <FlatList
        data={arqueos}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <View>
              <Text style={styles.itemText}>
                Inicio: {new Date(item.fecha_inicio).toLocaleString()}
              </Text>
              <Text style={styles.itemText}>
                Monto inicial: ${item.monto_inicial}
              </Text>
              {item.monto_final && (
                <Text style={styles.itemText}>
                  Monto final: ${item.monto_final}
                </Text>
              )}
              {item.diferencia && (
                <Text style={styles.itemText}>
                  Diferencia: ${item.diferencia}
                </Text>
              )}
            </View>

            {(rol === "Administrador" || rol === "Cajero") &&
              item.fecha_fin === null && (
                <TouchableOpacity
                  style={styles.edit}
                  onPress={() => setCerrarId(item.id)}
                >
                  <Text style={styles.editText}>Cerrar</Text>
                </TouchableOpacity>
              )}
          </View>
        )}
      />
    </View>
  );
}

/* ================= STYLES ================= */

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#f2f4f8",
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 15,
    textAlign: "center",
  },
  form: {
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 10,
    padding: 12,
    marginBottom: 10,
    backgroundColor: "#fff",
  },
  button: {
    backgroundColor: "#27ae60",
    padding: 12,
    borderRadius: 10,
    alignItems: "center",
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
  },
  cancel: {
    textAlign: "center",
    marginTop: 10,
    color: "#666",
  },
  item: {
    backgroundColor: "#fff",
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  itemText: {
    fontSize: 14,
  },
  edit: {
    backgroundColor: "#f39c12",
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 6,
  },
  editText: {
    fontSize: 12,
    color: "#fff",
  },
});