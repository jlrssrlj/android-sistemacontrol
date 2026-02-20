import { useState } from "react";
import { createGasto } from "../services/gastoservice";

import {
  View,
  Text,
  TextInput,
  Button,
  Alert,
} from "react-native";

export default function GastoCreate() {
  const [descripcion, setDescripcion] = useState("");
  const [valor, setValor] = useState("");
  const [fecha, setFecha] = useState("");

  const handleSubmit = async () => {
    try {
      await createGasto({
        descripcion,
        valor: Number(valor),
        fecha,
      });

      setDescripcion("");
      setValor("");
      setFecha("");

      Alert.alert("Éxito", "Gasto registrado correctamente");
    } catch (error) {
      console.error("Error creando gasto", error);
      Alert.alert("Error", "No se pudo registrar el gasto");
    }
  };

  return (
    <View style={{ padding: 16 }}>
      <Text style={{ fontSize: 20, fontWeight: "bold", marginBottom: 12 }}>
        Nuevo Gasto
      </Text>

      <TextInput
        placeholder="Descripción"
        value={descripcion}
        onChangeText={setDescripcion}
        style={{ borderWidth: 1, marginBottom: 10, padding: 8 }}
      />

      <TextInput
        placeholder="Valor"
        value={valor}
        onChangeText={setValor}
        keyboardType="numeric"
        style={{ borderWidth: 1, marginBottom: 10, padding: 8 }}
      />

      <TextInput
        placeholder="Fecha (YYYY-MM-DD)"
        value={fecha}
        onChangeText={setFecha}
        style={{ borderWidth: 1, marginBottom: 16, padding: 8 }}
      />

      <Button title="Guardar" onPress={handleSubmit} />
    </View>
  );
}
