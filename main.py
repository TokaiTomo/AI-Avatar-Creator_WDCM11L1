import io
import streamlit as st
from huggingface_hub import InferenceClient
import config
st.set_page_config(page_title="Avatar Creator", page_icon="🛠️", layout="centered")
OPTIONS = {

"avatar type": ["boy hero", "girl hero", "wizard", "robot explorer", "space warrior", "animal adventurer","penguin"],

"hairstyle": ["short spiky hair", "curly hair", "long straight hair", "ponytail", "glowing hair", "helmet"],

"outfit": ["superhero suit", "magical robe", "space armor", "casual hoodie", "battle costume", "royal outfit"],

"expression": ["happy", "confident", "excited", "brave", "mysterious", "playful"],

"background": ["forest", "space station", "magic castle", "city skyline", "rainbow world", "cloud kingdom"],

"art style": ["cartoon style", "anime style", "3D game style", "fantasy illustration", "comic style"],

}

client=InferenceClient(api_key=config.HF_API_KEY)
st.session_state.setdefault("generated_image", None)
st.title("Avatar Creator")
st.write("Create your own personal avatar with the help of AI")
st.markdown("Choose your own avatar options or write your own prompt")
st.subheader("Workshop: ")
mode=st.selectbox("Choose prompt mode",["Use set options","Write custom prompt"])
if mode=="Use set options":
    values={k: st.selectbox(f"Choose {k}",v)for k,v in OPTIONS.items()}
    extra=st.text_input("Extra Information (optional)",placeholder="Example: Give it a wand or something I don't care").strip()
    prompt=(f"A kid friendly{values['avatar type']}, "
            f"with {values['hairstyle']}, "
            f"wearing {values['outfit']}, "
            f"with a {values['expression']} expression, "
            f"{values['art style']}, colorful, and super detailed, image")
    final_prompt=f"{prompt},{extra}"if extra else prompt
else:
    final_prompt=st.text_area(
        "Write your own prompt",
        placeholder="A Potato with a hat...",
        height=150,
    ).strip()
with st.expander("See your prompt here"):
    st.write(final_prompt or "Your prompt will appear here")
if st.button("Create avatar"):
    if not config.HF_API_KEY:
        st.error("API key is missing put in .env")
    elif not final_prompt:
        st.warning("Make a prompt first")
    else:
        with st.spinner("Creating Avatar..."):
            try:
                st.session_state.generated_image=client.text_to_image(
                    prompt=final_prompt,
                    model=config.HF_IMAGE_MODEL,
                )
                st.success("Avatar Created")

            except Exception as e:
                st.error("The computer went kaboom kaboom kaboom, something went wrong: {e}")
if st.session_state.generated_image:
    st.image(st.session_state.generated_image, caption="Your AI avatar", use_container_width=True)
    buffer=io.BytesIO()
    st.session_state.generated_image.save(buffer,format="PNG")
    st.download_button(
        "Download",
        data=buffer.getvalue(),
        file_name="avatar.png",
        mine="image/png",
    )