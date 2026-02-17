import { useEffect, useState } from 'react'
import { View, Text, FlatList, ActivityIndicator } from 'react-native'
// 1. IMPORTANTE: Importa tu CSS global para que NativeWind cargue los estilos
import "./global.css"; 

interface Proveedor {
  id: number
  nombre: string
  nit: string
  direccion: string
  telefono: string
}

export default function App() {
  const [proveedores, setProveedores] = useState<Proveedor[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Nota: 10.0.2.2 es correcto para el emulador de Android (localhost de la PC)
    fetch('http://192.168.1.2:8000/api/proveedores/')
      .then(res => res.json())
      .then(data => setProveedores(data))
      .catch(err => console.error("Error en fetch:", err))
      .finally(() => setLoading(false))
  }, [])

  return (
    // Usa 'flex' y 'bg-slate-100' (asegúrate que existan en tu paleta de Tailwind)
    <View className="flex-1 px-4 bg-slate-100 pt-14">
      <Text className="mb-6 text-3xl font-bold text-center text-slate-800">
        Proveedores
      </Text>

      {loading ? (
        <View className="items-center justify-center flex-1">
          <ActivityIndicator size="large" color="#1e293b" />
        </View>
      ) : (
        <FlatList
          data={proveedores}
          keyExtractor={(item) => item.id.toString()}
          showsVerticalScrollIndicator={false} // Limpieza visual
          renderItem={({ item }) => (
            <View className="p-5 mb-4 bg-white border shadow-sm rounded-2xl border-slate-200">
              <Text className="mb-1 text-xl font-bold text-slate-900">
                {item.nombre}
              </Text>
              <View className="space-y-1">
                <Text className="font-medium text-slate-500">NIT: {item.nit}</Text>
                <Text className="text-slate-600">📍 {item.direccion}</Text>
                <Text className="text-slate-600">📞 {item.telefono}</Text>
              </View>
            </View>
          )}
          // 2. Si la lista está vacía, mostrar un mensaje
          ListEmptyComponent={() => (
            <Text className="mt-10 text-center text-slate-400">No hay proveedores registrados</Text>
          )}
        />
      )}
    </View>
  )
}
