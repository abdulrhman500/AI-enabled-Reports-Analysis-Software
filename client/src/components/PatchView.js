import * as React from 'react';
import { useState, useEffect } from 'react';
import { alpha } from '@mui/material/styles';
import DoneAllIcon from '@mui/icons-material/DoneAll';
import { visuallyHidden } from '@mui/utils';
import { Button, Checkbox, Paper, Typography, Toolbar, TableSortLabel, TableRow, TableHead, TableContainer, TableCell, TableBody, Table, Box, Card, CardContent, Grid, ListItem, ListItemText, Collapse, List, Tooltip } from '@mui/material';
import { getComparator, stableSort, headCells} from '../utils/PatchUtils'
import { useParams } from 'react-router-dom';
import swal from 'sweetalert2'
import { api } from '../utils/AxiosUtils';
import Loading from './Loading';
import { formatDistanceToNow, format } from 'date-fns';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import { BarChart } from '@mui/x-charts/BarChart';
import AdminPatchDial from './AdminPatchDial';
import ChangeVerdict from './ChangeVerdict';

const valueFormatter = (value) => `${value} report`;


const EnhancedTableHead = (props) => {
  const { onSelectAllClick, order, orderBy, numSelected, rowCount, onRequestSort, puplished } =
    props;
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow>
       
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={'center'}
            padding={headCell.disablePadding ? 'none' : 'normal'}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : 'asc'}
              onClick={createSortHandler(headCell.id)}
              sx={{color:'darkgoldenrod',marginLeft:"18px"}}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <Box component="span" sx={visuallyHidden}>
                  {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
         {!puplished && <TableCell padding="checkbox">
          <Checkbox
            color="primary"
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
            inputProps={{
              'aria-label': 'select all desserts',
            }}
          />
        </TableCell>}
      </TableRow>
    </TableHead>
  );
}

function EnhancedTableToolbar(props) {
  const { numSelected, setOpenEdit } = props;
  return (
    <Toolbar
      sx={{
        pl: { sm: 2 },
        pr: { xs: 1, sm: 1 },
        ...(numSelected > 0 && {
          bgcolor: (theme) =>
            alpha(theme.palette.primary.main, theme.palette.action.activatedOpacity),
        }),
      }}
    >
      {numSelected > 0 ? (
        <Typography
          sx={{ flex: '1 1 100%' }}
          color="inherit"
          variant="subtitle1"
          component="div"
        >
          {numSelected} selected
        </Typography>
      ) : false}

      {numSelected > 0 ? (
          <Button sx={{width:'200px'}} onClick={()=> setOpenEdit(true)}>
            <DoneAllIcon />Change verdict
          </Button>
          ) : false}
    </Toolbar>
  );
}

