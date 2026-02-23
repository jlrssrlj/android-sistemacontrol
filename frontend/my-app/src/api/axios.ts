import axios from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";

const API = axios.create({
    /*baseURL: "http://192.168.20.67:8000/api",*/
    baseURL: "http://10.9.220.219:8000/api",
    headers:{
        "Content-Type":"application/json",
    },
});
API.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default API;