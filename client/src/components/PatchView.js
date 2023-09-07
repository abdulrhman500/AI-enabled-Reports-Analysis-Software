import * as React from 'react';
import { useEffect } from 'react';
import PropTypes from 'prop-types';
import { alpha } from '@mui/material/styles';
import DoneAllIcon from '@mui/icons-material/DoneAll';
import FilterListIcon from '@mui/icons-material/FilterList';
import { visuallyHidden } from '@mui/utils';
import { Button, Tooltip, IconButton, Checkbox, Paper, Typography, Toolbar, TableSortLabel, TableRow, TableHead, TableContainer, TableCell, TableBody, Table, Box } from '@mui/material';
import { getComparator, stableSort, headCells} from '../utils/PatchUtils'
import { useParams } from 'react-router-dom';
const rows = [
    {name:'Abdelrahman Saleh Hassan Saleh 01',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'accepted'},
    {name:'Abdelrahman Saleh Hassan Saleh 02',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'accepted'},
    {name:'Abdelrahman Saleh Hassan Saleh 03',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'accepted'},
    {name:'Abdelrahman Saleh Hassan Saleh 04',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'accepted'},
    {name:'Abdelrahman Saleh Hassan Saleh 05',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'accepted'},
    {name:'Abdelrahman Saleh Hassan Saleh 06',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'accepted'},
    {name:'Abdelrahman Saleh Hassan Saleh 07',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'rejected'},
    {name:'Abdelrahman Saleh Hassan Saleh 08',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'rejected'},
    {name:'Abdelrahman Saleh Hassan Saleh 09',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'rejected'},
    {name:'Abdelrahman Saleh Hassan Saleh 10',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'rejected'},
    {name:'Abdelrahman Saleh Hassan Saleh 11',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'rejected'},
    {name:'Abdelrahman Saleh Hassan Saleh 12',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'rejected'},
    {name:'Abdelrahman Saleh Hassan Saleh 13',id:'52-11256',filename:'Abdelrahman Saleh Hassan Saleh  52-11256 - Abdelrahman Saleh',judgement:'rejected'},
];
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
  const { numSelected, patch } = props;
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
      ) : (
        <Typography
          sx={{ flex: '1 1 100%' }}
          variant="h6"
          id="tableTitle"
          component="div"
          color={'GrayText'}
          marginLeft={'15px'}
        >
          {`${patch.charAt(0).toUpperCase()}${patch.replace('-',' ').substring(1)}`}
        </Typography>
      )}

      {numSelected > 0 ? (
          <Button sx={{width:'200px'}}>
            <DoneAllIcon />Change status
          </Button>
          ) : (
        <Tooltip title="Filter list">
          <IconButton>
            <FilterListIcon />
          </IconButton>
        </Tooltip>
      )}
    </Toolbar>
  );
}

export default function EnhancedTable() {
    const [order, setOrder] = React.useState('asc');
    const [orderBy, setOrderBy] = React.useState('calories');
    const [selected, setSelected] = React.useState([]);
    const [puplished, setPuplished] = React.useState(true)

    const { patch } = useParams()
    const handleRequestSort = (event, property) => {
      const isAsc = orderBy === property && order === 'asc';
      setOrder(isAsc ? 'desc' : 'asc');
      setOrderBy(property);
    };

    const handleSelectAllClick = (event) => {
        if(puplished) return
        if (event.target.checked) {
          const newSelected = rows.map((n) => n.name);
          setSelected(newSelected);
          return;
        }
        setSelected([]);
    };

    const handleClick = (event, name) => {
        if(puplished) return
        const selectedIndex = selected.indexOf(name);
        let newSelected = [];
        if (selectedIndex === -1) {
          newSelected = newSelected.concat(selected, name);
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

    const isSelected = (name) => selected.indexOf(name) !== -1;

    const visibleRows = React.useMemo(
      () =>
        stableSort(rows, getComparator(order, orderBy)).slice(0,rows.length),
      [order, orderBy],
    );
    useEffect(()=>{
      if(patch=='winter-23') setPuplished(false)
      else setPuplished(true)
    },[patch])

    return (
      <Box sx={{ width: '100%' }}>
        <Paper sx={{ width: '100%', mb: 2 }}>
          <EnhancedTableToolbar numSelected={selected.length} patch={patch} puplished={puplished} />
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
                rowCount={rows.length}
                puplished={puplished}
              />
              <TableBody>
                {visibleRows.map((row, index) => {
                  const isItemSelected = isSelected(row.name);
                  const labelId = `enhanced-table-checkbox-${index}`;

                  return (
                    <TableRow
                      hover
                      onClick={(event) => handleClick(event, row.name)}
                      role="checkbox"
                      aria-checked={isItemSelected}
                      tabIndex={-1}
                      key={row.name}
                      selected={isItemSelected}
                      sx={{ cursor: 'pointer' }}
                    >
                      <TableCell align="center" component="th" id={labelId} scope="row" padding="none"> {row.name}</TableCell>
                      <TableCell align="center">{row.id}</TableCell>
                      <TableCell align="center">{row.filename}</TableCell>
                      <TableCell align="center"><Typography color={row.judgement=='accepted'? 'Highlight': 'red' }>{row.judgement}</Typography></TableCell>
                      {!puplished && 
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
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>

      </Box>
    );
}