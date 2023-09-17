import { Box, Button, Card, CardContent, Grid, Typography } from "@mui/material";
import AdminDial from "../components/AdminDial";
const AdminHome = () => {
    return (
        <Box>
            <Grid container spacing={2} columns={12} minWidth={'500px'}>
                <Grid item xs={12} md={12} lg={6} >
                    <Card>
                        <CardContent sx={{display:'flex',flexDirection:'column',padding:'10px 20px'}} >
                            <Box sx={{ flexGrow: 1 }}>
                                <Grid container spacing={2}>
                                    <Grid item xs={12}>
                                        <Typography marginBottom='10px' variant="h6" color='gray' fontStyle={'italic'} >Patches Info</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography><span style={{color:'purple'}}>{5}</span> total patches</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography><span style={{color:'green'}}>{481}</span> reports accepted</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography><span style={{color:'salmon'}}>{500}</span> reports uploaded</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography><span style={{color:'red'}}>{19}</span> reports rejected</Typography>
                                    </Grid>
                                    <Grid item xs={12}>
                                        <Typography marginTop='10px' color='gray'>Rejected reportes were reviewed by the admin.</Typography>
                                    </Grid>
                                </Grid>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} md={12} lg={6}>
                    <Card>
                        <CardContent sx={{display:'flex',flexDirection:'column',padding:'10px 20px'}} >
                            <Box sx={{ flexGrow: 1 }}>
                                <Grid container spacing={2}>
                                    <Grid item xs={12}>
                                        <Typography marginBottom='10px' variant="h6" color='gray' fontStyle={'italic'} >System Info</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography><span style={{color:'green'}}>{481}</span> reports accepted</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography><span style={{color:'green'}}>{480}</span> reports accepted after review</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography><span style={{color:'red'}}>{19}</span> reports rejected</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography><span style={{color:'red'}}>{18}</span> reports rejected after review</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                    <Typography marginTop='10px'>Total System accuracy: <span style={{color:'green'}}>{99.6}%</span></Typography>
                                    </Grid>
                                </Grid>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} md={12} lg={12}>
                    <Card>
                        <CardContent sx={{display:'flex',flexDirection:'column',padding:'10px 20px'}} >
                            <Box sx={{ flexGrow: 1 }}>
                                <Grid container spacing={2}>
                                    <Grid item xs={12}>
                                        <Typography marginBottom='10px' variant="h6" color='gray' fontStyle={'italic'} >Current patch Info</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography><span style={{color:'salmon'}}>{100}</span> reports uploaded</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography><span style={{color:'green'}}>{91}</span> reports accepted</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography><span style={{color:'red'}}>{8}</span> reports rejected</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography marginTop='10px' color='gray'>automatically closes on 12/12/2023</Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Grid container spacing={2} >
                                            <Grid item xs={6}>
                                                <Button variant="outlined" color='warning' sx={{width:'100px'}} >Run Tests</Button>
                                            </Grid>
                                            <Grid item xs={6}>
                                                <Button variant="outlined" color="error" sx={{width:'100px'}} >Close</Button>
                                            </Grid>
                                        </Grid>
                                    </Grid>
                                </Grid>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
            <AdminDial />
        </Box>
    );
}
 
export default AdminHome;