#!/usr/bin/env python3
import json
import sys
import requests

# Configurações do TheHive
THEHIVE_API = 'http://1/HtVNYO2DSXmjDYdh/xp5jHpMLQ0F4w:9000/api/v1/alert'
API_KEY = '1/HtVNYO2DSXmjDYdh/xp5jHpMLQ0F4w'
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}

# Recebe o alerta do Wazuh
alert_input = sys.stdin.read()
alert = json.loads(alert_input)

# Filtra por nível de alerta: apenas >= 11
if int(alert['rule']['level']) < 11:
    exit(0)

# Monta o payload para o TheHive
payload = {
    "title": f"Wazuh Alert - {alert['rule']['description']}",
    "description": f"Alert from Wazuh:\n{json.dumps(alert, indent=2)}",
    "type": "external",
    "source": "Wazuh",
    "sourceRef": alert['id'],
    "severity": int(alert['rule']['level']),
    "tlp": 2,
    "tags": ["wazuh", alert['rule']['level']],
    "artifacts": [
        {
            "dataType": "ip",
            "data": alert['srcip'],
            "tags": ["source-ip"]
        }
    ] if 'srcip' in alert else []
}

# Envia o alerta para o TheHive
response = requests.post(THEHIVE_API, headers=HEADERS, data=json.dumps(payload))

# Loga a resposta
print(f"Response status: {response.status_code}")
print(response.text)
