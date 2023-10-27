import * as React from "react";
import IconButton from "@mui/material/IconButton";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import Button from "@mui/material/Button";
import { styled } from "@mui/material/styles";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import CloseIcon from "@mui/icons-material/Close";
import { Card, CardContent, Grid, TextField } from "@mui/material";
import Typography from "@mui/material/Typography";
import { Box } from "@mui/material";
import UploadIcon from '@mui/icons-material/Upload';
import { useState, useEffect } from "react";
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import swal from 'sweetalert2'
import { api } from "../utils/AxiosUtils";
import Loading from "./Loading";
import NoActivePatch from "./NoActivePatch";
import { formatDistanceToNow } from "date-fns";

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiDialogContent-root": {
    padding: theme.spacing(2),
  },
  "& .MuiDialogActions-root": {
    padding: theme.spacing(1),
  },
}));

export default function StudentPdfUpload() {
  const [pdf, setPdf] = useState();
  const [pdfFile , setPdfFile] = useState("");
  const [uploading, setUploading] = useState(false)
  const [changed, setChanged] = useState(false) 
  const [patch, setPatch] = useState(null)
  const [loading, setLoading] = useState(true)
  const [already, setAlready] = useState(false)
  const [openEdit, setOpenEdit] = useState(false);
  
  const handleCloseEdit = (e) => {
    e.stopPropagation()
    setOpenEdit(false);
    setPdf(null)
    setPdfFile("")
    setChanged(false)
  };

  const handlePdfChange = (file) => {
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPdf(reader.result);
      };
      reader.readAsDataURL(file);

      setPdfFile(file); // Set the pdf file
    }
  };

  const handelClickEdit = () => {
    setOpenEdit(true)
  }

  const handelSubmitEdit = async (e) => {
    e.preventDefault();
    const data = new FormData();
    if (pdf) {
      data.append("file", pdfFile);
    }
    else return
    setUploading(true)
    api({
        method: 'post',
        maxBodyLength: Infinity,
        url: '/user/student-submission',
        data : data,
      }).then((res)=>{
      setChanged(false)
      setUploading(false)
      setOpenEdit(false)
      setAlready(true)
      setPdf('')
      setPdfFile('')
      swal.fire('Uploaded internship report Successfully', 'Successful', 'success');
      }).catch((error)=>{
        console.log(error);
        setUploading(false)
        setOpenEdit(false)
        setPdf('')
        setPdfFile('')
        swal.fire('failed to uploade internship report', 'Failed', 'error');
      })
  }
  
  useEffect(()=>{
    if(!patch){
      api({
        method: 'get',
        url: '/user/student-patch',
      }).then((res)=>{
        if (res.data.data) {
          console.log(res.data.data);
          setPatch(res.data.data)
          setAlready(res.data.uploaded)
          setLoading(false)
        }
        else {
          setLoading(false)
        }
      }).catch((error)=>{
        console.log(error);
        setLoading(false)
      })
    }
  },[])

  if (loading) return (<Loading />)
  if (!patch) return (<NoActivePatch />)
  return (
    <div>
      <Grid container>
        <Grid item xs={12}>
          <Card>
            <CardContent sx={{display:'flex',flexDirection:'column',padding:'10px 20px'}} >
              <Box sx={{ flexGrow: 1 }}>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                      <Typography textAlign={'center'} marginBottom='10px' variant="h5" color='gray'>{patch.semester} patch is currently open</Typography>
                  </Grid>
                  <Grid item xs={12} >
                      <Typography textAlign={'center'}>Opened <span style={{color:'Highlight'}}>{formatDistanceToNow(new Date(patch.start_date))}</span> ago</Typography>
                  </Grid>
                  <Grid item xs={12}>
                      <Typography textAlign={'center'}>Closes in <span style={{color:'darkcyan'}}>{formatDistanceToNow(new Date(patch.close_date))}</span></Typography>
                  </Grid>
                  <Grid item xs={12} sx={{display:'flex',flexDirection:'column',alignItems:'center'}}>
                      <Button
                      endIcon={<CloudUploadIcon />}
                      aria-haspopup="true"
                      onClick={handelClickEdit}
                    >Upload
                    </Button> 
                  </Grid>
                  {already? <Grid item xs={12}>
                      <Typography textAlign={'center'}>You uploaded a report in this patch, uploading again will replace your previous upload</Typography>
                  </Grid>: false}
              </Grid>
            </Box>
          </CardContent>  
        </Card>
      </Grid>
    </Grid>

      <BootstrapDialog
        onClose={(changed || uploading)? ()=>{}:handleCloseEdit}
        aria-labelledby="customized-dialog-title"
        open={openEdit}
        fullWidth
      >
        <DialogTitle sx={{ textAlign: 'center' }} id="customized-dialog-title">
          Upload internship report
        </DialogTitle>
        <IconButton
          aria-label="close"
          onClick={handleCloseEdit}
          sx={{
            position: "absolute",
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
        <Box component = "form" sx={{padding:'10px'}} onSubmit={handelSubmitEdit}>
            <input
            id="upload"
            key="upload"
            type="file"
            accept="application/pdf"
            hidden
            onChange={(e) => {handlePdfChange(e.target.files[0]); setChanged(true)}}
            />
            <Button style={{display:'block',margin:'0 10px 15px auto'}}>
              <label htmlFor="upload" >
                <div style={{display:'flex',flexFlow:'row'}}>
                <Typography>Select PDF</Typography>
                <UploadIcon sx={ {color:'#009be5'}}/>
                </div>
              </label>
            </Button>
            {pdf && <div >
              <iframe
              style={{display:'block',width:'80%',margin:'0 auto',height:"100vh"}}
              src={pdf?  pdf:''}
              alt="pdf"
              />
            </div>}
        <Button sx={{display:'block', margin:'15px 10px 10px auto'}} type = "submit" disabled={uploading || !changed}>
          Save changes
        </Button>
        </Box>
      </BootstrapDialog>
    </div>
  );
}
