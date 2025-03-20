// lobby.js
const API_URL = "https://powarznastrona.pythonanywhere.com";

function getLobbyCodeFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('lobby_code');
}

function getMemberNameFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('member_name');
}

document.addEventListener('DOMContentLoaded', () => {
    const lobbyCode = getLobbyCodeFromURL();
    const memberName = getMemberNameFromUrl();
    
    if (!lobbyCode) {
        alert("Invalid lobby Code!");
        window.location.href = '/'; // Redirect to home page or a fallback location
        return;
    }
    
    // Update the room code display
    const roomCodeElement = document.querySelector('.room-code');
    if (roomCodeElement) {
        roomCodeElement.textContent = `Room Code: ${lobbyCode}`;
    }
    
    // Start polling for lobby updates
    checkLobbyUpdates(lobbyCode);
});

async function fetchLobbyId(lobbyCode) {
    const response = await fetch(`${API_URL}/get_lobby_id_from_code?lobby_code=${lobbyCode}`);
    if (!response.ok) throw new Error('Failed to fetch lobby id');
    return response.json();
}

async function fetchLobbyMembers(lobbyId) {
    const response = await fetch(`${API_URL}/get_lobby_members?lobby_id=${lobbyId}`);
    if (!response.ok) throw new Error('Failed to fetch lobby members');
    return response.json();
}

async function fetchGameStarted(lobbyId) {
    const response = await fetch(`${API_URL}/is_game_started?lobby_id=${lobbyId}`);
    if (!response.ok) throw new Error('Failed to fetch game status');
    return response.json();
}

async function checkLobbyUpdates(lobbyCode, interval = 5000) {
    setInterval(async () => {
        try {
            const lobbyData = await fetchLobbyId(lobbyCode);
            const lobbyId = lobbyData.lobby_id;
            const membersData = await fetchLobbyMembers(lobbyId);
            const gameStartedData = await fetchGameStarted(lobbyId);
            console.log("Lobby ID:", lobbyId);
            console.log("Game Started:", gameStartedData);
            updateLobby(membersData.members, gameStartedData);
        } catch (error) {
            console.error('Error:', error);
        }
    }, interval);
}

function updateLobby(members, gameStarted) {
    // If the game has started, redirect to the game page
    if (gameStarted.game_started === true) {
        const lobbyCode = getLobbyCodeFromURL();
        const memberName = getMemberNameFromUrl();
        window.location.href = `${API_URL}/Main/Online/game.html?lobby_code=${lobbyCode}&member_name=${memberName}`;
        return;
    }
    
    // Update the members list in the DOM
    const membersContainer = document.querySelector('.members');
    if (membersContainer) {
        membersContainer.innerHTML = '';
        members.forEach(member => {
            const memberDiv = document.createElement('div');
            memberDiv.className = 'member';
            memberDiv.textContent = member;
            membersContainer.appendChild(memberDiv);
        });
    }
}
