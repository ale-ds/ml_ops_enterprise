# 🏗️ MLOps Enterprise: California Housing Prediction

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-active-success.svg">
  <img alt="Python" src="https://img.shields.io/badge/python-3.11+-blue.svg">
  <img alt="MLflow" src="https://img.shields.io/badge/mlflow-2.x-orange.svg">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg">
</p>

---

Este projeto demonstra a transformação de um fluxo de trabalho de Ciência de Dados, de um protótipo em Notebook para uma **arquitetura MLOps Enterprise robusta e modular**. O objetivo é estabelecer um padrão que garanta reprodutibilidade, rastreabilidade e escalabilidade.

## 📋 Índice

- [📖 Sobre o Projeto](#-sobre-o-projeto)
- [📂 Estrutura de Arquivos](#-estrutura-de-arquivos)
- [🚀 Como Executar](#-como-executar)
  - [1. Pré-requisitos](#1-pré-requisitos)
  - [2. Configuração do Ambiente](#2-configuração-do-ambiente)
  - [3. Inicialização do Servidor MLflow](#3-inicialização-do-servidor-mlflow)
  - [4. Execução do Pipeline de Treino](#4-execução-do-pipeline-de-treino)
- [🧪 Executando os Testes](#️-executando-os-testes)
- [📊 Resultados e Métricas](#-resultados-e-métricas)
- [🛠️ Guia de Solução de Problemas](#️-guia-de-solução-de-problemas)
- [📝 Licença](#-licença)

---

## 📖 Sobre o Projeto

O foco não é apenas treinar um modelo de previsão de preços de casas, mas estabelecer um padrão de **MLOps** que prioriza:

> **Reprodutibilidade:** Uso de `Makefiles` e ambientes virtuais para garantir que cada execução seja consistente.

> **Rastreabilidade:** Tracking centralizado de experimentos com MLflow em uma arquitetura cliente-servidor.

> **Escalabilidade:** Código modular (`src/`) totalmente desacoplado de configurações (`config/`), permitindo fácil manutenção e expansão.

## 📂 Estrutura de Arquivos

A organização do projeto segue o princípio de *Separation of Concerns*, onde cada componente tem uma responsabilidade única.

```
ml_ops_enterprise/
├── .github/
│   └── workflows/
│       └── main.yml        # Define o pipeline de CI/CD com GitHub Actions.
├── .gitignore              # Arquivos e diretórios a serem ignorados pelo Git.
├── config/
│   ├── data/
│   │   └── raw.yaml        # Configurações para os dados brutos (ex: paths).
│   └── model/
│       └── random_forest.yaml # Hiperparâmetros e configurações do modelo.
├── data/
│   ├── 01_raw/             # Armazena os dados brutos (não versionados).
│   ├── 02_processed/       # Armazena os dados processados.
│   └── 03_features/        # Armazena os dados após a engenharia de features.
├── scripts/
│   ├── buid_project.sh     # Script para construir o projeto (ex: build de imagem Docker).
│   └── tree.conf           # Configuração que contém a estrutura de diretórios e arquivos que serão criados.
├── src/
│   ├── __init__.py         # Torna o diretório 'src' um pacote Python.
│   ├── data_prep/
│   │   ├── __init__.py
│   │   └── extractor.py    # Scripts para extrair e carregar os dados.
│   ├── features/
│   │   ├── __init__.py
│   │   └── transformer.py  # Módulos para engenharia e transformação de features.
│   ├── models/
│   │   ├── __init__.py
│   │   └── train.py        # Lógica para treinamento e avaliação do modelo.
│   ├── serving/
│   │   ├── __init__.py
│   │   └── api.py          # Código para servir o modelo como uma API (ex: com FastAPI).
│   └── validation/
│       └── schema.py       # Define o esquema de validação dos dados de entrada.
├── tests/
│   ├── integration/
│   │   └── test_model_integrity.py # Testes de integração para validar a integridade do modelo.
│   └── unit/               # Diretório para testes de unidade.
├── conda.yaml              # Dependências do projeto para ambientes Conda.
├── Dockerfile              # Define a imagem Docker para a aplicação.
├── Makefile                # Orquestrador de comandos para automação de tarefas (ex: `make train`).
├── MLproject               # Define a estrutura e os entry points para o MLflow Projects.
├── README.md               # Documentação do projeto.
└── requirements.txt        # Dependências do projeto para ambientes pip.
```

---

## 🚀 Como Executar

Siga os passos abaixo para configurar e executar o projeto.

### 1. Pré-requisitos

- **Python 3.11+**
- **Make:** Geralmente nativo no Linux/macOS. Para Windows, utilize WSL ou Git Bash.

### 2. Configuração do Ambiente

Crie um ambiente virtual para isolar as dependências do projeto.

```bash
# 1. Crie o ambiente virtual
python -m venv .venv

# 2. Ative o ambiente (ESSENCIAL!)
# No macOS/Linux:
source .venv/bin/activate
# No Windows:
# .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
```

### 3. Inicialização do Servidor MLflow

Para simular um ambiente de produção, subimos o MLflow em modo servidor. **Abra um novo terminal**, ative o ambiente virtual (`source .venv/bin/activate`) e execute:

```bash
# A porta 5001 é usada para evitar conflitos com o AirPlay no macOS
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlruns \
    --host 127.0.0.1 \
    --port 5001
```

> Mantenha este terminal aberto. A interface do MLflow estará acessível em **[http://127.0.0.1:5001](http://127.0.0.1:5001)**.

### 4. Execução do Pipeline de Treino

No seu terminal de desenvolvimento principal (com o `.venv` ativado), use um único comando `make` para orquestrar todo o pipeline:

```bash
make train
```

Este comando irá:
1.  Definir a variável de ambiente `MLFLOW_TRACKING_URI` para se conectar ao servidor MLflow.
2.  Definir o nome do experimento no MLflow.
3.  Executar o pipeline de treinamento definido no `MLproject`.

---

## 🧪 Executando os Testes

Este projeto inclui testes de integração para garantir a integridade do modelo antes do deploy. O principal teste (`tests/integration/test_model_integrity.py`) simula um "Engenheiro de Deploy" que valida o contrato de entrada e saída do modelo mais recente registrado no MLflow.

Para executar os testes, utilize o seguinte comando:

```bash
make test
```

Este comando utiliza o `pytest` para descobrir e executar todos os testes localizados na pasta `tests/`. É um passo crucial para garantir a qualidade e a confiabilidade do pipeline.

---

## 📊 Resultados e Métricas

Todos os experimentos são rastreados e logados com:

- **Parâmetros:** Capturados de `config/model/random_forest.yaml`.
- **Métricas:** `RMSE` do modelo.
- **Artefatos:** O modelo treinado, os arquivos de configuração e gráficos relevantes.

## 🛠️ Guia de Solução de Problemas

**🔴 Erro: `503 Service Unavailable` ou `403 Forbidden`**
- **Causa:** Conflito de porta no macOS. O serviço AirPlay Receiver pode usar a porta `5000`.
- **Solução:** O projeto já está configurado para usar a porta `5001`. Garanta que o servidor MLflow foi iniciado nesta porta.

**🔴 Erro: `ModuleNotFoundError: No module named 'mlflow'`**
- **Causa:** O ambiente virtual não foi ativado no terminal onde o comando `make train` foi executado.
- **Solução:** Ative o ambiente com `source .venv/bin/activate` antes de executar o `make`.

**🔴 Erro: `RESOURCE_DOES_NOT_EXIST` (Run ID Mismatch)**
- **Causa:** Tentativa de definir um experimento (`mlflow.set_experiment`) dentro de um script que já foi iniciado por um `mlflow run`.
- **Solução:** A arquitetura do projeto segue a regra: "O Orquestrador manda, o Script obedece". O `train.py` não define URI ou experimento; ele apenas loga no contexto injetado pelo `Makefile`.

---

## 📝 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais informações.
