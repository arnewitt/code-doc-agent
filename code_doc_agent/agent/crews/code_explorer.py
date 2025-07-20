import yaml
from crewai import Agent, Crew, Task
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
)
from code_doc_agent.utils.schemas import DocPlan

# Agents Prompting Template for Llama 3.3
with open("code_doc_agent/agent/prompting_templates/system.txt", "r") as f:
    system_template = f.read()

with open("code_doc_agent/agent/prompting_templates/prompt.txt", "r") as f:
    prompt_template = f.read()

with open("code_doc_agent/agent/prompting_templates/response.txt", "r") as f:
    response_template = f.read()

# Load agent and task configurations from YAML files
with open("code_doc_agent/config/planner_agents.yaml", "r") as f:
    agents_config = yaml.safe_load(f)

with open("code_doc_agent/config/planner_tasks.yaml", "r") as f:
    tasks_config = yaml.safe_load(f)

code_explorer = Agent(
    config=agents_config["code_explorer"],
    system_template=system_template,
    prompt_template=prompt_template,
    response_template=response_template,
    tools=[DirectoryReadTool(), FileReadTool()],
)
documentation_planner = Agent(
    config=agents_config["documentation_planner"],
    system_template=system_template,
    prompt_template=prompt_template,
    response_template=response_template,
    tools=[DirectoryReadTool(), FileReadTool()],
)

analyze_codebase = Task(config=tasks_config["analyze_codebase"], agent=code_explorer)
create_documentation_plan = Task(
    config=tasks_config["create_documentation_plan"],
    agent=documentation_planner,
    output_pydantic=DocPlan,
)

planning_crew = Crew(
    agents=[code_explorer, documentation_planner],
    tasks=[analyze_codebase, create_documentation_plan],
    verbose=False,
)
