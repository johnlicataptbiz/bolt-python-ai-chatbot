from os import getenv
from .base_provider import BaseAPIProvider


class ProviderTemplate(BaseAPIProvider):
    """A minimal provider skeleton showing required methods.

    Replace the implementation with real API calls for your provider. Export
    credentials as `NEW_PROVIDER_API_KEY` (or change the env var name here).
    """

    def __init__(self):
        self.api_key = getenv("NEW_PROVIDER_API_KEY", "")
        self.model = None

    def set_model(self, model_name: str):
        self.model = model_name

    def get_models(self) -> dict:
        # Return a dict shape compatible with `ai/providers/__init__.py` merging logic.
        # Key is provider name; the value can include display helpers.
        return {"newprovider": {"display_name": "NewProvider", "models": ["default"]}}

    def generate_response(self, prompt: str, system_content: str) -> str:
        # Minimal placeholder implementation. Replace with a real API call.
        return f"[newprovider:{self.model or 'default'}] {system_content}\n{prompt}\n=> (mock response)"
