// Particle Animation
const particleCanvas = document.getElementById('particleCanvas');
const ctx = particleCanvas.getContext('2d');

particleCanvas.width = window.innerWidth;
particleCanvas.height = window.innerHeight;

const particles = [];
const particleCount = 100;

class Particle {
    constructor() {
        this.x = Math.random() * particleCanvas.width;
        this.y = Math.random() * particleCanvas.height;
        this.size = Math.random() * 2 + 1;
        this.speedX = Math.random() * 0.5 - 0.25;
        this.speedY = Math.random() * 0.5 - 0.25;
        this.opacity = Math.random() * 0.5 + 0.2;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x > particleCanvas.width) this.x = 0;
        if (this.x < 0) this.x = particleCanvas.width;
        if (this.y > particleCanvas.height) this.y = 0;
        if (this.y < 0) this.y = particleCanvas.height;
    }

    draw() {
        ctx.fillStyle = `rgba(99, 102, 241, ${this.opacity})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function initParticles() {
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }
}

function animateParticles() {
    ctx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
    
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    // Draw connections
    particles.forEach((a, i) => {
        particles.slice(i + 1).forEach(b => {
            const dx = a.x - b.x;
            const dy = a.y - b.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 100) {
                ctx.strokeStyle = `rgba(99, 102, 241, ${0.1 * (1 - distance / 100)})`;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(a.x, a.y);
                ctx.lineTo(b.x, b.y);
                ctx.stroke();
            }
        });
    });

    requestAnimationFrame(animateParticles);
}

window.addEventListener('resize', () => {
    particleCanvas.width = window.innerWidth;
    particleCanvas.height = window.innerHeight;
});

// Mouse interaction with particles
particleCanvas.addEventListener('mousemove', (e) => {
    const mouseX = e.clientX;
    const mouseY = e.clientY;

    particles.forEach(particle => {
        const dx = mouseX - particle.x;
        const dy = mouseY - particle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 100) {
            particle.x -= dx * 0.02;
            particle.y -= dy * 0.02;
        }
    });
});

initParticles();
animateParticles();

// Loading Screen
let loadingProgress = 0;
const loadingTexts = [
    'Initializing AI System...',
    'Loading Neural Networks...',
    'Connecting to Backend...',
    'Preparing Interface...',
    'Almost Ready...'
];

function updateLoading() {
    const progressBar = document.getElementById('loadingProgress');
    const loadingText = document.getElementById('loadingText');
    
    if (loadingProgress < 100) {
        loadingProgress += Math.random() * 15 + 5;
        if (loadingProgress > 100) loadingProgress = 100;
        
        progressBar.style.width = loadingProgress + '%';
        
        const textIndex = Math.floor((loadingProgress / 100) * loadingTexts.length);
        if (textIndex < loadingTexts.length) {
            loadingText.textContent = loadingTexts[textIndex];
        }
        
        setTimeout(updateLoading, 200);
    } else {
        setTimeout(() => {
            document.getElementById('loadingScreen').classList.add('hidden');
            initializeApp();
        }, 500);
    }
}

function initializeApp() {
    // Load saved settings
    const savedEndpoint = localStorage.getItem('apiEndpoint');
    const savedApiKey = localStorage.getItem('apiKey');
    
    if (savedEndpoint) {
        document.getElementById('apiEndpoint').value = savedEndpoint;
    }
    if (savedApiKey) {
        document.getElementById('apiKey').value = savedApiKey;
    }
    
    // Load chat history from localStorage
    loadChatHistory();
    
    // Add welcome message
    setTimeout(() => {
        addMessage("Hello! I'm DavoodAI, your intelligent assistant. I can help you with various tasks using natural language processing and voice interaction. How can I assist you today?", 'ai');
    }, 500);
    
    showToast('System initialized successfully!', 'success');
}

updateLoading();

// Scroll to chat
function scrollToChat() {
    document.getElementById('chatSection').scrollIntoView({ behavior: 'smooth' });
}

// Chat functionality
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const typingIndicator = document.getElementById('typingIndicator');
let messageHistory = [];
let isTyping = false;

async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message || isTyping) return;

    // Add user message
    addMessage(message, 'user');
    chatInput.value = '';
    isTyping = true;

    // Show typing indicator
    typingIndicator.style.display = 'flex';

    // Get response delay from settings
    const responseDelay = parseInt(document.getElementById('responseDelay').value) || 1500;
    const useContext = document.getElementById('contextToggle').checked;

    try {
        // Call API
        const result = await aiApi.sendMessage(message, useContext);
        
        setTimeout(() => {
            typingIndicator.style.display = 'none';
            addMessage(result.response, 'ai');
            
            // Speak response if TTS is enabled
            if (document.getElementById('voiceToggle').checked) {
                ttsHandler.speak(result.response);
            }
            
            isTyping = false;
        }, responseDelay);
    } catch (error) {
        typingIndicator.style.display = 'none';
        addMessage('Sorry, I encountered an error. Please try again.', 'ai');
        isTyping = false;
        showToast('Error sending message', 'error');
    }
}

function sendQuickMessage(message) {
    chatInput.value = message;
    sendMessage();
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? 'U' : 'AI';

    const content = document.createElement('div');
    content.className = 'message-content';
    const p = document.createElement('p');
    
    // Parse markdown-like syntax
    let formattedText = text
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\*([^*]+)\*/g, '<em>$1</em>');
    
    p.innerHTML = formattedText;
    content.appendChild(p);
    
    // Add timestamp
    const timestamp = document.createElement('div');
    timestamp.className = 'message-timestamp';
    timestamp.textContent = new Date().toLocaleTimeString();
    content.appendChild(timestamp);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);

    // Store in history
    messageHistory.push({
        text: text,
        sender: sender,
        timestamp: new Date().toISOString()
    });
    
    // Save to localStorage
    saveChatHistory();
    
    // Check message limit
    const messageLimit = parseInt(document.getElementById('messageLimit').value) || 100;
    if (messageHistory.length > messageLimit) {
        messageHistory = messageHistory.slice(-messageLimit);
        const messages = chatMessages.querySelectorAll('.message');
        if (messages.length > messageLimit) {
            messages[0].remove();
        }
    }

    // Auto scroll
    if (document.getElementById('autoscrollToggle').checked) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function saveChatHistory() {
    localStorage.setItem('chatHistory', JSON.stringify(messageHistory));
}

function loadChatHistory() {
    const saved = localStorage.getItem('chatHistory');
    if (saved) {
        messageHistory = JSON.parse(saved);
        messageHistory.forEach(msg => {
            addMessageFromHistory(msg.text, msg.sender);
        });
    }
}

function addMessageFromHistory(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? 'U' : 'AI';

    const content = document.createElement('div');
    content.className = 'message-content';
    const p = document.createElement('p');
    p.textContent = text;
    content.appendChild(p);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);
}

function clearChat() {
    if (confirm('Are you sure you want to clear the chat?')) {
        chatMessages.innerHTML = '';
        messageHistory = [];
        saveChatHistory();
        aiApi.clearHistory();
        showToast('Chat cleared', 'info');
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function handleTyping() {
    // Could add "user is typing" indicator to backend
    const input = chatInput.value;
    const sendButton = document.getElementById('sendButton');
    
    if (input.trim()) {
        sendButton.style.background = 'linear-gradient(135deg, var(--primary), var(--secondary))';
    } else {
        sendButton.style.background = 'rgba(99, 102, 241, 0.3)';
    }
}

function handleAttachment() {
    showToast('File attachment feature coming soon!', 'info');
    // In production, this would open a file picker
}

// Voice functionality
let isVoiceActive = false;
let audioContext;
let analyser;
let dataArray;
let animationId;

function toggleVoice() {
    isVoiceActive = !isVoiceActive;
    const voiceButton = document.getElementById('voiceButton');
    const voiceVisualizer = document.getElementById('voiceVisualizer');

    if (isVoiceActive) {
        voiceButton.classList.add('active');
        voiceVisualizer.style.display = 'block';
        startVoiceVisualization();
    } else {
        voiceButton.classList.remove('active');
        voiceVisualizer.style.display = 'none';
        stopVoiceVisualization();
    }
}

function startVoiceVisualization() {
    const canvas = document.getElementById('visualizerCanvas');
    const canvasCtx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    // Create mock audio data for visualization
    const bufferLength = 64;
    dataArray = new Uint8Array(bufferLength);

    function draw() {
        animationId = requestAnimationFrame(draw);

        // Generate random data to simulate audio
        for (let i = 0; i < bufferLength; i++) {
            dataArray[i] = Math.random() * 255;
        }

        canvasCtx.fillStyle = 'rgba(99, 102, 241, 0.05)';
        canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

        const barWidth = (canvas.width / bufferLength) * 0.8;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            const barHeight = (dataArray[i] / 255) * canvas.height * 0.8;
            
            const gradient = canvasCtx.createLinearGradient(0, canvas.height - barHeight, 0, canvas.height);
            gradient.addColorStop(0, '#6366F1');
            gradient.addColorStop(0.5, '#8B5CF6');
            gradient.addColorStop(1, '#EC4899');
            
            canvasCtx.fillStyle = gradient;
            canvasCtx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);

            x += barWidth + 2;
        }
    }

    draw();
}

function stopVoiceVisualization() {
    if (animationId) {
        cancelAnimationFrame(animationId);
    }
}

// Settings panel
function toggleSettings() {
    const settingsPanel = document.getElementById('settingsPanel');
    settingsPanel.classList.toggle('open');
    
    // Save settings when closing
    if (!settingsPanel.classList.contains('open')) {
        saveSettings();
    }
}

function saveSettings() {
    const endpoint = document.getElementById('apiEndpoint').value;
    const apiKey = document.getElementById('apiKey').value;
    const ttsEngine = document.getElementById('ttsEngine').value;
    const voiceSpeed = document.getElementById('voiceSpeed').value;
    
    aiApi.setEndpoint(endpoint);
    aiApi.setApiKey(apiKey);
    ttsHandler.setEngine(ttsEngine);
    ttsHandler.setSpeed(parseFloat(voiceSpeed));
    
    showToast('Settings saved', 'success');
}

async function testConnection() {
    const result = await aiApi.testConnection();
    showToast(result.message, result.success ? 'success' : 'error');
}

function exportChat() {
    const data = {
        messages: messageHistory,
        exportDate: new Date().toISOString(),
        totalMessages: messageHistory.length
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `davoodai-chat-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    showToast('Chat exported successfully', 'success');
}

