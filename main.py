"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
main.py

Descripción
-----------

Punto de entrada principal del sistema.

Responsabilidades

✓ Inicializar el proyecto
✓ Crear el estado inicial
✓ Ejecutar el Graph
✓ Mostrar resultados
✓ Registrar errores
✓ Preparar futuras integraciones

Compatible con:

    - Google Colab
    - Ollama
    - llama3.1:8b
    - LangGraph
    - LangChain

==============================================================================
"""

from __future__ import annotations

import traceback

from graph import GRAPH
from state import LinkedinState, ReviewDecision, WorkflowStatus
from tools.filesystem import FILES
from tools.logger import LOG


##########################################################################
# Crear estado inicial
##########################################################################

def create_initial_state(
    topic: str
) -> LinkedinState:
    """
    Construye el estado inicial del workflow.
    """

    return {

        ##################################################################
        # Entrada principal
        ##################################################################

        "tema": topic,

        ##################################################################
        # Estado del workflow
        ##################################################################

        "workflow_status": WorkflowStatus.RESEARCH,

        ##################################################################
        # Decisión inicial
        ##################################################################

        "decision": ReviewDecision.REJECTED,

        ##################################################################
        # Contadores
        ##################################################################

        "iteracion": 1,

        "max_iteraciones": 5,

        ##################################################################
        # Información de mercado
        ##################################################################

        "mercado": {},

        ##################################################################
        # Arquitectura
        ##################################################################

        "arquitectura_contenido": {},

        ##################################################################
        # Publicación
        ##################################################################

        "borrador": "",

        ##################################################################
        # SEO
        ##################################################################

        "seo": {},

        ##################################################################
        # Legal
        ##################################################################

        "legal": {},

        ##################################################################
        # Revisión técnica
        ##################################################################

        "tecnico": None,

        ##################################################################
        # Resultado del Editor
        ##################################################################

        "editor": None,

        ##################################################################
        # Prompt Imagen
        ##################################################################

        "prompt_imagen": "",

        ##################################################################
        # Imagen generada
        ##################################################################

        "image_path": "",

        ##################################################################
        # URL LinkedIn
        ##################################################################

        "linkedin_url": "",

        ##################################################################
        # Historial
        ##################################################################

        "historial": [],

        ##################################################################
        # Mensajes
        ##################################################################

        "mensajes": [],

        ##################################################################
        # Errores
        ##################################################################

        "errores": [],

    }


##########################################################################
# Ejecutar Workflow
##########################################################################

def execute(
    topic: str
):
    """
    Ejecuta el workflow completo.
    """

    LOG.workflow(
        "Inicio del workflow"
    )

    state = create_initial_state(
        topic
    )

    result = GRAPH.invoke(
        state
    )

    LOG.workflow(
        "Workflow finalizado"
    )

    return result


##########################################################################
# Mostrar resultado
##########################################################################

def show_summary(
    state: LinkedinState
):
    """
    Muestra un resumen de la ejecución.
    """

    print()

    print("=" * 80)

    print("RESUMEN")

    print("=" * 80)

    print()

    print("Tema")

    print(state["tema"])

    print()

    print("Estado")

    print(state["workflow_status"])

    print()

    print("Iteraciones")

    print(state["iteracion"])

    print()

    print("Decisión")

    print(state["decision"])

    print()

    print("=" * 80)

    print()


##########################################################################
# Guardar estado final
##########################################################################

def save_state(
    state: LinkedinState
):
    """
    Guarda el estado completo del workflow.
    """

    filename = FILES.new_state_filename()

    FILES.save_json(
        filename,
        state
    )

    LOG.info(
        f"Estado almacenado en: {filename}"
    )


##########################################################################
# Programa principal
##########################################################################

def main():
    """
    Punto de entrada.
    """

    print()

    print("=" * 80)
    print("LinkedIn AI MultiAgent")
    print("=" * 80)
    print()

    topic = input(
        "Tema inicial: "
    ).strip()

    if not topic:

        print()

        print("Debe ingresar un tema.")

        return

    try:

        result = execute(
            topic
        )

        show_summary(
            result
        )

        save_state(
            result
        )

    except (RuntimeError, ValueError, OSError) as error:

        LOG.exception(
            error
        )

        traceback.print_exc()

    except KeyboardInterrupt:

        print()
        print("Ejecución cancelada por el usuario.")


##########################################################################
# Inicio
##########################################################################

if __name__ == "__main__":

    main()

