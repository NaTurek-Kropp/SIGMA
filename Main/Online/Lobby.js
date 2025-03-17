let lobbyData = [];


function getLobbyCodeFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('lobby_code'); 
}
function getMemberNameFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('member_name'); 
}

const lobbyCode = getLobbyCodeFromURL();
const member_name = getMemberNameFromUrl();
document.addEventListener('DOMContentLoaded', () => {
    if (!lobbyCode) {
        alert("Invalid lobby Code!");
        window.location.href = '/'; //Home a place where i can go
        return;
    }

    document.querySelector('.room-code').textContent = `Room Code: ${lobbyCode}`;

    checkLobbyUpdates(lobbyCode);
});


async function fetchLobbyId(lobbyCode) {
    const response = await fetch(`http://127.0.0.1:5000/get_lobby_id_from_code?lobby_code=${lobbyCode}`);
    if (!response.ok) throw new Error('Failed to fetch lobby id');
    return response.json();
}

async function fetchLobbyMembers(lobbyId) {
    const response = await fetch(`http://127.0.0.1:5000/get_lobby_members?lobby_id=${lobbyId}`);
    if (!response.ok) throw new Error('Failed to fetch lobby members');
    return response.json();
}

async function fetchGameStarted(lobbyId) {
    const response = await fetch(`http://127.0.0.1:5000/is_game_started?lobby_id=${lobbyId}`);
    if (!response.ok) throw new Error('Failed to fetch game status');
    return response.json();
}

async function checkLobbyUpdates(lobbyCode, interval = 5000) {
    setInterval(async () => {
        try {
            const lobbyId = await fetchLobbyId(lobbyCode);
            const membersData = await fetchLobbyMembers(lobbyId.lobby_id);
            const gameStarted = await fetchGameStarted(lobbyId.lobby_id);
            console.log(lobbyId.lobby_id)
            console.log(gameStarted)
            updateLobby(membersData.members, gameStarted);
        } catch (error) {
            console.error('Error:', error);
        }
    }, interval);
}


function updateLobby(members, gameStarted) {
    if (gameStarted.game_started == true) {
        window.location.href = `http://127.0.0.1:5500/Main/Online/game.html?lobby_code=${lobbyCode}&member_name=${member_name}`
    }
    const membersContainer = document.querySelector('.members');
    membersContainer.innerHTML = '';
    members.forEach(member => {
        const memberDiv = document.createElement('div');
        memberDiv.className = 'member';
        memberDiv.textContent = member;
        membersContainer.appendChild(memberDiv);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    checkLobbyUpdates(lobbyCode);
});