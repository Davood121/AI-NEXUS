import streamlit as st
import requests
from ai_system import FreeAISystem
import threading
import time

# Initialize AI system
@st.cache_resource
def get_ai_system():
    return FreeAISystem()

def main():
    st.title("🤖 Free AI Assistant")
    st.sidebar.title("Features")
    
    # Initialize AI
    ai = get_ai_system()
    
    # Feature selection
    feature = st.sidebar.selectbox(
        "Choose Feature:",
        ["💬 Chat", "🔍 Web Search", "🌐 Translate", "💻 Code Assistant", "📷 Vision"]
    )
    
    if feature == "💬 Chat":
        st.header("Chat with AI")
        
        # Chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your message..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = ai.generate_response(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
    
    elif feature == "🔍 Web Search":
        st.header("Web Search + AI Analysis")
        
        query = st.text_input("Enter search query:")
        if st.button("Search & Analyze"):
            if query:
                with st.spinner("Searching..."):
                    results = ai.web_search(query)
                    response = ai.generate_response(f"Analyze these search results about: {query}", results)
                    
                    st.subheader("AI Analysis:")
                    st.write(response)
                    
                    st.subheader("Search Results:")
                    for result in results:
                        st.write(f"**{result['title']}**")
                        st.write(result['body'])
                        st.write(f"[Link]({result['url']})")
                        st.divider()
    
    elif feature == "🌐 Translate":
        st.header("AI Translator")
        
        text_to_translate = st.text_area("Enter text to translate:")
        target_language = st.selectbox("Target Language:", 
                                     ["Spanish", "French", "German", "Italian", "Portuguese", "Chinese", "Japanese"])
        
        if st.button("Translate"):
            if text_to_translate:
                with st.spinner("Translating..."):
                    translation = ai.translate_text(text_to_translate, target_language)
                    st.subheader(f"Translation to {target_language}:")
                    st.write(translation)
    
    elif feature == "💻 Code Assistant":
        st.header("AI Code Assistant")
        
        coding_request = st.text_area("Describe what you want to code:")
        
        if st.button("Generate Code"):
            if coding_request:
                with st.spinner("Generating code..."):
                    code_response = ai.code_assistant(coding_request)
                    st.subheader("Generated Code:")
                    st.code(code_response)
    
    elif feature == "📷 Vision":
        st.header("AI Vision")
        
        uploaded_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image")
            
            if st.button("Analyze Image"):
                with st.spinner("Analyzing image..."):
                    # For now, just describe that an image was uploaded
                    analysis = ai.analyze_image("User uploaded an image for analysis")
                    st.subheader("Image Analysis:")
                    st.write(analysis)
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🆓 Completely Free Features:")
    st.sidebar.markdown("- 🧠 Llama 3.1 AI Brain")
    st.sidebar.markdown("- 🔍 Web Search")
    st.sidebar.markdown("- 🗣️ Text-to-Speech")
    st.sidebar.markdown("- 🎤 Voice Recognition")
    st.sidebar.markdown("- 🌐 Translation")
    st.sidebar.markdown("- 💻 Code Generation")
    st.sidebar.markdown("- 📷 Image Analysis")
    st.sidebar.markdown("- 💾 Conversation Memory")

if __name__ == "__main__":
    main()