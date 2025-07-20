import nest_asyncio
from utils import ConfigLoader
from app import Application


def setup():
    config_loader = ConfigLoader()
    config_loader.load_dotenv()
    config_loader.ensure_nvapi_key()
    nest_asyncio.apply()


if __name__ == "__main__":
    setup()
    project_url = "https://github.com/arnewitt/text-pii-masking"
    app = Application(project_url=project_url)
    app.run_doc_workflow()
