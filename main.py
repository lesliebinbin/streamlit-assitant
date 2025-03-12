import streamlit as st
from assistant import AzureOpenAIAssitant

with st.sidebar:
    api_key = st.text_input("API Key", key="api_key", type="password")
    api_version = st.text_input(
        "API Version", key="api_version", value="2024-08-01-preview"
    )
    azure_endpoint = st.text_input(
        "Azure Endpoint",
        key="azure_endpoint",
    )
    deployment_name = st.text_input(
        "Deployment Name", key="deployment_name", value="gpt-4o-mini"
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
    if not api_key:
        st.info("Please add your api key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt["text"]})
    with st.chat_message("user"):
        for file in prompt["files"]:
            st.markdown(f"📎 **{file.name}**")
        st.write(prompt["text"])
    response = assitant(
        api_key, api_version, azure_endpoint, deployment_name
    ).client.chat.completions.create(
        model=deployment_name, messages=st.session_state.messages
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
