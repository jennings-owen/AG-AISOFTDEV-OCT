import streamlit as st
import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8001"
CHAT_ENDPOINT = f"{API_BASE_URL}/chat"
STATEFUL_CHAT_ENDPOINT = f"{API_BASE_URL}/stateful_chat"

def main():
    """Main Streamlit application function."""
    
    # Page configuration
    st.set_page_config(
        page_title="Chat with AI Agent",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize session state for conversation memory
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "use_stateful" not in st.session_state:
        st.session_state.use_stateful = True
    
    # Title and description
    st.title("🤖 Chat with AI Agent")
    st.markdown("Ask any question and get a response from the AI agent!")
    
    # Sidebar for settings and conversation management
    with st.sidebar:
        st.header("💬 Conversation Settings")
        
        # Toggle between stateful and stateless chat
        use_stateful = st.checkbox(
            "Enable Conversation Memory", 
            value=st.session_state.use_stateful,
            help="When enabled, the agent will remember previous messages in the conversation."
        )
        st.session_state.use_stateful = use_stateful
        
        if use_stateful:
            # Show session info
            if st.session_state.session_id:
                st.success(f"🔗 Session: {st.session_state.session_id[:8]}...")
            else:
                st.info("🆕 New session will be created")
            
            # Clear conversation button
            if st.button("🗑️ Clear Conversation", type="secondary"):
                st.session_state.session_id = None
                st.session_state.conversation_history = []
                st.rerun()
        else:
            st.info("💭 Stateless mode - no memory between messages")
        
        # Show conversation history count
        if st.session_state.conversation_history:
            st.metric(
                "Messages in Conversation", 
                len(st.session_state.conversation_history)
            )
    
    # Display conversation history
    if st.session_state.conversation_history and st.session_state.use_stateful:
        st.subheader("📝 Conversation History")
        
        # Create a container for chat history with scrollable area
        chat_container = st.container()
        with chat_container:
            for i, exchange in enumerate(st.session_state.conversation_history, 1):
                # Use expander for each exchange to make it more organized
                with st.expander(f"💬 Exchange {i}", expanded=(i == len(st.session_state.conversation_history))):
                    st.markdown(f"**👤 You:** {exchange['question']}")
                    st.markdown(f"**🤖 AI:** {exchange['answer']}")
        
        # Add some spacing before the input form
        st.markdown("---")
        st.subheader("💬 Continue the Conversation")
    elif st.session_state.use_stateful:
        st.info("🚀 Start your first message to begin a conversation with memory!")
    
    # Create a form for user input
    with st.form(key="chat_form", clear_on_submit=True):
        # Text input for user's question
        user_question = st.text_area(
            "Your Question:",
            placeholder="Type your question here...",
            height=100,
            help="Enter your question and click 'Send' to get a response from the AI agent."
        )
        
        # Submit button
        submit_button = st.form_submit_button(
            label="Send",
            type="primary",
            use_container_width=True
        )
    
    # Handle form submission
    if submit_button and user_question.strip():
        # Show spinner while processing
        with st.spinner("Getting response from AI agent..."):
            try:
                if st.session_state.use_stateful:
                    # Use stateful chat endpoint
                    payload = {
                        "question": user_question.strip(),
                        "session_id": st.session_state.session_id
                    }
                    endpoint = STATEFUL_CHAT_ENDPOINT
                else:
                    # Use stateless chat endpoint
                    payload = {"question": user_question.strip()}
                    endpoint = CHAT_ENDPOINT
                
                # Make POST request to appropriate endpoint
                response = requests.post(
                    endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30  # 30 second timeout
                )
                
                # Check if request was successful
                response.raise_for_status()
                
                # Parse the JSON response
                response_data = response.json()
                answer = response_data.get("answer", "No answer received")
                
                # Handle session_id for stateful conversations
                if st.session_state.use_stateful:
                    returned_session_id = response_data.get("session_id")
                    if returned_session_id:
                        st.session_state.session_id = returned_session_id
                    
                    # Add to conversation history
                    st.session_state.conversation_history.append({
                        "question": user_question.strip(),
                        "answer": answer
                    })
                    
                    # Show success message and rerun to display updated history
                    st.success("✅ Response received and added to conversation!")
                    st.rerun()
                else:
                    # For stateless mode, show the response directly
                    st.success("Response received!")
                    
                    # Create two columns for better layout
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.subheader("Your Question:")
                        st.info(user_question)
                    
                    with col2:
                        st.subheader("AI Agent Response:")
                        st.success(answer)
                
                # Show session info for stateful mode
                if st.session_state.use_stateful and st.session_state.session_id:
                    st.caption(f"🔗 Session ID: {st.session_state.session_id}")
                
            except requests.exceptions.ConnectionError:
                st.error("❌ **Connection Error**: Could not connect to the AI agent server. Please make sure the FastAPI server is running on http://localhost:8001")
                st.info("💡 **Tip**: Start the server by running `uvicorn main:app --reload --port 8001` in the terminal")
                
            except requests.exceptions.Timeout:
                st.error("❌ **Timeout Error**: The request took too long. Please try again.")
                
            except requests.exceptions.HTTPError as e:
                st.error(f"❌ **HTTP Error**: {e}")
                if hasattr(e.response, 'text'):
                    st.code(e.response.text)
                    
            except requests.exceptions.RequestException as e:
                st.error(f"❌ **Request Error**: {e}")
                
            except json.JSONDecodeError:
                st.error("❌ **JSON Error**: Invalid response format from server")
                
            except Exception as e:
                st.error(f"❌ **Unexpected Error**: {str(e)}")
    
    elif submit_button:
        st.warning("⚠️ Please enter a question before submitting.")
    
    # Add some information in the sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This is a chat interface that connects to a FastAPI backend with an AI agent.
        
        **Features:**
        - **Stateless Mode**: Each message is independent
        - **Stateful Mode**: Agent remembers conversation context
        
        **How to use:**
        1. Choose your conversation mode (stateful recommended)
        2. Type your question in the text area
        3. Click 'Send' to get a response
        4. For follow-ups, try "Can you tell me more about that?"
        
        **Requirements:**
        - FastAPI server running on localhost:8001
        - Server should have `/chat` and `/stateful_chat` endpoints
        """)
        
        st.header("🔧 Server Status")
        if st.button("Check Server Health"):
            try:
                health_response = requests.get(f"{API_BASE_URL}/", timeout=5)
                if health_response.status_code == 200:
                    st.success("✅ Server is running!")
                    
                    # Check if stateful endpoint is available
                    try:
                        test_payload = {"question": "test", "session_id": "health-check"}
                        test_response = requests.post(STATEFUL_CHAT_ENDPOINT, json=test_payload, timeout=5)
                        if test_response.status_code == 200:
                            st.success("✅ Stateful chat endpoint is available!")
                        else:
                            st.warning("⚠️ Stateful chat endpoint may not be available")
                    except:
                        st.warning("⚠️ Could not verify stateful chat endpoint")
                else:
                    st.error(f"❌ Server returned status: {health_response.status_code}")
            except Exception:
                st.error("❌ Server is not reachable")

if __name__ == "__main__":
    main()