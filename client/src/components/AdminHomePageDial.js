import { Autocomplete, Box, Button, Grid, SpeedDial, SpeedDialAction, SpeedDialIcon, TextField, Typography } from "@mui/material";
import LibraryAddIcon from '@mui/icons-material/LibraryAdd';
import EditCalendarIcon from '@mui/icons-material/EditCalendar';
import SaveAltIcon from '@mui/icons-material/SaveAlt';
import SettingsSuggestIcon from '@mui/icons-material/SettingsSuggest';
import SettingsIcon from '@mui/icons-material/Settings';
import IconButton from "@mui/material/IconButton";
import { styled } from "@mui/material/styles";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import CloseIcon from "@mui/icons-material/Close";
import swal from 'sweetalert2'
import { api } from "../utils/AxiosUtils";
import { useRef, useState } from "react";


const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiDialogContent-root": {
    padding: theme.spacing(2),
  },
  "& .MuiDialogActions-root": {
    padding: theme.spacing(1),
  },
}));
const actions = [
  { icon: <LibraryAddIcon />, name: 'Start instant patch', id: 'start' },
  { icon: <EditCalendarIcon />, name: 'Schedual patch', id: 'schedual' },
];
const AdminHomePageDial = () => {
    const [openDialog, setOpenDialog] = useState()
    const [uploading, setUploading] = useState(false)
    const [changed, setChanged] = useState(false) 
    const todaysDate = new Date().toISOString().split("T")[0]
    const dialogRef = useRef()

    const reload = () => window.location.reload(false);

    const handleDial = (id) => {
        setOpenDialog(id)
    }
    const handleCloseDialog = () => {
        setOpenDialog('')
        setChanged(false)
    }
    const handleAddPatch = (e) => {
        e.preventDefault()
        setUploading(true)
        const data = new FormData(e.target)
        const semester = data.get('start_date')? `${data.get('semester')} ${new Date(data.get('start_date')).getFullYear()%100}`:`${data.get('semester')} ${new Date().getFullYear()%100}`
        data.set('semester', semester)
        console.log(data.get('start_date'));
        if(data.get('start_date') && ( new Date(data.get('start_date')) > new Date(data.get('close_date')) )){
            console.log('something');
            swal.fire({target:dialogRef.current,title:'Failed to create patch', text:"Patch close date can not be closer than it's start date", icon:'error'});
            setUploading(false)
            return
        }
        api({url:'/user/patch',method:'post',data}).then((res)=>{
            setOpenDialog('')
            setUploading(false)
            swal.fire('Created patch Successfully', 'Successful', 'success');
            setTimeout( reload, 3000)
            }).catch((error)=>{
              console.log(error);
              setUploading(false)
              swal.fire({target:dialogRef.current,title:'Failed to create patch', text: error.response.data.error? error.response.data.error:"Server error", icon:'error'});
        })
    }

    return (
        <Box>
            <SpeedDial
            ariaLabel="SpeedDial openIcon example"
            sx={{ position: 'fixed', bottom: 16, right: 16 }}
            icon={<SpeedDialIcon icon={<SettingsIcon />} openIcon={<SettingsSuggestIcon />} />}
        >
            {actions.map((action) => (
            <SpeedDialAction
                key={action.name}
                icon={action.icon}
                tooltipTitle={action.name}
                onClick={()=>{handleDial(action.id)}}
            />
            ))}
            </SpeedDial>
            <BootstrapDialog
                ref={dialogRef}
                onClose={(changed || uploading)? ()=>{}:handleCloseDialog}
                aria-labelledby="customized-dialog-title"
                open={['start','schedual'].includes(openDialog)}
                fullWidth
            >
                <DialogTitle sx={{ textAlign: 'center' }} id="customized-dialog-title">
                New Patch
                </DialogTitle>
                <IconButton
                aria-label="close"
                onClick={handleCloseDialog}
                sx={{
                    position: "absolute",
                    right: 8,
                    top: 8,
                    color: (theme) => theme.palette.grey[500],
                }}
                >
                <CloseIcon />
                </IconButton>
                <Grid container spacing={6} component = "form" sx={{padding:'10px'}} onSubmit={handleAddPatch}>
                    <Grid item xs={12} >
                        <Autocomplete
                            id="semester"
                            key="semester"
                            options={['Winter','Spring','Summer','Fall']}
                            required
                            isOptionEqualToValue={(option, value) => value? option.toString() === value.toString() : true}
                            renderInput={(params) => <TextField onChange={()=> {if(!changed) setChanged(true)}} {...params} key={"semester"} name={"semester"} required onInvalid={(e)=>{(e.target.value.toString==='')? e.target.setCustomValidity("Please select a semester"):e.target.setCustomValidity('');}} label={'Patch semester'} />}
                        />
                    </Grid>
                    { openDialog === 'schedual'?
                    <Grid item xs={12} >
                        <TextField
                        label={"Start date"}
                        type='date'
                        name="start_date"
                        InputLabelProps={{
                            shrink: true,
                        }}
                        inputProps={{
                            min: todaysDate,
                        }}
                        required
                        fullWidth
                        onChange={()=> {if(!changed) setChanged(true)}}
                        />
                    </Grid> : false}
                    <Grid item xs={12} >
                        <TextField
                        label={"Close date"}
                        type='date'
                        name="close_date"
                        InputLabelProps={{
                            shrink: true,
                        }}
                        inputProps={{
                            min: todaysDate,
                        }}
                        required
                        fullWidth
                        onChange={()=> {if(!changed) setChanged(true)}}
                        />
                    </Grid>
                    <Button sx={{display:'block', margin:'15px 10px 10px auto'}} type = "submit" disabled={uploading || !changed}>
                    Create patch
                    </Button>
                </Grid>
            </BootstrapDialog>
        </Box>
    );
}
 
export default AdminHomePageDial;