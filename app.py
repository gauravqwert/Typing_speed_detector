import streamlit as st
import time
import random

# CSS Styles with animations
st.markdown("""
<style>
    :root {
        --primary: #4a6bff;
        --success: #28a745;
        --danger: #dc3545;
        --light: #f8f9fa;
        --dark: #343a40;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 5px var(--primary); }
        50% { box-shadow: 0 0 20px var(--primary); }
        100% { box-shadow: 0 0 5px var(--primary); }
    }

    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        animation: fadeIn 0.5s ease-in-out;
        margin-bottom: 1rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .sentence-display {
        font-family: 'Courier New', monospace;
        font-size: 1.3rem;
        line-height: 2rem;
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        white-space: pre-wrap;
        box-shadow: inset 0 0 8px rgba(0,0,0,0.05);
        margin: 1rem 0;
        min-height: 120px;
    }

    .timer {
        font-size: 2.5rem;
        font-weight: bold;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        background: white;
        text-align: center;
        animation: pulse 1.5s infinite;
        margin: 1rem auto;
        width: fit-content;
    }
    .timer.warning { color: #ffc107; animation: pulse 0.8s infinite; }
    .timer.danger { color: var(--danger); animation: pulse 0.4s infinite; }
    .correct { color: var(--success); font-weight: bold; }
    .incorrect { color: var(--danger); text-decoration: underline; font-weight: bold; }
    .next-char { 
        background-color: rgba(74, 107, 255, 0.2); 
        border-radius: 4px; 
        padding: 0 2px;
        font-weight: bold;
    }
    .cursor { 
        border-left: 2px solid var(--primary);
        animation: blink 1s step-end infinite;
    }
    @keyframes blink {
        from, to { border-color: transparent }
        50% { border-color: var(--primary); }
    }
    .typing-input {
        font-size: 1.2rem;
        padding: 0.8rem;
    }
    .stats {
        display: flex;
        justify-content: space-between;
        margin: 1rem 0;
    }
    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        flex: 1;
        margin: 0 0.5rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Sample paragraphs
paragraphs = [
    "The quick brown fox jumps over the lazy dog.",
    "Programming is the process of creating instructions that tell a computer how to perform tasks.",
    "Typing quickly and accurately is an essential skill in today's digital world.",
    "To be or not to be, that is the question. Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune.",
    "The five boxing wizards jump quickly. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump!",
    "Artificial intelligence will transform every industry in ways we can't yet imagine. The future belongs to those who can adapt.",
    "Streamlit is an open-source app framework that turns data scripts into shareable web apps in minutes. It's pure Python magic!",
    "The journey of a thousand miles begins with a single step. Persistence and practice are the keys to mastering any skill."
]

# Initialize session state
if 'test' not in st.session_state:
    st.session_state.test = {
        'started': False,
        'completed': False,
        'paragraph': "",
        'start_time': None,
        'typed_text': "",
        'timer': 60,
        'last_update': time.time()
    }
    st.session_state.user_input = ""


def start_test():
    st.session_state.test.update({
        'started': True,
        'completed': False,
        'paragraph': random.choice(paragraphs),
        'start_time': time.time(),
        'typed_text': "",
        'timer': 60,
        'last_update': time.time()
    })
    st.session_state.user_input = ""
    # Force a rerun to start the test
    st.rerun()


def update_test():
    if not st.session_state.test['started'] or st.session_state.test['completed']:
        return

    # Update typed text with current input value
    st.session_state.test['typed_text'] = st.session_state.user_input
    st.session_state.test['last_update'] = time.time()

    # End test if full text is typed
    if len(st.session_state.user_input) >= len(st.session_state.test['paragraph']):
        st.session_state.test['completed'] = True
        st.rerun()


def calculate_results():
    typed = st.session_state.test['typed_text']
    para = st.session_state.test['paragraph']

    correct_chars = 0
    if typed:
        for i in range(min(len(typed), len(para))):
            if typed[i] == para[i]:
                correct_chars += 1

    elapsed = time.time() - st.session_state.test['start_time']
    minutes = max(elapsed / 60, 0.0166667)
    wpm = (correct_chars / 5) / minutes
    accuracy = (correct_chars / len(typed)) * 100 if typed else 0
    return {
        'wpm': wpm,
        'accuracy': accuracy,
        'correct': correct_chars,
        'total': len(typed),
        'time': elapsed
    }


# Main app
st.title("⌨️ Typing Speed Test")
st.caption("Test your typing speed and accuracy in a 1-minute challenge")

if not st.session_state.test['started']:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Instructions")
    st.write("1. Click Start Test to begin")
    st.write("2. Type the displayed text as quickly and accurately as possible")
    st.write("3. The test will automatically end after 1 minute or when you complete the text")
    st.write("4. Your results will be displayed with WPM and accuracy metrics")
    st.button("🚀 Start Test", on_click=start_test, type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Calculate remaining time
    elapsed = time.time() - st.session_state.test['start_time']
    remaining = max(0, 60 - elapsed)
    st.session_state.test['timer'] = remaining

    # End test if time is up
    if remaining <= 0:
        st.session_state.test['completed'] = True
        st.rerun()

    # Timer display
    tclass = "danger" if remaining < 5 else "warning" if remaining < 15 else ""
    st.markdown(f'<div class="timer {tclass}">{int(remaining)} seconds</div>', unsafe_allow_html=True)

    # Real-time stats
    if st.session_state.test['typed_text']:
        results = calculate_results()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="stat-box">📊 <strong>WPM</strong><br>{results["wpm"]:.1f}</div>',
                        unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-box">🎯 <strong>Accuracy</strong><br>{results["accuracy"]:.1f}%</div>',
                        unsafe_allow_html=True)
        with col3:
            st.markdown(
                f'<div class="stat-box">✅ <strong>Correct</strong><br>{results["correct"]}/{results["total"]}</div>',
                unsafe_allow_html=True)

    # Paragraph display with highlights
    typed_text = st.session_state.test['typed_text']
    para = st.session_state.test['paragraph']
    display_chars = []

    for i, ch in enumerate(para):
        if i < len(typed_text):
            display_chars.append(f'<span class="{"correct" if typed_text[i] == ch else "incorrect"}">{ch}</span>')
        elif i == len(typed_text):
            display_chars.append(f'<span class="next-char"><span class="cursor">{ch}</span></span>')
        else:
            display_chars.append(ch)

    st.markdown(f'<div class="sentence-display">{"".join(display_chars)}</div>', unsafe_allow_html=True)

    # Typing input - now only created once per render
    st.text_input("Type here (don't look at your keyboard!):",
                  key="user_input",
                  on_change=update_test,
                  disabled=st.session_state.test['completed'],
                  label_visibility="collapsed",
                  placeholder="Start typing here...")

    # Show results when completed
    if st.session_state.test['completed']:
        results = calculate_results()
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Final Results")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Words Per Minute", f"{results['wpm']:.1f}")
            st.metric("Time Taken", f"{results['time']:.1f} seconds")
        with col2:
            st.metric("Accuracy", f"{results['accuracy']:.1f}%")
            st.metric("Correct Characters", f"{results['correct']}/{results['total']}")

        st.progress(results['accuracy'] / 100, text="Accuracy Progress")
        st.markdown('</div>', unsafe_allow_html=True)

        st.button("🔄 Restart Test", on_click=start_test, type="primary", use_container_width=True)

    # Auto-rerun to update the display while test is running
    if not st.session_state.test['completed']:
        time.sleep(0.1)
        st.rerun()
