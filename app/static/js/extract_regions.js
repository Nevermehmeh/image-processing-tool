document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const templateSelect = document.getElementById('template-select');
    const imageUpload = document.getElementById('image-upload');
    const loadImageBtn = document.getElementById('load-image');
    const imageContainer = document.getElementById('image-container');
    const imagePreview = document.getElementById('image-preview');
    const dropZone = document.getElementById('drop-zone');
    const previewContainer = document.getElementById('preview-container');
    const extractForm = document.getElementById('extract-form');
    const processAnotherBtn = document.getElementById('process-another');
    const region1Preview = document.getElementById('region1-preview');
    const region2Preview = document.getElementById('region2-preview');
    const downloadRegion1 = document.getElementById('download-region1');
    const downloadRegion2 = document.getElementById('download-region2');
    
    // State
    let currentTemplate = null;
    let currentImage = null;
    
    // Initialize the application
    init();
    
    function init() {
        // Initialize event listeners
        setupEventListeners();
        
        // Load templates
        loadTemplates();
    }
    
    function setupEventListeners() {
        // File upload
        loadImageBtn.addEventListener('click', handleImageUpload);
        imageUpload.addEventListener('change', handleImageUpload);
        
        // Template selection
        templateSelect.addEventListener('change', handleTemplateSelect);
        
        // Process another image
        processAnotherBtn.addEventListener('click', resetForm);
        
        // Drag and drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            imageContainer.addEventListener(eventName, preventDefaults, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            imageContainer.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            imageContainer.addEventListener(eventName, unhighlight, false);
        });
        
        imageContainer.addEventListener('drop', handleDrop, false);
    }
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight() {
        imageContainer.classList.add('bg-light');
    }
    
    function unhighlight() {
        imageContainer.classList.remove('bg-light');
    }
    
    async function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            await handleImageFile(files[0]);
        }
    }
    
    async function handleImageUpload() {
        const file = imageUpload.files[0];
        if (file) {
            await handleImageFile(file);
        }
    }
    
    async function handleImageFile(file) {
        const validation = validateImageFile(file, 20); // 20MB max
        if (!validation.valid) {
            showAlert('danger', validation.message);
            return;
        }
        
        try {
            const dataUrl = await readFileAsDataURL(file);
            currentImage = file;
            await loadImage(dataUrl);
            
            // Show extract button if template is selected
            if (currentTemplate) {
                extractRegions();
            }
        } catch (error) {
            console.error('Error loading image:', error);
            showAlert('danger', 'Failed to load image. Please try again.');
        }
    }
    
    function loadImage(src) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                // Check image size
                if (img.naturalWidth > 6000 || img.naturalHeight > 6000) {
                    reject(new Error('Image dimensions exceed the maximum allowed size of 6000x6000px'));
                    return;
                }
                
                // Scale image to fit container while maintaining aspect ratio
                const containerWidth = imageContainer.clientWidth;
                const containerHeight = imageContainer.clientHeight;
                
                const imageAspectRatio = img.naturalWidth / img.naturalHeight;
                let width = containerWidth;
                let height = containerWidth / imageAspectRatio;
                
                if (height > containerHeight) {
                    height = containerHeight;
                    width = height * imageAspectRatio;
                }
                
                imagePreview.style.width = `${width}px`;
                imagePreview.style.height = `${height}px`;
                
                imagePreview.src = src;
                imagePreview.style.display = 'block';
                dropZone.style.display = 'none';
                
                resolve();
            };
            
            img.onerror = () => {
                reject(new Error('Failed to load image'));
            };
            
            img.src = src;
        });
    }
    
    async function loadTemplates() {
        try {
            const response = await fetch('/api/templates');
            if (!response.ok) {
                throw new Error('Failed to load templates');
            }
            
            const templates = await response.json();
            
            // Clear existing options except the first one
            while (templateSelect.options.length > 1) {
                templateSelect.remove(1);
            }
            
            // Add templates to select
            templates.forEach(template => {
                const option = document.createElement('option');
                option.value = template.id;
                option.textContent = template.name;
                templateSelect.appendChild(option);
            });
            
        } catch (error) {
            console.error('Error loading templates:', error);
            showAlert('danger', 'Failed to load templates. Please refresh the page to try again.');
        }
    }
    
    async function handleTemplateSelect(e) {
        const templateId = e.target.value;
        if (!templateId) return;
        
        try {
            const response = await fetch(`/api/templates/${templateId}`);
            if (!response.ok) {
                throw new Error('Failed to load template details');
            }
            
            currentTemplate = await response.json();
            
            // Show template info in modal (optional)
            showTemplateInfo(currentTemplate);
            
            // If image is already loaded, extract regions
            if (currentImage) {
                extractRegions();
            }
            
        } catch (error) {
            console.error('Error loading template:', error);
            showAlert('danger', 'Failed to load template. Please try again.');
        }
    }
    
    function showTemplateInfo(template) {
        // This is a placeholder. You can implement a modal or tooltip to show template details
        console.log('Selected template:', template);
    }
    
    async function extractRegions() {
        if (!currentTemplate || !currentImage) return;
        
        const loadingModal = showLoading('Extracting regions...');
        
        try {
            // Create FormData to send the image
            const formData = new FormData();
            formData.append('file', currentImage);
            formData.append('template_id', currentTemplate.id);
            
            // Send to server for processing
            const response = await fetch('/api/extract-regions', {
                method: 'POST',
                body: formData,
                // Khi sử dụng FormData, không cần set Content-Type,
                // trình duyệt sẽ tự động thêm boundary phù hợp
                // headers: {
                //     'Accept': 'application/json'
                // }
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to extract regions');
            }
            
            const result = await response.json();
            
            // Update previews
            region1Preview.src = result.region1.url;
            region2Preview.src = result.region2.url;
            
            // Update download links
            downloadRegion1.href = result.region1.url;
            downloadRegion1.download = result.region1.filename;
            downloadRegion2.href = result.region2.url;
            downloadRegion2.download = result.region2.filename;
            
            // Show preview container
            previewContainer.style.display = 'block';
            
            // Scroll to preview
            previewContainer.scrollIntoView({ behavior: 'smooth' });
            
        } catch (error) {
            console.error('Error extracting regions:', error);
            showAlert('danger', error.message || 'Failed to extract regions');
        } finally {
            hideLoading(loadingModal);
        }
    }
    
    function resetForm() {
        // Reset form
        extractForm.reset();
        
        // Reset image preview
        imagePreview.src = '';
        imagePreview.style.display = 'none';
        dropZone.style.display = 'block';
        
        // Reset previews
        region1Preview.src = '#';
        region2Preview.src = '#';
        
        // Hide preview container
        previewContainer.style.display = 'none';
        
        // Reset state
        currentImage = null;
        currentTemplate = null;
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});
