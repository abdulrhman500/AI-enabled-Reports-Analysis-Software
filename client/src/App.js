import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import PageNotFound from "./components/PageNotFound";
import Home from "./pages/Home";
import LogIn from "./pages/LogIn";
function App() {
  return (
    <Router>
            <Routes >
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<LogIn />} />
              <Route path="*" element={<PageNotFound />} />
            </Routes>
    </Router >
  );
}

export default App;
