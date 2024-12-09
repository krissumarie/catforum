function toggleMenu() {
    const navLinks = document.getElementById("nav-links");
    navLinks.classList.toggle("visible");
}

window.previewProfilePicture = function(event) {
        const file = event.target.files[0]; // Get the selected file
        if (file) {
            const reader = new FileReader(); // Use FileReader to read the file
            reader.onload = function(e) {
                // Set the image preview to the file's content
                document.getElementById('profilePicturePreview').src = e.target.result;
            };
            reader.readAsDataURL(file); // Read the file as a data URL
        }
    }

function previewPostImage(event) {
        const file = event.target.files[0]; // Get the selected file
        if (file) {
            const reader = new FileReader(); // Create a FileReader to read the file
            reader.onload = function(e) {
                const preview = document.getElementById('postImagePreview');
                preview.src = e.target.result; // Set the <img> src to the file content
                preview.style.display = 'block'; // Show the preview image
            };
            reader.readAsDataURL(file); // Read the file as a data URL
        }
    }

document.getElementById('image').addEventListener('change', function (event) {
    const file = event.target.files[0];
    const preview = document.getElementById('postImagePreview');
    const placeholder = document.getElementById('placeholder');

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.classList.add('show'); // Show the image
            placeholder.classList.add('hidden'); // Hide the placeholder
        };

        reader.readAsDataURL(file);
    } else {
        preview.classList.remove('show');
        placeholder.classList.remove('hidden');
    }
});