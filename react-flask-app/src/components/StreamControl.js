// https://dev.to/dev_elie/sending-data-from-react-to-flask-apm

// this thing interacts with the flask backend by sending a 
// POST request to the /stream_control endpoint with the 
// command as an argument
export default class StreamControl {

    static SendCommand(command) {

        return fetch('/stream_control', 
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({"cmd": command})
            })
            .then(response => response.json())
        .catch(error => {  
            console.log(error);
        });
    }
}