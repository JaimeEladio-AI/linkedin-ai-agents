"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
agents/content_architect.py

Descripción
-----------

Arquitecto de Contenido.

Responsabilidades

✓ Analizar el informe de mercado
✓ Definir el objetivo de la publicación
✓ Identificar la audiencia
✓ Diseñar la estructura narrativa
✓ Definir el Hook inicial
✓ Definir CTA
✓ Proponer el enfoque diferenciador

No redacta publicaciones.

==============================================================================

"""

from __future__ import annotations

from typing import Dict
from typing import Any

from state import LinkedinState
from state import WorkflowStatus

from prompts import ARCHITECT_SYSTEM
from prompts import ARCHITECT_HUMAN

from tools.logger import LOG
from tools.ollama_client import OLLAMA

##########################################################################
# Arquitecto
##########################################################################

class ContentArchitectAgent:

    """
    Diseña la estrategia editorial.
    """

    ######################################################################

    def build_context(

        self,

        state: LinkedinState,

    ) -> str:

        report = state["mercado"]

        return f"""

Tema:

{state["tema"]}

Tendencias

{report.tendencias}

Competidores

{report.competidores}

Casos de uso

{report.casos_uso}

Empresas

{report.empresas}

Noticias

{report.noticias}

"""

##########################################################################

    def design(

        self,

        context: str,

    ):

        prompt = ARCHITECT_HUMAN.format(

            contexto=context

        )

        return OLLAMA.invoke_json(

            ARCHITECT_SYSTEM,

            prompt,

        )

##########################################################################

    def save_architecture(

        self,

        state: LinkedinState,

        architecture,

    ):

        state["arquitectura_contenido"] = (

            architecture

        )

        state["workflow_status"] = (

            WorkflowStatus.CREATOR

        )

        return state

##########################################################################

    def run(

        self,

        state: LinkedinState,

    ):

        LOG.agent_start(

            "CONTENT ARCHITECT"

        )

        context = self.build_context(

            state

        )

        architecture = self.design(

            context

        )

        state = self.save_architecture(

            state,

            architecture,

        )

        LOG.agent_finish(

            "CONTENT ARCHITECT"

        )

        return state

##########################################################################
# Nodo
##########################################################################

CONTENT_ARCHITECT = (

    ContentArchitectAgent()

)


def architect_node(

    state: LinkedinState,

):

    return CONTENT_ARCHITECT.run(

        state

    )

