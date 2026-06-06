#!/usr/bin/env python3
"""
Script de validación para el Ejercicio Final de QA
Valida que todos los componentes estén correctamente configurados
"""

import os
import sys
import json
from pathlib import Path

def validate_directory_structure():
    """Valida la estructura de directorios requerida"""
    print("🔍 Validando estructura de directorios...")
    
    required_paths = [
        "proxy/Dockerfile",
        "proxy/mitmproxy/addons/interceptor.py",
        "proxy/mitmproxy/addons/config_loader.py", 
        "proxy/mitmproxy/addons/rule_engine.py",
        "proxy/mitmproxy/addons/modifiers.py",
        "proxy/mitmproxy/config/rules/example_api_a.json",
        "proxy/mitmproxy/config/rules/example_api_b.json",
        "proxy/mitmproxy/config/rules/README.md",
        "security/zap/Dockerfile",
        "security/sonarqube/Dockerfile", 
        "performance/k6/Dockerfile",
        "chaos/toxiproxy/Dockerfile",
        "secrets/README.md",
        "docs/architecture.md",
        "docs/troubleshooting.md",
        "docs/examples/advanced_security_testing.md",
        ".env.example",
        ".gitignore",
        "docker-compose.yml",
        "README.md"
    ]
    
    missing_paths = []
    for path in required_paths:
        if not Path(path).exists():
            missing_paths.append(path)
    
    if missing_paths:
        print(f"❌ Directorios/archivos faltantes: {missing_paths}")
        return False
    else:
        print("✅ Todos los directorios y archivos requeridos están presentes")
        return True

def validate_json_files():
    """Valida que los archivos JSON tengan sintaxis correcta"""
    print("\n🔍 Validando archivos JSON...")
    
    json_files = [
        "proxy/mitmproxy/config/rules/example_api_a.json",
        "proxy/mitmproxy/config/rules/example_api_b.json",
        "chaos/toxiproxy/config/example_proxy.json",
        "security/sonarqube/quality-gates/default.json"
    ]
    
    invalid_json = []
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except Exception as e:
            invalid_json.append((file_path, str(e)))
    
    if invalid_json:
        print(f"❌ Archivos JSON inválidos: {invalid_json}")
        return False
    else:
        print("✅ Todos los archivos JSON tienen sintaxis válida")
        return True

def validate_docker_compose():
    """Valida el archivo docker-compose.yml"""
    print("\n🔍 Validando docker-compose.yml...")
    
    try:
        with open("docker-compose.yml", 'r') as f:
            content = f.read()
        
        required_services = ['proxy', 'zap', 'k6', 'toxiproxy']
        missing_services = []
        
        for service in required_services:
            if f"{service}:" not in content:
                missing_services.append(service)
        
        if missing_services:
            print(f"❌ Servicios faltantes en docker-compose.yml: {missing_services}")
            return False
        
        # Verificar que todos los builds apunten a directorios existentes
        build_dirs = [
            "./proxy", "./security/zap", "./performance/k6", "./chaos/toxiproxy"
        ]
        missing_build_dirs = []
        
        for build_dir in build_dirs:
            if not Path(build_dir).exists():
                missing_build_dirs.append(build_dir)
        
        if missing_build_dirs:
            print(f"❌ Directorios de build faltantes: {missing_build_dirs}")
            return False
        
        print("✅ docker-compose.yml es válido y contiene todos los servicios requeridos")
        return True
    except Exception as e:
        print(f"❌ Error validando docker-compose.yml: {e}")
        return False

def validate_python_code():
    """Valida la sintaxis del código Python"""
    print("\n🔍 Validando código Python...")
    
    python_files = [
        "proxy/mitmproxy/addons/interceptor.py",
        "proxy/mitmproxy/addons/config_loader.py",
        "proxy/mitmproxy/addons/rule_engine.py", 
        "proxy/mitmproxy/addons/modifiers.py"
    ]
    
    invalid_python = []
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            compile(source, file_path, 'exec')
        except SyntaxError as e:
            invalid_python.append((file_path, str(e)))
        except Exception as e:
            invalid_python.append((file_path, str(e)))
    
    if invalid_python:
        print(f"❌ Archivos Python con errores: {invalid_python}")
        return False
    else:
        print("✅ Todo el código Python tiene sintaxis válida")
        return True

def validate_documentation():
    """Valida que la documentación esté presente"""
    print("\n🔍 Validando documentación...")
    
    doc_files = [
        "README.md",
        "docs/architecture.md", 
        "docs/troubleshooting.md",
        "proxy/mitmproxy/config/rules/README.md",
        "secrets/README.md"
    ]
    
    missing_docs = []
    for doc in doc_files:
        if not Path(doc).exists():
            missing_docs.append(doc)
    
    if missing_docs:
        print(f"❌ Documentación faltante: {missing_docs}")
        return False
    else:
        print("✅ Toda la documentación requerida está presente")
        return True

def main():
    """Función principal de validación"""
    print("🧪 Iniciando validación del Ejercicio Final de QA...")
    print("="*60)
    
    validations = [
        validate_directory_structure,
        validate_json_files,
        validate_docker_compose,
        validate_python_code,
        validate_documentation
    ]
    
    results = []
    for validation in validations:
        results.append(validation())
    
    print("\n" + "="*60)
    print("📊 Resumen de Validación:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (validation, result) in enumerate(zip(validations, results)):
        status = "✅" if result else "❌"
        print(f"{status} {validation.__name__}")
    
    print(f"\n✅ {passed}/{total} validaciones pasaron")
    
    if all(results):
        print("\n🎉 ¡La plataforma de pruebas QA está completamente configurada!")
        print("\n🚀 Para iniciar la plataforma:")
        print("   docker compose up --build")
        print("\n📋 Para probar las reglas de interceptación:")
        print("   1. Edita archivos en proxy/mitmproxy/config/rules/")
        print("   2. Las reglas se recargan automáticamente (hot-reload)")
        print("   3. Configura tu navegador con proxy localhost:8080")
        return 0
    else:
        print("\n💥 Algunas validaciones fallaron. Por favor revisa los errores anteriores.")
        return 1

if __name__ == "__main__":
    sys.exit(main())