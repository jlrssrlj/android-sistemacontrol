import API from "../../api/axios";

export const getVentas = async () => {
  const response = await API.get("/ventas/");
  return response.data;
};

export const createVenta = async (data: any) => {
  const response = await API.post("/ventas/", data);
  return response.data;
};

export const deleteVenta = async (id: number) => {
  await API.delete(`/ventas/${id}/`);
};
