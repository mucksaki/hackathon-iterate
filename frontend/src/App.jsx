import * as React from 'react';
import { Suspense } from 'react'
import { Routes, Route } from 'react-router-dom';
import './App.css'
import Box from "@mui/material/Box";

// Lazy loaded route components
const Homepage = React.lazy(() => import("./pages/Homepage"))

const App = () => {
  const [isLoading, setIsLoading] = React.useState(true);

  return (
    <Box
      component="main"
      sx={{
        width: '100%',
        minHeight: '100vh',
        margin: 0,
        padding: 0,
      }}
    >
      <Routes>
        <Route path="/" element={<Homepage />} />
      </Routes>
    </Box>
  )
}


export default App;