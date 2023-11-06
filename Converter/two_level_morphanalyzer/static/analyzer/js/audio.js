// record-play-audio.js

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    let mediaRecorder;
    let audioChunks = [];
    let audioPlayer = document.getElementById('audioPlayer');
    let startRecordingButton = document.getElementById('startRecording');
    let stopRecordingButton = document.getElementById('stopRecording');
    let sendAudioButton = document.getElementById('sendAudio');

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function (stream) {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = function (event) {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = function () {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioPlayer.src = URL.createObjectURL(audioBlob);
                startRecordingButton.disabled = false;
                sendAudioButton.disabled = false;
                // Save the audio to your Django backend here using fetch or XMLHttpRequest
                // For example, send it to a Django view for processing and storage
            };

            startRecordingButton.addEventListener('click', function () {
                audioChunks = [];
                mediaRecorder.start();
                startRecordingButton.disabled = true;
                stopRecordingButton.disabled = false;
                sendAudioButton.disabled = true;
            });

            stopRecordingButton.addEventListener('click', function () {
                mediaRecorder.stop();
                stopRecordingButton.disabled = true;
                startRecordingButton.disabled = false;
                sendAudioButton.disabled = false;
            });

            // playRecordingButton.addEventListener('click', function () {
            //     audioPlayer.play();
            // });
            sendAudioButton.addEventListener('click', function () {

                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioPlayer.src = URL.createObjectURL(audioBlob);
                const formData = new FormData();
                formData.append('audio', audioBlob, 'audio.wav');

                fetch('/speech_to_text/', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {

                        // window.location.reload(true);
                    const audioUrl = data.audio_url;
                    audioPlayer.src = audioUrl;

                    var text = data.text;
                    document.getElementById("myText").innerHTML = text;
                    startRecordingButton.disabled = true;
                    document.getElementById("audio").innerHTML = audioUrl;
                }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        })
        .catch(function (error) {
            console.error('Error accessing the microphone:', error);
        });
} else {
    console.error('MediaRecorder API not supported in this browser.');
}
