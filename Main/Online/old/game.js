document.addEventListener('DOMContentLoaded', () => {
    getButtons().forEach(button => {
        button.addEventListener('click', () => {
            const answer = button.id.toString();
            getButtons().forEach(button => {
                button.disabled = true;
            });
            sendAnswerToServer(answer);
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
//#region Tests
async function fetchMembersObjects(lobbyId) {
    const response = await fetch(`https://powarznastrona.pythonanywhere.com/get_lobby_member_objects?lobby_id=${lobbyId}`);
    if (!response.ok) throw new Error('Failed to fetch lobby member objects');
    return response.json();
}
//#endregion
async function fetchLobbyId(lobbyCode) {
    const response = await fetch(`https://powarznastrona.pythonanywhere.com/get_lobby_id_from_code?lobby_code=${lobbyCode}`);
    if (!response.ok) throw new Error('Failed to fetch lobby id');
    return response.json();
}
const lobbyCode = getLobbyCodeFromURL();
const memberName = getMemberNameFromUrl();

async function sendAnswerToServer(answer) {
    const lobbyId = await fetchLobbyId(lobbyCode)
    memberObjects = fetchMembersObjects(1)
    // memberObjects.forEach(member => {
    //     console.log(member.name)
    // });
    console.log(lobbyId.lobby_id)
    fetch('https://powarznastrona.pythonanywhere.com/submit_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ lobby_id: lobbyId.lobby_id, member_name: memberName, answer: answer})
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        waitForNextQuestion(lobbyCode)
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

async function waitForNextQuestion(lobbyCode, interval = 5000) {
    const lobbyId = await fetchLobbyId(lobbyCode)
    setInterval(async () => {
        try {
            const response = await fetch('https://powarznastrona.pythonanywhere.com/all_members_submitted', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ lobby_id: lobbyId})
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


