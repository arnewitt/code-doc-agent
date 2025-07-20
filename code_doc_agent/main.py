import nest_asyncio
from utils import ConfigLoader
from app import Application


def setup():
    config_loader = ConfigLoader()
    config_loader.ensure_nvapi_key()
    nest_asyncio.apply()


if __name__ == "__main__":
    setup()
    app = Application()
    app.run_doc_workflow()
