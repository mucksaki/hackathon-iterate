import { Box, IconButton, Avatar } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import PersonIcon from '@mui/icons-material/Person';
import Typography from '@mui/material/Typography';

const Header = ({ onAddClick }) => {
  return (
    <Box
      sx={{
        width: '100%',
        height: 60,
        backgroundColor: '#1a1a1a',
        display: 'flex',
        alignItems: 'center',
        px: 3,
        borderBottom: '1px solid #333',
      }}
    >
      <Typography
        variant="h5"
        sx={{
          color: '#ffffff',
          fontWeight: 'bold',
          mr: 3,
        }}
      >
        ClAire
      </Typography>
      
      <Box
        sx={{
          flex: 1,
          height: 8,
          backgroundColor: '#1976d2',
          borderRadius: 1,
          display: 'flex',
          gap: 0.5,
          px: 0.5,
          alignItems: 'center',
        }}
      >
        {Array.from({ length: 50 }).map((_, i) => (
          <Box
            key={i}
            sx={{
              width: 1,
              height: 4,
              backgroundColor: '#ffffff',
              opacity: 0.7,
            }}
          />
        ))}
      </Box>

      <IconButton
        onClick={onAddClick}
        sx={{
          backgroundColor: '#1976d2',
          color: '#ffffff',
          ml: 2,
          '&:hover': {
            backgroundColor: '#1565c0',
          },
        }}
      >
        <AddIcon />
      </IconButton>

      <Avatar
        sx={{
          ml: 2,
          width: 32,
          height: 32,
          backgroundColor: '#64b5f6',
        }}
      >
        <PersonIcon sx={{ fontSize: 20 }} />
      </Avatar>
    </Box>
  );
};

export default Header;

