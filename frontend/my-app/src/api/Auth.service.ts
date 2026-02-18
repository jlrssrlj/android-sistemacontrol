import API from "./axios";
import { LoginResponse } from "../types/auth.types";

export const loginRequest = async(
    username: string,
    password: string
): Promise<LoginResponse> =>{
    const response = await API.post("/login/",{
        username,
        password,
    });
    return response.data
}