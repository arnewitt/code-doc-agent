from crewai.tasks import TaskOutput
import re


def check_mermaid_syntax(task_output: TaskOutput):
    text = task_output.raw

    # Find all mermaid code blocks in the text
    mermaid_blocks = re.findall(r"```mermaid\n(.*?)\n```", text, re.DOTALL)

    for block in mermaid_blocks:
        diagram_text = block.strip()
        lines = diagram_text.split("\n")
        corrected_lines = []

        for line in lines:
            corrected_line = re.sub(
                r"\|.*?\|>", lambda match: match.group(0).replace("|>", "|"), line
            )
            corrected_lines.append(corrected_line)

        text = text.replace(block, "\n".join(corrected_lines))

    task_output.raw = text
    return (True, task_output)
