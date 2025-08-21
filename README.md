:

📩 WhatsApp Webhook Sender (Flask + Oracle)

Este projeto implementa um servidor HTTP em Flask que recebe requisições via webhook (disparadas a partir de triggers no Oracle) e envia mensagens automaticamente para a API do WhatsApp.

⚙️ Fluxo de Funcionamento

Um evento no banco de dados Oracle dispara uma trigger.

A trigger envia um JSON com os dados necessários para o servidor HTTP.

O servidor Flask recebe a requisição no endpoint configurado.

Os dados recebidos são processados e a mensagem é enviada para a API do WhatsApp.

📂 Estrutura do Projeto
.
├── app.py            # Servidor Flask
├── senderZap.py      # Funções para envio de mensagens via API do WhatsApp
├── .env              # Variáveis de ambiente (tokens, configs)
├── requirements.txt  # Dependências do projeto
└── README.md         # Documentação

🔧 Requisitos

Python 3.9+

Flask

Requests

Oracle configurado com a trigger de disparo

API do WhatsApp (token e URL fornecidos pelo serviço contratado)

Instale as dependências com:

pip install -r requirements.txt

🚀 Como rodar o servidor

Configure as variáveis de ambiente no arquivo .env:

API_URL=https://api.whatsapp.com/send
API_TOKEN=seu_token_aqui
NUMBER=5585999999999


Inicie o servidor Flask:

python app.py


O servidor rodará por padrão em:

http://localhost:5000

📥 Exemplo de Payload (JSON enviado pela Trigger Oracle)
{
  "number": "5585999999999",
  "message": "Olá! Seu pedido foi confirmado ✅"
}

📤 Exemplo de Resposta da API
{
  "status": "ok",
  "resultados": [
    {
      "number": "5585999999999",
      "message": "Enviado com sucesso"
    }
  ]
}

📌 Observações

Certifique-se de que a trigger no Oracle está configurada corretamente para enviar o POST no endpoint do servidor Flask.

O servidor pode ser colocado em produção usando Gunicorn + Nginx ou Docker.

Caso esteja rodando em Cloud, libere a porta configurada (default: 5000).