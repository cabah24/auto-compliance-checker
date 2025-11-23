# Auto-Compliance Windows


Herramienta para auditar configuración de seguridad Windows y generar un informe (PDF/HTML).


**Stack:** Python 3.9+, PowerShell (invocado desde Python), ReportLab, Jinja2.


### Objetivo
Recolectar evidencias de configuración en Windows (políticas de contraseña, firewall, defender, servicios, puertos), evaluarlas frente a reglas (CIS/NIST básicas) y generar un informe profesional.


### Cómo usar (local, entorno Windows)


1. Crear y activar un virtualenv:


```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
