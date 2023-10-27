import { useEffect, useState } from "react";
import { api } from "../utils/AxiosUtils";
import swal from 'sweetalert2'
import Loading from "./Loading";
import { Card, CardContent, Grid, Typography } from "@mui/material";
import { formatDistanceToNow } from "date-fns";

const PreviousReports = () => {
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)
    useEffect(()=>{
        if(!data) {
            api({
                method: 'get',
                url: '/user/student-submission',
              }).then((res)=>{
                console.log(res.data.data);
                setData(res.data.data)
                setLoading(false)
              }).catch((error)=>{      
                setLoading(false)   
                swal.fire('failed to get previous reports data', 'Failed', 'error');
              })
        }
    },[])
    if (loading) return (Loading())
    if (!data) return(
      <div className="PageNotFound">
      <h1>Sorry</h1>
      <h2>You do not have any previous submissions</h2>
  </div> 
    )
    return (
        <Grid container>
          {data.map((sub,idx) => 
            <Grid item xs={12} key={idx}>
              <Card>
            <CardContent sx={{display:'flex',flexDirection:'column',padding:'10px 20px'}} >
              <Grid container>
                <Grid item xs={12}>
                  <Typography textAlign={'center'} marginBottom='10px' variant="h5" color='gray'>{sub.patch.semester} Patch</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography textAlign={'center'}>File upload / <span style={{color:'Highlight'}}>{sub.file_upload}</span></Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography marginTop={'20px'} textAlign={'center'}>Uploaded <span style={{color:'darkcyan'}}>{formatDistanceToNow(new Date(sub.upload_date))} ago</span></Typography>
                </Grid>
                {sub.patch.processed? 
                <Grid item xs={12}>
                <Typography marginTop={'20px'} textAlign={'center'}>Verdict / {sub.verdict}</Typography>
              </Grid>:
              <Grid item xs={12}>
              <Typography marginTop={'20px'} color={'gray'} textAlign={'center'}>{sub.patch.open? "Awaiting patch closing" : "Awaiting confirmation"}</Typography>
            </Grid>
              }
              </Grid>
            </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
    );
}
 
export default PreviousReports;