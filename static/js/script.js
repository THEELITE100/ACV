const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const generateBtn = document.getElementById('generate-btn');
const loading = document.getElementById('loading');
const resultContainer = document.getElementById('result-container');
const controlsCard = document.getElementById('controls-card');
const imagePreview = document.getElementById('image-preview');
const uploadContent = document.getElementById('upload-content');
const resetBtn = document.getElementById('reset-btn');
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        handleFileSelection();
    }
});
fileInput.addEventListener('change', handleFileSelection);
function handleFileSelection() {
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        generateBtn.disabled = false;        
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'inline-block';
            uploadContent.style.display = 'none';
        }
        reader.readAsDataURL(file);
    }
}
generateBtn.addEventListener('click', async () => {
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('style', document.querySelector('input[name="style"]:checked').value);
    controlsCard.style.display = 'none';
    resultContainer.style.display = 'none';
    loading.style.display = 'block';

    try {
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById('img-before').src = data.original_url;
            document.getElementById('img-after').src = data.processed_url;
            document.getElementById('download-btn').href = data.processed_url;            
            loading.style.display = 'none';
            resultContainer.style.display = 'block';
        } else {
            alert(data.error);
            resetApp();
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong processing your image!");
        resetApp();
    }
});
resetBtn.addEventListener('click', resetApp);
function resetApp() {
    fileInput.value = "";
    generateBtn.disabled = true;    
    imagePreview.style.display = 'none';
    imagePreview.src = '';
    uploadContent.style.display = 'block';
    resultContainer.style.display = 'none';
    loading.style.display = 'none';
    controlsCard.style.display = 'block';
}