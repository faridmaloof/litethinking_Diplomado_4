import json
import os
from typing import Dict, Any

class ConfigLoader:
    def __init__(self, rules_dir: str):
        self.rules_dir = rules_dir
        self.rules = self.load_rules()

    def load_rules(self) -> Dict[str, Dict]:
        """Carga todas las reglas desde el directorio de reglas"""
        rules = {}
        if not os.path.exists(self.rules_dir):
            print(f"[WARNING] Rules directory does not exist: {self.rules_dir}")
            return rules

        for filename in os.listdir(self.rules_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.rules_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        # Merge all rules into a single dictionary
                        rules.update(data)
                except Exception as e:
                    print(f"[ERROR] Failed to load rule file {file_path}: {e}")
        return rules

    def get_rule(self, path: str, method: str, rule_type: str) -> Dict[str, Any]:
        """Obtiene una regla específica por ruta, método y tipo"""
        for rule_name, rule_data in self.rules.items():
            if (rule_data.get("Ruta") == path and 
                rule_data.get("Metodo").upper() == method.upper() and 
                rule_data.get("Tipo_intercepcion") == rule_type):
                return rule_data
        return {}