let lobbyData = [];


function getLobbyCodeFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('lobby_code'); 
}

const lobbyCode = getLobbyCodeFromURL();
document.addEventListener('DOMContentLoaded', () => {
    if (!lobbyCode) {
        alert("Invalid lobby Code!");
        window.location.href = '/'; //Home a place where i can go
        return;
    }

    document.querySelector('.room-code').textContent = `Room Code: ${lobbyCode}`;

    checkLobbyUpdates(lobbyCode);
});


function checkLobbyUpdates(lobbyCode, interval = 5000) {
    setInterval(async () => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/get_lobby_id_from_code?lobby_code=${lobbyCode}`)
            if (response.ok) {
                const lobbyId = await response.json();
                console.log(lobbyId)
                const membersResponse = await fetch(`http://127.0.0.1:5000/get_lobby_members?lobby_id=${lobbyId["lobby_id"]}`);
                if (membersResponse.ok) {
                    const data = await membersResponse.json();
                    updateLobby(data.members);
                } else {
                    console.error('Failed to fetch lobby members');
                }
            }
            else {
                console.error('Failed to fetch lobby id')
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }, interval);
}


function updateLobby(members) {
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