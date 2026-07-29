"""
======================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
config.py

Autor:
Proyecto de estudio LangGraph + Ollama + IA Agéntica

Descripción
-----------
Este módulo centraliza TODA la configuración del proyecto.

Ningún otro archivo debería leer directamente variables de entorno.

Toda la configuración debe obtenerse desde:

CONFIG = get_settings()

Objetivos

✔ Centralizar la configuración.
✔ Facilitar el mantenimiento.
✔ Evitar código duplicado.
✔ Validar parámetros críticos.
✔ Preparar el proyecto para producción.

======================================================================
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ConfigDict


########################################################################
# Cargar automáticamente el archivo .env
########################################################################

ROOT_DIR = Path(__file__).resolve().parent

ENV_FILE = ROOT_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


########################################################################
# Clase principal de configuración
########################################################################

class Settings(BaseModel):
    """
    Configuración global del proyecto.

    Esta clase agrupa absolutamente todas las variables
    utilizadas por el sistema.
    """

    model_config = ConfigDict(extra="ignore")

    ####################################################################
    # Información general
    ####################################################################

    PROJECT_NAME: str = "LinkedIn AI MultiAgent"

    VERSION: str = "1.0.0"

    AUTHOR: str = "Proyecto LangGraph"

    ####################################################################
    # Ollama
    ####################################################################

    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434"
    )

    OLLAMA_MODEL: str = Field(
        default="llama3.1:8b"
    )

    OLLAMA_TEMPERATURE: float = 0.30

    OLLAMA_TOP_P: float = 0.90

    OLLAMA_CONTEXT_WINDOW: int = 8192

    ####################################################################
    # OpenAI
    ####################################################################

    OPENAI_API_KEY: str = Field(
        default=""
    )

    OPENAI_IMAGE_MODEL: str = "gpt-image-1"

    IMAGE_SIZE: str = "1024x1024"

    ####################################################################
    # LinkedIn
    ####################################################################

    LINKEDIN_CLIENT_ID: str = ""

    LINKEDIN_CLIENT_SECRET: str = ""

    LINKEDIN_REDIRECT_URI: str = ""

    LINKEDIN_ACCESS_TOKEN: str = ""

    ####################################################################
    # Investigación
    ####################################################################

    TAVILY_API_KEY: str = ""

    ####################################################################
    # Directorios
    ####################################################################

    BASE_DIR: Path = ROOT_DIR

    OUTPUT_DIR: Path = ROOT_DIR / "outputs"

    IMAGE_DIR: Path = ROOT_DIR / "outputs" / "images"

    POST_DIR: Path = ROOT_DIR / "outputs" / "posts"

    LOG_DIR: Path = ROOT_DIR / "logs"

    MEMORY_DIR: Path = ROOT_DIR / "memory"

    RESOURCE_DIR: Path = ROOT_DIR / "resources"

    ####################################################################
    # LangGraph
    ####################################################################

    MAX_ITERATIONS: int = 5

    MAX_RETRIES: int = 3

    ENABLE_MEMORY: bool = True

    ####################################################################
    # Editor
    ####################################################################

    MIN_EDITOR_SCORE: int = 54

    ####################################################################
    # LinkedIn
    ####################################################################

    MAX_POST_SIZE: int = 3000

    DEFAULT_LANGUAGE: str = "es"

    DEFAULT_COUNTRY: str = "Chile"

    ####################################################################
    # Logging
    ####################################################################

    LOG_LEVEL: str = "INFO"

    SAVE_INTERMEDIATE_ARTICLES: bool = True

    ####################################################################
    # Utilidades
    ####################################################################

    ENABLE_DEBUG: bool = False

    SAVE_GRAPH_IMAGE: bool = True

    EXPORT_JSON_STATE: bool = True

    ####################################################################
    # Métodos auxiliares
    ####################################################################

    def create_directories(self):
        """
        Crea automáticamente todos los directorios
        utilizados por el proyecto.
        """

        directories = [
            self.OUTPUT_DIR,
            self.IMAGE_DIR,
            self.POST_DIR,
            self.LOG_DIR,
            self.MEMORY_DIR,
            self.RESOURCE_DIR,
        ]

        for directory in directories:
            directory.mkdir(
                parents=True,
                exist_ok=True
            )

########################################################################
# Función Singleton
########################################################################

@lru_cache
def get_settings() -> Settings:
    """
    Devuelve una única instancia de la configuración.

    Gracias al decorador lru_cache(),
    toda la aplicación comparte exactamente
    el mismo objeto Settings.
    """

    settings = Settings(

        OLLAMA_BASE_URL=os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434"
        ),

        OLLAMA_MODEL=os.getenv(
            "OLLAMA_MODEL",
            "llama3.1:8b"
        ),

        OPENAI_API_KEY=os.getenv(
            "OPENAI_API_KEY",
            ""
        ),

        LINKEDIN_CLIENT_ID=os.getenv(
            "LINKEDIN_CLIENT_ID",
            ""
        ),

        LINKEDIN_CLIENT_SECRET=os.getenv(
            "LINKEDIN_CLIENT_SECRET",
            ""
        ),

        LINKEDIN_REDIRECT_URI=os.getenv(
            "LINKEDIN_REDIRECT_URI",
            ""
        ),

        LINKEDIN_ACCESS_TOKEN=os.getenv(
            "LINKEDIN_ACCESS_TOKEN",
            ""
        ),

        TAVILY_API_KEY=os.getenv(
            "TAVILY_API_KEY",
            ""
        ),
    )

    settings.create_directories()

    return settings


########################################################################
# Instancia global
########################################################################

CONFIG = get_settings()
