"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
agents/technical_review.py

Descripción
-----------

Agente Revisor Técnico.

Responsabilidades

✓ Verificar exactitud técnica
✓ Detectar errores conceptuales
✓ Validar terminología
✓ Revisar consistencia tecnológica
✓ Evaluar rigor técnico
✓ Generar recomendaciones para el Editor

No modifica directamente la publicación.

==============================================================================

"""

from __future__ import annotations

from state import LinkedinState
from state import WorkflowStatus

from prompts import TECHNICAL_SYSTEM
from prompts import TECHNICAL_HUMAN

from tools.logger import LOG
from tools.ollama_client import OLLAMA

##########################################################################
# Technical Review Agent
##########################################################################

class TechnicalReviewAgent:

    """
    Revisor técnico especializado en IA Agéntica.
    """

    ######################################################################

    def review(

        self,

        state: LinkedinState,

        )-> dict:

        """
        Ejecuta la revisión técnica.
        """

        prompt = TECHNICAL_HUMAN.format(

            articulo=state["borrador"]

        )

        return OLLAMA.invoke_json(

            TECHNICAL_SYSTEM,

            prompt,

        )

##########################################################################

    def save(

        self,

        state: LinkedinState,

        report: dict,

        )-> LinkedinState:

        state["tecnico"] = report

        state["workflow_status"] = (

            WorkflowStatus.EDITOR

        )

        return state

##########################################################################

    def run(

        self,

        state: LinkedinState,

        )-> LinkedinState:

        LOG.agent_start(

            "TECHNICAL REVIEW"

        )

        report = self.review(

            state

        )

        state = self.save(

            state,

            report,

        )

        LOG.agent_finish(

            "TECHNICAL REVIEW"

        )

        return state

##########################################################################
# Nodo LangGraph
##########################################################################

TECHNICAL = TechnicalReviewAgent()


def technical_node(

    state: LinkedinState,

    )-> LinkedinState:

    return TECHNICAL.run(

        state

    )

