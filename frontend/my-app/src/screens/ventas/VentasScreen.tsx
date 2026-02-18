import React, { useEffect, useState } from "react";
import { View, Text, FlatList, TouchableOpacity } from "react-native";
import { getVentas } from "../services/saleservice";

export default function VentasScreen() {
  const [ventas, setVentas] = useState([]);

  const loadVentas = async () => {
    try {
      const data = await getVentas();
      setVentas(data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    loadVentas();
  }, []);

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 22, fontWeight: "bold" }}>
        Lista de Ventas
      </Text>

      <FlatList
        data={ventas}
        keyExtractor={(item: any) => item.id.toString()}
        renderItem={({ item }: any) => (
          <View
            style={{
              padding: 15,
              backgroundColor: "#f5f5f5",
              marginTop: 10,
              borderRadius: 10,
            }}
          >
            <Text>Venta #{item.id}</Text>
            <Text>Total: ${item.total}</Text>
            <Text>Fecha: {item.fecha}</Text>
          </View>
        )}
      />
    </View>
  );
}
