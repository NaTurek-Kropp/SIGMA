document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('button');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const answer = button.id.toString();
            sendAnswerToServer(answer);
        });
    });
});

function getLobbyCodeFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('lobby_code'); 
}
function getMemberNameFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('member_name'); 
}
const lobbyCode = getLobbyCodeFromURL();
const memberName = getMemberNameFromUrl();

async function sendAnswerToServer(answer) {
    const response = await fetch(`http://127.0.0.1:5000/get_lobby_id_from_code?lobby_code=${lobbyCode}`)
    if (response.ok) {
        const lobbyId = await response.json()
        console.log(lobbyId.lobby_id, memberName, answer)
        fetch('http://127.0.0.1:5000/submit_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ lobby_id: lobbyId.lobby_id, member_name: memberName, answer: answer})
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
}