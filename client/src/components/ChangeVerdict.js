import { styled } from "@mui/material/styles";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import { DialogContent, DialogActions, Autocomplete, Typography, Button, IconButton, TextField, Box } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { useEffect, useRef, useState } from "react";
import { api } from "../utils/AxiosUtils";
import swal from 'sweetalert2'

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
    "& .MuiDialogContent-root": {
      padding: theme.spacing(2),
    },
    "& .MuiDialogActions-root": {
      padding: theme.spacing(1),
    },
  }));
const ChangeVerdict = ({openEdit, setOpenEdit, selected, patchData ,submissionsData}) => {
    const editRef = useRef()
    const [changed, setChanged] = useState()
    const [processing, setProcessing] = useState(false)
    const [note, setNote] = useState('')
    const [verdict, setVerdict] = useState('')
    
    const reload = () => window.location.reload(false);

    const handleClose = () => {
        setOpenEdit(false)
        setNote('')
        setChanged(false)
        setVerdict('')
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        setProcessing(true)
        api({url:`/user/patch/${patchData.id}/update`,method:'post',data: {sub_ids:selected, note , verdict}}).then((res)=>{
            setProcessing(false)
            setOpenEdit(false)
            setChanged(false)
            swal.fire(res.data.message, 'Successful', 'success');
            setTimeout( reload, 3000)
        }).catch((error)=>{
            setProcessing(false)
            setChanged(false)
            console.log(error);
            swal.fire({target:editRef.current,title:'Failed to resume patch', text: error.response.data.error? error.response.data.error:"Server error", icon:'error'});
        })
    }

    useEffect(()=>{
        if (submissionsData && submissionsData.length > 0) {
            let tempNote = submissionsData[0].note
            let tempVerdict = submissionsData[0].verdict
            
            submissionsData.forEach(sub => {
                if (tempNote != sub.note) tempNote =''
                if (tempVerdict != sub.verdict) tempVerdict =''
            });
            setNote(tempNote)
            setVerdict(tempVerdict)
        }
    },[selected,submissionsData])
    return (
        <BootstrapDialog
          ref={editRef}
          onClose={changed? ()=>{} : handleClose}
          aria-labelledby="customized-dialog-title"
          open={openEdit}
          fullWidth
        >
            <DialogTitle sx={{ textAlign: 'center' }} id="customized-dialog-title">
                Change verdict
            </DialogTitle>
            <IconButton
            aria-label="close"
            onClick={handleClose}
            sx={{
                position: "absolute",
                right: 8,
                top: 8,
                color: (theme) => theme.palette.grey[500],
            }}
            >
            <CloseIcon />
            </IconButton>
            <DialogContent>
            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
              <Autocomplete
                id="verdict"
                key="verdict"
                options={['Approved','Rejected','Pending']}
                required
                value={verdict}
                onChange={(event, newValue) => {
                    setVerdict(newValue);
                    setChanged(true)
                }}
                isOptionEqualToValue={(option, value) => value? option.toString() === value.toString() : true}
                renderInput={(params) => <TextField margin="normal" {...params} key={"verdict"} name={"verdict"} required onInvalid={(e)=>{(e.target.value.toString==='')? e.target.setCustomValidity("Please select a verdict"):e.target.setCustomValidity('');}} label={'Verdict'} />}
              />
              <TextField
                fullWidth
                id="note"
                value={note}
                onChange={e => {setNote(e.target.value); setChanged(true);}}
                label="Note"
                name="note"
                margin="normal"
              />
              <Typography textAlign={'center'} color={'gray'} mt={'10px'} >*All selected submissions will be updated by this action</Typography>
            <Button sx={{display:'block', width:'150px', margin:'15px auto 10px auto'}} type = "submit" disabled={processing} >
                Confirm
            </Button>
            </Box>
            </DialogContent>
            <DialogActions>

            </DialogActions>
        </BootstrapDialog>
    );
}
 
export default ChangeVerdict;