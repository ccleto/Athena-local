import re
import sys

def extract_and_format_ips(input_file, output_file):
    """Extracts ExitAddress IPs from the raw Tor list and formats them for Wazuh CDB."""
    ips = set()
    # Regex to find 'ExitAddress', capture the following IP, and check for a date pattern afterwards
    # This works even if the content is on a single line.
    regex = re.compile(r"ExitAddress\s+([\d\.]+)\s+\d{4}-\d{2}-\d{2}")

    try:
        with open(input_file, 'r') as f:
            content = f.read()
            # Find all occurrences of the pattern
            matches = regex.findall(content)
            for ip in matches:
                ips.add(ip)
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada \'{input_file}\' não encontrado.", file=sys.stderr)
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo de entrada \'{input_file}\': {e}", file=sys.stderr)
        return

    if not ips:
        print(f"Nenhum IP encontrado no arquivo \'{input_file}\'. Verifique o formato e o regex.", file=sys.stderr)
        return

    try:
        with open(output_file, 'w') as f:
            for ip in sorted(list(ips)): # Sort for consistency
                f.write(f"{ip}:\n") # Format for Wazuh CDB list (IP:)
        print(f"Lista de IPs formatada salva em \'{output_file}\'. Total de IPs únicos: {len(ips)}")
    except Exception as e:
        print(f"Erro ao escrever o arquivo de saída \'{output_file}\': {e}", file=sys.stderr)

if __name__ == "__main__":
    input_filename = "/home/ubuntu/tor_exit_nodes_raw.txt"
    output_filename = "/home/ubuntu/tor_exit_nodes.cdb.txt" # Changed extension for clarity
    extract_and_format_ips(input_filename, output_filename)

