import json
import random
import uuid
import datetime
import re
from typing import Any, Dict
from modifiers import apply_modification, apply_header_modification, apply_body_modification
from config_loader import ConfigLoader


class RuleEngine:
    def __init__(self, rules_dir: str):
        self.config_loader = ConfigLoader(rules_dir)
    
    def process_request(self, request):
        """Procesa una solicitud entrante contra las reglas generales"""
        # Buscar regla para interceptar request
        rule = self.config_loader.get_rule(request.path, request.method, "Request")
        if rule:
            # Aplicar modificación si existe regla
            return apply_modification(request, rule)
        return False
    
    def process_response(self, response, original_request=None):
        """Procesa una respuesta saliente contra las reglas generales"""
        # Buscar regla para interceptar response
        if original_request:
            rule = self.config_loader.get_rule(original_request.path, original_request.method, "Response")
            if rule:
                # Aplicar modificación si existe regla
                return apply_modification(response, rule)
        return False
    
    def process_request_headers(self, request):
        """Procesa los headers de una solicitud entrante"""
        # Buscar regla específica para headers de request
        rule = self.config_loader.get_rule(request.path, request.method, "RequestHeader")
        if rule:
            return apply_header_modification(request, rule)
        return False
    
    def process_request_body(self, request):
        """Procesa el body de una solicitud entrante"""
        # Buscar regla específica para body de request
        rule = self.config_loader.get_rule(request.path, request.method, "RequestBody")
        if rule:
            return apply_body_modification(request, rule)
        return False
    
    def process_response_headers(self, response, original_request=None):
        """Procesa los headers de una respuesta saliente"""
        if original_request:
            # Buscar regla específica para headers de response
            rule = self.config_loader.get_rule(original_request.path, original_request.method, "ResponseHeader")
            if rule:
                return apply_header_modification(response, rule)
        return False
    
    def process_response_body(self, response, original_request=None):
        """Procesa el body de una respuesta saliente"""
        if original_request:
            # Buscar regla específica para body de response
            rule = self.config_loader.get_rule(original_request.path, original_request.method, "ResponseBody")
            if rule:
                return apply_body_modification(response, rule)
        return False