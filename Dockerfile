FROM python:3.13-slim as python-base

# Configurações do Python e do Pip
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Caminhos para Poetry e Virtualenv
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN pip install poetry

# Define diretório para dependências do projeto
WORKDIR $PYSETUP_PATH

# Copia os arquivos de configuração do Poetry primeiro (para aproveitar cache)
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false

# Instala dependências de produção
RUN poetry install --no-interaction --no-root

# Copia o restante do código
WORKDIR /app
COPY . /app/

# Expõe a porta do Django
EXPOSE 8000

# Comando padrão
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
