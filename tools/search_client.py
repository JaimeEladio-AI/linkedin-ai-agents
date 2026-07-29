"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
tools/search_client.py

Descripción
-----------

Cliente unificado para búsquedas Web.

Objetivos

✓ Desacoplar el proveedor de búsqueda
✓ Permitir cambiar Tavily, Brave, SerpAPI o Google
✓ Centralizar las consultas
✓ Facilitar pruebas unitarias

Versión 1.0

Proveedor recomendado:
Tavily

==============================================================================

"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from typing import List
from typing import Dict
from typing import Any

from tools.logger import LOG
from config import CONFIG

##########################################################################
# Interfaz
##########################################################################

class SearchProvider(ABC):

    """
    Interfaz base para cualquier
    proveedor de búsqueda.
    """

    @abstractmethod
    def search(

        self,

        query: str,

        max_results: int = 5,

    ) -> List[Dict[str, Any]]:

        pass

##########################################################################
# Mock Provider
##########################################################################

class MockSearchProvider(

    SearchProvider

):

    """
    Implementación temporal.

    Será reemplazada por Tavily.
    """

    def search(

        self,

        query,

        max_results=5,

    ):

        LOG.info(

            f"Mock Search: {query}"

        )

        return [

            {

                "title": "Resultado de ejemplo",

                "url": "https://example.com",

                "content":

                    "Este es un resultado temporal.",

            }

        ]

##########################################################################
# Search Client
##########################################################################

class SearchClient:

    """
    Cliente desacoplado.
    """

    def __init__(

        self,

        provider: SearchProvider,

    ):

        self.provider = provider

    ######################################################################

    def search(

        self,

        query: str,

        max_results: int = 5,

    ):

        LOG.info(

            f"Buscando: {query}"

        )

        return self.provider.search(

            query,

            max_results,

        )

##########################################################################
# Instancia Global
##########################################################################

SEARCH = SearchClient(

    MockSearchProvider()

)
