async function uploadAudio() {

    // Get the selected audio file
    const file = document.getElementById("audioFile").files[0];

    // Check if a file is selected
    if (!file) {
        alert("Please select a WAV audio file.");
        return;
    }

    // Create FormData object
    const formData = new FormData();
    formData.append("audio", file);

    try {

        // Send the audio file to the server
        const response = await fetch("/transcribe", {
            method: "POST",
            body: formData
        });

        // Get the response
        const data = await response.json();

        // Display the transcription
        document.getElementById("result").innerText = data.text;

    } catch (error) {
        console.error(error);
        alert("Something went wrong while transcribing the audio.");
    }
}