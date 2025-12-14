import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Home from '../components/home/Home';

export default function Homepage() {
    const navigate= useNavigate();

    return <Home />
}