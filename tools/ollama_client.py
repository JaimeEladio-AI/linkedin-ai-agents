"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
tools/ollama_client.py

Descripción
-----------

Cliente centralizado para Ollama.

Responsabilidades

✓ Conectar con Ollama
✓ Administrar ChatOllama
✓ Manejar errores
✓ Reintentos automáticos
✓ Invocaciones simples
✓ Invocaciones con System + Human Prompt
✓ Salidas JSON
✓ Registro de actividad

Compatible con

    Ollama
    llama3.1:8b
    LangChain
    LangGraph
    Google Colab

==============================================================================

"""

from __future__ import annotations

import json
import time

from typing import Optional
from typing import Dict
from typing import Any

from langchain_ollama import ChatOllama
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from config import CONFIG
from tools.logger import LOG


##########################################################################
# Cliente Ollama
##########################################################################

class OllamaClient:

    """
    Cliente centralizado para Ollama.
    """

    ######################################################################

    def __init__(self):

        self.model = CONFIG.OLLAMA_MODEL

        self.base_url = CONFIG.OLLAMA_BASE_URL

        self.temperature = CONFIG.TEMPERATURE

        self.client = ChatOllama(

            model=self.model,

            base_url=self.base_url,

            temperature=self.temperature,

        )

    ######################################################################

    def invoke(

        self,

        prompt: str,

    ) -> str:

        """
        Ejecuta un prompt simple.
        """

        LOG.info(
            "Invocando Ollama..."
        )

        response = self.client.invoke(

            prompt

        )

        return response.content

    ######################################################################

    def chat(

        self,

        system_prompt: str,

        human_prompt: str,

    ) -> str:

        """
        Conversación System + Human.
        """

        messages = [

            SystemMessage(
                content=system_prompt
            ),

            HumanMessage(
                content=human_prompt
            )

        ]

        response = self.client.invoke(

            messages

        )

        return response.content

    ######################################################################

    def invoke_json(

        self,

        system_prompt: str,

        human_prompt: str,

        retries: int = 3,

    ) -> Dict[str, Any]:

        """
        Solicita salida JSON.
        """

        prompt = human_prompt + """

Responde únicamente con JSON válido.

No agregues comentarios.

No agregues Markdown.

"""

        for attempt in range(retries):

            try:

                response = self.chat(

                    system_prompt,

                    prompt,

                )

                return json.loads(

                    response

                )

            except Exception as error:

                LOG.warning(

                    f"Intento {attempt+1} fallido."

                )

                time.sleep(2)

        raise RuntimeError(

            "No fue posible obtener un JSON válido."

        )

    ######################################################################

    def health(self):

        """
        Verifica la conexión con Ollama.
        """

        try:

            self.invoke(

                "Responde únicamente OK"

            )

            return True

        except Exception:

            return False

    ######################################################################

    def info(self):

        """
        Información del modelo.
        """

        return {

            "model": self.model,

            "base_url": self.base_url,

            "temperature": self.temperature,

        }

##########################################################################
# Instancia Singleton
##########################################################################

OLLAMA = OllamaClient()
