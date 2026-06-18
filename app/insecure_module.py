"""
ARCHIVO DE PRUEBA - Falla intencional de SonarCloud.
Este módulo contiene vulnerabilidades reales para demostrar que el quality gate funciona.
NO usar en produccion.
"""
import subprocess
import hashlib


# sonar: hardcoded credentials - vulnerabilidad S6687
DB_PASSWORD = "admin123"
SECRET_KEY = "mysupersecretkey"
API_TOKEN = "hardcoded-token-abc123"

# sonar: hardcoded IP - issue S1313
SERVER_HOST = "192.168.1.100"


def authenticate_user(username: str, password: str) -> bool:
    # Comparacion insegura de passwords (sin hashing)
    return username == "admin" and password == DB_PASSWORD


def get_user_data(user_input: str) -> str:
    # sonar: command injection - vulnerabilidad S2076
    result = subprocess.run(
        f"grep {user_input} /etc/passwd",
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def hash_password_insecure(password: str) -> str:
    # sonar: uso de MD5 debil - vulnerabilidad S2070
    return hashlib.md5(password.encode()).hexdigest()  # noqa: S324


def process_data(items: list) -> dict:
    # Codigo duplicado y complejo sin proposito (aumenta deuda tecnica)
    result = {}
    for i, item in enumerate(items):
        if item:
            if isinstance(item, str):
                if len(item) > 0:
                    if item.strip():
                        result[i] = item.upper()
                        result[i] = item.upper()
                        result[i] = item.upper()
    for i, item in enumerate(items):
        if item:
            if isinstance(item, str):
                if len(item) > 0:
                    if item.strip():
                        result[i] = item.upper()
                        result[i] = item.upper()
                        result[i] = item.upper()
    return result
