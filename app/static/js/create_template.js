document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const imageUpload = document.getElementById('image-upload');
    const loadImageBtn = document.getElementById('load-image');
    const imageContainer = document.getElementById('image-container');
    const imagePreview = document.getElementById('image-preview');
    const dropZone = document.getElementById('drop-zone');
    const regionsContainer = document.getElementById('regions-container');
    const templateForm = document.getElementById('template-form');
    const resetRegionsBtn = document.getElementById('reset-regions');
    const saveTemplateBtn = document.getElementById('save-template');
    
    // Region inputs
    const region1Width = document.getElementById('region1-width');
    const region1Height = document.getElementById('region1-height');
    const region1Lock = document.getElementById('region1-lock');
    const region2Width = document.getElementById('region2-width');
    const region2Height = document.getElementById('region2-height');
    const region2Lock = document.getElementById('region2-lock');
    
    // State
    let regions = [];
    let isDragging = false;
    let currentRegion = null;
    let startX, startY, startLeft, startTop, startWidth, startHeight;
    let isResizing = false;
    let currentHandle = null;
    let imageAspectRatio = 1;
    let imageNaturalWidth = 0;
    let imageNaturalHeight = 0;
    
    // Initialize the application
    init();
    
    function init() {
        // Initialize event listeners
        setupEventListeners();
        
        // Create region elements
        createRegion('region1', 'rgba(255, 0, 0, 0.3)', 'Region 1');
        createRegion('region2', 'rgba(0, 0, 255, 0.3)', 'Region 2');
    }
    
    function setupEventListeners() {
        // File upload
        loadImageBtn.addEventListener('click', handleImageUpload);
        imageUpload.addEventListener('change', handleImageUpload);
        
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
        
        // Region size inputs
        [region1Width, region1Height].forEach(input => {
            input.addEventListener('input', () => updateRegionSize('region1'));
        });
        
        [region2Width, region2Height].forEach(input => {
            input.addEventListener('input', () => updateRegionSize('region2'));
        });
        
        // Form submission
        templateForm.addEventListener('submit', handleFormSubmit);
        resetRegionsBtn.addEventListener('click', resetRegions);
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
            await loadImage(dataUrl);
            regionsContainer.style.display = 'block';
        } catch (error) {
            console.error('Error loading image:', error);
            showAlert('danger', 'Failed to load image. Please try again.');
        }
    }
    
    function loadImage(src) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                // Store natural dimensions for scaling
                imageNaturalWidth = img.naturalWidth;
                imageNaturalHeight = img.naturalHeight;
                imageAspectRatio = img.naturalWidth / img.naturalHeight;
                
                // Check image size
                if (img.naturalWidth > 9000 || img.naturalHeight > 9000) {
                    reject(new Error('Image dimensions exceed the maximum allowed size of 9000x9000px'));
                    return;
                }
                
                // Scale image to fit container while maintaining aspect ratio
                const containerWidth = imageContainer.clientWidth;
                const containerHeight = imageContainer.clientHeight;
                
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
                
                // Initialize regions
                initializeRegions();
                
                resolve();
            };
            
            img.onerror = () => {
                reject(new Error('Failed to load image'));
            };
            
            img.src = src;
        });
    }
    
    function createRegion(id, color, label) {
        const region = document.createElement('div');
        region.className = 'region';
        region.id = id;
        region.style.backgroundColor = color;
        region.textContent = label;
        
        // Create resize handles
        const handles = ['nw', 'ne', 'sw', 'se'];
        handles.forEach(handle => {
            const handleEl = document.createElement('div');
            handleEl.className = `region-handle ${handle}`;
            handleEl.dataset.handle = handle;
            region.appendChild(handleEl);
            
            // Add event listeners for resizing
            handleEl.addEventListener('mousedown', startResize);
        });
        
        // Add event listeners for dragging
        region.addEventListener('mousedown', startDrag);
        
        // Add to DOM
        imageContainer.appendChild(region);
        
        // Store reference
        regions.push({
            id,
            element: region,
            color,
            width: 200,
            height: 200,
            x: 0,
            y: 0
        });
        
        return region;
    }
    
    function initializeRegions() {
        const containerRect = imageContainer.getBoundingClientRect();
        const imageRect = imagePreview.getBoundingClientRect();
        
        // Calculate scale factors
        const scaleX = imageRect.width / imageNaturalWidth;
        const scaleY = imageRect.height / imageNaturalHeight;
        
        // Position regions
        regions.forEach((region, index) => {
            // Calculate initial position (stagger regions)
            const x = 50 + (index * 60);
            const y = 50 + (index * 60);
            
            // Update region state
            region.x = x / scaleX;
            region.y = y / scaleY;
            region.width = 200 / scaleX;
            region.height = 200 / scaleY;
            
            // Update UI
            updateRegionElement(region);
            
            // Update input fields
            if (index === 0) {
                region1Width.value = Math.round(region.width);
                region1Height.value = Math.round(region.height);
            } else {
                region2Width.value = Math.round(region.width);
                region2Height.value = Math.round(region.height);
            }
        });
    }
    
    function updateRegionElement(region) {
        const containerRect = imageContainer.getBoundingClientRect();
        const imageRect = imagePreview.getBoundingClientRect();
        
        // Calculate scale factors
        const scaleX = imageRect.width / imageNaturalWidth;
        const scaleY = imageRect.height / imageNaturalHeight;
        
        // Calculate position relative to container
        const left = imageRect.left - containerRect.left + (region.x * scaleX);
        const top = imageRect.top - containerRect.top + (region.y * scaleY);
        const width = region.width * scaleX;
        const height = region.height * scaleY;
        
        // Update element
        region.element.style.left = `${left}px`;
        region.element.style.top = `${top}px`;
        region.element.style.width = `${width}px`;
        region.element.style.height = `${height}px`;
    }
    
    function startDrag(e) {
        if (e.target.classList.contains('region-handle')) {
            return; // Let resize handle take over
        }
        
        e.preventDefault();
        
        currentRegion = regions.find(r => r.element === this);
        if (!currentRegion) return;
        
        isDragging = true;
        
        const containerRect = imageContainer.getBoundingClientRect();
        const imageRect = imagePreview.getBoundingClientRect();
        
        // Calculate scale factors
        const scaleX = imageRect.width / imageNaturalWidth;
        const scaleY = imageRect.height / imageNaturalHeight;
        
        // Calculate initial position
        startX = e.clientX;
        startY = e.clientY;
        startLeft = currentRegion.x * scaleX;
        startTop = currentRegion.y * scaleY;
        
        // Add event listeners
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', stopDrag);
    }
    
    function drag(e) {
        if (!isDragging || !currentRegion) return;
        
        const containerRect = imageContainer.getBoundingClientRect();
        const imageRect = imagePreview.getBoundingClientRect();
        
        // Calculate scale factors
        const scaleX = imageRect.width / imageNaturalWidth;
        const scaleY = imageRect.height / imageNaturalHeight;
        
        // Calculate new position
        let newLeft = startLeft + (e.clientX - startX);
        let newTop = startTop + (e.clientY - startY);
        
        // Convert back to image coordinates
        const newX = Math.max(0, Math.min(newLeft / scaleX, imageNaturalWidth - currentRegion.width));
        const newY = Math.max(0, Math.min(newTop / scaleY, imageNaturalHeight - currentRegion.height));
        
        // Update region state
        currentRegion.x = newX;
        currentRegion.y = newY;
        
        // Update UI
        updateRegionElement(currentRegion);
    }
    
    function stopDrag() {
        isDragging = false;
        currentRegion = null;
        
        // Remove event listeners
        document.removeEventListener('mousemove', drag);
        document.removeEventListener('mouseup', stopDrag);
    }
    
    function startResize(e) {
        e.preventDefault();
        e.stopPropagation();
        
        currentRegion = regions.find(r => r.element.contains(this));
        if (!currentRegion) return;
        
        isResizing = true;
        currentHandle = this.dataset.handle;
        
        const containerRect = imageContainer.getBoundingClientRect();
        const imageRect = imagePreview.getBoundingClientRect();
        
        // Calculate scale factors
        const scaleX = imageRect.width / imageNaturalWidth;
        const scaleY = imageRect.height / imageNaturalHeight;
        
        // Store initial values
        startX = e.clientX;
        startY = e.clientY;
        startLeft = currentRegion.x * scaleX;
        startTop = currentRegion.y * scaleY;
        startWidth = currentRegion.width * scaleX;
        startHeight = currentRegion.height * scaleY;
        
        // Add event listeners
        document.addEventListener('mousemove', resize);
        document.addEventListener('mouseup', stopResize);
    }
    
    function resize(e) {
        if (!isResizing || !currentRegion) return;
        
        const containerRect = imageContainer.getBoundingClientRect();
        const imageRect = imagePreview.getBoundingClientRect();
        
        // Calculate scale factors
        const scaleX = imageRect.width / imageNaturalWidth;
        const scaleY = imageRect.height / imageNaturalHeight;
        
        // Calculate delta
        const deltaX = e.clientX - startX;
        const deltaY = e.clientY - startY;
        
        // Calculate new dimensions and position
        let newLeft = startLeft;
        let newTop = startTop;
        let newWidth = startWidth;
        let newHeight = startHeight;
        
        // Apply resizing based on handle
        if (currentHandle.includes('w')) {
            newLeft += deltaX;
            newWidth -= deltaX;
        }
        
        if (currentHandle.includes('e')) {
            newWidth += deltaX;
        }
        
        if (currentHandle.includes('n')) {
            newTop += deltaY;
            newHeight -= deltaY;
        }
        
        if (currentHandle.includes('s')) {
            newHeight += deltaY;
        }
        
        // Enforce minimum size
        const minSize = 20; // pixels
        if (Math.abs(newWidth) < minSize) {
            if (currentHandle.includes('w')) {
                newLeft = newLeft + newWidth - (newWidth > 0 ? minSize : -minSize);
            }
            newWidth = newWidth > 0 ? minSize : -minSize;
        }
        
        if (Math.abs(newHeight) < minSize) {
            if (currentHandle.includes('n')) {
                newTop = newTop + newHeight - (newHeight > 0 ? minSize : -minSize);
            }
            newHeight = newHeight > 0 ? minSize : -minSize;
        }
        
        // Convert back to image coordinates
        const regionX = Math.max(0, Math.min(newLeft / scaleX, imageNaturalWidth));
        const regionY = Math.max(0, Math.min(newTop / scaleY, imageNaturalHeight));
        const regionWidth = Math.max(minSize / scaleX, Math.min(Math.abs(newWidth) / scaleX, imageNaturalWidth - regionX));
        const regionHeight = Math.max(minSize / scaleY, Math.min(Math.abs(newHeight) / scaleY, imageNaturalHeight - regionY));
        
        // Update region state
        currentRegion.x = regionX;
        currentRegion.y = regionY;
        currentRegion.width = regionWidth;
        currentRegion.height = regionHeight;
        
        // Update input fields
        if (currentRegion.id === 'region1') {
            region1Width.value = Math.round(regionWidth);
            region1Height.value = Math.round(regionHeight);
        } else {
            region2Width.value = Math.round(regionWidth);
            region2Height.value = Math.round(regionHeight);
        }
        
        // Update UI
        updateRegionElement(currentRegion);
    }
    
    function stopResize() {
        isResizing = false;
        currentRegion = null;
        currentHandle = null;
        
        // Remove event listeners
        document.removeEventListener('mousemove', resize);
        document.removeEventListener('mouseup', stopResize);
    }
    
    function updateRegionSize(regionId) {
        const region = regions.find(r => r.id === regionId);
        if (!region) return;
        
        // Get values from inputs
        let width, height;
        
        if (regionId === 'region1') {
            width = parseInt(region1Width.value) || 0;
            height = parseInt(region1Height.value) || 0;
            
            // Maintain aspect ratio if locked
            if (region1Lock.checked && region1Width === document.activeElement) {
                const aspectRatio = region.width / region.height;
                height = Math.round(width / aspectRatio);
                region1Height.value = height;
            } else if (region1Lock.checked && region1Height === document.activeElement) {
                const aspectRatio = region.width / region.height;
                width = Math.round(height * aspectRatio);
                region1Width.value = width;
            }
        } else {
            width = parseInt(region2Width.value) || 0;
            height = parseInt(region2Height.value) || 0;
            
            // Maintain aspect ratio if locked
            if (region2Lock.checked && region2Width === document.activeElement) {
                const aspectRatio = region.width / region.height;
                height = Math.round(width / aspectRatio);
                region2Height.value = height;
            } else if (region2Lock.checked && region2Height === document.activeElement) {
                const aspectRatio = region.width / region.height;
                width = Math.round(height * aspectRatio);
                region2Width.value = width;
            }
        }
        
        // Update region state
        region.width = width;
        region.height = height;
        
        // Update UI
        updateRegionElement(region);
    }
    
    function resetRegions() {
        if (confirm('Are you sure you want to reset all regions to their default positions?')) {
            initializeRegions();
        }
    }
    
    async function handleFormSubmit(e) {
        e.preventDefault();
        
        // Validate form
        const templateName = document.getElementById('template-name').value.trim();
        if (!templateName) {
            showAlert('danger', 'Vui lòng nhập tên template');
            return;
        }
        
        if (!imagePreview.src) {
            showAlert('danger', 'Vui lòng tải lên ảnh trước');
            return;
        }
        
        // Check if regions overlap
        if (checkRegionsOverlap()) {
            showAlert('danger', 'Các vùng không được chồng lên nhau. Vui lòng điều chỉnh vị trí.');
            return;
        }
        
        // Show loading state
        const loadingModal = showLoading('Đang lưu template...');
        
        try {
            console.log('Bắt đầu tạo preview template...');
            const previewImage = await createTemplatePreview();
            console.log('Đã tạo xong preview template');
            
            // Create template data
            const templateData = {
                name: templateName,
                original_width: imageNaturalWidth,
                original_height: imageNaturalHeight,
                region1: {
                    width: regions[0].width,
                    height: regions[0].height,
                    x: regions[0].x,
                    y: regions[0].y
                },
                region2: {
                    width: regions[1].width,
                    height: regions[1].height,
                    x: regions[1].x,
                    y: regions[1].y
                },
                // Add image data for preview
                image: previewImage
            };
            
            console.log('Đang gửi dữ liệu đến máy chủ...', templateData);
            
            // Log kích thước của ảnh base64 (tính bằng KB)
            if (templateData.image) {
                console.log('Kích thước ảnh base64:', Math.round(templateData.image.length / 1024) + 'KB');
            }
            
            // Log dữ liệu region
            console.log('Region 1:', templateData.region1);
            console.log('Region 2:', templateData.region2);
            
            // Send to server
            let response;
            try {
                response = await fetch('/api/templates', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(templateData)
                });
            } catch (error) {
                console.error('Lỗi khi gọi API:', error);
                throw error;
            }
            
            const responseData = await response.text();
            
            if (!response.ok) {
                let errorData;
                try {
                    errorData = JSON.parse(responseData);
                    console.error('Lỗi từ máy chủ (JSON):', errorData);
                } catch (e) {
                    console.error('Lỗi từ máy chủ (raw):', responseData);
                    errorData = { error: responseData || `Lỗi không xác định (${response.status} ${response.statusText})` };
                }
                
                // Hiển thị chi tiết lỗi từ server nếu có
                const errorMessage = errorData.error || errorData.message || 
                                   `Không thể lưu template. Mã lỗi: ${response.status}`;
                console.error('Chi tiết lỗi:', errorData);
                throw new Error(errorMessage);
            }
            
            // Parse dữ liệu phản hồi thành JSON
            let result;
            try {
                result = JSON.parse(responseData);
                console.log('Phản hồi từ máy chủ:', result);
            } catch (e) {
                console.error('Lỗi khi phân tích phản hồi JSON:', e);
                throw new Error('Lỗi khi xử lý phản hồi từ máy chủ');
            }
            
            // Show success message
            showAlert('success', 'Đã lưu template thành công!');
            
            // Reset form
            templateForm.reset();
            imagePreview.src = '';
            imagePreview.style.display = 'none';
            dropZone.style.display = 'block';
            regionsContainer.style.display = 'none';
            
            // Redirect to extract page
            setTimeout(() => {
                window.location.href = '/extract-regions';
            }, 1500);
            
        } catch (error) {
            console.error('Lỗi khi lưu template:', error);
            showAlert('danger', error.message || 'Đã xảy ra lỗi khi lưu template. Vui lòng thử lại.');
        } finally {
            hideLoading(loadingModal);
        }
    }
    
    function checkRegionsOverlap() {
        if (regions.length < 2) return false;
        
        const r1 = regions[0];
        const r2 = regions[1];
        
        return !(r1.x + r1.width < r2.x || 
                r2.x + r2.width < r1.x || 
                r1.y + r1.height < r2.y || 
                r2.y + r2.height < r1.y);
    }
    
    async function createTemplatePreview() {
        try {
            console.log('Bắt đầu tạo preview...');
            console.log('Kích thước ảnh gốc:', imageNaturalWidth, 'x', imageNaturalHeight);
            
            // Tạo canvas để vẽ preview
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Đặt kích thước canvas phù hợp với ảnh
            canvas.width = imageNaturalWidth;
            canvas.height = imageNaturalHeight;
            
            // Vẽ ảnh lên canvas
            const img = new Image();
            img.crossOrigin = 'Anonymous'; // Giúp tránh lỗi CORS
            
            // Tạo một promise để đợi ảnh tải xong
            await new Promise((resolve, reject) => {
                img.onload = resolve;
                img.onerror = (e) => {
                    console.error('Lỗi khi tải ảnh:', e);
                    reject(new Error('Không thể tải ảnh'));
                };
                
                // Kiểm tra xem có phải là data URL không
                if (imagePreview.src.startsWith('data:')) {
                    img.src = imagePreview.src;
                } else {
                    // Nếu không phải data URL, thử tạo một canvas mới để vẽ lại ảnh
                    const tempCanvas = document.createElement('canvas');
                    const tempCtx = tempCanvas.getContext('2d');
                    tempCanvas.width = imagePreview.naturalWidth;
                    tempCanvas.height = imagePreview.naturalHeight;
                    tempCtx.drawImage(imagePreview, 0, 0);
                    img.src = tempCanvas.toDataURL('image/png');
                }
            });
            
            console.log('Đã tải xong ảnh, kích thước:', img.width, 'x', img.height);
            
            // Vẽ ảnh lên canvas
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            
            // Vẽ các vùng đã chọn
            regions.forEach((region, index) => {
                if (!region) return;
                
                console.log(`Vẽ vùng ${index + 1}:`, region);
                
                // Vẽ đường viền
                ctx.strokeStyle = region.id === 'region1' ? 'red' : 'blue';
                ctx.lineWidth = 5;
                ctx.strokeRect(
                    region.x,
                    region.y,
                    region.width,
                    region.height
                );
                
                // Thêm nhãn
                ctx.fillStyle = region.id === 'region1' ? 'red' : 'blue';
                ctx.font = 'bold 24px Arial';
                ctx.fillText(
                    region.id === 'region1' ? 'Vùng 1' : 'Vùng 2',
                    region.x + 10,
                    region.y + 30
                );
            });
            
            console.log('Đã vẽ xong các vùng, đang chuyển đổi sang data URL...');
            
            // Chuyển đổi thành data URL
            const dataUrl = canvas.toDataURL('image/png');
            console.log('Đã tạo xong data URL, độ dài:', dataUrl.length);
            
            return dataUrl;
            
        } catch (error) {
            console.error('Lỗi khi tạo preview:', error);
            throw new Error('Không thể tạo preview: ' + error.message);
        }
    }
});
