import os
from dotenv import load_dotenv


class ConfigLoader:
    """Handles environment and API key loading."""

    def __init__(self, dotenv_path: str = ".env"):
        self.dotenv_path = dotenv_path

    def load_dotenv(self):
        """Load environment variables from a .env file."""
        load_dotenv(self.dotenv_path)

    def ensure_nvapi_key(self):
        import getpass

        if not os.environ.get("NVIDIA_NIM_API_KEY", "").startswith("nvapi-"):
            nvapi_key = getpass.getpass("Enter your NVIDIA API key: ")
            assert nvapi_key.startswith(
                "nvapi-"
            ), f"{nvapi_key[:5]}... is not a valid key"
            os.environ["NVIDIA_NIM_API_KEY"] = nvapi_key
            os.environ["NVIDIA_API_KEY"] = nvapi_key
        os.environ["NVIDIA_API_KEY"] = os.environ.get("NVIDIA_NIM_API_KEY", "")
