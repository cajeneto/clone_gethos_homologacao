# Use uma imagem base mais completa com Python 3.12
FROM python:3.12

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto
COPY . .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta 8000
EXPOSE 8000

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]