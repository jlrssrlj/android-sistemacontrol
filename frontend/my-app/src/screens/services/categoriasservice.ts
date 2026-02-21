import API from "../../api/axios";

export interface Categorias {
  id: number;
  nombre: string;
}

export const getCategorias = async (): Promise<Categorias[]> => {
  const res = await API.get("/categorias/");
  return res.data;
};

export const createCategorias = async (nombre: string) => {
  return API.post("/categorias/", { nombre });
};

export const updateCategorias = async (id: number, nombre: string) => {
  return API.put(`/categorias/${id}/`, { nombre });
};

export const deleteCategorias = async (id: number) => {
  return API.delete(`/categorias/${id}/`);
};