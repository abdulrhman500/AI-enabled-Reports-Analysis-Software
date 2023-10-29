import * as React from 'react';
import PropTypes from 'prop-types';
import Typography from '@mui/material/Typography';
import Skeleton from '@mui/material/Skeleton';
import Grid from '@mui/material/Grid';

const variants = ['h1', 'h2', 'h1', 'h2', 'h1'];

const Loading = () => {
  return (
    <div>
      {variants.map((variant, index) => (
        <Typography component="div" key={index} variant={variant}>
            <Skeleton />
        </Typography>
      ))}
    </div>
  );
}
export default Loading