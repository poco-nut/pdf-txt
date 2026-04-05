document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const uploadArea = document.getElementById('uploadArea');
    const fileInfo = document.getElementById('fileInfo');
    const convertBtn = document.getElementById('convertBtn');
    const resetBtn = document.getElementById('resetBtn');
    const progressContainer = document.getElementById('progressContainer');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    const result = document.getElementById('result');

    let selectedFile = null;

    // 点击浏览按钮触发文件输入
    browseBtn.addEventListener('click', () => {
        fileInput.click();
    });

    // 点击上传区域触发文件输入
    uploadArea.addEventListener('click', (e) => {
        if (e.target !== browseBtn && e.target.tagName !== 'BUTTON') {
            fileInput.click();
        }
    });

    // 文件输入变化事件
    fileInput.addEventListener('change', handleFileSelect);

    // 拖放功能
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');

        if (e.dataTransfer.files.length) {
            const file = e.dataTransfer.files[0];
            if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
                selectedFile = file;
                updateFileInfo(file);
            } else {
                showError('Please select a PDF file.');
            }
        }
    });

    // 处理文件选择
    function handleFileSelect(e) {
        const file = e.target.files[0];
        if (!file) return;

        if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
            selectedFile = file;
            updateFileInfo(file);
        } else {
            showError('Please select a PDF file.');
            fileInput.value = '';
        }
    }

    // 更新文件信息显示
    function updateFileInfo(file) {
        const fileSize = (file.size / (1024 * 1024)).toFixed(2); // MB

        fileInfo.innerHTML = `
            <div class="file-info-content">
                <div class="file-icon">
                    <i class="fas fa-file-pdf"></i>
                </div>
                <div class="file-details">
                    <h4>${file.name}</h4>
                    <p>Size: ${fileSize} MB</p>
                </div>
            </div>
        `;
        fileInfo.classList.add('show');
        convertBtn.disabled = false;
    }

    // 转换按钮点击事件
    convertBtn.addEventListener('click', convertFile);

    // 重置按钮点击事件
    resetBtn.addEventListener('click', resetAll);

    // 转换文件
    async function convertFile() {
        if (!selectedFile) {
            showError('No file selected.');
            return;
        }

        // 检查文件大小（限制50MB）
        if (selectedFile.size > 50 * 1024 * 1024) {
            showError('File size exceeds 50MB limit.');
            return;
        }

        // 禁用转换按钮，显示进度条
        convertBtn.disabled = true;
        progressContainer.style.display = 'block';
        progressFill.style.width = '30%';
        progressText.textContent = 'Uploading PDF...';
        hideResult();

        // 创建FormData对象
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            // 发送到后端
            progressFill.style.width = '60%';
            progressText.textContent = 'Converting to text...';

            const response = await fetch('http://localhost:5000/api/convert', {
                method: 'POST',
                body: formData
            });

            progressFill.style.width = '90%';
            progressText.textContent = 'Processing result...';

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Server error: ${response.status}`);
            }

            // 获取文件名
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'converted.txt';
            if (contentDisposition) {
                const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition);
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, '');
                }
            }

            // 创建Blob并下载
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            // 显示成功消息
            progressFill.style.width = '100%';
            progressText.textContent = 'Conversion complete!';

            setTimeout(() => {
                showSuccess('File converted and downloaded successfully!');
                progressContainer.style.display = 'none';
                convertBtn.disabled = false;
            }, 500);

        } catch (error) {
            console.error('Conversion error:', error);
            showError(`Conversion failed: ${error.message}`);
            progressContainer.style.display = 'none';
            convertBtn.disabled = false;
        }
    }

    // 重置所有
    function resetAll() {
        selectedFile = null;
        fileInput.value = '';
        fileInfo.classList.remove('show');
        convertBtn.disabled = true;
        progressContainer.style.display = 'none';
        hideResult();
    }

    // 显示成功消息
    function showSuccess(message) {
        result.innerHTML = `
            <div class="success">
                <h3><i class="fas fa-check-circle"></i> Success!</h3>
                <p>${message}</p>
            </div>
        `;
        result.className = 'result success';
        result.style.display = 'block';
    }

    // 显示错误消息
    function showError(message) {
        result.innerHTML = `
            <div class="error">
                <h3><i class="fas fa-exclamation-triangle"></i> Error</h3>
                <p>${message}</p>
            </div>
        `;
        result.className = 'result error';
        result.style.display = 'block';
    }

    // 隐藏结果消息
    function hideResult() {
        result.style.display = 'none';
    }

    // 初始状态
    resetAll();
});