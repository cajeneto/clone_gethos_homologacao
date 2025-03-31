# Use uma imagem base com Python
FROM python:3.12-slim

# Instale dependências do sistema, incluindo as bibliotecas do PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto
COPY . .

# Crie e ative o ambiente virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instale as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Defina o comando de inicialização
CMD ["gunicorn", "gethosapp.wsgi", "--bind", "0.0.0.0:8000"]