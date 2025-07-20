from pydantic import BaseModel
from pathlib import Path
from typing import List


class DocItem(BaseModel):
    """Represents a documentation item"""

    title: str
    description: str
    prerequisites: str
    examples: list[str]
    goal: str


class DocPlan(BaseModel):
    """Documentation plan"""

    overview: str
    docs: list[DocItem]


class DocumentationState(BaseModel):
    """
    State for the documentation flow
    """

    project_url: str = "https://github.com/arnewitt/text-pii-masking"
    repo_path: Path = "./workdir"
    docs: List[str] = []
