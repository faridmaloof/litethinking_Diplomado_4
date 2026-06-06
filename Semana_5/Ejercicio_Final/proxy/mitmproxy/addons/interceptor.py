from mitmproxy import http
import json
import os
import threading
from typing import Dict, Tuple, Any
from config_loader import ConfigLoader
from rule_engine import RuleEngine

class Interceptor:
    def __init__(self):
        rules_dir = '/home/mitmproxy/config/rules'
        self.rule_engine = RuleEngine(rules_dir)
    
    def request(self, flow: http.HTTPFlow):
        """Intercepta y modifica requests"""
        try:
            # Aplicar reglas de tipo Request
            modified = self.rule_engine.process_request(flow.request)
            if modified:
                flow.metadata["rule_applied"] = True
                
            # Aplicar reglas específicas para headers
            header_modified = self.rule_engine.process_request_headers(flow.request)
            if header_modified:
                flow.metadata["header_rule_applied"] = True
                
            # Aplicar reglas específicas para body
            body_modified = self.rule_engine.process_request_body(flow.request)
            if body_modified:
                flow.metadata["body_rule_applied"] = True
                
        except Exception as e:
            print(f"[ERROR] Error processing request: {e}")
    
    def response(self, flow: http.HTTPFlow):
        """Intercepta y modifica responses"""
        try:
            # Aplicar reglas de tipo Response
            modified = self.rule_engine.process_response(flow.response, flow.request)
            if modified:
                flow.metadata["rule_applied"] = True
                
            # Aplicar reglas específicas para headers de respuesta
            header_modified = self.rule_engine.process_response_headers(flow.response, flow.request)
            if header_modified:
                flow.metadata["header_rule_applied"] = True
                
            # Aplicar reglas específicas para body de respuesta
            body_modified = self.rule_engine.process_response_body(flow.response, flow.request)
            if body_modified:
                flow.metadata["body_rule_applied"] = True
                
        except Exception as e:
            print(f"[ERROR] Error processing response: {e}")

addons = [Interceptor()]