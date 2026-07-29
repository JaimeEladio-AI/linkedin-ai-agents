"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
agents/creator.py

Descripción
-----------

Agente Creador.

Responsabilidades

✓ Redactar la publicación para LinkedIn
✓ Utilizar lenguaje simple y cercano
✓ Mantener rigor técnico
✓ Transformar conceptos complejos en explicaciones accesibles
✓ Generar un primer borrador de alta calidad

Entradas

- Tema
- Investigación de mercado
- Arquitectura editorial

Salidas

- Publicación completa

==============================================================================

"""

from __future__ import annotations

from state import LinkedinState
from state import WorkflowStatus

from prompts import CREATOR_SYSTEM
from prompts import CREATOR_HUMAN

from tools.logger import LOG
from tools.ollama_client import OLLAMA

##########################################################################
# Creator Agent
##########################################################################

class CreatorAgent:

    """
    Redactor principal.
    """

    ######################################################################

    def build_context(

        self,

        state: LinkedinState,

    ) -> str:

        architecture = state["arquitectura_contenido"]

        research = state["mercado"]

        return f"""Tema

        {state["tema"]}

        Arquitectura Editorial

        {architecture}

        Hallazgos del Mercado

        Tendencias:
        {research.tendencias}

        Casos de Uso:
        {research.casos_uso}

        Competidores:
        {research.competidores}

        Empresas:
        {research.empresas}

        """

##########################################################################

    def write_post(

        self,

        context: str,

    ) -> str:

        prompt = CREATOR_HUMAN.format(

            contexto=context

        )

        return OLLAMA.chat(

            CREATOR_SYSTEM,

            prompt,

        )

##########################################################################

    def save_post(

        self,

        state: LinkedinState,

        post: str,

    ):

        state["borrador_anterior"] = state.get("borrador", "")

        state["borrador"] = post

        state["workflow_status"] = (

            WorkflowStatus.SEO

        )

        return state

##########################################################################

    def run(

        self,

        state: LinkedinState,

    ):

        LOG.agent_start(

            "CREATOR"

        )

        context = self.build_context(

            state

        )

        post = self.write_post(

            context

        )

        state = self.save_post(

            state,

            post,

        )

        LOG.agent_finish(

            "CREATOR"

        )

        LOG.info(
            f"Borrador generado ({len(post)} caracteres)"
        )

        return state

##########################################################################
# Nodo
##########################################################################

CREATOR = CreatorAgent()


def creator_node(

    state: LinkedinState,

):

    return CREATOR.run(

        state

    )

