"""
Carga reglas estáticas (por ahora desde standards/cis_windows.json)
"""
from importlib.resources import path
import json
from pathlib import Path




def load_standards(path: str = None):
    p = Path(path or Path(__file__).parent.parent.parent / 'standards' / 'cis_windows.json')
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)