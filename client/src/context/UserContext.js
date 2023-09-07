import { createContext, useReducer, useState } from "react";
import { http } from "../utils/AxiosUtils";
export const UserContext = createContext()

export const userReducer = (state, action) => {
    switch (action.type) {
        case 'LOGIN':
            return { user: action.payload }
        case 'RESTORE':
            return { user: action.payload }
        case 'LOGOUT':
            return { user: {name:'',type:''} }
        default:
            return state
    }
}

export const UserContextProvider = ({ children }) => {
    const [state, dispatch] = useReducer(userReducer, { user: null })
    const [loading, setLoading] = useState(false)
    if(!state.user){
        http({method:'get',url:'/user/user',withCredentials:true}).then((response)=>{
                console.log(response.data.user);
                dispatch({type:'RESTORE',payload: response.data.user})
                setLoading(false)
            }).catch((error)=>{
                setLoading(false)
                dispatch({type:'RESTORE',payload:{name:'',type:''}})
            })
    }
    return (
        <UserContext.Provider value={{ ...state, dispatch, loading }}>
            {children}
        </UserContext.Provider>
    )
}
