import { useUserContext } from "../hooks/useUserContext";
import {Navigate} from 'react-router-dom';
import AdminPdfUpload from '../components/AdminPdfUpload'
import { Typography } from "@mui/material";
const AdminHome = () => {
    const { user } = useUserContext()
    if (user) return ( <div>
        <Typography textAlign={'center'}>Hello {user.username}</Typography>
        {/* <AdminPdfUpload></AdminPdfUpload> */}
    </div> );
    else if(user == null) return ( <Navigate to="/login" />)
    else return ( <Navigate to="/login" />)
}
 
export default AdminHome;