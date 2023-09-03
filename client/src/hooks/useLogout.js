import { useUserContext } from "./useUserContext"
export const useLogout = () => {
    const { dispatch } = useUserContext()
    const logout = async () => {
        await dispatch({ type: 'LOGOUT' })        
        return true
    }
    return { logout }
}