from flask import Flask, request, jsonify
from senderZap import *




app = Flask(__name__)
# Lista global para armazenar números formatados
numeros_whatsapp = []

def format_number(numero_raw):
    """Formata número para 55DDDNNNNNNN"""
    numero = ''.join(filter(str.isdigit, str(numero_raw)))
    if not numero.startswith('55'):
        numero = '55' + numero
    return numero

@app.route("/webhook/winthor", methods=["POST"])
def receber_glpi():
    """Recebe dados do webhook do Oracle e envia para WhatsApp"""
    try:
        # Limpa a lista de números para esta requisição
        numeros_whatsapp.clear()

        # 🔹 Decode com fallback (tenta utf-8, se falhar usa latin1)
        try:
            raw_data = request.data.decode("utf-8")
        except UnicodeDecodeError:
            raw_data = request.data.decode("latin1")
        print("📩 RAW RECEBIDO:", raw_data)

        import json, os, datetime
        # 🔹 Tenta parsear JSON
        try:
            dados = request.get_json(silent=True)
            if not dados:
                dados = json.loads(raw_data)
        except Exception:
            try:
                dados = json.loads(raw_data)
            except Exception as e2:
                print("❌ Falha ao parsear JSON:", e2)

                # 🔹 NOVO: salvar raw_data em arquivo de log diário
                log_dir = "webhook_logs"
                os.makedirs(log_dir, exist_ok=True)
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                log_file = os.path.join(log_dir, f"invalid_json_{today}.log")

                with open(log_file, "a", encoding="utf-8") as f:
                    f.write("\n" + "="*60 + "\n")
                    f.write(f"⏰ {datetime.datetime.now()}\n")
                    f.write(f"IP: {request.remote_addr}\n")
                    f.write(raw_data + "\n")

                # retorna 200 para não quebrar o fluxo do integrador
                return jsonify({
                    "status": "erro",
                    "motivo": "JSON inválido",
                    "raw_salvo_em": log_file
                }), 200  

        # Extrair informações do payload
        importado = dados.get("importado", "N/A")
        codfilial = dados.get("codfilial", "N/A")
        codusur = dados.get("codusur", "N/A")
        nome_rca = dados.get("nome_rca", "NOME NÃO INFORMADO")
        cod_supervisor = dados.get("cod_supervisor", "N/A")
        nome_supervisor = dados.get("nome_supervisor", "NOME NÃO INFORMADO")
        numped = dados.get("numped", "N/A")
        origem = dados.get("origemped", "N/A")
        observacao_pc = dados.get("observacao_pc", "Sem observação").strip()
        data_evento = dados.get("data", "Data não informada")

        # Se houver número de telefone no JSON
        numero_rca = dados.get("telefone_rca")
        numero_sup = dados.get("telefone_supervisor")

        # Formata e salva na lista global se existir
        for numero in [numero_rca, numero_sup]:
            if numero:
                numero_formatado = format_number(numero)
                if numero_formatado not in numeros_whatsapp:
                    numeros_whatsapp.append(numero_formatado)
        
        for numero in NUMERO_ADMIN:
            if numero not in numeros_whatsapp:
                numeros_whatsapp.append(numero)

        mensagem = (
            "🚨 *Alerta de Pedido NÃO Integrado*\n"
            "──────────────────────────────\n"
            f"🏢 Filial: *{codfilial}*\n"
            f"📦 Status: *{importado}*\n"
            f"👤 RCA: *{codusur} - {nome_rca}*\n"
            f"🧑‍💼 Supervisor: *{cod_supervisor} - {nome_supervisor}*\n"
            f"📝 Número do Pedido: *{numped}*\n"
            f"🌐 Origem: *{origem}*\n"
            f"⚠️ Observação: {observacao_pc}\n"
            f"📅 Data: {data_evento}\n"
            "──────────────────────────────\n\n\n"
            "*☎️ Falar com o analista responsável ou com o supervisor.*\n\n"
            f"❗️*_Orienta-se a ver o caso na rotina 2596_*❗️\n\n"
            "_Mensagem enviada pelo sistema de monitoramento_"
        )

        print("📤 ENVIANDO WHATSAPP:", mensagem)
        print("📲 Lista de números formatados:", numeros_whatsapp)

        # Enviar para todos os números da lista
        resultados = []
        for numero in numeros_whatsapp:
            r = send_message(mensagem, numero_destino=numero)
            resultados.append({numero: r})

        return jsonify({"status": "ok", "resultados": resultados}), 200

    except Exception as e:
        import traceback
        print("❌ ERRO:", str(e))
        print(traceback.format_exc())
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="10.0.127.11", port=8501, debug=False)
