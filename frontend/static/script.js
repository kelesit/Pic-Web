document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const preview = document.getElementById('preview');
    const processBtn = document.getElementById('processBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const loading = document.getElementById('loading');
    let currentFile = null;

    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#000';
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#ccc';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#ccc';
        const file = e.dataTransfer.files[0];
        handleFile(file);
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        handleFile(file);
    });

    processBtn.style.display = 'none';
    downloadBtn.style.display = 'none';

    function handleFile(file) {
        if (file && file.type.startsWith('image/')) {
            currentFile = file;
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.src = e.target.result;
                preview.style.display = 'block';
                processBtn.style.display = 'inline-block';
                downloadBtn.style.display = 'none';
                document.querySelector('.image-preview').style.display = 'block';

                console.log('File loaded, processBtn:', processBtn.style.display);
            };
            reader.readAsDataURL(file);
        }
    }

    processBtn.addEventListener('click', async() => {
        if (!currentFile) return;

        loading.style.display = 'block';
        const formData = new FormData();
        formData.append('image', currentFile);

        try {
            const response = await fetch('/api/v1/process', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                preview.src = URL.createObjectURL(blob);
                downloadBtn.style.display = 'inline-block';
            } else {
                alert('Error processing image');
            }
        } catch (error) {
            console.error(error);
            alert('Error processing image');
        } finally {
            loading.style.display = 'none';
        }
    });
});