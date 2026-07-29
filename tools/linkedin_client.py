"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
tools/linkedin_client.py

Descripción
-----------

Cliente centralizado para LinkedIn.

Responsabilidades

✓ Publicación en modo DRY RUN
✓ Publicación real mediante API REST
✓ Carga de imágenes
✓ Registro de publicaciones
✓ Recuperación de URL
✓ Manejo de errores

Versión 1.0

Por defecto trabaja en modo DRY RUN.

==============================================================================

"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json

import requests

from config import CONFIG

from tools.logger import LOG
from tools.filesystem import FILES

##########################################################################
# LinkedIn Client
##########################################################################

class LinkedInClient:

    """
    Cliente oficial de LinkedIn.
    """

    ######################################################################

    def __init__(self):

        self.dry_run = CONFIG.LINKEDIN_DRY_RUN

        self.access_token = CONFIG.LINKEDIN_ACCESS_TOKEN

        self.person_urn = CONFIG.LINKEDIN_PERSON_URN

##########################################################################

    def dry_publish(

        self,

        text,

        image,

    ):

        """
        Simulación de publicación.
        """

        filename = FILES.new_post_filename()

        data = {

            "date":

                datetime.now().isoformat(),

            "text":

                text,

            "image":

                str(image),

            "status":

                "DRY_RUN"

        }

        FILES.save_json(

            filename,

            data,

        )

        LOG.info(

            "Publicación simulada."

        )

        return {

            "url":

                filename.as_posix()

        }

##########################################################################

    def real_publish(

        self,

        text,

        image,

    ):

        """
        Implementación API LinkedIn.

        Se desarrollará completamente
        en la versión siguiente.
        """

        raise NotImplementedError(

            "Pendiente implementación OAuth2."

        )

##########################################################################

    def publish(

        self,

        text,

        image,

    ):

        if self.dry_run:

            return self.dry_publish(

                text,

                image,

            )

        return self.real_publish(

            text,

            image,

        )

##########################################################################

    def info(

        self,

    ):

        return {

            "dry_run":

                self.dry_run,

            "provider":

                "LinkedIn"

        }

##########################################################################

LINKEDIN = LinkedInClient()

