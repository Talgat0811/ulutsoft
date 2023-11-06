// record-play-audio.js




if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
	
    let mediaRecorder;
    let audioChunks = [];
    let audioPlayer = document.getElementById('audioPlayer');
    let startRecordingButton = document.getElementById('startRecording');
    let stopRecordingButton = document.getElementById('stopRecording');
    //let sendAudioButton = document.getElementById('sendAudio');
    const loading = document.getElementById("loading");
    const audio_info = document.getElementById("audio_info");
  	const audio_text = document.getElementById("audio_text");
  	const my_text = document.getElementById("myText");
    let startTime;
    const recordingDuration = 1 * 61 * 1000; // 1 minutes in milliseconds
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function (stream) {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = function (event) {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            
            function updateTimer() {
            const currentTime = new Date().getTime();
            const elapsedTime = currentTime - startTime;
            const remainingTime = recordingDuration - elapsedTime;

            if (remainingTime < 0) {
                stopRecording();
                return;
            }
            const seconds = Math.floor(elapsedTime / 1000);
            const minutes = Math.floor(seconds / 60);
            const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
            document.getElementById('timer').textContent = formattedTime;
            }
            
            
            function stopRecording() {
            mediaRecorder.stop();
                stopRecordingButton.disabled = true;
                startRecordingButton.disabled = false;
            }
            mediaRecorder.onstart = () => {
                startTime = new Date().getTime();
                updateTimer();
                timerInterval = setInterval(updateTimer, 1000); // Update timer every second
                setTimeout(stopRecording, recordingDuration); // Automatically stop recording after 5 minutes
            };
            mediaRecorder.onstop = function () {
                clearInterval(timerInterval);
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioPlayer.src = URL.createObjectURL(audioBlob);
                audioPlayer.style.display = "none";
                startRecordingButton.disabled = true;
                //sendAudioButton.disabled = false;
                // Save the audio to your Django backend here using fetch or XMLHttpRequest
                // For example, send it to a Django view for processing and storage
                loading.style.display = "block";
                audio_info.style.display = "none";
          		audio_text.style.display = "none";
          		my_text.style.display = "none";
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
                        audioPlayer.type="audio/wav"
                        loading.style.display = "none";
                    audioPlayer.style.display = "block";
			audio_info.style.display = "block";
          		audio_text.style.display = "block";
                    var text = data.text;
                    document.getElementById("myText").innerHTML = text;
                    my_text.style.display = "block";
                    startRecordingButton.disabled = false;
                    document.getElementById("audio").innerHTML = audioUrl;
                }

                })


                .catch(error => {
                    console.error('Error:', error);
                });
            };
            startRecordingButton.addEventListener('click', function () {
                audioChunks = [];
                mediaRecorder.start();
                startRecordingButton.disabled = true;
                stopRecordingButton.disabled = false;
                //sendAudioButton.disabled = true;
            });

            stopRecordingButton.addEventListener('click', function () {
                mediaRecorder.stop();
                stopRecordingButton.disabled = true;
                startRecordingButton.disabled = false;

            });

            // playRecordingButton.addEventListener('click', function () {
            //     audioPlayer.play();
            // });

        })
        .catch(function (error) {
            console.error('Error accessing the microphone:', error);
        });
} else {
    console.error('MediaRecorder API not supported in this browser.');
}
