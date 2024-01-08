poetry config --local virtualenvs.in-project true
poetry init -n
poetry install
source .venv/bin/activate
poetry add fastapi[all]
poetry add pytest --dev