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
  Producto,
  getProducto,
  createProducto,
  deleteProducto,
  updateProducto,
} from "../services/productosservice";

export default function ProductoScreen() {
  const { rol } = useContext(AuthContext);

  const [producto, setProducto] = useState<Producto[]>([]);
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [precio, setPrecio] = useState("");
  const [stock, setStock] = useState("");
  const [categoria, setCategoria] = useState("");
  const [proveedor, setProveedor] = useState("");


  const [editId, setEditId] = useState<number | null>(null);
  const [editNombre, setEditNombre] = useState("");

  const cargarProducto = async () => {
    const data = await getProducto();
    setProducto(data);
  };

  useEffect(() => {
    cargarProducto();
  }, []);

  /* ================= CREAR ================= */
  const handleCreate = async () => {
    if (!nombre.trim()) return;

    try {
      await createProducto({
          nombre,
          descripcion,
          precio: parseFloat(precio),
          stock: parseInt(stock),
          categoria: Number(categoria),
          proveedor: Number(proveedor),
          
      });
      cargarProducto();
    } catch {
      Alert.alert("Error", "No autorizado");
    }
  };

  /* ================= EDITAR ================= */
  const handleEdit = (producto: Producto) => {
    setEditId(producto.id);
    setNombre(producto.nombre);
    setDescripcion(producto.descripcion);
    setPrecio(producto.precio.toString());
    setStock(producto.stock.toString());
    setCategoria(producto.categoria.toString());
    setProveedor(producto.proveedor.toString());
  };

  const handleUpdate = async () => {
    if (editId === null) return;

    try {
      await updateProducto(editId, {
        nombre,
        descripcion,
        precio: parseFloat(precio),
        stock: parseInt(stock),
        categoria: Number(categoria),
        proveedor: Number(proveedor),
      });

      setEditId(null);
      cargarProducto();
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
          await deleteProducto(id);
          cargarProducto();
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
        data={producto}
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