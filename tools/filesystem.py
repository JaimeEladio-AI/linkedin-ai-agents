"""
==========================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
tools/filesystem.py

Descripción
-----------

Este módulo centraliza todas las operaciones relacionadas con el
sistema de archivos.

Ningún otro componente del proyecto debe utilizar directamente:

    open(...)
    Path(...)
    os.makedirs(...)

Todas esas operaciones deben realizarse utilizando esta clase.

Ventajas

✓ Código desacoplado.
✓ Fácil mantenimiento.
✓ Fácil testing.
✓ Evita duplicación.
✓ Compatible con Google Colab.

==========================================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

from config import CONFIG


class FileSystem:
    """
    Clase encargada de administrar todos los archivos del proyecto.
    """

    ####################################################################
    # Constructor
    ####################################################################

    def __init__(self):

        self.output_dir = CONFIG.OUTPUT_DIR
        self.image_dir = CONFIG.IMAGE_DIR
        self.post_dir = CONFIG.POST_DIR
        self.log_dir = CONFIG.LOG_DIR
        self.memory_dir = CONFIG.MEMORY_DIR
        self.resource_dir = CONFIG.RESOURCE_DIR

    ####################################################################
    # Directorios
    ####################################################################

    def ensure_directories(self):
        """
        Garantiza que todos los directorios existan.
        """

        directories = [

            self.output_dir,

            self.image_dir,

            self.post_dir,

            self.log_dir,

            self.memory_dir,

            self.resource_dir,

        ]

        for directory in directories:

            directory.mkdir(
                parents=True,
                exist_ok=True
            )

    ####################################################################
    # JSON
    ####################################################################

    def save_json(
        self,
        filename: Path,
        data: dict
    ):

        filename.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    ####################################################################

    def load_json(
        self,
        filename: Path
    ) -> dict:

        if not filename.exists():

            return {}

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    ####################################################################
    # Texto
    ####################################################################

    def save_text(
        self,
        filename: Path,
        content: str
    ):

        filename.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        filename.write_text(
            content,
            encoding="utf-8"
        )

    ####################################################################

    def load_text(
        self,
        filename: Path
    ) -> str:

        if not filename.exists():

            return ""

        return filename.read_text(
            encoding="utf-8"
        )

    ####################################################################
    # Markdown
    ####################################################################

    def save_markdown(
        self,
        filename: Path,
        markdown: str
    ):

        self.save_text(
            filename,
            markdown
        )

    ####################################################################
    # Recursos
    ####################################################################

    def resource(
        self,
        filename: str
    ) -> Path:

        return self.resource_dir / filename

    ####################################################################
    # Memoria
    ####################################################################

    def memory(
        self,
        filename: str
    ) -> Path:

        return self.memory_dir / filename

    ####################################################################
    # Logs
    ####################################################################

    def log(
        self,
        filename: str
    ) -> Path:

        return self.log_dir / filename

    ####################################################################
    # Imágenes
    ####################################################################

    def image(
        self,
        filename: str
    ) -> Path:

        return self.image_dir / filename

    ####################################################################
    # Publicaciones
    ####################################################################

    def post(
        self,
        filename: str
    ) -> Path:

        return self.post_dir / filename

    ####################################################################
    # Fecha actual
    ####################################################################

    @staticmethod
    def timestamp():

        return datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

    ####################################################################
    # Nombre automático para publicación
    ####################################################################

    def new_post_filename(self):

        return self.post(
            f"linkedin_post_{self.timestamp()}.md"
        )

    ####################################################################
    # Nombre automático para imagen
    ####################################################################

    def new_image_filename(self):

        return self.image(
            f"linkedin_image_{self.timestamp()}.png"
        )

    ####################################################################
    # Estado del Workflow
    ####################################################################

    def new_state_filename(self):

        return self.post(
            f"workflow_state_{self.timestamp()}.json"
        )

    ####################################################################
    # Resultado del Editor
    ####################################################################

    def new_review_filename(self):

        return self.post(
            f"review_{self.timestamp()}.json"
        )


##########################################################################
# Instancia Singleton
##########################################################################

FILES = FileSystem()

FILES.ensure_directories()
