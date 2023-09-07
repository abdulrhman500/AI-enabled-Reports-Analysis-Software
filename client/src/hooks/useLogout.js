import { http } from "../utils/AxiosUtils"
import { useUserContext } from "./useUserContext"
export const useLogout = () => {
    const { dispatch } = useUserContext()
    const logout = async () => {
        let success = false
        await http({ method: "post", url: '/user/logout', withCredentials: true }).then(async () => {
            success = true
            await dispatch({ type: 'LOGOUT' })
        })
        return success
    }
    return { logout }
}