import { useState } from "react";
import { useUserContext } from "./useUserContext";
export const useLogin = () => {
    const [error,setError] = useState(null)
    const [isLoading,setIsLoading] = useState('')
    const {dispatch} = useUserContext()
    const login = async (email,password) =>{
        setIsLoading(true)
        setError(null)
        let success = false
        if(email == 'osama'){
            if(password == '123'){
                await dispatch({type:'LOGIN',payload:{name:'Osama Hossiny', role: "admin"}})
                success = true
            } else setError('Wrong Password')
        }
        else {
            setError('Invalid user name')
        }
        return success
    }
    return {login, isLoading, error}
}