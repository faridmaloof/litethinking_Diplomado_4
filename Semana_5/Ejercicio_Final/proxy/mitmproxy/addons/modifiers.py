import json
import random
import uuid
import datetime
import base64
import re
import time
from typing import Any, Dict, Union


def evaluate_dynamic_functions(text: str) -> str:
    """
    Evalúa las funciones dinámicas en un texto entre < >
    """
    def replace_match(match):
        function_call = match.group(1)  # Group 1 captures what's inside < >
        try:
            # Parse the function name and arguments properly
            if '(' in function_call and ')' in function_call:
                # Find the position of the opening parenthesis
                paren_pos = function_call.find('(')
                func_name = function_call[:paren_pos]
                args_str = function_call[paren_pos+1:function_call.rfind(')')]
            else:
                func_name = function_call
                args_str = ""
                
            if func_name == 'Aleatorio':
                # Eliminar espacios en blanco
                args_str = args_str.strip()
                
                # Verificar si es una lista (comienza con [ y termina con ])
                if args_str.startswith('[') and args_str.endswith(']'):
                    # Es una lista, extraer elementos
                    list_content = args_str[1:-1]  # Remover [ y ]
                    
                    # Separar elementos por coma, manejando correctamente cadenas con comillas
                    elements = []
                    current_element = ""
                    inside_quotes = False
                    quote_char = None
                    
                    i = 0
                    while i < len(list_content):
                        char = list_content[i]
                        
                        # Verificar si estamos dentro de comillas
                        if char in ['"', "'"] and (i == 0 or i > 0 and list_content[i-1] != '\\'):
                            if not inside_quotes:
                                inside_quotes = True
                                quote_char = char
                            elif char == quote_char:
                                inside_quotes = False
                                
                        # Si estamos fuera de comillas y encontramos una coma, es un separador
                        if char == ',' and not inside_quotes:
                            elements.append(current_element.strip())
                            current_element = ""
                            i += 1
                            continue
                        
                        current_element += char
                        i += 1
                    
                    # Agregar el último elemento
                    if current_element.strip():
                        elements.append(current_element.strip())
                    
                    # Eliminar comillas de los elementos si están presentes
                    cleaned_elements = []
                    for elem in elements:
                        elem = elem.strip()
                        if len(elem) >= 2 and (((elem.startswith("'") and elem.endswith("'")) or (elem.startswith('"') and elem.endswith('"')))):
                            elem = elem[1:-1]  # Remover comillas exteriores
                        cleaned_elements.append(elem)
                    
                    return str(random.choice(cleaned_elements))
                else:
                    # Debe ser un rango numérico, ejemplo: "10, 15"
                    # Dividir por comas y convertir a enteros
                    parts = [x.strip() for x in args_str.split(',')]
                    if len(parts) >= 2:
                        min_val = int(parts[0])
                        max_val = int(parts[1])
                        return str(random.randint(min_val, max_val))
                    else:
                        # Si solo hay un número, devolverlo
                        return str(int(parts[0]))
            elif func_name == 'UUID':
                return str(uuid.uuid4())
            elif func_name == 'FechaActual':
                format_str = args_str.strip('"\'')
                return datetime.datetime.now().strftime(format_str)
            elif func_name == 'TextoAleatorio':
                length = int(args_str)
                chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                return ''.join(random.choice(chars) for _ in range(length))
            elif func_name == 'Base64':
                text_to_encode = args_str.strip('"\'')
                return base64.b64encode(text_to_encode.encode()).decode()
            elif func_name == 'Delay':
                delay_ms = int(args_str)
                time.sleep(delay_ms / 1000.0)  # Convertir a segundos
                return str(delay_ms)  # Devolver el valor como string
            elif func_name == 'Error':
                # Para esta función, simplemente devolvemos el código de error
                # El manejo real del error se hará en otro lugar si es necesario
                error_code = int(args_str)
                return str(error_code)
        except Exception as e:
            print(f"[ERROR] Error evaluando función '{function_call}': {e}")
            return match.group(0)  # Devolver la cadena original si hay error
        
        # Si no coincide ninguna función conocida, devolver la cadena original
        return match.group(0)
    
    # Buscar y reemplazar todas las funciones dinámicas en el texto
    pattern = r'<([^<>]+)>'
    result = re.sub(pattern, replace_match, text)
    return result


