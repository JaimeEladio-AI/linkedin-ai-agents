"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
agents/publisher.py

Descripción
-----------

Agente Publicador.

Responsabilidades

✓ Verificar aprobación del Editor
✓ Verificar existencia de la imagen
✓ Publicar en LinkedIn
✓ Registrar la URL de la publicación
✓ Soportar modo simulación (Dry Run)

NOTA

La publicación real requiere:

- LinkedIn Developer Application
- OAuth 2.0
- Access Token válido

Durante el desarrollo se utilizará DRY RUN.

==============================================================================

"""

from __future__ import annotations

from pathlib import Path

from state import LinkedinState
from state import ReviewDecision
from state import WorkflowStatus

from tools.logger import LOG

from tools.linkedin_client import LINKEDIN

##########################################################################
# Publisher Agent
##########################################################################

class PublisherAgent:

    """
    Publicador oficial del sistema.
    """

    ######################################################################

    def validate(

        self,

        state: LinkedinState,

    ):

        """
        Verifica que la publicación
        pueda publicarse.
        """

        if state["decision"] != ReviewDecision.APPROVED:

            raise RuntimeError(

                "La publicación no fue aprobada."

            )

        if not state["borrador"]:

            raise RuntimeError(

                "No existe publicación."

            )

        if not state["image_path"]:

            raise RuntimeError(

                "No existe imagen."

            )

##########################################################################

    def publish(

        self,

        state,

    ):

        """
        Publica en LinkedIn.
        """

        return LINKEDIN.publish(

            text=state["borrador"],

            image=Path(

                state["image_path"]

            )

        )

##########################################################################

    def save(

        self,

        state,

        result,

    ):

        state["linkedin_url"] = (

            result["url"]

        )

        state["workflow_status"] = (

            WorkflowStatus.FINISHED

        )

        return state

##########################################################################

    def run(

        self,

        state,

    ):

        LOG.agent_start(

            "PUBLISHER"

        )

        self.validate(

            state

        )

        result = self.publish(

            state

        )

        state = self.save(

            state,

            result,

        )

        LOG.agent_finish(

            "PUBLISHER"

        )

        return state

##########################################################################
# Nodo LangGraph
##########################################################################

PUBLISHER = PublisherAgent()


def publisher_node(

    state,

):

    return PUBLISHER.run(

        state

    )
