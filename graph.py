"""
==========================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
graph.py

Descripción
-----------

Define el StateGraph principal del sistema.

Este módulo:

✓ Registra los nodos.
✓ Define el flujo.
✓ Implementa las rutas condicionales.
✓ Compila el grafo.

En esta primera versión los nodos son stubs.
Posteriormente serán reemplazados por los agentes reales.

==========================================================================
"""

from __future__ import annotations

from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

from state import LinkedinState
from state import ReviewDecision
from state import WorkflowStatus

from tools.logger import LOG

##########################################################################
# Supervisor
##########################################################################

def supervisor_node(
    state: LinkedinState
):

    LOG.agent_start("SUPERVISOR")

    state["workflow_status"] = WorkflowStatus.RESEARCH

    LOG.agent_finish("SUPERVISOR")

    return state

##########################################################################
# Investigación
##########################################################################

def market_node(
    state: LinkedinState
):

    LOG.agent_start("MARKET")

    state["workflow_status"] = WorkflowStatus.CONTENT_ARCHITECT

    LOG.agent_finish("MARKET")

    return state

##########################################################################
# Arquitecto
##########################################################################

def architect_node(
    state: LinkedinState
):

    LOG.agent_start("ARCHITECT")

    state["workflow_status"] = WorkflowStatus.CREATOR

    LOG.agent_finish("ARCHITECT")

    return state

##########################################################################
# Creador
##########################################################################

def creator_node(
    state: LinkedinState
):

    LOG.agent_start("CREATOR")

    state["workflow_status"] = WorkflowStatus.SEO

    LOG.agent_finish("CREATOR")

    return state

##########################################################################
# SEO
##########################################################################

def seo_node(
    state: LinkedinState
):

    LOG.agent_start("SEO")

    state["workflow_status"] = WorkflowStatus.LEGAL

    LOG.agent_finish("SEO")

    return state

##########################################################################
# Legal
##########################################################################

def legal_node(
    state: LinkedinState
):

    LOG.agent_start("LEGAL")

    state["workflow_status"] = WorkflowStatus.TECHNICAL

    LOG.agent_finish("LEGAL")

    return state

##########################################################################
# Técnico
##########################################################################

def technical_node(
    state: LinkedinState
):

    LOG.agent_start("TECHNICAL")

    state["workflow_status"] = WorkflowStatus.EDITOR

    LOG.agent_finish("TECHNICAL")

    return state

##########################################################################
# Editor
##########################################################################

def editor_node(
    state: LinkedinState
):

    LOG.agent_start("EDITOR")

    # Simulación temporal
    state["decision"] = ReviewDecision.APPROVED
    state["workflow_status"] = WorkflowStatus.IMAGE

    LOG.agent_finish("EDITOR")

    return state

##########################################################################
# Imagen
##########################################################################

def image_node(
    state: LinkedinState
):

    LOG.agent_start("IMAGE")

    state["workflow_status"] = WorkflowStatus.PUBLISHER

    LOG.agent_finish("IMAGE")

    return state

##########################################################################
# Publicador
##########################################################################

def publisher_node(
    state: LinkedinState
):

    LOG.agent_start("PUBLISHER")

    state["workflow_status"] = WorkflowStatus.FINISHED

    LOG.agent_finish("PUBLISHER")

    return state

##########################################################################
# Registro de Nodos
##########################################################################

NODE_REGISTRY = {

    "supervisor": supervisor_node,

    "market": market_node,

    "architect": architect_node,

    "creator": creator_node,

    "seo": seo_node,

    "legal": legal_node,

    "technical": technical_node,

    "editor": editor_node,

    "image": image_node,

    "publisher": publisher_node,

}

##########################################################################
# Router principal
##########################################################################

def workflow_router(
    state: LinkedinState,
):
    """
    Decide cuál será el siguiente nodo del workflow
    según el estado actual.
    """

    status = state["workflow_status"]

    if status == WorkflowStatus.RESEARCH:
        return "market"

    if status == WorkflowStatus.CONTENT_ARCHITECT:
        return "architect"

    if status == WorkflowStatus.CREATOR:
        return "creator"

    if status == WorkflowStatus.SEO:
        return "seo"

    if status == WorkflowStatus.LEGAL:
        return "legal"

    if status == WorkflowStatus.TECHNICAL:
        return "technical"

    if status == WorkflowStatus.EDITOR:
        return "editor"

    if status == WorkflowStatus.IMAGE:
        return "image"

    if status == WorkflowStatus.PUBLISHER:
        return "publisher"

    if status == WorkflowStatus.FINISHED:
        return END

    if status == WorkflowStatus.FAILED:
        return END

    return END

##########################################################################
# Router Editor
##########################################################################

def editor_router(
    state: LinkedinState,
):
    """
    El Editor decide si la publicación
    continúa o vuelve al Creador.
    """

    if state["decision"] == ReviewDecision.APPROVED:
        return "image"

    if state["iteracion"] >= state["max_iteraciones"]:
        state["workflow_status"] = WorkflowStatus.FAILED
        return END

    state["iteracion"] += 1

    return "creator"

##########################################################################
# Constructor
##########################################################################

def build_graph():

    workflow = StateGraph(
        LinkedinState
    )

    ###############################################################
    # Registro de nodos
    ###############################################################

    for name, node in NODE_REGISTRY.items():

        workflow.add_node(
            name,
            node,
        )

    ###############################################################
    # Inicio
    ###############################################################

    workflow.add_edge(
        START,
        "supervisor",
    )

    ###############################################################
    # Flujo principal
    ###############################################################

    workflow.add_conditional_edges(
        "supervisor",
        workflow_router,
    )

    workflow.add_conditional_edges(
        "market",
        workflow_router,
    )

    workflow.add_conditional_edges(
        "architect",
        workflow_router,
    )

    workflow.add_conditional_edges(
        "creator",
        workflow_router,
        {
            "market": "market",
            "architect": "architect",
            "creator": "creator",
            "seo": "seo",
            "legal": "legal",
            "technical": "technical",
            "editor": "editor",
            "image": "image",
            "publisher": "publisher",
            END: END,
        },
    )

    workflow.add_conditional_edges(
        "seo",
        workflow_router,
    )

    workflow.add_conditional_edges(
        "legal",
        workflow_router,
    )

    workflow.add_conditional_edges(
        "technical",
        workflow_router,
    )

    ###############################################################
    # Editor
    ###############################################################

    workflow.add_conditional_edges(
        "editor",
        editor_router,
    )

    ###############################################################
    # Imagen
    ###############################################################

    workflow.add_conditional_edges(
        "image",
        workflow_router,
    )

    ###############################################################
    # Publicador
    ###############################################################

    workflow.add_conditional_edges(
        "publisher",
        workflow_router,
    )

    ###############################################################
    # Compilar
    ###############################################################

    return workflow.compile()

##########################################################################
# Instancia Global
##########################################################################

GRAPH = build_graph()
