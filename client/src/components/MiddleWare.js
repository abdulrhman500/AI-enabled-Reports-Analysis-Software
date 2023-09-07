import { useEffect } from "react";
import { useUserContext } from "../hooks/useUserContext";
import Loading from "./Loading";
import { Outlet, Navigate } from "react-router-dom";

const MiddleWare = ({type}) => {
    const { user } = useUserContext()

    if(!user) return(<Loading/>)
    else if(user.type == 'Admin' && type !== "Admin"){
        return (<Navigate to="/admin" />)
    }
    else if(user.type == 'Student' && type !== "Student"){
        return (<Navigate to="/student" />)
    }
    else if(!user.type && type !== "Login"){
        return (<Navigate to="/login" />)
    } 
    else return(<Outlet/>)
}
export default MiddleWare