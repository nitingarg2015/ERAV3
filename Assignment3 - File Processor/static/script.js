// Declare constants for elements
const fileInput = document.getElementById("fileInput");
const output = document.getElementById("output");
const uploadFileButton = document.getElementById("uploadFileButton");
const viewFileButton = document.getElementById("viewFileButton");
const fileMetadataDiv = document.getElementById("fileMetadata");
const viewPreprocessedFileButton = document.getElementById("viewPreprocessedFile");
const viewAugmentedFileButton = document.getElementById("viewAugmentedFile");

// Initialize file name variable
let uploadedFileName = '';

// Event listener for upload button
uploadFileButton.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select a file to upload.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            uploadedFileName = data.filename; // Store uploaded filename
            fileMetadataDiv.textContent = `Uploaded: ${data.filename}, Size: ${data.size} bytes`;
            viewFileButton.disabled = false; // Enable view file button
            viewPreprocessedFileButton.disabled = false;
            viewAugmentedFileButton.disabled = false;
        } else {
            fileMetadataDiv.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error:', error);
        fileMetadataDiv.textContent = 'Error uploading file.';
    }
});

// Event listener for view file button
viewFileButton.addEventListener('click', async () => {
    try {
        const response = await fetch(`/view_file?filename=${uploadedFileName}`);
        const data = await response.json();
        if (response.ok) {
            if (data.type === 'text') {
                output.textContent = data.content; // Display text content
            } else if (data.type === 'image') {
                // output.innerHTML = `<img src="uploads/${data.content}" alt="${data.content}" style="max-width: 100%; height: auto;">`; // Display image
                output.innerHTML = `<img src="/uploads/${data.content}" alt="alttext" style="max-width: 100%; height: auto;">`; // Display image
            } else if (data.type === 'audio') {
                output.innerHTML = `<audio controls><source src="uploads/${data.content}" type="audio/mpeg">Your browser does not support the audio element.</audio>`; // Play audio
            }
        } else {
            output.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error:', error);
        output.textContent = 'Error fetching file content.';
    }
});

// Event listener for viewPreprocessedFile button
viewPreprocessedFileButton.addEventListener('click', async () => {
    try {
        const response = await fetch(`/preprocess_file?filename=${uploadedFileName}`);
        const data = await response.json();
        console.log('Response:', response);

        if (response.ok) {
            if (data.type === 'text') {
                output.textContent = data.content; // Display text content
            } else if (data.type === 'image') {
                displayImages(data.content); // Call the displayImages function
            } else if (data.type === 'audio') {
                displayAudio(data.content); // Call the displayAudio function
            }
        } else {
            output.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error:', error);
        output.textContent = 'Error fetching file content.';
    }
});

// Event listener for viewAugmentedFile button
viewAugmentedFileButton.addEventListener('click', async () => {
    try {
        const response = await fetch(`/augment_file?filename=${uploadedFileName}`);
        const data = await response.json();
        console.log('Response:', response);

        if (response.ok) {
            if (data.type === 'text') {
                output.textContent = data.content; // Display text content
            } else if (data.type === 'image') {
                displayImages(data.content); // Call the displayImages function
            } else if (data.type === 'audio') {
                displayAudio(data.content); // Call the displayAudio function
            }
        } else {
            output.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error:', error);
        output.textContent = 'Error fetching file content.';
    }
});

// Function to handle image display
function displayImages(dataContent) {
    output.innerHTML = ''; // Clear any previous content

    for (const [key, base64Image] of Object.entries(dataContent)) {
        // Create a new div for each image and its title
        const container = document.createElement('div');

        // Create an img element for the base64 image
        const imgElement = document.createElement('img');
        imgElement.src = `data:image/png;base64,${base64Image}`; // Set the src to the base64 image
        imgElement.alt = key; // Use the key as the alt text for the image
        imgElement.style.margin = '10px'; // Optional: Add some margin
        imgElement.width = 200; // Optional: Set the width of the image

        // Create a title element (h3 or div) for the image title
        const titleElement = document.createElement('h3');
        titleElement.innerHTML = key; // Set the title to the key

        // Append the title and image to the container
        container.appendChild(titleElement);
        container.appendChild(imgElement);

        // Append the container to the output
        output.appendChild(container);
    }
}

// Function to handle audio display
function displayAudio(dataContent) {
    output.innerHTML = ''; // Clear any previous content

    for (const [key, base64Audio] of Object.entries(dataContent)) {
        // Create a new div for each audio and its title
        const container = document.createElement('div');

        // Create an audio element
        const audioElement = document.createElement('audio');
        audioElement.controls = true; // Enable audio controls

        try {
            // Convert base64 to blob and create a URL
            const audioBlob = base64ToBlob(base64Audio, 'audio/wav');
            const audioUrl = URL.createObjectURL(audioBlob);
            audioElement.src = audioUrl;
        } catch (error) {
            console.error("Error creating audioBlob:", error);
            // Handle error gracefully, e.g., display a message to the user
            const errorMessage = document.createElement('p');
            errorMessage.textContent = `Error loading audio for: ${key}`;
            container.appendChild(errorMessage);
        }

        // Create a title for the audio
        const audioTitle = document.createElement('p');
        audioTitle.textContent = `Processed Audio: ${key}`;

        // Append the title and audio element to the container
        container.appendChild(audioTitle);
        container.appendChild(audioElement);

        // Append the container to the output
        output.appendChild(container);
    }
}

// Function to convert base64 string to Blob
function base64ToBlob(base64, mimeType) {
    try {
        // Decode base64 string
        const byteCharacters = atob(base64);
        const byteArrays = [];

        for (let offset = 0; offset < byteCharacters.length; offset += 1024) {
            const slice = byteCharacters.slice(offset, offset + 1024);
            const byteNumbers = new Array(slice.length);

            for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            const byteArray = new Uint8Array(byteNumbers);
            byteArrays.push(byteArray);
        }

        return new Blob(byteArrays, { type: mimeType });
    } catch (error) {
        console.error("Error in base64ToBlob:", error);
        throw new Error("Failed to convert base64 to Blob");
    }
}