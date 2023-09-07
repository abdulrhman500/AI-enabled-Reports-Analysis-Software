import { useState } from "react";
import { useUserContext } from "./useUserContext";
import { http } from "../utils/AxiosUtils";
export const useLogin = () => {
    const [error,setError] = useState(null)
    const [isLoading,setIsLoading] = useState('')
    const {dispatch} = useUserContext()
    const login = async (email,password) =>{
        setIsLoading(true)
        setError(null)
        let success = false
        await http.post(
            "/user/login",
            {
              email: email,
              password: password
            }
          ).then( async (res)=> {
            success = true
            await dispatch({type:'LOGIN',payload:res.data})
        }).catch((error)=>{
            console.log(error);
            setError(error.response.data.error)
          });
        return success
    }
    return {login, isLoading, error}
}