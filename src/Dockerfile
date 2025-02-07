FROM python:3.12-slim

# Instalar dependências do sistema e Poetry
RUN apt update && \
    apt install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Instalar o Poetry
RUN pip install poetry

# Definir o diretório de trabalho
WORKDIR /src

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock /src/

# Instalar dependências com Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Copiar o código-fonte para o diretório de trabalho
COPY . /src/

# Expor a porta padrão do Streamlit
EXPOSE 8501

# Definir o comando padrão para iniciar o Streamlit
CMD ["streamlit", "run", "dataapp/frontend/app_teste.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
