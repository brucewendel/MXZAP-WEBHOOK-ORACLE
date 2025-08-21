# 📩 WhatsApp Webhook Sender (Flask + Oracle)

Este projeto implementa um **servidor HTTP em Flask** que recebe **requisições via webhook** (disparadas a partir de **triggers no Oracle**) e envia mensagens automaticamente para a **API do WhatsApp**.  

---

## ⚙️ Fluxo de Funcionamento

1. Um evento no banco de dados **Oracle** dispara uma **trigger**.  
2. A trigger envia um **JSON** com os dados necessários para o servidor HTTP.  
3. O servidor **Flask** recebe a requisição no endpoint configurado.  
4. Os dados recebidos são processados e a mensagem é enviada para a **API do WhatsApp**.  

---

## 📂 Estrutura do Projeto

├── app.py # Servidor Flask
├── senderZap.py # Funções para envio de mensagens via API do WhatsApp
├── .env # Variáveis de ambiente (tokens, configs)
├── requirements.txt # Dependências do projeto
└── README.md # Documentação

## 📌 Observações

Certifique-se de que a trigger no Oracle está configurada corretamente para enviar o **POST** no endpoint do servidor Flask.

O servidor pode ser colocado em produção usando **Gunicorn + Nginx ou Docker**.

Caso esteja rodando em Cloud, libere a porta configurada (default: 5000).