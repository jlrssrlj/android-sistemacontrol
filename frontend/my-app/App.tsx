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
    
    fetch('http://192.168.1.2:8000/api/proveedoresand/')
      .then(res => res.json())
      .then(data => setProveedores(data))
      .catch(err => console.error("Error en fetch:", err))
      .finally(() => setLoading(false))
  }, [])

  return (
    
    <View className="flex-1 bg-slate-100 px-4 pt-14">
      <Text className="text-3xl font-bold text-center mb-6 text-slate-800">
        Proveedores
      </Text>

      {loading ? (
        <View className="flex-1 justify-center items-center">
          <ActivityIndicator size="large" color="#1e293b" />
        </View>
      ) : (
        <FlatList
          data={proveedores}
          keyExtractor={(item) => item.id.toString()}
          showsVerticalScrollIndicator={false} 
          renderItem={({ item }) => (
            <View className="bg-white p-5 rounded-2xl mb-4 shadow-sm border border-slate-200">
              <Text className="text-xl font-bold text-slate-900 mb-1">
                {item.nombre}
              </Text>
              <View className="space-y-1">
                <Text className="text-slate-500 font-medium">NIT: {item.nit}</Text>
                <Text className="text-slate-600">📍 {item.direccion}</Text>
                <Text className="text-slate-600">📞 {item.telefono}</Text>
              </View>
            </View>
          )}
          
          ListEmptyComponent={() => (
            <Text className="text-center text-slate-400 mt-10">No hay proveedores registrados</Text>
          )}
        />
      )}
    </View>
  )
}
