import streamlit as st
import json
from datetime import datetime
import os

# Page config
st.set_page_config(page_title="Make a Decision", page_icon="🎯", layout="wide")

# Initialize session state
if 'decisions' not in st.session_state:
    st.session_state.decisions = []

if 'current_view' not in st.session_state:
    st.session_state.current_view = 'form'

# Theme colors
themes = {
    'Coral': {'primary': '#f87171', 'secondary': '#fee2e2'},
    'Ocean': {'primary': '#60a5fa', 'secondary': '#dbeafe'},
    'Forest': {'primary': '#4ade80', 'secondary': '#dcfce7'},
    'Sunset': {'primary': '#fb923c', 'secondary': '#fed7aa'},
    'Purple': {'primary': '#c084fc', 'secondary': '#f3e8ff'}
}

# Sidebar for theme and navigation
with st.sidebar:
    st.title("🎨 Settings")
    theme = st.selectbox("Choose Theme", list(themes.keys()))
    
    st.markdown("---")
    st.title("📋 Navigation")
    if st.button("➕ New Decision", use_container_width=True):
        st.session_state.current_view = 'form'
    if st.button(f"📚 History ({len(st.session_state.decisions)})", use_container_width=True):
        st.session_state.current_view = 'history'

# Apply custom CSS
st.markdown(f"""
    <style>
    .main {{
        background-color: {themes[theme]['secondary']};
    }}
    .stButton>button {{
        border-radius: 20px;
        font-weight: bold;
    }}
    h1 {{
        color: {themes[theme]['primary']};
        text-align: center;
        padding: 20px;
        border-radius: 20px;
        background-color: {themes[theme]['primary']};
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("# MAKE A DECISION")

# Form View
if st.session_state.current_view == 'form':
    st.markdown("### 📝 New Decision")
    
    with st.form("decision_form"):
        # Dilemma
        dilemma = st.text_input("**DILEMMA:** What decision do you need to make?")
        
        # Date fields
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("**DATE:**")
        with col2:
            needed_by = st.date_input("**DECISION NEEDED BY:**")
        
        # Importance level
        st.markdown("**DECISION IMPORTANCE:**")
        importance = st.radio(
            "importance",
            ["TRIVIAL", "NON-LETHAL", "WORTHWHILE", "WEIGHTY", "LIFE-CHANGING"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Indecisiveness level
        st.markdown("**INDECISIVENESS LEVEL:**")
        indecisiveness = st.radio(
            "indecisiveness",
            ["WISHY", "WASHY", "NEUTRAL", "FASTISH", "MIND MADE UP"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Best/Worst case
        col1, col2 = st.columns(2)
        with col1:
            best_case = st.text_area("**BEST-CASE SCENARIO:**", height=100)
        with col2:
            worst_case = st.text_area("**WORST-CASE SCENARIO:**", height=100)
        
        # Gut feelings and Plus/Minus
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**GUT FEELINGS:**")
            gut_feelings = []
            for i in range(4):
                feeling = st.text_input(f"Feeling {i+1}", key=f"gut_{i}", label_visibility="collapsed")
                gut_feelings.append(feeling)
        
        with col2:
            st.markdown("**PLUSES (+) AND MINUSES (-):**")
            pluses_minuses = []
            for i in range(4):
                symbol = "➕" if i % 2 == 0 else "➖"
                item = st.text_input(f"{symbol}", key=f"pm_{i}", label_visibility="collapsed")
                pluses_minuses.append({"type": "plus" if i % 2 == 0 else "minus", "text": item})
        
        # Conclusions
        col1, col2 = st.columns(2)
        with col1:
            intuitive = st.text_area("**INTUITIVE CONCLUSION:**", height=100)
        with col2:
            rational = st.text_area("**RATIONAL CONCLUSION:**", height=100)
        
        # Final decision
        decision = st.text_area("**DECISION:** What's your final decision?", height=100)
        
        # Next steps
        next_steps = st.text_area("**NEXT STEPS:** What actions will you take?", height=100)
        
        # Submit button
        submitted = st.form_submit_button("💾 Save Decision", use_container_width=True)
        
        if submitted:
            if not dilemma:
                st.error("Please enter a dilemma!")
            else:
                new_decision = {
                    'id': datetime.now().timestamp(),
                    'dilemma': dilemma,
                    'date': str(date),
                    'needed_by': str(needed_by),
                    'importance': importance,
                    'indecisiveness': indecisiveness,
                    'best_case': best_case,
                    'worst_case': worst_case,
                    'gut_feelings': gut_feelings,
                    'pluses_minuses': pluses_minuses,
                    'intuitive': intuitive,
                    'rational': rational,
                    'decision': decision,
                    'next_steps': next_steps,
                    'created_at': datetime.now().isoformat(),
                    'rating': None
                }
                st.session_state.decisions.insert(0, new_decision)
                st.success("✅ Decision saved!")
                st.session_state.current_view = 'history'
                st.rerun()

# History View
elif st.session_state.current_view == 'history':
    st.markdown("### 📚 Decision History")
    
    if len(st.session_state.decisions) == 0:
        st.info("No decisions yet. Start by making your first decision!")
    else:
        # Print button
        if st.button("🖨️ Print History"):
            st.markdown("Use your browser's print function (Ctrl+P or Cmd+P) to print this page")
        
        for idx, dec in enumerate(st.session_state.decisions):
            with st.container():
                st.markdown(f"---")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {dec['dilemma']}")
                    st.caption(f"Made on: {datetime.fromisoformat(dec['created_at']).strftime('%B %d, %Y')}")
                
                with col2:
                    rate_col1, rate_col2, rate_col3 = st.columns(3)
                    with rate_col1:
                        if st.button("👍", key=f"good_{idx}"):
                            st.session_state.decisions[idx]['rating'] = 'good'
                            st.rerun()
                    with rate_col2:
                        if st.button("👎", key=f"bad_{idx}"):
                            st.session_state.decisions[idx]['rating'] = 'bad'
                            st.rerun()
                    with rate_col3:
                        if st.button("🗑️", key=f"delete_{idx}"):
                            st.session_state.decisions.pop(idx)
                            st.rerun()
                
                # Details
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    if dec.get('importance'):
                        st.markdown(f"**Importance:** {dec['importance']}")
                with info_col2:
                    if dec.get('indecisiveness'):
                        st.markdown(f"**Level:** {dec['indecisiveness']}")
                
                if dec.get('decision'):
                    st.markdown(f"**Decision:** {dec['decision']}")
                
                if dec.get('next_steps'):
                    st.markdown(f"**Next Steps:** {dec['next_steps']}")
                
                # Rating display
                if dec.get('rating'):
                    if dec['rating'] == 'good':
                        st.success("✅ Rated as: Good Decision")
                    else:
                        st.error("❌ Rated as: Bad Decision")
