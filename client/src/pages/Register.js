
import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import { Alert } from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { useNavigate } from 'react-router-dom';
import { useRegister } from '../hooks/useRegister';

export default function Register() {
  const navigate = useNavigate()
  const { register, isLoading } = useRegister()
  const [error, setError] = React.useState('')
  const handleSubmit = async (event) => {
    const data = new FormData(event.currentTarget);
    event.preventDefault();
    if( data.get('password')!== data.get('confirm-password')){
      setError("Passwords don't match")
      return
    }
    const registered = await register(data.get('email'), data.get('password'),data.get('username'),parseInt(data.get('user_id').replace('-','')))
    if ( !registered.error) {
      navigate('/')
    }
    else {
      setError(registered.error)
    }
    
  };
  const validateId = (e) => {
    setError('')
    const regex = /^\d{2}-\d+$/;
    if (regex.test(e.target.value)) {
      e.target.setCustomValidity("")
    } else {
      e.target.setCustomValidity("Student id should be of the format ##-#####")
}
  }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          margin:'10vh 0'
        }}
      >
        <Avatar sx={{ m: 1}}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Create an account
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} >
              <TextField
                required
                fullWidth
                type='text'
                id="username"
                label="Name"
                name="username"
                onChange={() => setError('')}
                autoComplete="user-name"
              />
            </Grid>
            <Grid item xs={12} >
              <TextField
                required
                fullWidth
                type='text'
                id="user_id"
                label="Student ID"
                name="user_id"
                onChange={validateId}
              />
            </Grid>
            <Grid item xs={12} >
              <TextField
                required
                fullWidth
                type='email'
                id="email"
                label="Student email"
                name="email"
                onChange={() => setError('')}
                autoComplete="email"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                onChange={() => setError('')}
                autoComplete="password"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                name="confirm-password"
                label="Confirm password"
                type="password"
                id="confirm-password"
                onChange={() => setError('')}
                autoComplete="password"
              />
            </Grid>
          </Grid>
          {error && (

            <Grid item xs={12} marginTop={2}>
              <Alert severity="error" fullWidth>
                {error}
              </Alert>
            </Grid>
          )}

          <Button display={isLoading}
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Register
          </Button>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link href="/login" variant="body2">
                Already have an account
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
}