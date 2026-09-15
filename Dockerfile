# Usa uma imagem oficial e leve do Python 3.11
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Evita que o Python grave arquivos .pyc no disco e desativa o buffer de saída
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala as dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências e instala as bibliotecas Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código-fonte da aplicação para dentro do container
COPY . .

# Expõe a porta em que o Uvicorn vai rodar
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]