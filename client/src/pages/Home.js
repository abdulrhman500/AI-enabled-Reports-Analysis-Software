import { useUserContext } from "../hooks/useUserContext";
import {Navigate} from 'react-router-dom';
const Home = () => {
    const { user } = useUserContext()
    if (user) return ( <div>
        <h1>hello {user.name}</h1>
    </div> );
    else if(user == null) return ( <Navigate to="/login" />)
    else return ( <Navigate to="/login" />)
}
 
export default Home;