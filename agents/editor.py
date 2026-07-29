"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
agents/editor.py

Descripción
-----------

Agente Editor.

Responsabilidades

✓ Consolidar todas las revisiones
✓ Evaluar la calidad global
✓ Calcular el Score
✓ Aprobar o rechazar
✓ Generar informe de mejoras
✓ Controlar las iteraciones

==============================================================================

"""

from __future__ import annotations

from state import LinkedinState
from state import WorkflowStatus
from state import ReviewDecision

from prompts import EDITOR_SYSTEM
from prompts import EDITOR_HUMAN

from tools.logger import LOG
from tools.ollama_client import OLLAMA

from tools.scoring import (
    SCORING,
    ScoreCriterion,
)
##########################################################################
# Editor Agent
##########################################################################

class EditorAgent:

    """
    Editor General del sistema.
    """

    ######################################################################

    def build_context(

        self,

        state: LinkedinState,

    ) -> str:

        return f"""

PUBLICACIÓN

{state["borrador"]}

============================

SEO

{state["seo"]}

============================

LEGAL

{state["legal"]}

============================

TÉCNICO

{state["tecnico"]}

"""

    ######################################################################

    def review(

        self,

        context,

    ):

        prompt = EDITOR_HUMAN.format(

            contexto=context

        )

        return OLLAMA.invoke_json(

            EDITOR_SYSTEM,

            prompt,

        )

    ######################################################################

    def build_score(

        self,

        review: dict,

    ):

        criteria = []

        for item in review["criteria"]:

            criteria.append(

                ScoreCriterion(

                    name=item["name"],

                    weight=item["weight"],

                    passed=item["passed"],

                    observations=item["observations"]

                )

            )

        return SCORING.calculate(

            criteria

        )

    ######################################################################

    def decide(

        self,

        state: LinkedinState,

        score,

        review,

        )-> LinkedinState:

        state["editor"] = review

        if score.approved:

            state["decision"] = (

                ReviewDecision.APPROVED

            )

            state["workflow_status"] = (

                WorkflowStatus.IMAGE

            )

            return state

        state["decision"] = (

            ReviewDecision.REJECTED

        )

        state["iteracion"] += 1

        state["workflow_status"] = (

            WorkflowStatus.CREATOR

        )

        return state

    ######################################################################

    def run(

        self,

        state: LinkedinState,

         )-> LinkedinState:

        LOG.agent_start(

            "EDITOR"

        )

        context = self.build_context(

            state

        )

        review = self.review(

            context

        )

        score = self.build_score(

            review

        )

        state = self.decide(

            state,

            score,

            review,

        )

        LOG.agent_finish(

            "EDITOR"

        )

        return state

##########################################################################
# Nodo LangGraph
##########################################################################

EDITOR = EditorAgent()


def editor_node(

    state: LinkedinState,

)-> LinkedinState:

    return EDITOR.run(

        state

    )

