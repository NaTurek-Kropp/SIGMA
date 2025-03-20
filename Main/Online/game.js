// game.js
const API_URL = "https://powarznastrona.pythonanywhere.com";

function getLobbyCodeFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('lobby_code');
}

function getMemberNameFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('member_name');
}

function getButtons() {
    return document.querySelectorAll('button');
}

document.addEventListener('DOMContentLoaded', () => {
    const buttons = getButtons();
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const answer = button.id.toString();
            // Disable all buttons to prevent multiple answers\n            buttons.forEach(btn => btn.disabled = true);
            sendAnswerToServer(answer);
        });
    });
});

async function fetchLobbyId(lobbyCode) {
    const response = await fetch(`${API_URL}/get_lobby_id_from_code?lobby_code=${lobbyCode}`);
    if (!response.ok) throw new Error('Failed to fetch lobby id');
    return response.json();
}

// (Optional) Test function to fetch lobby member objects if needed
async function fetchMembersObjects(lobbyId) {
    const response = await fetch(`${API_URL}/get_lobby_member_objects?lobby_id=${lobbyId}`);
    if (!response.ok) throw new Error('Failed to fetch lobby member objects');
    return response.json();
}

async function sendAnswerToServer(answer) {
    try {
        const lobbyCode = getLobbyCodeFromURL();
        const memberName = getMemberNameFromUrl();
        const lobbyData = await fetchLobbyId(lobbyCode);
        const lobbyId = parseInt(lobbyData.lobby_id);
        
        // (Optional) Fetch and log member objects for debugging\n        // const memberObjects = await fetchMembersObjects(lobbyId);\n        // memberObjects.members.forEach(member => console.log(member.name));
        
        const response = await fetch(`${API_URL}/submit_answer`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ lobby_id: lobbyId, member_name: memberName, answer: answer })
        });
        const result = await response.json();
        console.log('Success:', result);
        waitForNextQuestion(lobbyCode);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function waitForNextQuestion(lobbyCode, interval = 5000) {
    const lobbyData = await fetchLobbyId(lobbyCode);
    const lobbyId = parseInt(lobbyData.lobby_id);
    setInterval(async () => {
        try {
            const response = await fetch(`${API_URL}/all_members_submitted`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lobby_id: lobbyId })
            });
            const result = await response.json();
            if (result.all_submitted) {
                // Re-enable answer buttons once all members have submitted\n                getButtons().forEach(button => button.disabled = false);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }, interval);
}
