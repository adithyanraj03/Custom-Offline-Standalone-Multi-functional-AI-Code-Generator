import streamlit as st
from llama_cpp import Llama
import cv2
import numpy as np
from cryptography.fernet import Fernet
import time
import streamlit.web.cli as stcli
import sys

# Load the model
model_path = r"B:\Research\Standalone-Offline-LLM\models\Custom-Model-version-12.gguf"
llm = Llama(model_path=model_path, n_ctx=2048, n_threads=4)


def generate_code(prompt):
    full_prompt = f"Write Java code for the following task: {prompt}\n\nCode:"
    output = llm(full_prompt, max_tokens=500)

    # Debugging: Print the raw output from the model
    print("Model Output:", output)

    # Check if 'choices' exists and is a list, then extract 'text'
    if isinstance(output, dict) and 'choices' in output:
        if isinstance(output['choices'], list) and len(output['choices']) > 0:
            return output['choices'][0]['text'].strip()  # Access the first choice's text

    # If no valid output, return an error message
    return "No valid code generated."


def process_image(image):
    img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


def encrypt_message(message, key):
    f = Fernet(key)
    encrypted = f.encrypt(message.encode())
    return encrypted


def decrypt_message(encrypted, key):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    return decrypted.decode()


def typewriter_effect(text):
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.code(full_text, language="java")
        time.sleep(0.02)  # Adjust typing speed here

def main():
    st.title("Multi-functional AI Code Generator by Adithya N Raj")

    task = st.selectbox("Select a task", ["Generate Code", "Process Image"])

    if task == "Generate Code":
        prompt = st.text_area("Enter your code generation prompt:")
        if st.button("Generate"):
            with st.spinner("Generating code..."):
                try:
                    code = generate_code(prompt)
                    st.subheader("Generated Code:")

                    # Display the code with typewriter effect
                    if code.strip():
                        typewriter_effect(code)
                    else:
                        st.warning("The model did not generate any code.")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    elif task == "Process Image":
        uploaded_file = st.file_uploader("Choose an image...", type="jpg")
        if uploaded_file is not None:
            processed_img = process_image(uploaded_file)
            st.image(processed_img, caption="Processed Image", use_column_width=True)
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        sys.argv = ["streamlit", "run", "main.py", "--global.developmentMode=false"]
        sys.exit(stcli.main())
    else:
        main()

