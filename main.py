
"""
Main runner for the Auto-Compliance Windows checker.
Corredor principal para el verificador de cumplimiento automático de Windows.
This script collects various system configurations and outputs the results in JSON format.
Este script recopila varias configuraciones del sistema y genera los resultados en formato JSON.
"""
import json
from src.collector.passwords_ps import collect_password_policies
from src.collector.firewall_ps import collect_firewall_defender

def main():
    results = {}

    # Auditoría de contraseñas
    results["passwords"] = collect_password_policies()

    # Auditoría de firewall y defender
    results["firewall_defender"] = collect_firewall_defender()

    # Guardar resultados
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("Resultados guardados en results.json")

if __name__ == "__main__":
    main()