let currentImage = null;
let imageTransform = {
    scale: 1,
    rotate: 0,
    translateX: 0,
    translateY: 0
};

function loadImageEditor(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        currentImage = e.target.result;
        const previewImg = document.getElementById('preview-image');
        previewImg.src = currentImage;
        previewImg.style.objectFit = 'contain';
        
        document.getElementById('image-editor').style.display = 'block';
        resetControls();
    };
    reader.readAsDataURL(file);
}

function resetControls() {
    imageTransform = { scale: 1, rotate: 0, translateX: 0, translateY: 0 };
    
    document.getElementById('zoom-slider').value = 1;
    document.getElementById('rotate-slider').value = 0;
    document.getElementById('position-x').value = 0;
    document.getElementById('position-y').value = 0;
    
    updatePreview();
}

function updatePreview() {
    const img = document.getElementById('preview-image');
    const transform = `
        scale(${imageTransform.scale}) 
        rotate(${imageTransform.rotate}deg) 
        translate(${imageTransform.translateX}px, ${imageTransform.translateY}px)
    `;
    
    img.style.transform = transform;
    
    // Atualizar valores exibidos
    document.getElementById('zoom-value').textContent = Math.round(imageTransform.scale * 100) + '%';
    document.getElementById('rotate-value').textContent = imageTransform.rotate + '°';
}

function resetImage() {
    resetControls();
}

function applyChanges() {
    // Criar canvas para processar a imagem
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = function() {
        // Definir tamanho do canvas (quadrado para foto de perfil)
        const size = 300;
        canvas.width = size;
        canvas.height = size;
        
        // Configurar transformações
        ctx.save();
        ctx.translate(size/2, size/2);
        ctx.scale(imageTransform.scale, imageTransform.scale);
        ctx.rotate(imageTransform.rotate * Math.PI / 180);
        ctx.translate(imageTransform.translateX, imageTransform.translateY);
        
        // Desenhar imagem centralizada
        const aspectRatio = img.width / img.height;
        let drawWidth, drawHeight;
        
        if (aspectRatio > 1) {
            drawWidth = size;
            drawHeight = size / aspectRatio;
        } else {
            drawWidth = size * aspectRatio;
            drawHeight = size;
        }
        
        ctx.drawImage(img, -drawWidth/2, -drawHeight/2, drawWidth, drawHeight);
        ctx.restore();
        
        // Converter para base64 e armazenar
        const imageData = canvas.toDataURL('image/jpeg', 0.9);
        document.getElementById('image-data').value = imageData;
        
        // Feedback visual
        const applyBtn = document.querySelector('.editor-buttons button:last-child');
        const originalText = applyBtn.textContent;
        applyBtn.textContent = 'Aplicado!';
        applyBtn.style.background = '#4CAF50';
        
        setTimeout(() => {
            applyBtn.textContent = originalText;
            applyBtn.style.background = '';
        }, 1500);
    };
    
    img.src = currentImage;
}

// Event listeners para os controles
document.addEventListener('DOMContentLoaded', function() {
    const zoomSlider = document.getElementById('zoom-slider');
    const rotateSlider = document.getElementById('rotate-slider');
    const positionX = document.getElementById('position-x');
    const positionY = document.getElementById('position-y');
    
    if (zoomSlider) {
        zoomSlider.addEventListener('input', function() {
            imageTransform.scale = parseFloat(this.value);
            updatePreview();
        });
    }
    
    if (rotateSlider) {
        rotateSlider.addEventListener('input', function() {
            imageTransform.rotate = parseInt(this.value);
            updatePreview();
        });
    }
    
    if (positionX) {
        positionX.addEventListener('input', function() {
            imageTransform.translateX = parseInt(this.value);
            updatePreview();
        });
    }
    
    if (positionY) {
        positionY.addEventListener('input', function() {
            imageTransform.translateY = parseInt(this.value);
            updatePreview();
        });
    }
});