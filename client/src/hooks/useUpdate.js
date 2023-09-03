import { useState } from "react";
import { useUserContext } from "./useUserContext";

export const useUpdate = () => {
    const [error,setError] = useState(null)
    const [isLoading,setIsLoading] = useState('')
    const {dispatch} = useUserContext()
    const update = async (data) =>{
        if(data){
            await dispatch({type:'RESTORE',payload:data})
            return
        }
        setIsLoading(true)
        setError(null)
        let success = false
        // check if logged in logic
        return success
    }
    return {update, isLoading, error}
}