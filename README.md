# Streamlit Chatbot

This project is a Streamlit-based chatbot application that integrates with Azure OpenAI to provide conversational AI capabilities. The chatbot allows users to interact with an AI assistant and upload files for the assistant to process.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a [.env](http://_vscodecontentref_/6) file in the root directory and add your  OpenAzureAI credentials:
    ```env
    API_KEY=<your-api-key>
    API_VERSION=<your-api-version>
    AZURE_ENDPOINT=<your-azure-endpoint>
    DEPLOYMENT_NAME=<your-deployment-name>
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run main.py
    ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Enter your Azure OpenAI credentials in the sidebar.

4. Interact with the chatbot by typing messages and uploading files.

## Files

- [main.py](http://_vscodecontentref_/7): The main entry point of the Streamlit application.
- [assistant.py](http://_vscodecontentref_/8): Contains the [AzureOpenAIAssitant](http://_vscodecontentref_/9) class that handles interactions with Azure OpenAI.
- [requirements.txt](http://_vscodecontentref_/10): Lists the dependencies required for the project.

## License

This project is licensed under the MIT License.
