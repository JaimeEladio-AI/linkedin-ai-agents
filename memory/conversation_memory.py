"""
==========================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
memory/conversation_memory.py

Descripción
-----------

Este módulo implementa la memoria temporal del workflow.

Su objetivo es registrar toda la conversación y las acciones
realizadas por los agentes durante UNA ejecución del proceso.

La información almacenada aquí se descarta al finalizar el workflow.

Características

✓ Historial de mensajes.
✓ Historial de agentes.
✓ Historial de decisiones.
✓ Historial de iteraciones.
✓ Compatible con LangGraph.

==========================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any


##########################################################################
# Registro individual de memoria
##########################################################################

@dataclass(slots=True)
class MemoryEvent:
    """
    Representa un evento ocurrido durante la ejecución.
    """

    timestamp: str

    agent: str

    event_type: str

    content: Any


##########################################################################
# Memoria conversacional
##########################################################################

class ConversationMemory:
    """
    Memoria temporal del workflow.
    """

    def __init__(self):

        self._events: List[MemoryEvent] = []

    ######################################################################
    # Agregar evento
    ######################################################################

    def add_event(
        self,
        agent: str,
        event_type: str,
        content: Any,
    ) -> None:
        """
        Registra un nuevo evento en memoria.
        """

        event = MemoryEvent(
            timestamp=datetime.now().isoformat(),
            agent=agent,
            event_type=event_type,
            content=content,
        )

        self._events.append(event)

    ######################################################################
    # Obtener todos los eventos
    ######################################################################

    def events(self) -> List[MemoryEvent]:
        """
        Devuelve todos los eventos registrados.
        """

        return list(self._events)

    ######################################################################
    # Eventos por agente
    ######################################################################

    def events_by_agent(
        self,
        agent: str,
    ) -> List[MemoryEvent]:

        return [
            event
            for event in self._events
            if event.agent == agent
        ]

    ######################################################################
    # Último evento
    ######################################################################

    def last_event(self):

        if not self._events:

            return None

        return self._events[-1]

    ######################################################################
    # Cantidad de eventos
    ######################################################################

    def count(self):

        return len(self._events)

    ######################################################################
    # Reiniciar memoria
    ######################################################################

    def clear(self):

        self._events.clear()

    ######################################################################
    # Exportar a diccionario
    ######################################################################

    def to_dict(self):

        return [
            {
                "timestamp": e.timestamp,
                "agent": e.agent,
                "event_type": e.event_type,
                "content": e.content,
            }
            for e in self._events
        ]

    ######################################################################
    # Cargar desde diccionario
    ######################################################################

    def load(self, data):

        self.clear()

        for item in data:

            self._events.append(
                MemoryEvent(
                    timestamp=item["timestamp"],
                    agent=item["agent"],
                    event_type=item["event_type"],
                    content=item["content"],
                )
            )

##########################################################################
# Instancia global
##########################################################################

CONVERSATION_MEMORY = ConversationMemory()
