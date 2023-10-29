import { Box, Button, DialogActions, DialogContent, SpeedDial, SpeedDialAction, SpeedDialIcon, Typography } from "@mui/material";
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
import { useEffect, useRef, useState } from "react";
import BlindsClosedIcon from '@mui/icons-material/BlindsClosed';
import StopIcon from '@mui/icons-material/Stop';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import DeleteIcon from '@mui/icons-material/Delete';
import * as XLSX from 'xlsx';
import { useNavigate } from "react-router-dom";

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiDialogContent-root": {
    padding: theme.spacing(2),
  },
  "& .MuiDialogActions-root": {
    padding: theme.spacing(1),
  },
}));

const AdminPatchDial = ({patchData, submissionsData}) => {
    const [openDialog, setOpenDialog] = useState()
    const [actions, setActions] = useState([])
    const [processing, setProcessing] = useState(false)
    const navigate = useNavigate()

    const dialogRef = useRef()
    const handleDial = (id) => {
        setOpenDialog(id)
    }
    const handleCloseDialog = () => {
        setOpenDialog('')
    }
    const reload = () => window.location.reload(false);

    const handleClosePatch = () => {
        api({url:`/user/patch/${patchData.id}/close`,method:'post'}).then((res)=>{
            setOpenDialog('')
            setProcessing(false)
            swal.fire(res.data.message, 'Successful', 'success');
            setTimeout( reload, 3000)
        }).catch((error)=>{
            setProcessing(false)
            console.log(error);
            swal.fire({target:dialogRef.current,title:'Failed to close patch', text: error.response.data.error? error.response.data.error:"Server error", icon:'error'});
        })
    }
    const handleFinalizePatch = () => {
        api({url:`/user/patch/${patchData.id}/save`,method:'post'}).then((res)=>{
            setOpenDialog('')
            setProcessing(false)
            swal.fire(res.data.message, 'Successful', 'success');
            setTimeout( reload, 3000)
        }).catch((error)=>{
            setProcessing(false)
            console.log(error);
            swal.fire({target:dialogRef.current,title:'Failed to finalize patch', text: error.response.data.error? error.response.data.error:"Server error", icon:'error'});
        })
    }
    const handleDeletePatch = () => {
        api({url:`/user/patch/${patchData.id}/delete`,method:'post'}).then((res)=>{
            setOpenDialog('')
            swal.fire(res.data.message, 'Successful', 'success');
            setProcessing(false)
            navigate("/admin")
            setTimeout( reload, 3000)
        }).catch((error)=>{
            setProcessing(false)
            console.log(error);
            swal.fire({target:dialogRef.current,title:'Failed to delete patch', text: error.response.data.error? error.response.data.error:"Server error", icon:'error'});
        })
    }

    const handleResuemePatch = () => {
        api({url:`/user/patch/${patchData.id}/resume`,method:'post'}).then((res)=>{
            setOpenDialog('')
            setProcessing(false)
            swal.fire(res.data.message, 'Successful', 'success');
            setTimeout( reload, 3000)
        }).catch((error)=>{
            setProcessing(false)
            console.log(error);
            swal.fire({target:dialogRef.current,title:'Failed to resume patch', text: error.response.data.error? error.response.data.error:"Server error", icon:'error'});
        })
    }

    const handleExportExcel = () => {
        const workbook = XLSX.utils.book_new();
        const worksheet = XLSX.utils.json_to_sheet(submissionsData);
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
        const blob = new Blob([XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })]);
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${patchData.semester}.xlsx`;
        link.click();
        setProcessing(false)
    }

    const handleButtonClick = () => {
        setProcessing(true)
        switch (openDialog) {
            case 'save':
                handleFinalizePatch()
                break;
            case 'delete':
                handleDeletePatch()
                break;
            case 'export':
                handleExportExcel()
                break;
            case 'resume':
                handleResuemePatch()
                break;
            case 'close':
                handleClosePatch()
                break;
            default:
                setProcessing(false)
                break;
        }
    }

    const getDialogTitle = (tag) => {
        let action = actions.find(a => a.id == tag)
        return action && action.name? action.name : ""
    }
    const getDialogMessage = (tag) => {
        let message = ''
        switch (tag) {
            case 'save':
                message = "Finalizing patch results requires the patch to be closed. The patch can not be modified after finalization. Are you sure you want to finalize the patch results?."
                break;
            case 'delete':
                message = "Only patchs that were schedualed to open can be deleted. Are you sure you want to delte this this patch?."
                break;
            case 'export':
                message = "Exporting patch results only accounts for the current state of the patch. Are you sure you want to export the result into excel sheet?."
                break;
            case 'resume':
                message = "Resuming patchs works for patches that were closed prematurely, and were not yet finalized. Are you sure you want to resume this patch?."
                break;
            case 'close':
                message = "Closing a patch prematurely would pause all student uploads and allow you to finalize the patch. Are you sure you want to close this patch?."
                break;
            default:
                break;
        }
        return message
    }

    useEffect(()=>{

        const temp = [
        ];
        if (new Date(patchData.start_date) < new Date()) {
            if (new Date(patchData.close_date) > new Date()) {
                if (patchData.open) {
                    temp.push({ icon: <StopIcon />, name: 'Close patch override', id: 'close' })
                } else if (!patchData.processed) {
                    temp.push({ icon: <PlayArrowIcon />, name: 'Resume patch', id: 'resume' })
                }
            }
        } else {
            temp.push({ icon: <DeleteIcon />, name: 'Delete patch', id: 'delete' })
        }
        if (!patchData.processed) temp.push({ icon: <BlindsClosedIcon />, name: 'Finalize patch results', id: 'save' })
        temp.push({ icon: <SaveAltIcon />, name: 'Export patch results', id: 'export' })
        setActions(temp)
    },[patchData])


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
                onClose={handleCloseDialog}
                aria-labelledby="customized-dialog-title"
                open={openDialog? true : false}
                fullWidth
            >
                <DialogTitle sx={{ textAlign: 'center' }} id="customized-dialog-title">
                    {getDialogTitle(openDialog)}
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
                <DialogContent>
                    <Typography textAlign={'center'}>{getDialogMessage(openDialog)}</Typography>
                </DialogContent>
                <DialogActions>
                <Button sx={{display:'block', width:'150px', margin:'15px auto 10px auto'}} type = "button" onClick={handleButtonClick} disabled={processing}>
                    Confirm
                </Button>

                </DialogActions>
            </BootstrapDialog>
        </Box>
    );
}
 
export default AdminPatchDial;