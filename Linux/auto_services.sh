#!/bin/bash
clear

# === DEFINIR CORES ===
RED='\033[0;31m'
# GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # Sem cor

# Função para exibir título com linha destacada

# Exibe um título com uma linha destacada em volta
print_section_title() {
    local title="$1"
    local padding=15
    local total_width=70
    local title_len=${#title}
    local side_len=$(( (total_width - title_len - 2) / 2 ))
    local line
    line=$(printf '=%.0s' $(seq 1 $side_len))
    echo -e "\n${CYAN}${line} ${title} ${line}${NC}"
}

# Validar se o script esta rodando como root
if [ "$(id -u)" != "0" ]; then
    echo -e "${RED}Este script deve ser executado como root ou com privilégios de sudo.${NC}"
    exit 1
fi

print_section_title "SISTEMA E KERNEL"
echo -e "${BOLD}Hostname:${NC} $(hostname)"
echo -e "${BOLD}Kernel:${NC} $(uname -r)"
echo -e "${BOLD}Arquitetura:${NC} $(uname -m)"

if command -v lsb_release &>/dev/null; then
    echo -e "${BOLD}Distribuição:${NC} $(lsb_release -d | cut -f2-)"
    echo -e "${BOLD}Versão:${NC} $(lsb_release -r | cut -f2-)"
else
    echo -e "${YELLOW}lsb_release não instalado. Distribuição não identificada.${NC}"
fi

print_section_title "CPU"
CPU_COUNT=$(lscpu | grep "^CPU(s):" | awk '{print $2}')
MODEL_NAME=$(lscpu | grep "Model name" | sed 's/Model name:[ \t]*//')
echo -e "${BOLD}Modelo:${NC} $MODEL_NAME"
echo -e "${BOLD}Quantidade de CPUs:${NC} $CPU_COUNT"

print_section_title "MEMÓRIA"
TOTAL_MEM=$(free -h | awk '/^Mem:/ {print $2}')
USED_MEM=$(free -h | awk '/^Mem:/ {print $3}')
echo -e "${BOLD}Memória Total:${NC} $TOTAL_MEM"
echo -e "${BOLD}Memória Usada:${NC} $USED_MEM"
echo -e "${BOLD}Resumo do vmstat (em KB):${NC}"
vmstat -s | head -n 10

print_section_title "DISCO E PARTIÇÕES"
echo -e "${BOLD}Dispositivos e Partições:${NC}"
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT | grep -v loop
echo
echo -e "${BOLD}Uso de Disco por Partição:${NC}"
df -h --output=source,size,used,avail,pcent,target | grep "^/dev"
echo -e "${BOLD}Montagens ativas:${NC}"
mount | grep "^/dev"

print_section_title "STORAGE iSCSI"
if command -v iscsiadm &>/dev/null; then
    iscsiadm -m session 2>/dev/null || echo -e "${YELLOW}Nenhuma sessão iSCSI ativa.${NC}"
else
    echo -e "${YELLOW}iscsiadm não está instalado.${NC}"
fi

print_section_title "IP E INTERFACES"
echo -e "${BOLD}Endereços IP (excluindo localhost):${NC}"
ip -o -4 addr show | awk '!/127.0.0.1/ {print "Interface: "$2" | IP: "$4}'
echo
echo -e "${BOLD}Rotas:${NC}"
ip route

print_section_title "SERVIÇOS ATIVOS"
echo -e "${BOLD}Serviços em execução:${NC}"
systemctl list-units --type=service --state=running | awk 'NR==1 || /running/' | column -t
