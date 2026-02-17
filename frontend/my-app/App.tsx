import { useState } from 'react';
import { View, TextInput, Button, Text, ActivityIndicator } from 'react-native';
import "./global.css";

interface LoginResponse {
  access: string;
  refresh: string;
  empleado_id: number;
  rol: string;
}

export default function LoginScreen() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    try {
      setMessage('');
      setLoading(true);

      const res = await fetch('http://192.168.1.2:8000/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const data: LoginResponse | { error: string } = await res.json();

      if (!res.ok) {
        setMessage((data as { error: string }).error || 'Login fallido');
        return;
      }

      setMessage(`Login exitoso! Bienvenido, rol: ${(data as LoginResponse).rol}`);
    } catch (err: any) {
      setMessage('Error de conexión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="justify-center flex-1 px-4 bg-slate-100">
      <Text className="mb-6 text-2xl font-bold text-center">Login</Text>

      <TextInput
        placeholder="Usuario"
        value={username}
        onChangeText={setUsername}
        className="p-3 mb-3 bg-white border rounded"
      />

      <TextInput
        placeholder="Contraseña"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        className="p-3 mb-3 bg-white border rounded"
      />

      {loading ? (
        <ActivityIndicator size="large" color="#1e293b" className="my-3" />
      ) : (
        <Button title="Iniciar sesión" onPress={handleLogin} />
      )}

      {message && (
        <Text className="mt-4 text-center text-slate-700">{message}</Text>
      )}
    </View>
  );
}
