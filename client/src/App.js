import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import PageNotFound from "./components/PageNotFound";
import MainLayout from "./components/MainLayout";
import { Navigate } from "react-router-dom";
import LogIn from "./pages/LogIn";
import AdminHome from "./pages/AdminHome";
import MiddleWare from "./components/MiddleWare";
import PatchView from './components/PatchView'
import Register from "./pages/Register";
import StudentHome from "./pages/StudentHome";
function App() {
  return (
    <Router>
      <Routes >

        <Route exact path="/" element={<MiddleWare type="Guest" />} />

        <Route path="/login" element={<MiddleWare type="Login" />} >
          <Route path="/login" element={<LogIn />} />
        </Route>
      
        <Route path="/register" element={<MiddleWare type="Login" />} >
          <Route path="/register" element={<Register />} />
        </Route>

        <Route path="/admin" element={<MiddleWare type="Admin"/>} >
          <Route path="/admin" element={<MainLayout/>} >
            <Route exact path="/admin/" element={<AdminHome />} />
            <Route exact path="/admin/patch/:patch" element={<PatchView />} />
          </Route>
        </Route>

        <Route path="/student" element={<MiddleWare type="Student"/>} >
          <Route path="/student" element={<MainLayout/>} >
            <Route exact path="/student/" element={<StudentHome />} />
            <Route exact path="/student/patch/:patch" element={<PatchView />} />
          </Route>
        </Route>

        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </Router >
  );
}

export default App;
