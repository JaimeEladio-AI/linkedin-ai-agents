"""
==========================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
memory/article_memory.py

Descripción
-----------

Memoria permanente de publicaciones.

Este componente almacena el conocimiento histórico del sistema
para evitar repetir contenido y apoyar la planificación editorial.

Cada publicación queda registrada con sus principales metadatos.

==========================================================================

"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List
from typing import Optional

from tools.filesystem import FILES


##########################################################################
# Registro individual
##########################################################################

@dataclass(slots=True)
class ArticleRecord:
    """
    Representa una publicación realizada.
    """

    fecha: str

    tema: str

    titulo: str

    resumen: str

    hashtags: List[str]

    keywords: List[str]

    imagen: str

    cta: str

    score: int

    url_linkedin: str

    modelo: str

    ##########################################################################

class ArticleMemory:

    """
    Base histórica de publicaciones.
    """

    FILE_NAME = "history.json"

    ######################################################################

    def __init__(self):

        self.file = FILES.memory(
            self.FILE_NAME
        )

        self._articles = []

        self.load()

    ######################################################################

    def load(self):

        data = FILES.load_json(
            self.file
        )

        self._articles = []

        for item in data:

            self._articles.append(

                ArticleRecord(**item)

            )

    ######################################################################

    def save(self):

        FILES.save_json(

            self.file,

            [

                asdict(article)

                for article in self._articles

            ]

        )

##########################################################################

    def add(

        self,

        article: ArticleRecord

    ):

        self._articles.append(

            article

        )

        self.save()

##########################################################################

    def all(self):

        return list(self._articles)


##########################################################################

    def search_by_topic(

        self,

        topic: str

    ):

        return [

            article

            for article in self._articles

            if topic.lower()

            in article.tema.lower()

        ]


##########################################################################

    def search_by_hashtag(

        self,

        hashtag: str

    ):

        return [

            article

            for article in self._articles

            if hashtag

            in article.hashtags

        ]

##########################################################################

    def search_by_keyword(

        self,

        keyword: str

    ):

        return [

            article

            for article in self._articles

            if keyword

            in article.keywords

        ]

##########################################################################

    def last(self):

        if not self._articles:

            return None

        return self._articles[-1]

##########################################################################

    def count(self):

        return len(

            self._articles

        )

##########################################################################

    def clear(self):

        self._articles.clear()

        self.save()

##########################################################################

ARTICLE_MEMORY = ArticleMemory()

