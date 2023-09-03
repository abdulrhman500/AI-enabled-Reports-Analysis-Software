import { createContext, useEffect, useReducer, useState } from "react";

export const UserContext = createContext()

export const userReducer = (state, action) => {
    switch (action.type) {
        case 'LOGIN':
            return { user: action.payload }
        case 'RESTORE':
            return { user: action.payload }
        case 'LOGOUT':
            return { user: null }
        default:
            return state
    }
}

export const UserContextProvider = ({ children }) => {
    const [state, dispatch] = useReducer(userReducer, { user: null })
    const [loading, setLoading] = useState(false)
    useEffect(()=>{
        setLoading(false)
    },[])
    return (
        <UserContext.Provider value={{ ...state, dispatch, loading }}>
            {children}
        </UserContext.Provider>
    )
}
