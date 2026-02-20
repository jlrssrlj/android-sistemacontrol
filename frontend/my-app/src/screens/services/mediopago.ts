import API from "../../api/axios";

export interface MedioPago {
  id: number;
  nombre: string;
}

export const getMediosPago = async (): Promise<MedioPago[]> => {
  const res = await API.get("/mediopagos/");
  return res.data;
};

export const createMedioPago = async (nombre: string) => {
  return API.post("/mediopagos/", { nombre });
};

export const updateMedioPago = async (id: number, nombre: string) => {
  return API.put(`/mediopagos/${id}/`, { nombre });
};

export const deleteMedioPago = async (id: number) => {
  return API.delete(`/mediopagos/${id}/`);
};