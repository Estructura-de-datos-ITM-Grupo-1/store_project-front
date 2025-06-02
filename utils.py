import datetime
import re
from typing import Dict, Any, List
from models import ItemFactura, Factura 
import json 
from pathlib import Path 

CONFIG_FILE_PATH = Path("invoice_config.json")

_invoice_prefix = "FAC"
_invoice_suffix = ""
_current_invoice_number = 1

def _load_config():
    global _last_invoice_number, _invoice_prefix, _invoice_suffix
    if CONFIG_FILE_PATH.exists():
        try:
            with open(CONFIG_FILE_PATH, 'r') as f:
                config = json.load(f)
                _last_invoice_number = config.get("last_invoice_number", 0)
                _invoice_prefix = config.get("invoice_prefix", "FAC-")
                _invoice_suffix = config.get("invoice_suffix", "")
        except json.JSONDecodeError:
            
            _last_invoice_number = 0
            _invoice_prefix = "FAC-"
            _invoice_suffix = ""
            _save_config() 
    else:
        _save_config() 

def _save_config():
    config = {
        "last_invoice_number": _last_invoice_number,
        "invoice_prefix": _invoice_prefix,
        "invoice_suffix": _invoice_suffix
    }
    with open(CONFIG_FILE_PATH, 'w') as f:
        json.dump(config, f, indent=4)

_load_config()

def format_currency(amount: float) -> str:
    formatted = f"${amount:,.2f}".replace(",", ".")
    
    
    if formatted.endswith('.00'):
        formatted = formatted[:-3]  
    
    return formatted

def generate_invoice_number(preview: bool = False) -> str:   
    try:
        with open("data/last_invoice_number.txt", "r") as f:
            last_number = f.read().strip()
    except FileNotFoundError:
        last_number = "FAC-000001"  

    if not last_number.startswith("FAC-"):
        last_number = "FAC-000001"  
    number_part = last_number.split("-")[1]
    current_number = int(number_part)
    next_number = current_number + 1
    new_number = f"FAC-{next_number:06d}"
    
    if not preview:
        
        with open("data/last_invoice_number.txt", "w") as f:
            f.write(new_number)
    
    return new_number

def set_invoice_number_config(prefix: str, suffix: str):
    global _invoice_prefix, _invoice_suffix
    _invoice_prefix = prefix
    _invoice_suffix = suffix
    _save_config() 
    
def calculate_invoice_totals(items: List[ItemFactura]) -> Dict[str, float]:
    subtotal_base = 0.0
    descuento_total = 0.0
    iva_total = 0.0
    
    for item in items:
        subtotal_item_base = item.cantidad * item.precio_unitario
        subtotal_base += subtotal_item_base
        
        descuento_item = subtotal_item_base * (item.descuento / 100)
        descuento_total += descuento_item
        
        subtotal_despues_descuento = subtotal_item_base - descuento_item
        
        iva_item = subtotal_despues_descuento * (item.iva / 100)
        iva_total += iva_item
        
    total_factura = subtotal_base - descuento_total + iva_total
    
    return {
        'subtotal_base': subtotal_base,
        'descuento_total': descuento_total,
        'iva_total': iva_total,
        'total_factura': total_factura
    }