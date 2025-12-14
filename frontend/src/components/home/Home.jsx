import { useState } from "react";
import Box from "@mui/material/Box";
import Header from "../layout/Header";
import SessionSidebar from "../sessions/SessionSidebar";
import ContentArea from "../content/ContentArea";
import AskNotes from "../chat/AskNotes";
import CreateSessionDialog from "../sessions/CreateSessionDialog";

const Home = () => {
    const [selectedSession, setSelectedSession] = useState(null);
    const [selectedConversation, setSelectedConversation] = useState(null);
    const [createDialogOpen, setCreateDialogOpen] = useState(false);
    const [refreshTrigger, setRefreshTrigger] = useState(0);

    const handleSessionSelect = (session) => {
        setSelectedSession(session);
        setSelectedConversation(null); // Reset conversation when session changes
    };

    const handleConversationSelect = (conversation) => {
        setSelectedConversation(conversation);
    };

    const handleAddClick = () => {
        setCreateDialogOpen(true);
    };

    const handleDialogClose = () => {
        setCreateDialogOpen(false);
    };

    const handleSessionCreated = (session) => {
        handleSessionSelect(session);
        setRefreshTrigger(prev => prev + 1); // Trigger refresh
        handleDialogClose();
    };

    return (
        <Box
            sx={{
                width: '100%',
                height: '100vh',
                display: 'flex',
                flexDirection: 'column',
                backgroundColor: '#f5f5f5',
            }}
        >
            <Header onAddClick={handleAddClick} />
            
            <Box
                sx={{
                    flex: 1,
                    display: 'flex',
                    overflow: 'hidden',
                }}
            >
                {/* Left Sidebar - Sessions */}
                <Box
                    sx={{
                        width: 300,
                        height: '100%',
                        overflow: 'hidden',
                    }}
                >
                    <SessionSidebar
                        onSessionSelect={handleSessionSelect}
                        onConversationSelect={handleConversationSelect}
                        selectedSession={selectedSession}
                        selectedConversation={selectedConversation}
                        onAddSession={handleAddClick}
                        refreshTrigger={refreshTrigger}
                        onRefresh={() => setRefreshTrigger(prev => prev + 1)}
                    />
                </Box>

                {/* Center Content Area */}
                <Box
                    sx={{
                        flex: 1,
                        height: '100%',
                        overflow: 'hidden',
                    }}
                >
                    <ContentArea
                        selectedConversation={selectedConversation}
                        selectedSession={selectedSession}
                    />
                </Box>

                {/* Right Sidebar - Ask Notes */}
                <Box
                    sx={{
                        width: 400,
                        height: '100%',
                        overflow: 'hidden',
                    }}
                >
                    <AskNotes selectedSession={selectedSession} />
                </Box>
            </Box>

            <CreateSessionDialog
                open={createDialogOpen}
                onClose={handleDialogClose}
                onSessionCreated={handleSessionCreated}
            />
        </Box>
    );
};

export default Home;
