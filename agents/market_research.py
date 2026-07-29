"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
agents/market_research.py

Descripción
-----------

Agente Investigador de Mercado.

Responsabilidades

✓ Buscar información reciente
✓ Detectar tendencias
✓ Identificar competidores
✓ Encontrar casos de uso
✓ Analizar el mercado chileno
✓ Proponer el mejor enfoque editorial

No redacta publicaciones.

No genera imágenes.

Su única salida es un informe estructurado.

==============================================================================

"""

from __future__ import annotations

from typing import List
from typing import Dict
from typing import Any

from state import LinkedinState
from state import MarketResearch
from state import WorkflowStatus

from prompts import MARKET_SYSTEM
from prompts import MARKET_HUMAN

from tools.logger import LOG
from tools.search_client import SEARCH
from tools.ollama_client import OLLAMA

##########################################################################
# Investigador
##########################################################################

class MarketResearchAgent:

    """
    Investigador especializado.
    """

    ######################################################################

    def search(

        self,

        tema: str,

    ):

        """
        Consulta el buscador.
        """

        return SEARCH.search(

            tema,

            max_results=10,

        )

    ##########################################################################

    def build_context(

        self,

        results: list[dict],

    ) -> str:

        """
        Convierte los resultados
        en un único contexto.
        """

        context = ""

        for item in results:

            context += f"""Título:
            {item["title"]}

            Contenido:
            {item["content"]}

            Fuente:
            {item["url"]}

            """

        return context

##########################################################################

    def analyze(

        self,

        tema: str,

        context: str,

    )-> dict:

        """
        Solicita el análisis al LLM.
        """

        prompt = MARKET_HUMAN.format(

            tema=tema,

            contexto=context,

        )

        return OLLAMA.invoke_json(

            MARKET_SYSTEM,

            prompt,

        )

##########################################################################

    def build_model(

        self,

        data,

    ):

        """
        Convierte JSON a modelo.
        """

        return MarketResearch(

            **data

        )

##########################################################################

    def run(

        self,

        state: LinkedinState,

    ):

        """
        Ejecuta el análisis completo.
        """

        LOG.agent_start(

            "MARKET_RESEARCH"

        )

        tema = state["tema"]

        results = self.search(

            tema

        )

        context = self.build_context(

            results

        )

        analysis = self.analyze(

            tema,

            context,

        )

        report = self.build_model(

            analysis

        )

        state["mercado"] = report

        state["workflow_status"] = (

            WorkflowStatus.CONTENT_ARCHITECT

        )

        LOG.agent_finish(

            "MARKET_RESEARCH"

        )

        return state

##########################################################################
# Nodo
##########################################################################

MARKET = MarketResearchAgent()


def market_node(

    state: LinkedinState,

):

    return MARKET.run(

        state

    )

