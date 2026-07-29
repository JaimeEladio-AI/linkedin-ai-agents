"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
agents/supervisor.py

Descripción
-----------

Supervisor del workflow.

Este agente actúa como el Director General del sistema.

Responsabilidades

✓ Validar el estado recibido
✓ Inicializar la ejecución
✓ Controlar el número máximo de iteraciones
✓ Gestionar errores globales
✓ Preparar el flujo para el siguiente agente

No genera contenido.

No utiliza prompts largos.

No interactúa directamente con el usuario.

==============================================================================

"""

from __future__ import annotations

from typing import Dict
from typing import Any

from state import LinkedinState
from state import WorkflowStatus

from tools.logger import LOG

##########################################################################
# Supervisor
##########################################################################

class SupervisorAgent:

    """
    Supervisor principal.
    """

    ######################################################################

    def validate_input(

        self,

        state: LinkedinState,

    ):

        """
        Valida el estado inicial.
        """

        if not state["topic"]:

            raise ValueError(

                "No existe un tema inicial."

            )

        if state["max_iterations"] <= 0:

            raise ValueError(

                "max_iterations debe ser mayor que cero."

            )

##########################################################################

    def check_iterations(

        self,

        state: LinkedinState,

    ):

        """
        Verifica que el workflow
        pueda continuar.
        """

        if state["iteration"] > state["max_iterations"]:

            raise RuntimeError(

                "Se alcanzó el número máximo de iteraciones."

            )

##########################################################################

    def initialize(

        self,

        state: LinkedinState,

    ):

        """
        Inicializa el workflow.
        """

        LOG.workflow(

            "Inicializando Supervisor"

        )

        state["workflow_status"] = (

            WorkflowStatus.RESEARCH

        )

        return state

##########################################################################

    def run(

        self,

        state: LinkedinState,

    ) -> LinkedinState:

        """
        Ejecuta el Supervisor.
        """

        self.validate_input(

            state

        )

        self.check_iterations(

            state

        )

        state = self.initialize(

            state

        )

        return state

##########################################################################
# Nodo LangGraph
##########################################################################

SUPERVISOR = SupervisorAgent()


def supervisor_node(

    state: LinkedinState,

):

    LOG.agent_start(

        "SUPERVISOR"

    )

    result = SUPERVISOR.run(

        state

    )

    LOG.agent_finish(

        "SUPERVISOR"

    )

    return result

