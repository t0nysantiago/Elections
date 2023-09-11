# Use a imagem oficial do Python como base
FROM python:latest

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos necessários para o contêiner
COPY . /app

# Instale as dependências usando o pip
RUN pip install -r requirements.txt

# Exponha a porta na qual a API será executada (ajuste conforme necessário)
EXPOSE 8000

# Comando para iniciar a sua aplicação (ajuste conforme necessário)
CMD ["python", "app.py"]