def deep_merge(base_dict: Dict, override_dict: Dict) -> Dict:
    """
    Realiza un merge profundo entre dos diccionarios
    """
    result = base_dict.copy()
    
    for key, value in override_dict.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def apply_modification(message: Any, rule: Dict) -> bool:
    """
    Aplica modificación completa o parcial a un mensaje (request o response)
    """
    try:
        modification_type = rule.get('Tipo_modificacion', '').lower()
        data = rule.get('Datos', {})
        
        # Verificar si es una respuesta y hay un código de error en los datos
        if hasattr(message, 'status_code') and 'code' in data:
            # Si el campo 'code' contiene un código de error, establecerlo
            if isinstance(data['code'], int) or (isinstance(data['code'], str) and str(data['code']).isdigit()):
                error_code = int(data['code'])
                if 400 <= error_code <= 599:  # Es un código de error HTTP
                    message.status_code = error_code
        
        # Si es una respuesta HTTP o solicitud con body
        if hasattr(message, 'text') and message.text:
            original_data = {}
            
            # Intentar parsear el body como JSON si es posible
            try:
                original_data = json.loads(message.text)
            except json.JSONDecodeError:
                # Si no es JSON, dejar original_data como diccionario vacío o como string
                original_data = {}
            
            if modification_type == 'completo':
                # Reemplazar completamente el body con los datos de la regla
                processed_data = process_dynamic_values(data)
                message.text = json.dumps(processed_data)
            elif modification_type == 'parcial':
                # Hacer merge de los datos de la regla con los originales
                processed_data = process_dynamic_values(data)
                
                # Si original_data es un diccionario, hacer merge
                if isinstance(original_data, dict):
                    merged_data = deep_merge(original_data, processed_data)
                    message.text = json.dumps(merged_data)
                else:
                    # Si no es un diccionario, usar los datos procesados directamente
                    message.text = json.dumps(processed_data)
            
            # Actualizar Content-Length si es una respuesta HTTP
            if hasattr(message, 'headers'):
                message.headers['Content-Length'] = str(len(message.text.encode()))
            
            return True
        elif modification_type == 'completo':
            # Si no hay body existente pero se quiere una modificación completa
            processed_data = process_dynamic_values(data)
            message.text = json.dumps(processed_data)
            
            # Actualizar Content-Length si es una respuesta HTTP
            if hasattr(message, 'headers'):
                message.headers['Content-Length'] = str(len(message.text.encode()))
            
            # Si es una respuesta y tenemos un código de estado, establecerlo
            if hasattr(message, 'status_code') and 'code' in processed_data:
                if isinstance(processed_data['code'], int) or (isinstance(processed_data['code'], str) and str(processed_data['code']).isdigit()):
                    status_code = int(processed_data['code'])
                    message.status_code = status_code
            
            return True
        else:
            # No hay body existente y no se requiere modificación completa
            return False
            
    except Exception as e:
        print(f"[ERROR] Error aplicando modificación: {e}")
        return False


def process_dynamic_values(obj: Any) -> Any:
    """
    Procesa recursivamente un objeto buscando valores dinámicos
    """
    if isinstance(obj, str):
        # Si es string, evaluar posibles funciones dinámicas
        return evaluate_dynamic_functions(obj)
    elif isinstance(obj, dict):
        # Si es diccionario, procesar recursivamente cada valor
        return {key: process_dynamic_values(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        # Si es lista, procesar recursivamente cada elemento
        return [process_dynamic_values(item) for item in obj]
    else:
        # Otros tipos, devolver tal cual
        return obj


def apply_header_modification(message: Any, rule: Dict) -> bool:
    """
    Aplica modificaciones específicas a los headers de un mensaje (request o response)
    """
    try:
        modification_type = rule.get('Tipo_modificacion', '').lower()
        headers_data = rule.get('Headers', {})
        
        if not headers_data:
            return False
            
        # Procesar valores dinámicos en los headers
        processed_headers = process_dynamic_values(headers_data)
        
        # Aplicar los headers según el tipo de modificación
        if modification_type == 'completo':
            # Reemplazar completamente los headers
            for key, value in processed_headers.items():
                message.headers[key] = str(value)
        elif modification_type == 'parcial':
            # Agregar o actualizar headers específicos
            for key, value in processed_headers.items():
                message.headers[key] = str(value)
        elif modification_type == 'eliminar':
            # Eliminar headers específicos
            for key in processed_headers:
                if key in message.headers:
                    del message.headers[key]
        
        return True
    except Exception as e:
        print(f"[ERROR] Error aplicando modificación de headers: {e}")
        return False


def apply_body_modification(message: Any, rule: Dict) -> bool:
    """
    Aplica modificaciones específicas al body de un mensaje (request o response)
    """
    try:
        modification_type = rule.get('Tipo_modificacion', '').lower()
        body_data = rule.get('Body', {})
        
        if not body_data:
            return False
            
        # Procesar valores dinámicos en el body
        processed_body = process_dynamic_values(body_data)
        
        # Si el mensaje tiene body
        if hasattr(message, 'text') and message.text:
            original_body = {}
            
            # Intentar parsear el body como JSON si es posible
            try:
                original_body = json.loads(message.text)
            except json.JSONDecodeError:
                # Si no es JSON, dejar original_body como diccionario vacío
                original_body = {}
            
            if modification_type == 'completo':
                # Reemplazar completamente el body
                message.text = json.dumps(processed_body)
            elif modification_type == 'parcial':
                # Hacer merge de los datos del body con los originales
                if isinstance(original_body, dict):
                    merged_body = deep_merge(original_body, processed_body)
                    message.text = json.dumps(merged_body)
                else:
                    # Si no es un diccionario, usar los datos procesados directamente
                    message.text = json.dumps(processed_body)
            elif modification_type == 'agregar':
                # Agregar datos al body existente
                if isinstance(original_body, dict):
                    merged_body = deep_merge(original_body, processed_body)
                    message.text = json.dumps(merged_body)
                else:
                    # Si no es un diccionario, reemplazarlo
                    message.text = json.dumps(processed_body)
        else:
            # Si no hay body existente, crear uno
            message.text = json.dumps(processed_body)
        
        # Actualizar Content-Length si es una respuesta HTTP
        if hasattr(message, 'headers'):
            message.headers['Content-Length'] = str(len(message.text.encode()))
        
        return True
    except Exception as e:
        print(f"[ERROR] Error aplicando modificación de body: {e}")
        return False