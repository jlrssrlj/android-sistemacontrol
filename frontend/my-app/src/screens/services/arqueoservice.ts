import API from "../../api/axios"

export interface Arqueo{
    id: number;
    empleado: number;
    fecha_inicio: string;
    fecha_fin?: string | null;
    monto_inicial: string;
    monto_final?: string | null;
    diferencia?: string | null;
}
/* ver arqueos */
export const getArqueo = async(): Promise<Arqueo[]> => {
    const res = await API.get("/arqueos/")
    return res.data;
};

/* abrir arqueo */
export const abrirarqueo = async (monto_inicial: string) =>{
    return API. post("/arqueos/",{
        monto_inicial,
    });
}
/**cerrar */
export const cerrarArqueo = async (
    id:number,
    monto_final: string
) =>{
    return API.put(`/arqueos/${id}/`,{
        monto_final,
    });
};
