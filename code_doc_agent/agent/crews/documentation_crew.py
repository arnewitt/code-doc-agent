import yaml
from crewai import Agent, Task, Crew
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
)
from crewai_tools import DirectoryReadTool, FileReadTool, WebsiteSearchTool
from agent.guardrails import check_mermaid_syntax

# Load agent and task configurations from YAML files
with open("code_doc_agent/config/documentation_agents.yaml", "r") as f:
    agents_config = yaml.safe_load(f)

with open("code_doc_agent/config/documentation_tasks.yaml", "r") as f:
    tasks_config = yaml.safe_load(f)

overview_writer = Agent(
    config=agents_config["overview_writer"],
    tools=[
        DirectoryReadTool(),
        FileReadTool(),
        WebsiteSearchTool(
            website="https://mermaid.js.org/intro/",
            config=dict(
                embedder=dict(
                    provider="nvidia",
                    config=dict(model="nvidia/nv-embedqa-e5-v5"),
                )
            ),
        ),
    ],
)

documentation_reviewer = Agent(
    config=agents_config["documentation_reviewer"],
    tools=[
        DirectoryReadTool(
            directory="code_doc_agent/docs/", name="Check existing documentation folder"
        ),
        FileReadTool(),
    ],
)

draft_documentation = Task(
    config=tasks_config["draft_documentation"], agent=overview_writer
)

qa_review_documentation = Task(
    config=tasks_config["qa_review_documentation"],
    agent=documentation_reviewer,
    guardrail=check_mermaid_syntax,
    max_retries=5,
)

documentation_crew = Crew(
    agents=[overview_writer, documentation_reviewer],
    tasks=[draft_documentation, qa_review_documentation],
    verbose=False,
)
