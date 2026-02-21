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
  Categorias,
  getCategorias,
  createCategorias,
  deleteCategorias,
} from "../services/categoriasservice";

export default function CategoriasScreen() {
  const { rol } = useContext(AuthContext);

  const [Categoria, setCategoria] = useState<Categorias[]>([]);
  const [nombre, setNombre] = useState("");

  const cargarCategoria = async () => {
    const data = await getCategorias();
    setCategoria(data);
  };

  useEffect(() => {
    cargarCategoria();
  }, []);

  const handleCreate = async () => {
    if (!nombre.trim()) return;

    try {
      await createCategorias(nombre);
      setNombre("");
      cargarCategoria();
    } catch {
      Alert.alert("Error", "No autorizado");
    }
  };

  const handleDelete = async (id: number) => {
    Alert.alert("Confirmar", "¿Eliminar categoria?", [
      { text: "Cancelar" },
      {
        text: "Eliminar",
        onPress: async () => {
          await deleteCategorias(id);
          cargarCategoria();
        },
      },
    ]);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Categorias</Text>

      {/* CREAR (solo Admin) */}
      {rol === "Administrador" && (
        <View style={styles.form}>
          <TextInput
            placeholder="Nombre de la Categoria"
            value={nombre}
            onChangeText={setNombre}
            style={styles.input}
          />
          <TouchableOpacity style={styles.button} onPress={handleCreate}>
            <Text style={styles.buttonText}>Crear</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* LISTA */}
      <FlatList
        data={Categoria}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text style={styles.itemText}>{item.nombre}</Text>

            {rol === "Administrador" && (
              <TouchableOpacity
                onPress={() => handleDelete(item.id)}
                style={styles.delete}
              >
                <Text style={styles.deleteText}>Eliminar</Text>
              </TouchableOpacity>
            )}
          </View>
        )}
      />
    </View>
  );
}
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
    backgroundColor: "#4a90e2",
    padding: 12,
    borderRadius: 10,
    alignItems: "center",
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
  },
  item: {
    backgroundColor: "#fff",
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    flexDirection: "row",
    justifyContent: "space-between",
  },
  itemText: {
    fontSize: 16,
  },
  delete: {
    backgroundColor: "#e74c3c",
    paddingHorizontal: 12,
    paddingVertical: 5,
    borderRadius: 6,
  },
  deleteText: {
    color: "#fff",
    fontSize: 12,
  },
});