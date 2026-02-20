import React, { createContext, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { loginRequest } from "../api/Auth.service";

interface AuthContextProps {
  userToken: string | null;
  rol: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextProps>(
  {} as AuthContextProps
);

export const AuthProvider = ({ children }: any) => {
  const [userToken, setUserToken] = useState<string | null>(null);
  const [rol, setRol] = useState<string | null>(null);

  const login = async (username: string, password: string) => {
    const data = await loginRequest(username, password);

    await AsyncStorage.setItem("token", data.access);
    await AsyncStorage.setItem("rol", data.rol);

    setUserToken(data.access);
    setRol(data.rol);
  };

  const logout = async () => {
    await AsyncStorage.multiRemove(["token", "rol"]);
    setUserToken(null);
    setRol(null);
  };

  return (
    <AuthContext.Provider value={{ userToken, rol, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};