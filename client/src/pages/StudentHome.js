import * as React from 'react';
import { styled } from '@mui/material/styles';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import { Suspense } from 'react';
import StudentPdfUpload from "../components/StudentPdfUpload";
import PreviousReports from "../components/PreviousReports";
function CustomTabPanel(props) {
    const { children, value, index, ...other } = props;
  
    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && (
          <Box sx={{ p: 3 }}>
            <Typography component="div">{children}</Typography>
          </Box>
        )}
      </div>
    );
  }
  
  CustomTabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.number.isRequired,
    value: PropTypes.number.isRequired,
  };
 
const StyledTabs = styled((props) => (
  <Tabs
    {...props}
    TabIndicatorProps={{ children: <span className="MuiTabs-indicatorSpan" /> }}
  />
))({
  '& .MuiTabs-indicator': {
    display: 'flex',
    justifyContent: 'center',
    backgroundColor: 'transparent',
  },
  '& .MuiTabs-indicatorSpan': {
    maxWidth: 40,
    width: '100%',
    backgroundColor: '#03b5d2',
  },
  '& .MuiTabScrollButton-horizontal': {
    color:'gray',
  },
});

const StyledTab = styled((props) => <Tab disableRipple {...props} />)(
  ({ theme }) => ({
    textTransform: 'none',
    fontWeight: theme.typography.fontWeightRegular,
    fontSize: theme.typography.pxToRem(15),
    marginRight: theme.spacing(1),
    color: '#fff',
    '&.Mui-selected': {
      color: 'rgb(79,195,247)',
    },
    '&.Mui-focusVisible': {
      backgroundColor: 'rgba(100, 95, 228)',
    },
  }),
);

export default function TabsSkeleton({selectedTap}) {
  const [value, setValue] = useState( selectedTap? selectedTap : 0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  useEffect(()=>{
    setValue(selectedTap? selectedTap : 0)
  },[selectedTap])

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ maxHeight:'60px',bgcolor: '#101F33' }}>
        <StyledTabs
          value={value}
          onChange={handleChange}
          variant="scrollable"
          scrollButtons
          allowScrollButtonsMobile
          aria-label="styled tabs example"
        >
          {['Upload report','Previous reports'].map((tapName,index)=><StyledTab key={index} label={tapName}/>)}
        </StyledTabs>
        <Box sx={{ p: 3 }} />
      </Box>
      {[StudentPdfUpload,PreviousReports].map((Component,index)=><CustomTabPanel key={index} value={value} index={index}><Suspense><Component setTap={setValue}/></Suspense></CustomTabPanel>)}
    </Box>
  );
}