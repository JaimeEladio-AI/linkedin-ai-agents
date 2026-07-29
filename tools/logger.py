"""
==========================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
tools/logger.py

Descripción
-----------

Este módulo centraliza el sistema de registro (logging) del proyecto.

Objetivos

✓ Registrar todas las acciones del workflow.
✓ Registrar la actividad de cada agente.
✓ Registrar errores.
✓ Registrar tiempos de ejecución.
✓ Registrar puntuaciones del Editor.
✓ Registrar publicaciones.

Todo el proyecto utilizará esta clase.

Ningún agente debe utilizar print() para depuración.

==========================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from config import CONFIG
from tools.filesystem import FILES


##########################################################################
# Clase principal
##########################################################################

class ProjectLogger:
    """
    Administrador central de logs del proyecto.
    """

    ######################################################################

    def __init__(self):

        self._configured = False

        self.configure()

    ######################################################################

    def configure(self):
        """
        Configura Loguru.
        """

        if self._configured:
            return

        logger.remove()

        ##############################################################
        # Consola
        ##############################################################

        logger.add(
            sys.stdout,
            level=CONFIG.LOG_LEVEL,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )

        ##############################################################
        # Log general
        ##############################################################

        logger.add(
            FILES.log("workflow.log"),
            level="INFO",
            rotation="10 MB",
            retention=20,
            encoding="utf-8",
        )

        ##############################################################
        # Log errores
        ##############################################################

        logger.add(
            FILES.log("errors.log"),
            level="ERROR",
            rotation="5 MB",
            retention=30,
            encoding="utf-8",
        )

        self._configured = True

    ######################################################################
    # Logger por agente
    ######################################################################

    def agent(self, name: str):
        """
        Devuelve un logger asociado a un agente.
        """

        return logger.bind(agent=name)

    ######################################################################
    # Workflow
    ######################################################################

    def workflow(self, message: str):

        logger.info(f"[WORKFLOW] {message}")

    ######################################################################
    # Agente
    ######################################################################

    def agent_start(
        self,
        agent: str
    ):

        logger.info(
            f"[{agent}] Inicio"
        )

    ######################################################################

    def agent_finish(
        self,
        agent: str
    ):

        logger.info(
            f"[{agent}] Finalizado"
        )

    ######################################################################
    # Iteración
    ######################################################################

    def iteration(
        self,
        number: int
    ):

        logger.info(
            f"========== ITERACIÓN {number} =========="
        )

    ######################################################################
    # Publicación
    ######################################################################

    def published(
        self,
        url: Optional[str] = None
    ):

        if url:

            logger.success(
                f"Publicación realizada correctamente: {url}"
            )

        else:

            logger.success(
                "Publicación realizada correctamente."
            )

    ######################################################################
    # Editor
    ######################################################################

    def editor_score(
        self,
        score: int
    ):

        logger.info(
            f"Puntaje Editor: {score}"
        )

    ######################################################################
    # Advertencias
    ######################################################################

    def warning(
        self,
        message: str
    ):

        logger.warning(message)

    ######################################################################
    # Errores
    ######################################################################

    def error(
        self,
        message: str
    ):

        logger.error(message)

    ######################################################################
    # Información
    ######################################################################

    def info(
        self,
        message: str
    ):

        logger.info(message)

    ######################################################################
    # Depuración
    ######################################################################

    def debug(
        self,
        message: str
    ):

        logger.debug(message)

    ######################################################################
    # Excepción
    ######################################################################

    def exception(
        self,
        exception: Exception
    ):

        logger.exception(exception)


    ##########################################################################
# Instancia global
##########################################################################

LOG = ProjectLogger()
