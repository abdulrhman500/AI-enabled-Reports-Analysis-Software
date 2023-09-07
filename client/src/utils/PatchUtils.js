const descendingComparator = (a, b, orderBy) => {
    if (b[orderBy] < a[orderBy]) {
      return -1;
    }
    if (b[orderBy] > a[orderBy]) {
      return 1;
    }
    return 0;
  }
  
export const getComparator = (order, orderBy) => {
    return order === 'desc'
      ? (a, b) => descendingComparator(a, b, orderBy)
      : (a, b) => -descendingComparator(a, b, orderBy);
  }
export const stableSort = (array, comparator) => {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
      const order = comparator(a[0], b[0]);
      if (order !== 0) {
        return order;
      }
      return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
  }
  
export const headCells = [
    {
      id: 'name',
      numeric: false,
      disablePadding: true,
      label: 'Student Name',
    },
    {
      id: 'id',
      numeric: false,
      disablePadding: true,
      label: 'Student ID',
    },
    {
      id: 'filename',
      numeric: false,
      disablePadding: true,
      label: 'File Upload',
    },
    {
      id: 'judgement',
      numeric: false,
      disablePadding: true,
      label: 'Judgement',
    },
];