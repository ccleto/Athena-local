#!/usr/bin/env python

import sys
import json
import requests
import urllib.parse
from datetime import datetime, timedelta

# Configurações fixas
CHAT_ID = "-4701086596"
DASHBOARD_BASE_URL = "https://wazuh.fwathena.com/app/discover"

# Lê argumentos do Wazuh
alert_file = sys.argv[1]
hook_url = sys.argv[3]

# Lê o alerta JSON
with open(alert_file, 'r') as f:
    alert_json = json.load(f)

# Extrai dados principais
alert_level = alert_json['rule'].get('level', "N/A")
description = alert_json['rule'].get('description', "N/A")
agent = alert_json['agent'].get('name', "N/A")
timestamp_str = alert_json.get('@timestamp')

# Tratamento de segurança para timestamp
try:
    if "." in timestamp_str:
        alert_time = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        alert_time = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
except Exception as e:
    # Se der erro, usa hora atual (melhor que falhar o script)
    alert_time = datetime.utcnow()

# Intervalo: 1 minuto antes e depois
from_time = (alert_time - timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
to_time = (alert_time + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%S.000Z')

# Monta filtros
query_parts = [
    f'agent.name: "{agent}"',
    f'rule.description: "{description}"'
]
full_query = " AND ".join(query_parts)
encoded_query = urllib.parse.quote(full_query)

# Monta filtro de tempo fixo
time_filter = f"_g=(time:(from:'{from_time}',to:'{to_time}'))"

# Link completo
dashboard_link = (
    f"{DASHBOARD_BASE_URL}#/?_a=(query:(language:kuery,query:'{encoded_query}'))&{time_filter}"
)

# Texto da mensagem
msg_text = (
    f"🚨 *Novo Alerta Recebido!* 🚨\n\n"
    f"*Agente:* `{agent}`\n"
    f"*Nível:* `{alert_level}`\n"
    f"*Descrição:* {description}"
)

# Monta mensagem com botão
msg_data = {
    'chat_id': CHAT_ID,
    'text': msg_text,
    'parse_mode': 'Markdown',
    'reply_markup': {
        'inline_keyboard': [[
            {
                'text': '🔎 Investigar no Wazuh',
                'url': dashboard_link
            }
        ]]
    }
}

# Envia requisição
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
requests.post(hook_url, headers=headers, data=json.dumps(msg_data))

sys.exit(0)