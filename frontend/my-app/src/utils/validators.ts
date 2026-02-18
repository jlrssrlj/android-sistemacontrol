export const validateLogin = (username: string, password:string) =>{
    if(!username.trim()){
        return "El usuario es obligatorio";
    }
    if(!password.trim()){
        return "contraseña obligatoria";
    }    
    return null;
}