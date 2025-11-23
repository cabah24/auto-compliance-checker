"""
Collector para auditoría de Windows Defender y Firewall.
Devuelve una lista de checks en formato JSON.
"""

import subprocess
from typing import List, Dict

def _run_ps(cmd: str) -> str:
    """Ejecuta un comando PowerShell y devuelve stdout."""
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
        capture_output=True, text=True
    )
    if completed.returncode != 0:
        return completed.stdout + "\n" + completed.stderr
    return completed.stdout

def collect_firewall_defender() -> List[Dict]:
    checks = []

    # 1. Defensor de Windows - protección en tiempo real
    cmd_defender = "(Get-MpComputerStatus).RealtimeProtectionEnabled"
    out_defender = _run_ps(cmd_defender).strip()
    status_def = "PASS" if out_defender.lower() == "true" else "FAIL"
    checks.append({
        "check": "Windows Defender real-time protection",
        "status": status_def,
        "value": out_defender,
        "expected": "True",
        "severity": "High" if status_def == "FAIL" else "Low",
        "evidence": out_defender,
        "fix": "Activar protección en tiempo real en Windows Defender."
    })

    # 2. Estado del Firewall (Domain, Private, Public)
    profiles = ["Domain", "Private", "Public"]
    for profile in profiles:
        cmd_fw = f"(Get-NetFirewallProfile -Profile {profile}).Enabled"
        out_fw = _run_ps(cmd_fw).strip()
        status_fw = "PASS" if out_fw.lower() == "true" else "FAIL"
        checks.append({
            "check": f"Windows Firewall {profile} profile",
            "status": status_fw,
            "value": out_fw,
            "expected": "True",
            "severity": "High" if status_fw == "FAIL" else "Low",
            "evidence": out_fw,
            "fix": f"Activar Windows Firewall para el perfil {profile}."
        })

    # 3. Opcional: listar reglas críticas abiertas (puertos Any)
    cmd_rules = "Get-NetFirewallRule | Where-Object { $_.Enabled -eq 'True' -and $_.Direction -eq 'Inbound' } | Select-Object DisplayName,Action,Direction,Profile"
    out_rules = _run_ps(cmd_rules)
    checks.append({
        "check": "Inbound firewall rules",
        "status": "INFO",
        "value": None,
        "expected": "No reglas inseguras",
        "severity": "Medium",
        "evidence": out_rules,
        "fix": "Revisar reglas de entrada que permitan tráfico no controlado."
    })

    return checks