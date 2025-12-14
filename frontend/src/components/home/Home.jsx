import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import { useState } from "react";

const Home = () => {
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);

    const goodBoy = async () => {
        setLoading(true);
        try {
            const res = await fetch('/api/example/good_boy');
            if (!res.ok) throw new Error(`Erreur ${res.status}`);
            const data = await res.text();
            setResponse(data);
        } catch (err) {
            setResponse({ error: err.message });
        } finally {
            setLoading(false);
        }
    };
    return (
        <Box
            sx={{
                width: '100%',
                minHeight: '100vh',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                pt: 4,
                backgroundColor: '#1a1a1a',
                position: 'relative',
            }}
        >
            <Paper sx={{ p: 2, backgroundColor: '#2d2d2d' }}>
                <Typography variant="h4" sx={{ color: '#ffffff' }}>Web-App template</Typography>
            </Paper>
            <Button 
                variant="contained" 
                size="large"
                onClick={goodBoy}
                disabled={loading}
                sx={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                }}
            >
                {loading ? 'Loading...' : 'Click Me'}
            </Button>
            {response && (
                <Typography 
                    sx={{ 
                        color: '#ffffff',
                        position: 'absolute',
                        top: 'calc(50% + 60px)',
                        left: '50%',
                        transform: 'translateX(-50%)',
                        textAlign: 'center',
                    }}
                >
                    {typeof response === 'object' ? response.error : response}
                </Typography>
            )}
        </Box>
    );
};

export default Home;