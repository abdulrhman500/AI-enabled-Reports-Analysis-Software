
import React, { useState } from 'react';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Box from '@mui/material/Box';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';
import TaskAltIcon from '@mui/icons-material/TaskAlt';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import { Link } from 'react-router-dom';
import PendingActionsIcon from '@mui/icons-material/PendingActions';
import { useNavigate } from 'react-router-dom';
import { Collapse } from '@mui/material';
import ScheduleIcon from '@mui/icons-material/Schedule';

const item = {
  py: '2px',
  px: 3,
  color: 'rgba(255, 255, 255, 0.7)',
  '&:hover, &:focus': {
    bgcolor: 'rgba(255, 255, 255, 0.08)',
  },
};

const itemCategory = {
  boxShadow: '0 -1px 0 rgb(255,255,255,0.1) inset',
  py: 1.5,
  px: 3,
};

export default function Navigator(props) {
    const { patchData,...other } = props;
    const categories = [
      {
        id: "Patches",
        children: [],
      },
    ];
    patchData.forEach(patch => {
      let category = {id: patch.semester, patch_id: patch.id, icon: (patch.processed)?  <TaskAltIcon/>: patch.open?  <ScheduleIcon /> : <PendingActionsIcon />  }
      categories[0].children.push(category)
    });
    const [openCategory, setOpenCategory] = useState(null);
    const [activeButton, setActiveButton] = useState('');
    const navigate = useNavigate()
    const handleCategoryToggle = (category) => {
      if (category === openCategory) {
        setOpenCategory(null);
      } else {
        setOpenCategory(category);
      }
    };  
    const handleButtonChange = (newButton) => {
      setActiveButton(newButton);
    };
    const handleHome = () => {
      navigate('/admin/')
    }
    return (
      <Drawer variant="permanent" {...other}>
        <List disablePadding>   
          <ListItem sx={{ ...item, ...itemCategory, fontSize: 22, color: '#fff' }}>
          A.I.E.I.R.A.S
          </ListItem>
          <ListItem onClick={handleHome} sx={{ ...item, ...itemCategory }}>
            <ListItemIcon>
              <HomeIcon />
            </ListItemIcon>
            <ListItemText>Home</ListItemText>
          </ListItem>
          {categories.map(({ id, children }) => (
            <Box key={id} sx={{ bgcolor: '#101F33' }}>
              <ListItem sx={{ py: 2, px: 3 }} onClick={() => handleCategoryToggle(id)}>
                <ListItemText sx={{ color: '#fff' }}>{id}</ListItemText>
                {openCategory === id ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              </ListItem>
                <Collapse in={openCategory === id} timeout='auto'>
                  <List>
                    {children.map(({ id: childId, patch_id, icon }) => (
                      <Link 
                      to={`/admin/patch/${patch_id}/${childId.toLowerCase().replace(' ','-')}`} 
                      replace={true}
                      style={{ textDecoration: 'none' }} key={childId}>
                        <ListItem disablePadding>
                          <ListItemButton onClick={() => handleButtonChange(childId)} selected={activeButton === childId} sx={item}>
                            <ListItemIcon>{icon}</ListItemIcon>
                            <ListItemText>{childId}</ListItemText>
                          </ListItemButton>
                        </ListItem>
                      </Link>
                    ))}
                    <Divider sx={{ mt: 2 }} />
                  </List>
                </Collapse>
            </Box>
          ))}   
        </List>
      </Drawer>
    );
}
