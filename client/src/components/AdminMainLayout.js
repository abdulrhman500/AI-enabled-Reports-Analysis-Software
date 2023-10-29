import React, { useEffect } from "react";
import { Box, ThemeProvider, CssBaseline } from "@mui/material";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useState } from "react";
import Navigator from "./AdminNavigator.js";
import Header from "./Header";
import theme from "../theme.js";
import { useUserContext } from "../hooks/useUserContext.js";
import Loading from "./Loading.js";
import { Navigate, Outlet } from "react-router-dom";
import { api } from "../utils/AxiosUtils.js";

const AdminMainLayout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const isSmUp = useMediaQuery('(min-width:600px)');
  const {user} = useUserContext()
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };
  const [patchData, setPatchData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    if (!patchData){
      api({
        method: 'get',
        url: '/user/patch',
      }).then((res)=>{
        if (res.data.data) {
          console.log(res.data.data);
          setPatchData(res.data.data)
          setLoading(false)
        }
        else {
          setLoading(false)
          setPatchData([])
        }
      }).catch((error)=>{
        console.log(error);
        setLoading(false)
      })
    }
  },[])

  const drawerWidth = 256;
  if(!user) return <Loading />
  else if(!user.username) return (<Navigate to="/login" />)
  else if( user.username) return (
    <div>
        <ThemeProvider theme={theme}>
        <Box sx={{ display: "flex", minHeight: "100vh" }}>
          <CssBaseline />
          {!loading? <Box
            component="nav"
            sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
          >
            {isSmUp ? null : (
              <Navigator
                PaperProps={{ style: { width: drawerWidth } }}
                variant="temporary"
                open={mobileOpen}
                onClose={handleDrawerToggle}
                patchData={patchData}
              />
            )}

            <Navigator
              PaperProps={{ style: { width: drawerWidth } }}
              sx={{ display: { sm: "block", xs: "none" } }}
              patchData={patchData}
            />
          </Box> : false}

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

export default AdminMainLayout;
