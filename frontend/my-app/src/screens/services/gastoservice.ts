import axios from "axios";

const API_URL = "http://192.168.1.2:8000/api/gastos/";

export interface Gasto {
  id?: number;
  descripcion: string;
  valor: number;
  fecha: string;
}

export const getGastos = async (): Promise<Gasto[]> => {
  const response = await axios.get<Gasto[]>(API_URL);
  return response.data;
};

export const createGasto = async (gasto: Gasto): Promise<Gasto> => {
  const response = await axios.post<Gasto>(API_URL, gasto);
  return response.data;
};
