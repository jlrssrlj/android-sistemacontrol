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
  updateCategorias,
} from "../services/categoriasservice";

export default function CategoriasScreen() {
  const { rol } = useContext(AuthContext);

  const [categorias, setCategorias] = useState<Categorias[]>([]);
  const [nombre, setNombre] = useState("");


  const [editId, setEditId] = useState<number | null>(null);
  const [editNombre, setEditNombre] = useState("");

  const cargarCategoria = async () => {
    const data = await getCategorias();
    setCategorias(data);
  };

  useEffect(() => {
    cargarCategoria();
  }, []);

  /* ================= CREAR ================= */
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

  /* ================= EDITAR ================= */
  const handleEdit = (categoria: Categorias) => {
    setEditId(categoria.id);
    setEditNombre(categoria.nombre);
  };

  const handleUpdate = async () => {
    if (!editNombre.trim() || editId === null) return;

    try {
      await updateCategorias(editId, editNombre);
      setEditId(null);
      setEditNombre("");
      cargarCategoria();
    } catch {
      Alert.alert("Error", "No se pudo actualizar");
    }
  };

  /* ================= ELIMINAR ================= */
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

      {/* CREAR */}
      {rol === "Administrador" && (
        <View style={styles.form}>
          <TextInput
            placeholder="Nombre de la categoría"
            value={nombre}
            onChangeText={setNombre}
            style={styles.input}
          />
          <TouchableOpacity style={styles.button} onPress={handleCreate}>
            <Text style={styles.buttonText}>Crear</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* EDITAR */}
      {rol === "Administrador" && editId !== null && (
        <View style={styles.form}>
          <TextInput
            placeholder="Editar categoría"
            value={editNombre}
            onChangeText={setEditNombre}
            style={styles.input}
          />
          <TouchableOpacity style={styles.button} onPress={handleUpdate}>
            <Text style={styles.buttonText}>Guardar cambios</Text>
          </TouchableOpacity>

          <TouchableOpacity
            onPress={() => {
              setEditId(null);
              setEditNombre("");
            }}
          >
            <Text style={styles.cancel}>Cancelar</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* LISTA */}
      <FlatList
        data={categorias}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text style={styles.itemText}>{item.nombre}</Text>

            {rol === "Administrador" && (
              <View style={styles.actions}>
                <TouchableOpacity
                  onPress={() => handleEdit(item)}
                  style={styles.edit}
                >
                  <Text style={styles.editText}>Editar</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  onPress={() => handleDelete(item.id)}
                  style={styles.delete}
                >
                  <Text style={styles.deleteText}>Eliminar</Text>
                </TouchableOpacity>
              </View>
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
    fontSize: 16,
  },
  actions: {
    flexDirection: "row",
    gap: 8,
  },
  edit: {
    backgroundColor: "#f1c40f",
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 6,
  },
  editText: {
    fontSize: 12,
    color: "#000",
  },
  delete: {
    backgroundColor: "#e74c3c",
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 6,
  },
  deleteText: {
    color: "#fff",
    fontSize: 12,
  },
});