"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
agents/seo.py

Descripción
-----------

Agente SEO especializado en LinkedIn.

Responsabilidades

✓ Optimizar la publicación para LinkedIn
✓ Mejorar el Hook inicial
✓ Optimizar legibilidad
✓ Optimizar palabras clave
✓ Optimizar hashtags
✓ Mejorar CTA
✓ Generar prompt base para DALL·E 3

==============================================================================

"""

from __future__ import annotations

from state import LinkedinState
from state import WorkflowStatus

from prompts import SEO_SYSTEM
from prompts import SEO_HUMAN

from prompts import IMAGE_SYSTEM
from prompts import IMAGE_HUMAN

from tools.logger import LOG
from tools.ollama_client import OLLAMA

##########################################################################
# SEO Agent
##########################################################################

class SEOAgent:

    """
    Especialista SEO para LinkedIn.
    """

    ######################################################################

    def optimize_post(

        self,

        post: str,

    )-> dict:

        """
        Optimiza la publicación.
        """

        prompt = SEO_HUMAN.format(

            post=post

        )

        return OLLAMA.invoke_json(

            SEO_SYSTEM,

            prompt,

        )

##########################################################################

    def create_image_prompt(

        self,

        optimized_post: str,

    ):

        """
        Genera el prompt para DALL·E.
        """

        prompt = IMAGE_HUMAN.format(

            prompt=optimized_post

        )

        return OLLAMA.chat(

            IMAGE_SYSTEM,

            prompt,

        )

##########################################################################

    def save(

        self,

        state: LinkedinState,

        seo_result,

        image_prompt,

    ):

        state["borrador"] = seo_result["post"]

        state["seo"] = seo_result

        state["prompt_image"] = image_prompt

        state["workflow_status"] = (

            WorkflowStatus.LEGAL

        )

        return state

##########################################################################

    def run(

        self,

        state,

    ):

        LOG.agent_start(

            "SEO"

        )

        seo = self.optimize_post(

            state["borrador"]

        )

        image_prompt = self.create_image_prompt(

            seo["post"]

        )

        state = self.save(

            state,

            seo,

            image_prompt,

        )

        LOG.agent_finish(

            "SEO"

        )

        return state

##########################################################################
# Nodo LangGraph
##########################################################################

SEO = SEOAgent()


def seo_node(

    state: LinkedinState,

):

    return SEO.run(

        state
    )
