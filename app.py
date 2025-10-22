import streamlit as st
from gen import generate_reply
import pyperclip

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Review Reply Generator", page_icon="💬", layout="centered")

# ---------- HEADER ----------
st.markdown("""
    <style>
        .main {padding-top: 1rem;}
        .stTextArea textarea {font-size: 15px;}
        .block-container {padding-top: 2rem;}
        button[kind="secondary"] {margin-right: 0.5rem;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>AI Review Reply Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:grey;'>Write natural, human replies to Google reviews instantly.</p>", unsafe_allow_html=True)
st.divider()

# ---------- BUSINESS INFO INPUT ----------
st.markdown("### Business Details")

col1, col2, col3 = st.columns(3)
with col1:
    business_name = st.text_input("Business Name", placeholder="Pump Gym")
with col2:
    industry = st.text_input("Industry", value="Fitness")
with col3:
    location = st.text_input("Location", value="Cambridge")

# You can then pass these to your generate_reply() function if needed:
# e.g. response = generate_reply(review, business_name, industry, location)
# ---------- INPUTS ----------
st.subheader("📝 Review")
review = st.text_area(
    "Paste a Google review",
    height=130,
    placeholder="E.g. Amazing ... Great parking. Everything you need in a ... Plus it has a ...."
)
rating = st.slider("⭐ Star rating", 1, 5, 4, help="Select the star rating from the review.")
st.caption("This demo uses manual input. The full version will pull reviews and ratings directly from Google")
st.divider()
st.subheader("🎙️ Choose Tone")

# ---------- STATE INIT ----------
if "reply" not in st.session_state:
    st.session_state["reply"] = ""
if "edited_reply" not in st.session_state:
    st.session_state["edited_reply"] = ""
if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False
if "tone_choice" not in st.session_state:
    st.session_state["tone_choice"] = None

# ---------- GENERATE BUTTONS ----------
col1, col2 = st.columns(2)

with col1:
    if st.button("🧾 Generate Corporate Reply", use_container_width=True):
        if not review.strip():
            st.warning("Please paste a review first.")
        else:
            with st.spinner("Generating corporate reply..."):
                reply = generate_reply(review, rating, tone_choice="Corporate")
            st.session_state["reply"] = reply
            st.session_state["edited_reply"] = reply  # keep synced
            st.session_state["tone_choice"] = "Corporate"
            st.session_state["edit_mode"] = False

with col2:
    if st.button("💬 Generate Conversational Reply", use_container_width=True):
        if not review.strip():
            st.warning("Please paste a review first.")
        else:
            with st.spinner("Generating conversational reply..."):
                reply = generate_reply(review, rating, tone_choice="Conversational")
            st.session_state["reply"] = reply
            st.session_state["edited_reply"] = reply  # keep synced
            st.session_state["tone_choice"] = "Conversational"
            st.session_state["edit_mode"] = False

# ---------- OUTPUT ----------
if st.session_state["reply"]:
    st.divider()
    st.subheader("💬 Generated Reply")

    if st.session_state["edit_mode"]:
        st.session_state["edited_reply"] = st.text_area(
            "Edit Reply", 
            st.session_state["edited_reply"], 
            height=220
        )
    else:
        st.text_area("Output", st.session_state["reply"], height=220, disabled=True)

    colA, colB, colC = st.columns([1, 1, 1])

    # ✅ Approve (copy)
    with colA:
        if st.button("✅ Approve"):
            text_to_copy = (
                st.session_state["edited_reply"]
                if st.session_state["edit_mode"]
                else st.session_state["reply"]
            )
            try:
                pyperclip.copy(text_to_copy)
                st.success("Approved and copied to clipboard!")
            except Exception:
                st.warning("Copy unavailable in this demo. In the full version, replies will post directly to Google.")
            st.session_state["edit_mode"] = False

    # ✏️ Edit
    with colB:
        if st.button("✏️ Edit"):
            st.session_state["edit_mode"] = not st.session_state["edit_mode"]
            st.rerun()

    # 🔁 Regenerate
    with colC:
        if st.button("🔁 Regenerate"):
            tone = st.session_state.get("tone_choice")
            if not st.session_state.get("reply"):
                st.warning("Please generate a reply first.")
            elif not tone:
                st.warning("Please generate a reply first to set the tone.")
            else:
                with st.spinner("Regenerating reply..."):
                    new_reply = generate_reply(
                        review, 
                        rating, 
                        tone_choice=tone
                    )
                    st.session_state["reply"] = new_reply
                    st.session_state["edited_reply"] = new_reply
                    st.session_state["edit_mode"] = False
                st.success("✅ Reply regenerated successfully.")
                st.rerun()