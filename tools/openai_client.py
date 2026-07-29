"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
tools/openai_client.py

Descripción
-----------

Cliente centralizado para OpenAI.

Responsabilidades

✓ Generación de imágenes con DALL·E 3
✓ Descarga automática de imágenes
✓ Almacenamiento local
✓ Validación de API Key
✓ Manejo de errores
✓ Registro de actividad

NOTA

Este es el único componente del proyecto que requiere conexión
a Internet y una API Key de OpenAI.

El resto del sistema funciona completamente en local utilizando
Ollama + llama3.1:8b.

==============================================================================

"""

from __future__ import annotations

from pathlib import Path
import requests

from openai import OpenAI

from config import CONFIG
from tools.logger import LOG
from tools.filesystem import FILES


##########################################################################
# Cliente OpenAI
##########################################################################

class OpenAIClient:

    """
    Cliente centralizado para OpenAI.
    """

    ######################################################################

    def __init__(self):

        self.client = OpenAI(
            api_key=CONFIG.OPENAI_API_KEY
        )

    ######################################################################
    # Verificar API Key
    ######################################################################

    def health(self) -> bool:

        try:

            self.client.models.list()

            return True

        except Exception:

            return False

    ######################################################################
    # Generar imagen
    ######################################################################

    def generate_image(

        self,

        prompt: str,

        size: str = "1024x1024",

        quality: str = "hd",

        style: str = "natural",

    ) -> Path:

        """
        Genera una imagen utilizando DALL·E 3.
        """

        LOG.info(
            "Solicitando imagen a OpenAI..."
        )

        response = self.client.images.generate(

            model="dall-e-3",

            prompt=prompt,

            size=size,

            quality=quality,

            style=style,

            n=1,

        )

        image_url = response.data[0].url

        destination = FILES.new_image_filename()

        self.download_image(

            image_url,

            destination,

        )

        LOG.info(
            f"Imagen almacenada en {destination}"
        )

        return destination

    ######################################################################
    # Descargar imagen
    ######################################################################

    def download_image(

        self,

        url: str,

        destination: Path,

    ):

        response = requests.get(

            url,

            timeout=120,

        )

        response.raise_for_status()

        destination.write_bytes(

            response.content

        )

    ######################################################################
    # Información
    ######################################################################

    def info(self):

        return {

            "provider": "OpenAI",

            "image_model": "dall-e-3",

        }


##########################################################################
# Instancia Global
##########################################################################

OPENAI = OpenAIClient()
