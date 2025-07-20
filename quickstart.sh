clear
echo "Starting Code Documentation Agent..."

echo "Running cleanup from last run..."
uv run code_doc_agent/cleanup.py
echo "Finished cleanup from last run..."

echo "Starting Code Documentation Agent..."
if ! [ -e "docs/" ] ; then
    rm -r "docs"
    mkdir "docs"
    echo "Created a new /docs folder."
fi
if ! [ -e "docs/plan.json" ] ; then
    touch "docs/plan.json"
    echo "Created a new docs/plan.json file."
fi
if ! [ -e "workdir/" ] ; then
    mkdir "workdir"
    echo "Created a new /workdir folder."
fi

uv run code_doc_agent/main.py
echo "Code Documentation Agent has finished running."
echo "Cleaning up temporary files..."

rm -r db