function clearAllData() {
    if (confirm('This will clear all chat history and settings. Are you sure?')) {
        localStorage.clear();
        messageHistory = [];
        chatMessages.innerHTML = '';
        aiApi.clearHistory();
        showToast('All data cleared', 'info');
        setTimeout(() => location.reload(), 1000);
    }
}

// Intersection Observer for feature cards
const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.classList.add('visible');
            }, index * 100);
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card').forEach(card => {
    observer.observe(card);
});

// Toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    const toastIcon = document.getElementById('toastIcon');
    
    toast.className = `toast ${type}`;
    toastMessage.textContent = message;
    
    // Set icon based on type
    if (type === 'success') {
        toastIcon.innerHTML = '✓';
    } else if (type === 'error') {
        toastIcon.innerHTML = '✕';
    } else {
        toastIcon.innerHTML = 'ℹ';
    }
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Settings toggles
document.getElementById('particlesToggle').addEventListener('change', (e) => {
    particleCanvas.style.display = e.target.checked ? 'block' : 'none';
});

document.getElementById('animationsToggle').addEventListener('change', (e) => {
    if (!e.target.checked) {
        document.body.style.setProperty('--animation-duration', '0s');
    } else {
        document.body.style.removeProperty('--animation-duration');
    }
});

document.getElementById('voiceToggle').addEventListener('change', (e) => {
    ttsHandler.setEnabled(e.target.checked);
});

document.getElementById('voiceSpeed').addEventListener('input', (e) => {
    const value = e.target.value;
    document.getElementById('voiceSpeedValue').textContent = value + 'x';
    ttsHandler.setSpeed(parseFloat(value));
});

// Close settings panel when clicking outside
document.addEventListener('click', (e) => {
    const settingsPanel = document.getElementById('settingsPanel');
    const settingsButton = document.querySelector('.chat-header .icon-button');
    
    if (settingsPanel.classList.contains('open') && 
        !settingsPanel.contains(e.target) && 
        !settingsButton.contains(e.target)) {
        settingsPanel.classList.remove('open');
    }
});

console.log('DavoodAI Frontend initialized successfully!');