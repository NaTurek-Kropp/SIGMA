import Config from './Config.js';

window.member_name = "";
const API_URL = Config.getSetting('API_URL');

async function fetchLobbyId(lobbyCode) {
    const response = await fetch(`${API_URL}/get_lobby_id_from_code?lobby_code=${lobbyCode}`);
    if (!response.ok) throw new Error('Failed to fetch lobby id');
    return response.json();
}

document.addEventListener('DOMContentLoaded', () => {
    const joinButton = document.getElementById('joinLobbyButton');
    const codeInput = document.getElementById('lobbyCodeInput');

    joinButton.addEventListener('click', async () => {
        const lobbyCode = codeInput.value.trim();
        member_name = prompt("Enter your name:");

        if (!lobbyCode || !member_name) {
            alert('Please enter a valid lobby code and your name.');
            return;
        }

        try {
            const response = await fetch(`${API_URL}/join_lobby`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lobby_code: lobbyCode, member_name })
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.message);
                window.location.href = `${API_URL}/Main/Online/lobby.html?lobby_code=${lobbyCode}&member_name=${member_name}`;
            } else {
                alert('Error: ' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while trying to join the lobby.');
        }
    });
});
