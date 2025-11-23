"""
Collector para políticas de contraseña en Windows usando PowerShell.
Devuelve una lista de checks en formato JSON.
"""
import subprocess
import json
import re
from typing import List, Dict   




def _run_ps(cmd: str) -> str:
    """Ejecuta un comando PowerShell y devuelve stdout (texto)."""
    completed = subprocess.run([
    "powershell", "-NoProfile", "-NonInteractive", "-Command", cmd
    ], capture_output=True, text=True)
    if completed.returncode != 0:
    # Devolver stderr para facilitar debug
        return completed.stdout + "\n" + completed.stderr
    return completed.stdout




def _parse_net_accounts(output: str) -> Dict[str, str]:
# output habitual de `net accounts` tiene líneas como: "Minimum password length 7"
    data = {}
    for line in output.splitlines():
        if not line.strip():
            continue
    parts = re.split(r"\s{2,}", line.strip())
    if len(parts) >= 2:
        key = parts[0].strip()
        val = parts[1].strip()
        data[key] = val
    return data




def collect_password_policies() -> List[Dict]:
    """Recoge políticas de contraseña y devuelve una lista de checks.


    Cada check tiene: check, status (PASS/FAIL/INFO), value, expected, severity, evidence, fix
    """
    cmd = "net accounts"
    out = _run_ps(cmd)
    parsed = _parse_net_accounts(out)


    # Cargar reglas estándar sencillas (hardcoded por ahora)
    standards = {
    'Minimum password length': 12,
    'Maximum password age (days)': 90,
    'Lockout threshold': 5 # intentos fallidos
    }


    checks = []


    # Minimum password length
    minlen_raw = parsed.get('Minimum password length') or parsed.get('Minimum password length:')
    try:
        minlen = int(re.search(r"\d+", minlen_raw).group()) if minlen_raw else None
    except Exception:
        minlen = None


    if minlen is None:
        checks.append({
            'check': 'Minimum password length',
            'status': 'INFO',
            'value': None,
            'expected': standards['Minimum password length'],
            'severity': 'Medium',
            'evidence': out,
            'fix': 'Configurar la longitud mínima de contraseñas usando GPO o herramientas locales (net accounts / password policy).'
        })
    else:
        status = 'PASS' if minlen >= standards['Minimum password length'] else 'FAIL'
        checks.append({
            'check': 'Minimum password length',
            'status': status,
            'value': minlen,
            'expected': standards['Minimum password length'],
            'severity': 'High' if status == 'FAIL' else 'Low',
            'evidence': f'Output: {minlen_raw}',
            'fix': 'Establecer MinimumPasswordLength >= 12 en la política de contraseñas (GPO).'
        })


    # Maximum password age
    max_age_raw = parsed.get('Maximum password age (days)') or parsed.get('Maximum password age')
    try:
        max_age = int(re.search(r"\d+", max_age_raw).group()) if max_age_raw else None
    except Exception:
        max_age = None


    if max_age is None:
        checks.append({
        'check': 'Maximum password age (days)',
        'status': 'INFO',
        'value': None,
        'expected': standards['Maximum password age (days)'],
        'severity': 'Medium',
        'evidence': out,
        'fix': 'Configurar expiración máxima de contraseñas mediante GPO o net accounts.'
        })
    else:
        status = 'PASS' if max_age <= standards['Maximum password age (days)'] else 'FAIL'
        checks.append({
        'check': 'Maximum password age (days)',
        'status': status,
        'value': max_age,
        'expected': standards['Maximum password age (days)'],
        'severity': 'Medium' if status == 'FAIL' else 'Low',
        'evidence': f'Output: {max_age_raw}',
        'fix': 'Reducir MaximumPasswordAge a 90 días o menos en la política de contraseñas.'
        })


    # Lockout threshold (fallos)
    lockout_raw = parsed.get('Lockout threshold') or parsed.get('Lockout threshold (bad login attempts)')
    try:
        lockout = int(re.search(r"\d+", lockout_raw).group()) if lockout_raw else None
    except Exception:
     lockout = None


    if lockout is None:
        checks.append({
        'check': 'Account lockout threshold',
        'status': 'INFO',
        'value': None,
        'expected': standards['Lockout threshold'],
        'severity': 'Medium',
        'evidence': out,
        'fix': 'Establecer threshold de bloqueo de cuentas mediante GPO.'
        })
    else:
        status = 'PASS' if lockout <= standards['Lockout threshold'] else 'FAIL'
        checks.append({
        'check': 'Account lockout threshold',
        'status': status,
        'value': lockout,
        'expected': standards['Lockout threshold'],
        'severity': 'High' if status == 'FAIL' else 'Low',
        'evidence': f'Output: {lockout_raw}',
        'fix': 'Configurar Account lockout threshold = 5 ó menos.'
        })


    # Añadir raw output como evidencia adicional
    checks.append({
        'check': 'Raw net accounts output',
        'status': 'INFO',
        'value': None,
        'expected': None,
        'severity': 'Low',
        'evidence': out,
        'fix': ''
    })


    return checks