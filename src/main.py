# ============================================
# PROYECTO: Empresa de jardineria 
# ============================================
# Semana 01 - Bootcamp FastAPI Zero to Hero
#
# En este proyecto implementarás una API de saludos
# que demuestra el uso de:
# - FastAPI
# - Type hints
# - Path parameters
# - Query parameters
# - Documentación automática
# ============================================
from fastapi import FastAPI, HTTPException

# ============================================
# DATOS DE CONFIGURACIÓN (Dominio: Jardinería)
# ============================================

GREETINGS: dict[str, str] = {
    "es": "¡Bienvenido a Jardines Verdes, {name}!",
    "en": "Welcome to Green Gardens, {name}!",
    "fr": "Bienvenue aux Jardins Verts, {name}!",
}

# Simulación de base de datos de servicios
SERVICES_DB = {
    "podado": {"name": "Podado de Césped", "price": 25.0, "time_est": "1h"},
    "riego": {"name": "Instalación de Riego", "price": 150.0, "time_est": "4h"},
    "paisajismo": {"name": "Diseño Paisajista", "price": 500.0, "time_est": "2 days"}
}

# ============================================
# TODO 1: INSTANCIA DE FASTAPI
# ============================================
app = FastAPI(
    title="Gardening Company API",
    description="API para la gestión de servicios de jardinería, clientes y horarios.",
    version="1.0.0"
)

# ============================================
# TODO 2: ENDPOINT RAÍZ (RF-01)
# ============================================
@app.get("/")
async def root() -> dict[str, str | list[str]]:
    """Información básica de la API de Jardinería."""
    return {
        "name": "Jardines Verdes API",
        "version": "1.0.0",
        "domain": "empresa-de-jardineria",
        "endpoints": ["/docs", "/health", "/client/{name}", "/services/{id}/info"]
    }

# ============================================
# TODO 3: BIENVENIDA PERSONALIZADA (RF-02)
# ============================================
@app.get("/client/{name}")
async def welcome_client(name: str, language: str = "es") -> dict[str, str]:
    """Saluda al cliente en el idioma seleccionado."""
    template = GREETINGS.get(language, GREETINGS["es"])
    return {
        "message": template.format(name=name),
        "language": language
    }

# ============================================
# TODO 4: INFORMACIÓN DE ENTIDAD (RF-03)
# ============================================
@app.get("/services/{service_id}/info")
async def get_service_info(service_id: str, detail_level: str = "basic") -> dict:
    """Obtiene información de un servicio (ej: podado, riego, paisajismo)."""
    service = SERVICES_DB.get(service_id.lower())
    
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    if detail_level == "full":
        return {"id": service_id, **service, "availability": "Mon-Fri"}
    
    return {"id": service_id, "name": service["name"], "price": service["price"]}

# ============================================
# TODO 5: SERVICIO SEGÚN HORARIO (RF-04)
# ============================================
def get_garden_schedule(hour: int) -> tuple[str, list[str]]:
    """Determina la actividad de la empresa según la hora."""
    if 6 <= hour < 12:
        return ("Turno Mañana - Mantenimiento en exteriores", ["podado", "siembra"])
    elif 12 <= hour < 18:
        return ("Turno Tarde - Atención técnica y diseño", ["consultas", "paisajismo"])
    else:
        return ("Cerrado - Solo emergencias de riego", ["emergencias"])

@app.get("/service/schedule")
async def service_schedule(hour: int) -> dict:
    """Consulta la disponibilidad de servicios según la hora (0-23)."""
    if not (0 <= hour <= 23):
        raise HTTPException(status_code=400, detail="La hora debe estar entre 0 y 23")
    
    message, available = get_garden_schedule(hour)
    return {
        "hour": hour,
        "message": message,
        "available_services": available
    }

# ============================================
# TODO 6: HEALTH CHECK (RF-05)
# ============================================
@app.get("/health")
async def health_check() -> dict[str, str]:
    """Verifica el estado del sistema."""
    return {
        "status": "healthy",
        "domain": "jardineria",
        "workers_online": "active"
    }

# ============================================
# VERIFICACIÓN
# ============================================
# Una vez completados todos los TODOs:
#
# 1. Ejecutar:
#    docker compose up --build
#
# 2. Probar en el navegador:
#    http://localhost:8000/docs
#
# 3. Verificar cada endpoint:
#    - GET /
#    - GET /greet/Carlos
#    - GET /greet/Carlos?language=en
#    - GET /greet/García/formal?title=Dr.
#    - GET /greet/Ana/time-based?hour=10
#    - GET /health
# ============================================