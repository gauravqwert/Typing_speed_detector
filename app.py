import streamlit as st
import time
import random
import numpy as np
import pandas as pd
import joblib
from collections import defaultdict

# Custom CSS for styling
st.markdown("""
<style>
    :root {
        --primary: #4a6bff;
        --success: #28a745;
        --danger: #dc3545;
        --light: #f8f9fa;
        --dark: #343a40;
    }

    .test-container {
        background-color: var(--light);
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .sentence-display {
        font-family: 'Courier New', monospace;
        font-size: 1.3rem;
        line-height: 2rem;
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
        white-space: pre-wrap;
    }

    .timer-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1.5rem 0;
    }

    .timer {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary);
        padding: 0.5rem 1.5rem;
        background: white;
        border-radius: 50px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .timer.warning {
        color: #ffc107;
    }

    .timer.danger {
        color: var(--danger);
    }

    .result-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid var(--primary);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary);
        margin: 0.5rem 0;
    }

    .progress-container {
        height: 12px;
        background-color: #e9ecef;
        border-radius: 6px;
        margin: 1.5rem 0;
        overflow: hidden;
    }

    .progress-bar {
        height: 100%;
        border-radius: 6px;
        background-color: var(--success);
    }

    .correct {
        color: var(--success);
        font-weight: bold;
    }

    .incorrect {
        color: var(--danger);
        text-decoration: underline;
        font-weight: bold;
    }

    .current-word {
        background-color: rgba(74, 107, 255, 0.2);
        padding: 0 4px;
        border-radius: 4px;
    }

    .btn-primary {
        background-color: var(--primary) !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        font-size: 1.1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Sample paragraphs for typing test
paragraphs = [
    "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs.",
    "How vexingly quick daft zebras jump! Bright vixens jump; dozy fowl quack.",
    "Sphinx of black quartz, judge my vow. The five boxing wizards jump quickly.",
    "Programming is the process of creating instructions that tell a computer how to perform tasks.",
    "Typing quickly and accurately is an essential skill in today's digital world of computers."
]

# Initialize session state
if 'test' not in st.session_state:
    st.session_state.test = {
        'started': False,
        'completed': False,
        'paragraph': "",
        'start_time': None,
        'end_time': None,
        'typed_text': "",
        'timer': 60,
        'last_update': time.time()
    }


# Function to start new test
def start_test():
    st.session_state.test = {
        'started': True,
        'completed': False,
        'paragraph': random.choice(paragraphs),
        'start_time': time.time(),
        'end_time': None,
        'typed_text': "",
        'timer': 60,
        'last_update': time.time()
    }
    st.session_state.user_input = ""


# Function to handle typing and timer
def update_test():
    if not st.session_state.test['started'] or st.session_state.test['completed']:
        return

    # Update typed text
    st.session_state.test['typed_text'] = st.session_state.user_input

    # Update timer
    current_time = time.time()
    elapsed = current_time - st.session_state.test['start_time']
    remaining = max(0, 60 - elapsed)
    st.session_state.test['timer'] = remaining
    st.session_state.test['last_update'] = current_time

    # Check if time is up
    if remaining <= 0:
        st.session_state.test['completed'] = True
        st.session_state.test['end_time'] = current_time


# Function to calculate results
def calculate_results():
    test = st.session_state.test
    if not test['completed']:
        return None

    typed_text = test['typed_text']
    paragraph = test['paragraph']

    # Calculate correct characters and errors
    correct = 0
    errors = defaultdict(int)
    for i in range(min(len(typed_text), len(paragraph))):
        if typed_text[i] == paragraph[i]:
            correct += 1
        else:
            errors[paragraph[i]] += 1

    # Calculate WPM (5 characters = 1 word)
    wpm = (correct / 5) / (60 / 60)  # Words per minute

    # Calculate accuracy
    accuracy = (correct / len(typed_text)) * 100 if len(typed_text) > 0 else 0

    # Calculate words typed
    typed_words = len(typed_text.split())
    total_words = len(paragraph.split())

    return {
        'wpm': wpm,
        'accuracy': accuracy,
        'correct_chars': correct,
        'total_chars': len(typed_text),
        'errors': dict(errors),
        'typed_words': typed_words,
        'total_words': total_words,
        'paragraph': paragraph,
        'typed_text': typed_text
    }


# Main app layout
st.title("⌨️ Typing Speed Test (1 Minute)")
st.markdown("Test your typing speed and accuracy with this 1-minute timed test.")

# Test container
with st.container():
    st.markdown('<div class="test-container">', unsafe_allow_html=True)

    if not st.session_state.test['started']:
        st.button("Start 1-Minute Test", on_click=start_test, key="start_btn")
    else:
        # Update test state
        update_test()

        # Timer display
        timer_class = ""
        if st.session_state.test['timer'] < 15:
            timer_class = "warning"
        if st.session_state.test['timer'] < 5:
            timer_class = "danger"

        st.markdown(
            f'<div class="timer-container">'
            f'<div class="timer {timer_class}">{int(st.session_state.test["timer"])} seconds</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # Paragraph display with character highlighting
        if st.session_state.test['completed']:
            results = calculate_results()
            paragraph = results['paragraph']
            typed_text = results['typed_text']

            display_text = []
            for i, char in enumerate(paragraph):
                if i < len(typed_text):
                    if char == typed_text[i]:
                        display_text.append(f'<span class="correct">{char}</span>')
                    else:
                        display_text.append(f'<span class="incorrect">{char}</span>')
                else:
                    display_text.append(char)

            st.markdown(
                f'<div class="sentence-display">{"".join(display_text)}</div>',
                unsafe_allow_html=True
            )
        else:
            # Highlight current word during typing
            paragraph = st.session_state.test['paragraph']
            typed_words = st.session_state.test['typed_text'].split()
            current_word_index = len(typed_words)
            words = paragraph.split()

            display_text = []
            if current_word_index < len(words):
                current_word = words[current_word_index]
                word_start = paragraph.find(current_word)

                for i, char in enumerate(paragraph):
                    if word_start <= i < word_start + len(current_word):
                        display_text.append(f'<span class="current-word">{char}</span>')
                    else:
                        display_text.append(char)
            else:
                display_text = list(paragraph)

            st.markdown(
                f'<div class="sentence-display">{"".join(display_text)}</div>',
                unsafe_allow_html=True
            )

        # Typing input
        st.text_input(
            "Type the text above:",
            key="user_input",
            on_change=update_test,
            disabled=st.session_state.test['completed'],
            label_visibility="collapsed"
        )

        if st.session_state.test['completed']:
            st.button("Show Results", key="show_results_btn")

    st.markdown('</div>', unsafe_allow_html=True)

# Results display
if st.session_state.test['completed'] and st.session_state.get('show_results_btn', False):
    results = calculate_results()

    with st.container():
        st.markdown("## Your Results")

        # WPM and Accuracy cards
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                '<div class="result-card">'
                '<h3>Typing Speed</h3>'
                f'<div class="metric-value">{results["wpm"]:.1f}</div>'
                '<p>words per minute</p>'
                '</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                '<div class="result-card">'
                '<h3>Accuracy</h3>'
                f'<div class="metric-value">{results["accuracy"]:.1f}%</div>'
                '<p>character accuracy</p>'
                '</div>',
                unsafe_allow_html=True
            )

        # Progress bars
        st.markdown("### Progress")
        st.markdown(f"Words typed: {results['typed_words']}/{results['total_words']}")
        st.markdown(
            '<div class="progress-container">'
            f'<div class="progress-bar" style="width: {results["typed_words"] / results["total_words"] * 100}%"></div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"Correct characters: {results['correct_chars']}/{results['total_chars']}")
        st.markdown(
            '<div class="progress-container">'
            f'<div class="progress-bar" style="width: {results["correct_chars"] / results["total_chars"] * 100 if results["total_chars"] > 0 else 0}%"></div>'
            '</div>',
            unsafe_allow_html=True
        )

        # Error analysis
        if results['errors']:
            st.markdown("### Error Analysis")
            st.markdown("Most frequent mistakes:")
            for char, count in sorted(results['errors'].items(), key=lambda x: x[1], reverse=True)[:5]:
                st.markdown(f"- '{char}': {count} errors")

        st.button("Take Another Test", on_click=start_test, key="restart_btn")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #6c757d; font-size: 0.9rem;">'
    'Typing Speed Test • 1 Minute Challenge • Refresh to reset'
    '</div>',
    unsafe_allow_html=True
)