import streamlit as st
from app.helper import get_or_create_user_id
from app.db import get_chat_history

def sidebar_controls():
    """Creates sidebar controls for chat settings"""
    with st.sidebar:
        st.header("Settings")
        temperature = st.slider("Response Creativity", 0.0, 1.0, 0.3, key="temp_slider")
        num_results = st.slider("Retrieved Chunks", 1, 5, 2, key="num_results_slider")
        search_type = st.selectbox(
            "Search Strategy", 
            ["similarity", "mmr", "similarity_score_threshold"],
            key="search_type_select"
        )
        
        # Debug controls
        if st.session_state.get("debug_mode", False):
            st.divider()
            st.header("Debug")
            if st.button("Force Reload History"):
                if "history" in st.session_state:
                    del st.session_state["history"]
                st.rerun()
        
        return temperature, num_results, search_type

def show_chat_history():
    """Displays complete chat history with guaranteed loading"""
    try:
        # Initialize user session
        if "user_id" not in st.session_state:
            user_id = get_or_create_user_id()
            st.session_state["user_id"] = user_id
        
        # Debug output
        if st.session_state.get("debug_mode"):
            st.write(f"Debug: Loading history for user {st.session_state['user_id']}")
        
        # Load fresh history from DB
        try:
            history = get_chat_history(st.session_state["user_id"])
            if st.session_state.get("debug_mode"):
                st.write(f"Debug: Retrieved {len(history)} records")
            
            if history:
                st.subheader("🗂️ Chat History")
                for chat in reversed(history):  # Newest first
                    with st.container():
                        st.markdown(f"**Q:** {chat['question']}")
                        st.markdown(f"**A:** {chat['answer']}")
                        if st.session_state.get("debug_mode") and chat.get('context'):
                            with st.expander("View Context"):
                                st.text(chat['context'][:500] + ("..." if len(chat['context']) > 500 else ""))
                        st.caption(f"🕒 {chat['timestamp']} | Source: {chat['source_file']}")
                        st.divider()
            else:
                st.info("No previous conversations found")
                
        except Exception as e:
            st.error(f"History load error: {str(e)}")
            if st.session_state.get("debug_mode"):
                st.exception(e)
            
    except Exception as e:
        st.error("History display error")
        if st.session_state.get("debug_mode"):
            st.exception(e)