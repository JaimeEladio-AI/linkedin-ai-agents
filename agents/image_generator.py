"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
agents/image_generator.py

Descripción
-----------

Agente Generador de Imágenes.

Responsabilidades

✓ Tomar el prompt generado por SEO
✓ Validar que exista un prompt
✓ Solicitar la imagen a DALL·E 3
✓ Guardar la imagen localmente
✓ Registrar la ruta de salida
✓ Preparar la publicación para LinkedIn

==============================================================================

"""

from __future__ import annotations

from pathlib import Path

from state import LinkedinState
from state import WorkflowStatus

from tools.logger import LOG
from tools.openai_client import OPENAI

##########################################################################
# Image Generator Agent
##########################################################################

class ImageGeneratorAgent:

    """
    Generador de imágenes para LinkedIn.
    """

    ######################################################################

    def validate_prompt(

        self,

        state: LinkedinState,

    ):

        """
        Valida la existencia del prompt.
        """

        if not state["prompt_imagen"]:

            raise ValueError(

                "No existe un prompt para generar la imagen."

            )

##########################################################################

    def generate(

        self,

        prompt: str,

    ) -> Path:

        """
        Solicita la imagen a OpenAI.
        """

        return OPENAI.generate_image(

            prompt

        )

##########################################################################

    def save(

        self,

        state,

        image_path,

    ):

        state["image_path"] = str(

            image_path

        )

        state["workflow_status"] = (

            WorkflowStatus.PUBLISHER

        )

        return state

##########################################################################

    def run(

        self,

        state,

    ):

        LOG.agent_start(

            "IMAGE GENERATOR"

        )

        self.validate_prompt(

            state

        )

        image = self.generate(

            state["prompt_image"]

        )

        state = self.save(

            state,

            image,

        )

        LOG.agent_finish(

            "IMAGE GENERATOR"

        )

        return state

##########################################################################
# Nodo LangGraph
##########################################################################

IMAGE_GENERATOR = ImageGeneratorAgent()


def image_node(

    state,

):

    return IMAGE_GENERATOR.run(

        state
    )
