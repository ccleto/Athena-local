# 🛡️ Athena Security - Central de Scripts

Bem-vindo ao repositório oficial de scripts da Athena Security.  
Este espaço foi criado para manter organizados os scripts de monitoramento, automação, segurança e infraestrutura utilizados pela equipe técnica.

---

## 📂 Estrutura de Branches

Este repositório adota um modelo de versionamento baseado em branchs por stack e ambientes:

| Branch       | Finalidade                                                                 |
|--------------|----------------------------------------------------------------------------|
| `main`       | Produção – scripts finais, estáveis e prontos para uso em clientes.       |
| `dev`        | Desenvolvimento – onde todas as alterações são integradas e testadas.     |
| `wazuh`      | Scripts relacionados ao Wazuh (rules, decoders, FIM, automações, etc).    |
| `zabbix`     | Scripts de monitoramento com Zabbix (templates, triggers, APIs, etc).     |
| `scripts`    | Scripts gerais (Linux, Windows, Docker, backups, automações diversas).    |
| `feature/*`  | Branches temporárias para novas funcionalidades ou testes específicos.    |

---

## 🔁 Fluxo de Trabalho

### Etapas do fluxo padrão:

1. **Crie ou atualize os scripts em uma branch específica (`wazuh`, `zabbix`, etc).**
2. **Faça o `commit` das alterações.**
3. **Envie a branch para o repositório remoto (`push`).**
4. **Realize o merge da branch de stack para a `dev`.**
5. **Teste e valide na `dev`.**
6. **Quando estiver tudo certo, faça merge da `dev` para `main`.**

---

## 💻 Comandos Git - Guia Rápido

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/athena-security/scripts.git
cd scripts
```

### 2️⃣ Atualizar seu repositório local (pull)

#### Vá para a branch desejada
```bash 
git checkout dev
```

#### Atualize com o repositório remoto
```bash 
git pull origin dev
```

### 3️⃣ Criar uma nova branch de feature (opcional)
```bash 
git checkout -b feature/nome-da-feature
```
#### Exemplo:
```bash 
git checkout -b feature/wazuh-decoder-nginx
```

### 4️⃣ Adicionar arquivos e fazer commit

#### Adiciona todos os arquivos modificados
```bash 
git add .
```
#### Faz o commit com uma mensagem clara
```bash 
git commit -m "Adiciona decoder nginx para Wazuh"
```

### 5️⃣ Enviar alterações para o repositório remoto
```bash 
git push origin nome-da-branch
```
#### Exemplo:
```bash
git push origin wazuh
```

### 6️⃣ Fazer merge da branch da stack para a dev
```bash
git checkout dev
```
```bash
git merge wazuh
```
```bash
git push origin dev
```

### 7️⃣ Fazer merge da dev para a main
```bash
git checkout main
```
```bash
git merge dev
```
```bash
git push origin main
```
