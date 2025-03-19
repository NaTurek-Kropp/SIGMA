document.addEventListener('DOMContentLoaded', () => {
    getButtons().forEach(button => {
        button.addEventListener('click', () => {
            const answer = button.id.toString();
            getButtons().forEach(button => {
                button.disabled = true;
            });
            //sendAnswerToServer(answer);
        });
    });
});

function getButtons() {
    return document.querySelectorAll('button');
}
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

async function waitForNextQuestion(lobbyCode, interval = 5000) {
    setInterval(async () => {
        try {
            const response = await fetch('--/join_lobby', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ lobby_code: lobbyCode, member_name: member_name })
            });
            result = response.json();
            if (result.all_submitted) {
                getButtons().forEach(button => {
                    button.disabled = false;
                });
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }, interval);
}
