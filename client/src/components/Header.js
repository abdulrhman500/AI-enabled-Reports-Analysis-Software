import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import IconButton from '@mui/material/IconButton';
import Grid from '@mui/material/Grid';
import MenuIcon from '@mui/icons-material/Menu';
import NotificationsIcon from '@mui/icons-material/Notifications';
import Toolbar from '@mui/material/Toolbar';
import { Tooltip } from '@mui/material';
import AccountMenu from './AccountMenu';
import Badge from '@mui/material/Badge';
import { useUserContext } from '../hooks/useUserContext';
import { useNavigate } from 'react-router-dom';


function Header(props) {


  const { onDrawerToggle } = props;
  const navigate = useNavigate()
  const {user} =useUserContext()

  return (
    <React.Fragment>
      <AppBar color="primary" position="fixed" elevation={0}>
        <Toolbar>
          <Grid container spacing={1} alignItems="center">
            <Grid sx={{ display: { sm: 'none', xs: 'block' } }} item>
              <IconButton
                color="inherit"
                aria-label="open drawer"
                onClick={onDrawerToggle}
                edge="start"
              >
                <MenuIcon />
              </IconButton>
            </Grid>
            <Grid item></Grid>
            <Grid item xs />

            <AccountMenu />
            
          </Grid>
        </Toolbar>
      </AppBar>
    </React.Fragment>
  );
}

export default Header;
