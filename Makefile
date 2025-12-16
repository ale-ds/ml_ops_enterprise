PYTHON = python
PIP = pip
VENV_PYTHON = .venv/bin/python # Caminho para o Python dentro do ambiente

.PHONY: install setup train test clean

install:
	@echo "Instalando dependências..."
	$(PIP) install -r requirements.txt

setup: install
	@echo "Ambiente pronto."

# 1. Comando de Treinamento
train:
# 	@echo "Iniciando pipeline de Treinamento..."
# 	$(PIP) install -r requirements.txt
# 	$(PYTHON) src/models/train.py # Roda o orquestrador
	@echo "Iniciando pipeline de Treinamento via MLflow Project..."
	export MLFLOW_TRACKING_URI=http://127.0.0.1:5001 && \
	$(VENV_PYTHON) -m mlflow run . \
		--env-manager local \
		--experiment-name California_Housing_Enterprise

# 2. Comando de Teste
test:
	@echo "Executando testes de integração..."
	pytest tests/integration/

# Outros comandos
clean:
	rm -rf mlruns/ __pycache__/ .pytest_cache/