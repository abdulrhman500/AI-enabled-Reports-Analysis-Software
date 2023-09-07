import * as React from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const VisuallyHiddenInput = styled('input')`
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  bottom: 0;
  left: 0;
  white-space: nowrap;
  width: 1px;
`;

export default function InputFileUpload() {
  return (
    <div style={{height:'100vh',width:'100%'}}>
        <Button
        component="label"
        variant="contained"
        startIcon={<CloudUploadIcon />}
        href="#file-upload"
        sx={{display:'block',width:'120px',height:'60px',marginLeft:'auto',marginTop:'auto'}}
        >
        Upload a file
        <VisuallyHiddenInput type="file" />
        </Button>
    </div>
  );
}