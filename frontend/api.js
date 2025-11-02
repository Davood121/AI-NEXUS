// API Configuration and Communication
class AIApi {
    constructor() {
        this.endpoint = localStorage.getItem('apiEndpoint') || 'http://localhost:5000/api/chat';
        this.apiKey = localStorage.getItem('apiKey') || '';
        this.conversationHistory = [];
        this.maxHistoryLength = 10;
    }

    setEndpoint(endpoint) {
        this.endpoint = endpoint;
        localStorage.setItem('apiEndpoint', endpoint);
    }

    setApiKey(key) {
        this.apiKey = key;
        localStorage.setItem('apiKey', key);
    }

    async sendMessage(message, useContext = true) {
        try {
            const headers = {
                'Content-Type': 'application/json',
            };

            if (this.apiKey) {
                headers['Authorization'] = `Bearer ${this.apiKey}`;
            }

            const payload = {
                message: message,
                timestamp: new Date().toISOString(),
            };

            if (useContext && this.conversationHistory.length > 0) {
                payload.context = this.conversationHistory.slice(-this.maxHistoryLength);
            }

            const response = await fetch(this.endpoint, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Update conversation history
            this.conversationHistory.push({
                role: 'user',
                content: message,
                timestamp: new Date().toISOString()
            });
            
            this.conversationHistory.push({
                role: 'assistant',
                content: data.response || data.message,
                timestamp: new Date().toISOString()
            });

            return {
                success: true,
                response: data.response || data.message,
                data: data
            };
        } catch (error) {
            console.error('API Error:', error);
            return {
                success: false,
                error: error.message,
                response: this.getFallbackResponse(message)
            };
        }
    }

    async testConnection() {
        try {
            const response = await fetch(this.endpoint, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            return {
                success: response.ok,
                status: response.status,
                message: response.ok ? 'Connection successful!' : 'Connection failed!'
            };
        } catch (error) {
            return {
                success: false,
                message: `Connection failed: ${error.message}`
            };
        }
    }

    getFallbackResponse(message) {
        const responses = [
            "I'm currently running in offline mode. Your message has been received: " + message,
            "API connection unavailable. Here's a simulated response to: " + message,
            "I understand you said: " + message + ". However, I'm not connected to the backend right now.",
            "Your message '" + message + "' has been noted. Please check the API connection in settings.",
        ];
        return responses[Math.floor(Math.random() * responses.length)];
    }

    clearHistory() {
        this.conversationHistory = [];
    }

    getHistory() {
        return this.conversationHistory;
    }
}

// Text-to-Speech Handler
class TTSHandler {
    constructor() {
        this.enabled = true;
        this.engine = 'edge';
        this.speed = 1.0;
        this.synth = window.speechSynthesis;
    }

    setEngine(engine) {
        this.engine = engine;
    }

    setSpeed(speed) {
        this.speed = speed;
    }

    setEnabled(enabled) {
        this.enabled = enabled;
    }

    async speak(text) {
        if (!this.enabled) return;

        // Use Web Speech API as fallback
        if (this.synth) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = this.speed;
            utterance.pitch = 1;
            utterance.volume = 1;
            
            this.synth.cancel(); // Cancel any ongoing speech
            this.synth.speak(utterance);
        }

        // In production, this would call your Python TTS backend
        // Example: await fetch('/api/tts', { method: 'POST', body: JSON.stringify({ text, engine: this.engine }) });
    }

    stop() {
        if (this.synth) {
            this.synth.cancel();
        }
    }
}

// Initialize global instances
const aiApi = new AIApi();
const ttsHandler = new TTSHandler();