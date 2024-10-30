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

    // Display the image in the image container
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
        // imageContainer.innerHTML = `<img src="/static/images/${selectedAnimal}.jpg" alt="${selectedAnimal}">`;
    
}

// Function to handle file upload and display file information
// function uploadFile() {

//     const fileInput = document.getElementById("fileInput");
//     const uploadButton = document.querySelector("button[onclick='uploadFile()']");
//     const file = fileInput.files[0];
//     // If no file is selected, show an alert
//     if (!file) {
//         alert("Please select a file to upload.");
//         return;
//     }

//     // Proceed with the file upload process if a file is selected
//     const formData = new FormData();
//     formData.append("file", file);

//     // Display the image if always stored in specified location
//     // fileInfo.innerHTML = `<img src="image/${file.name}" alt="${file.name}">`;

//     // Use FileReader to read the file as a data URL if file store any location
//     const reader = new FileReader();
//     reader.onload = function(event) {
//         // Display the image using the data URL
//         fileInfo.innerHTML = `<img src="${event.target.result}" alt="${file.name}">`;

//         const messageElement = document.createElement("div");
//         messageElement.className = "message file-details";
//         messageElement.textContent = `File details: ${file.name}, ${file.size} bytes, ${file.type}`;
//         fileInfo.appendChild(messageElement);
//     }
//     // Read the file as a data URL
//     reader.readAsDataURL(file);

// }
