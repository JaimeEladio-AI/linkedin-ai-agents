"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
agents/legal.py

Descripción
-----------

Agente Asesor Legal y Ético.

Responsabilidades

✓ Revisar cumplimiento de derechos de autor
✓ Revisar protección de datos personales
✓ Detectar afirmaciones engañosas
✓ Evaluar riesgos regulatorios
✓ Verificar principios de IA Responsable
✓ Emitir observaciones para el Editor

No modifica directamente la publicación.

==============================================================================

"""

from __future__ import annotations

from state import LinkedinState
from state import WorkflowStatus

from prompts import LEGAL_SYSTEM
from prompts import LEGAL_HUMAN

from tools.logger import LOG
from tools.ollama_client import OLLAMA
##########################################################################
# Legal Agent
##########################################################################

class LegalAgent:

    """
    Revisor legal y ético.
    """

    ######################################################################

    def review(

        self,

        post: str,

        )-> dict:

        """
        Revisión legal.
        """

        prompt = LEGAL_HUMAN.format(

            borrador=post

        )

        return OLLAMA.invoke_json(

            LEGAL_SYSTEM,

            prompt,

        )

##########################################################################

    def save(

        self,

        state: LinkedinState,

        report,

        )-> LinkedinState:

        state["legal"] = report

        state["workflow_status"] = (

            WorkflowStatus.TECHNICAL

        )

        return state

##########################################################################

    def run(

        self,

        state: LinkedinState,

        )-> LinkedinState:

        LOG.agent_start(

            "LEGAL"

        )

        report = self.review(

            state["borrador"]

        )

        state = self.save(

            state,

            report,

        )

        LOG.agent_finish(

            "LEGAL"

        )

        return state

##########################################################################
# Nodo LangGraph
##########################################################################

LEGAL = LegalAgent()


def legal_node(

    state: LinkedinState,

):

    return LEGAL.run(

        state

    )

