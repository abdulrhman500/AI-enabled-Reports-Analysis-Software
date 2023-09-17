import { useState } from "react";
import { useUserContext } from "./useUserContext";
import { http } from "../utils/AxiosUtils";
export const useRegister = () => {
    const [isLoading,setIsLoading] = useState('')
    const {dispatch} = useUserContext()
    const register = async (email,password,username,user_id) =>{
        setIsLoading(true)
        let success = await http.post(
            "/user/register",
            {
              email,
              username,
              password,
              user_id
              
            }
          ).then( async (res)=> {
            await dispatch({type:'LOGIN',payload:res.data})
            return {message:'success'}
        }).catch((error)=>{
            return {error:error.response.data.error};
          });
        return success
    }
    return {register, isLoading}
}