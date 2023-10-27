import React from "react";
import { Box, ThemeProvider, CssBaseline } from "@mui/material";
import { useState } from "react";
import Header from "./Header.js";
import theme from "../theme.js";
import { useUserContext } from "../hooks/useUserContext.js";
import Loading from "./Loading.js";
import { Navigate, Outlet } from "react-router-dom";

const StudentMainLayout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const {user} = useUserContext()
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };
  if(!user) return <Loading />
  else if(!user.username) return (<Navigate to="/login" />)
  else if( user.username) return (
    <div>
        <ThemeProvider theme={theme}>
        <Box sx={{ display: "flex", minHeight: "100vh" }}>
          <CssBaseline />
          <Box sx={{ flex: 1, display: "flex", flexDirection: "column" }}>
            <Header onDrawerToggle={handleDrawerToggle}/>
            <div style={{margin:'calc(2% + 48px) 2% 2% 2%'}}>
                <Outlet />
            </div>
          </Box>
        </Box>
        </ThemeProvider>
    </div>
  );
};

export default StudentMainLayout;
