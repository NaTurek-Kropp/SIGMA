document.addEventListener('DOMContentLoaded', () => {
    const joinButton = document.getElementById('joinLobbyButton');
    const codeInput = document.getElementById('lobbyCodeInput');

    joinButton.addEventListener('click', async () => {
        const lobbyCode = codeInput.value.trim();
        const memberName = prompt("Enter your name:");

        if (!lobbyCode || !memberName) {
            alert('Please enter a valid lobby code and your name.');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/join_lobby', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ lobby_code: lobbyCode, member_name: memberName })
            });

            const result = await response.json();

            if (response.ok) {
                alert(result.message);
                window.location.href = `http://127.0.0.1:5500/Main/Online/lobby.html?lobby_code=${lobbyCode}`;
            } else {
                alert('Error: ' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while trying to join the lobby.');
        }
    });
});
