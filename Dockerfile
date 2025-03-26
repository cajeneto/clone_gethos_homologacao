# Use uma imagem base com Python 3.12
FROM python:3.12-slim

# Instale dependências do sistema (incluindo libstdc++ para o numpy)
RUN apt-get update && apt-get install -y \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos do projeto para o container
COPY . .

# Instale as dependências do Python listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta 8000 (padrão para o Django)
EXPOSE 8000

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]