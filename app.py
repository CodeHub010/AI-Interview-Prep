import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import io
import re

from interview import load_questions, evaluate_answer, get_feedback


# =========================================================
# VOICE FUNCTIONS
# =========================================================

def text_to_speech(text):
    """Convert text into speech audio."""
    tts = gTTS(text=str(text), lang="en")

    audio = io.BytesIO()
    tts.write_to_fp(audio)
    audio.seek(0)

    return audio


def speech_to_text(audio_file):
    """Convert recorded audio into text."""

    recognizer = sr.Recognizer()

    try:
        audio_file.seek(0)

        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:
        return None

    except sr.RequestError:
        return None

    except Exception as e:
        st.error(f"Speech recognition error: {e}")
        return None


# =========================================================
# SCORE FUNCTION
# =========================================================

def convert_score_to_number(score):
    """
    Convert different score formats into a number.

    Examples:
    85       -> 85
    "85"     -> 85
    "85/100" -> 85
    "Score: 85" -> 85
    """

    if isinstance(score, (int, float)):
        return float(score)

    if isinstance(score, str):

        match = re.search(r"\d+(\.\d+)?", score)

        if match:
            return float(match.group())

    return 0


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="🎙️",
    layout="centered"
)


# =========================================================
# TITLE
# =========================================================

st.title("🎙️ AI Interview Preparation Assistant")

st.write(
    "Practice interview questions using your voice "
    "and receive instant feedback."
)


# =========================================================
# LOAD QUESTIONS
# =========================================================

questions = load_questions()


# =========================================================
# CATEGORY
# =========================================================

category = st.selectbox(
    "Choose an interview category",
    list(questions.keys())
)


# =========================================================
# QUESTION
# =========================================================

question_list = questions[category]

question_number = st.selectbox(
    "Choose a question",
    range(len(question_list)),
    format_func=lambda x: f"Question {x + 1}"
)


# Your questions are dictionaries, so we take ["question"]
question = question_list[question_number]["question"]


# =========================================================
# DISPLAY QUESTION
# =========================================================

st.subheader("🎤 Interview Question")

st.info(question)


# =========================================================
# HEAR QUESTION
# =========================================================

if st.button("🔊 Hear Question"):

    question_audio = text_to_speech(question)

    st.audio(
        question_audio,
        format="audio/mp3"
    )


# =========================================================
# VOICE ANSWER
# =========================================================

st.subheader("🎙️ Your Answer")

st.write("Click the microphone button and speak your answer.")

audio_answer = st.audio_input(
    "Click here and speak your answer"
)


# =========================================================
# AFTER RECORDING
# =========================================================

if audio_answer:

    st.success("✅ Your voice has been recorded.")

    st.audio(
        audio_answer,
        format="audio/wav"
    )


    # =====================================================
    # ANALYZE ANSWER
    # =====================================================

    if st.button("🧠 Analyze My Answer"):

        # -----------------------------------------------
        # Speech to Text
        # -----------------------------------------------

        answer = speech_to_text(audio_answer)


        # -----------------------------------------------
        # Check Speech Recognition
        # -----------------------------------------------

        if answer is None:

            st.error(
                "❌ Sorry, I could not understand your voice."
            )

            st.info(
                "Please record your answer again and speak clearly."
            )

        else:

            # -------------------------------------------
            # Display Converted Text
            # -------------------------------------------

            st.subheader("📝 Your Answer")

            st.write(answer)


            # -------------------------------------------
            # Evaluate Answer
            # -------------------------------------------

            try:

                score = evaluate_answer(
                    question,
                    answer
                )

            except Exception as e:

                st.error(
                    f"Error while evaluating the answer: {e}"
                )

                score = 0


            # -------------------------------------------
            # Convert Score to Number
            # -------------------------------------------

            numeric_score = convert_score_to_number(score)


            # -------------------------------------------
            # Get Feedback
            # -------------------------------------------

            try:

                feedback = get_feedback(
                    numeric_score
                )

            except Exception as e:

                st.error(
                    f"Error while generating feedback: {e}"
                )

                feedback = (
                    "There was a problem generating feedback."
                )


            # -------------------------------------------
            # Display Score
            # -------------------------------------------

            st.subheader("📊 Score")

            st.metric(
                "Your Score",
                f"{numeric_score:.0f}"
            )


            # -------------------------------------------
            # Display Feedback
            # -------------------------------------------

            st.subheader("💡 Feedback")

            st.write(feedback)


            # -------------------------------------------
            # Voice Feedback
            # -------------------------------------------

            st.subheader("🔊 Voice Feedback")

            try:

                feedback_audio = text_to_speech(
                    feedback
                )

                st.audio(
                    feedback_audio,
                    format="audio/mp3"
                )

            except Exception as e:

                st.error(
                    f"Could not create voice feedback: {e}"
                )