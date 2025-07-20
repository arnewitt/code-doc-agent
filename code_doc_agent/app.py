import os
from agent.documentation_workflow import DocumentationFlow


class Application:

    def __init__(self):
        """Initialize the application."""
        self.flow = DocumentationFlow()

    def _run_documentation(self):
        """Start the actual code documentation process."""
        self.flow.kickoff()

    def _create_overview_md(self):
        """Create a markdown file that summarizes all of the .mdx files in the /docs folder."""
        markdown_file = "**Overview of documentation**\n"
        mdx_filenames = [f for f in os.listdir("docs") if f.endswith(".mdx")]
        for filename in mdx_filenames:
            file_title = filename.split(".")[0]
            markdown_file += f"- [{file_title}]({filename})\n"

        with open("docs/documentation_content_overview.mdx", "w") as f:
            f.write(markdown_file)

    def run_doc_workflow(self):
        """Run the documentation workflow."""
        self._run_documentation()
        self._create_overview_md()
