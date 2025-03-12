from openai import AzureOpenAI
from typing import IO


class AzureOpenAIAssitant:
    def __init__(
        self,
        api_key,
        azure_endpoint,
        api_version,
        deployment_name,
        assitant_name="basf_ai_task_force",
    ):
        self._client = AzureOpenAI(
            api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint
        )
        assitants = self._client.beta.assistants.list().data
        self._assitant = next((a for a in assitants if a.name == assitant_name), None)
        if self._assitant is None:
            self._assitant = self._client.beta.assistants.create(
                name=assitant_name,
                model=deployment_name,
                tools=[{"type": "file_search"}],
            )
        self._thread = self._client.beta.threads.create()

    @property
    def client(self):
        return self._client


    def upload_files(self, files: list[IO]):
        return [
            self._client.files.create(file=file, purpose="assistants").id
            for file in files
        ]

    def chat(self, prompt: str, attachment_ids: list[str] = None):
        self._client.beta.messages.create(
            thread_id=self._thread.id,
            content=prompt,
            role="user",
            attachments=[
                {"file_id": file_id, "tools": [{"type": "file_search"}]}
                for file_id in (attachment_ids or [])
            ],
        )
        with self._client.beta.threads.runs.stream(
            thread_id=self._thread.id, assitant_id=self._assitant.id
        ) as stream:
            stream.until_done()
            return stream.get_final_messages()
