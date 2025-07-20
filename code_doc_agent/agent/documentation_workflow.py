import subprocess
from pathlib import Path
from crewai.flow.flow import Flow, listen, start

from utils import DocumentationState
from agent.crews.code_explorer import planning_crew
from agent.crews.documentation_crew import documentation_crew


class DocumentationFlow(Flow[DocumentationState]):
    # Clone the repository, initial step
    # No need for AI Agents on this step, so we just use regular Python code
    @start()
    def clone_repo(self):
        print(f"# Cloning repository: {self.state.project_url}\n")
        # Extract repo name from URL
        repo_name = self.state.project_url.split("/")[-1]
        self.state.repo_path = f"{self.state.repo_path}/{repo_name}"

        # Check if directory exists
        if Path(self.state.repo_path).exists():
            print(f"# Repository directory already exists at {self.state.repo_path}\n")
            subprocess.run(["rm", "-rf", self.state.repo_path])
            print("# Removed existing directory\n")

        # Clone the repository
        subprocess.run(["git", "clone", self.state.project_url, self.state.repo_path])
        return self.state

    @listen(clone_repo)
    def plan_docs(self):
        print(f"# Planning documentation for: {self.state.repo_path}\n")
        result = planning_crew.kickoff(inputs={"repo_path": self.state.repo_path})
        print(f"# Planned docs for {self.state.repo_path}:")
        for doc in result.pydantic.docs:
            print(f"    - {doc.title}")
        return result

    @listen(plan_docs)
    def save_plan(self, plan):
        with open("docs/plan.json", "w") as f:
            f.write(plan.raw)

    @listen(plan_docs)
    def create_docs(self, plan):
        for doc in plan.pydantic.docs:
            print(f"\n# Creating documentation for: {doc.title}")
            result = documentation_crew.kickoff(
                inputs={
                    "repo_path": self.state.repo_path,
                    "title": doc.title,
                    "overview": plan.pydantic.overview,
                    "description": doc.description,
                    "prerequisites": doc.prerequisites,
                    "examples": "\n".join(doc.examples),
                    "goal": doc.goal,
                }
            )

            # Save documentation to file in docs folder
            docs_dir = Path("docs")
            docs_dir.mkdir(exist_ok=True)
            title = doc.title.lower().replace(" ", "_") + ".mdx"
            self.state.docs.append(str(docs_dir / title))
            with open(docs_dir / title, "w") as f:
                f.write(result.raw)
        print(f"\n# Documentation created for: {self.state.repo_path}")
