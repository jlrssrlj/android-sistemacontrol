import API from "../../api/axios";

export interface Producto {
  id: number;
  nombre: string;
  descripcion: string;
  precio: number;
  stock: number;
  categoria: number;   
  proveedor: number;   
}

export const getProducto = async (): Promise<Producto[]> => {
  const res = await API.get("/productos/");
  return res.data;
};

export const createProducto = async (producto: Omit<Producto, "id">) => {
  return API.post("/productos/", producto);
};

export const updateProducto = async (
  id: number,
  producto: Omit<Producto, "id">
) => {
  return API.put(`/productos/${id}/`, producto);
};

export const deleteProducto = async (id: number) => {
  return API.delete(`/productos/${id}/`);
};