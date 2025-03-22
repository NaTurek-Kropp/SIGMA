window.member_name = ""

function addRandomLetters(str) {
    let letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    let randomLetters = Array.from({ length: 20 }, () => letters[Math.floor(Math.random() * letters.length)]).join('');
    return str + randomLetters;
}


document.addEventListener('DOMContentLoaded', () => {
    const joinButton = document.getElementById('joinLobbyButton');
    const codeInput = document.getElementById('lobbyCodeInput');

    joinButton.addEventListener('click', async () => {
        const lobbyCode = codeInput.value.trim();
        member_name = prompt("Enter your name:");
        const member_name_encrypt = addRandomLetters(member_name)
        member_name = member_name_encrypt

        if (!lobbyCode || !member_name) {
            alert('Please enter a valid lobby code and your name.');
            return;
        }

        try {
            const response = await fetch('https://powarznastrona.pythonanywhere.com/join_lobby', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ lobby_code: lobbyCode, member_name: member_name })
            });

            const result = await response.json();



            if (response.ok) {
                alert(result.message);
                window.location.href = `https://powarznastrona.pythonanywhere.com/lobby?lobby_code=${lobbyCode}&member_name=${member_name}`;
            } else {
                alert('Error: ' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while trying to join the lobby.');
        }
    });
});
