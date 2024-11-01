const animalOptions = document.getElementsByName("animal");
const showImageButton = document.querySelector("button[onclick='showImage()']");
const imageContainer = document.getElementById("image-container");
const fileInfo = document.getElementById("file-info");
const fileInput = document.getElementById("fileInput");
const uploadButton = document.querySelector("button[onclick='uploadFile()']");


// Wait for the DOM content to load before attaching event listeners
document.addEventListener("DOMContentLoaded", () => {
    // Attach event listener to the "Show Image" button
    
    if (showImageButton) {
        showImageButton.addEventListener("click", showImage);
    }

    // Attach event listener to the "Upload" button
    
    if (uploadButton) {
        uploadButton.addEventListener("click", uploadFile);
    }
});

// Function to display the selected animal image
function showImage() {
    
    let selectedAnimal = null;

    // Determine which checkbox is selected
    for (const option of animalOptions) {
        if (option.checked) {
            selectedAnimal = option.value;
            break;
        }
    }

    // If no checkbox is selected, show an alert
    if (!selectedAnimal) {
        alert("Please select an animal.");
        return;
    }

    // Fetch the animal image URL from the Flask server
    fetch(`/get-animal-image?animal=${selectedAnimal}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // Display an error message if the image was not found
                imageContainer.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                // Display the image using the URL received from the server
                imageContainer.innerHTML = `<img src="${data.image_url}" alt="${selectedAnimal}" width="150">`;
            }
        })
        .catch(error => {
            // Log and display an error message if there was an issue with the fetch request
            console.error("Error fetching animal image:", error);
            imageContainer.innerHTML = `<p>Error fetching image.</p>`;
        });

    
}

// Function to handle file upload and display file information
function uploadFile() {
        // fileInfo.innerHTML = '<p>in uploadfile function.</p>'
        const file = fileInput.files[0];
        
        // If no file is selected, show an alert
        if (!file) {
            alert("Please select a file to upload.");
            return;
        }

        const formData = new FormData();

        formData.append('file', file);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                fileInfo.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                fileInfo.innerHTML = `
                    <p>File Name: ${data.name}</p>
                    <p>File Size: ${data.size}</p>
                    <p>File Type: ${data.type}</p>
                `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            fileInfo.innerHTML = '<p>An error occurred while uploading the file.</p>';
        });
        
}

