import dotenv

dotenv.load_dotenv()
import streamlit as st
from utils.assistant import AzureOpenAIAssitant
import os

with st.sidebar:
    api_key = st.text_input(
        "API Key",
        key="api_key",
        type="password",
        value=os.environ["API_KEY"],
    )

    api_version = st.text_input(
        "API Version", key="api_version", value=os.environ["API_VERSION"]
    )

    azure_endpoint = st.text_input(
        "Azure Endpoint", key="azure_endpoint", value=os.environ["AZURE_ENDPOINT"]
    )

    deployment_name = st.text_input(
        "Deployment Name", key="deployment_name", value=os.environ["DEPLOYMENT_NAME"]
    )


@st.cache_resource
def assitant(api_key, api_version, azure_endpoint, deployment_name):
    return AzureOpenAIAssitant(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint,
        deployment_name=deployment_name,
    )


st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(accept_file="multiple"):
    ai_assitant = assitant(api_key, api_version, azure_endpoint, deployment_name)
    if not api_key:
        st.info("Please add your api key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt["text"]})
    with st.chat_message("user"):
        uploaded_file_ids = ai_assitant.upload_files(prompt["files"])
        for file in prompt["files"]:
            st.markdown(f"📎 **{file.name}**")
        st.write(prompt["text"])
    response = ai_assitant.chat(prompt["text"], uploaded_file_ids)
    final_text_message = response[0].content[0].text.value
    st.session_state.messages.append(
        {"role": "assistant", "content": final_text_message}
    )
    st.chat_message("assistant").markdown(final_text_message)