export default function PatchView() {
    const [order, setOrder] = React.useState('asc');
    const [orderBy, setOrderBy] = React.useState('calories');
    const [selected, setSelected] = React.useState([]);

    const [patchData,setPatchData] = useState(null)
    const [submissionsData,setSubmissionsData] = useState([])
    const [loading,setLoading] = useState(true)
    const { patch_id } = useParams()
    const [statisticsOpen, setStatisticsOpen] = useState(false)
    const [statistics, setStatistics] = useState([])
    
    const [openEdit, setOpenEdit] = useState(false)

    useEffect(()=>{
      api({
        method: 'get',
        url: `/user/patch/${patch_id}/data`,
      }).then((res)=>{
        if (!res.data.error) {
          // console.log(res.data);
          setPatchData(res.data.patch)
          let temp = []
          let accepted = 0
          let falseAccepted = 0
          let rejected = 0
          let falseRejected = 0
          res.data.submissions.forEach(sub => {
            if (sub.judgement) accepted++
            else rejected++
            if (sub.judgement && ['Rejected','Pending'].includes(sub.verdict)) falseAccepted++
            if (!sub.judgement && ['Approved'].includes(sub.verdict)) falseRejected++

            let id_str = `${sub.student.user_id}`
              if (id_str.length >= 2) {
              const leftmostTwoDigits = id_str.slice(0, 2);
              const remainingDigits = id_str.slice(2);
              
              id_str = `${leftmostTwoDigits}-${remainingDigits}`;
            }
            let row = {name:sub.student.username, id:id_str,filename:sub.file_upload, judgement:sub.judgement? "Approved":"Rejected",verdict:sub.verdict,subId: sub.id, note: sub.note}
            temp.push(row)
          });
          setSubmissionsData(temp)
          setStatistics([{
            accepted,
            rejected,
            falseAccepted,
            falseRejected,
            total: accepted + rejected,
            type: res.data.patch.semester,
          }])
          setLoading(false)
        }
        else {
          swal.fire('Server Error', 'Error', 'error');
          setLoading(false)
        }
      }).catch((error)=>{
        console.log(error);
        setLoading(false)
        swal.fire('Server Error', 'Error', 'error');
      })
    },[patch_id])


    const handleRequestSort = (event, property) => {
      const isAsc = orderBy === property && order === 'asc';
      setOrder(isAsc ? 'desc' : 'asc');
      setOrderBy(property);
    };

    const handleSelectAllClick = (event) => {
        if (event.target.checked) {
          const newSelected = submissionsData.map((n) => n.subId);
          setSelected(newSelected);
          return;
        }
        setSelected([]);
    };

    const handleClick = (event, subId) => {
        const selectedIndex = selected.indexOf(subId);
        let newSelected = [];
        if (selectedIndex === -1) {
          newSelected = newSelected.concat(selected, subId);
        } else if (selectedIndex === 0) {
          newSelected = newSelected.concat(selected.slice(1));
        } else if (selectedIndex === selected.length - 1) {
          newSelected = newSelected.concat(selected.slice(0, -1));
        } else if (selectedIndex > 0) {
          newSelected = newSelected.concat(
            selected.slice(0, selectedIndex),
            selected.slice(selectedIndex + 1),
          );
        }
        setSelected(newSelected);
    };

    const isSelected = (subId) => selected.indexOf(subId) !== -1;

    const visibleRows = React.useMemo(
      () =>
        stableSort(submissionsData, getComparator(order, orderBy)).slice(0,submissionsData.length),
      [order, orderBy, submissionsData],
    );

    if (loading) return (<Loading />)
    if ( !patchData ) return( false )
    return (
      <Box sx={{ width: '100%' }}>
        <Card sx={{marginBottom:'20px'}}>
          <CardContent sx={{display:'flex',flexDirection:'column',padding:'10px 20px'}} >
            <Grid container gap={2}>
              <Grid item xs={12}>
                <Typography textAlign={'center'}variant="h5" color='gray'>{patchData.semester} Patch</Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography textAlign={'center'} variant="h6" color={patchData.open? "green":'#AB4B52'}>{(patchData.processed)?  "Finalized": patchData.open?  "Open" : (new Date(patchData.start_date) < new Date())? "Closed":"Scheduled"}</Typography>
              </Grid>
              {
                (new Date(patchData.start_date) < new Date())?
                  <Grid item xs={12} >
                    <Typography textAlign={'center'}>Opened <span style={{color:'Highlight'}}>{formatDistanceToNow(new Date(patchData.start_date), { addSuffix: true })}</span> <span style={{color:'gray'}}>({format(new Date(patchData.start_date), 'MMM do yy')})</span></Typography>
                </Grid>
                : 
                <Grid item xs={12} >
                <Typography textAlign={'center'}>Openes in <span style={{color:'Highlight'}}>{formatDistanceToNow(new Date(patchData.start_date))}</span> <span style={{color:'gray'}}>({format(new Date(patchData.start_date), 'MMM do yy')})</span></Typography>
            </Grid>
              }
              {
                (new Date(patchData.close_date) > new Date())?
                <Grid item xs={12}>
                  <Typography textAlign={'center'}>Closes in <span style={{color:'darkcyan'}}>{formatDistanceToNow(new Date(patchData.close_date))}</span> <span style={{color:'gray'}}>({format(new Date(patchData.close_date), 'MMM do yy')})</span></Typography>
                </Grid>
                : false
              }
              <Grid item xs={12} >
                <Box>
                  <ListItem sx={{ py: 2, px: 3 }} onClick={() => setStatisticsOpen(!statisticsOpen)}>
                    <ListItemText sx={{textAlign:'center', color:'maroon',marginLeft:'24px'}}>Patch Statistics
                    </ListItemText>
                    {statisticsOpen? <ExpandLessIcon /> : <ExpandMoreIcon />}
                  </ListItem>
                  <Collapse in={statisticsOpen} timeout='auto'>
                    <List>
                      <ListItem disablePadding>
                        <BarChart
                          dataset={statistics}
                          xAxis={[{ scaleType: 'band', dataKey: 'type' }]}
                          series={[
                            { dataKey: 'accepted', label: 'Accepted', valueFormatter },
                            { dataKey: 'rejected', label: 'Rejected', valueFormatter },
                            { dataKey: 'falseAccepted', label: 'False accepted', valueFormatter },
                            { dataKey: 'falseRejected', label: 'False rejected', valueFormatter },
                            { dataKey: 'total', label: 'Total submissions', valueFormatter },
                          ]}
                          colors={['green','orange','darkcyan','red','purple']}
                          yAxis={[
                              {
                              label: 'Reports',
                              max: ( statistics[0].total+ 10) - (statistics[0].total + 10) % 10
                              },
                          ]}
                          width={ 800 }
                          height={ 300 }
                        />
                      </ListItem>
                    </List>
                  </Collapse>
                  </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
        <Paper sx={{ width: '100%', mb: 2 }}>
          <EnhancedTableToolbar numSelected={selected.length} patch={patchData.semester} setOpenEdit={setOpenEdit} />
          <TableContainer>
            <Table
              sx={{ minWidth: 750 }}
              aria-labelledby="tableTitle"
              size={'medium'}
            >
              <EnhancedTableHead
                numSelected={selected.length}
                order={order}
                orderBy={orderBy}
                onSelectAllClick={handleSelectAllClick}
                onRequestSort={handleRequestSort}
                rowCount={submissionsData.length}
                puplished={patchData.processed}
              />
              <TableBody>
                {visibleRows.map((row, index) => {
                  const isItemSelected = isSelected(row.subId);
                  const labelId = `enhanced-table-checkbox-${index}`;

                  return (
                    <Tooltip title={row.note? row.note : "No note"}>
                    <TableRow
                      hover
                      onClick={(event) => handleClick(event, row.subId)}
                      role="checkbox"
                      aria-checked={isItemSelected}
                      tabIndex={-1}
                      key={row.subId}
                      selected={isItemSelected}
                      sx={{ cursor: 'pointer' }}
                    >
                      <TableCell align="center" component="th" id={labelId} scope="row" padding="none"> {row.name}</TableCell>
                      <TableCell align="center">{row.id}</TableCell>
                      <TableCell align="center">{row.filename}</TableCell>
                      <TableCell align="center"><Typography color={row.judgement=='Accepted'? 'darkcyan': '#AA4A44' }>{row.judgement}</Typography></TableCell>
                      <TableCell align="center"><Typography color={row.verdict=='Approved'? 'darkcyan': '#AA4A44' }>{row.verdict}</Typography></TableCell>
                      {!patchData.processed && 
                      <TableCell padding="checkbox">
                        <Checkbox
                          color="primary"
                          checked={isItemSelected}
                          inputProps={{
                            'aria-labelledby': labelId,
                          }}
                        />
                      </TableCell>}
                    </TableRow>
                    </Tooltip>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
        <AdminPatchDial patchData={patchData} submissionsData={submissionsData}/>
        <ChangeVerdict openEdit={openEdit} setOpenEdit={setOpenEdit} selected={selected} patchData={patchData} submissionsData={submissionsData} />
      </Box>
    );
}