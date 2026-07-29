"""
========================================================================

Proyecto:
LinkedIn AI MultiAgent

Archivo:
state.py

Descripción
-----------

Este archivo define el "estado" del grafo (StateGraph).

En LangGraph el estado es el objeto compartido entre todos los nodos.

Cada agente recibe el estado,
lo modifica y devuelve únicamente los cambios.

En proyectos pequeños suele utilizarse un TypedDict con
3 ó 4 variables.

En este proyecto construiremos un estado profesional,
pensado para múltiples agentes y futuras ampliaciones.

========================================================================
"""

from __future__ import annotations

from enum import Enum
from typing import TypedDict
#from typing import Optional
from typing import List
from typing import Dict
from typing import Any

from pydantic import BaseModel
from pydantic import Field

#########################################################################
# Estados posibles del flujo
#########################################################################

class WorkflowStatus(str, Enum):
    """
    Estado general del proceso.
    """

    START = "START"

    RESEARCH = "RESEARCH"

    CONTENT_ARCHITECT = "CONTENT_ARCHITECT"

    CREATOR = "CREATOR"

    SEO = "SEO"

    LEGAL = "LEGAL"

    TECHNICAL = "TECHNICAL"

    EDITOR = "EDITOR"

    IMAGE = "IMAGE"

    PUBLISHER = "PUBLISHER"

    FINISHED = "FINISHED"

    FAILED = "FAILED"

    #########################################################################
# Resultado del Editor
#########################################################################

class ReviewDecision(str, Enum):
    """
    Decisión del Editor.
    """

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"

    NEEDS_REWRITE = "NEEDS_REWRITE"

    #########################################################################
# Puntaje entregado por el Editor
#########################################################################

class ScoreCard(BaseModel):

    claridad: int = Field(default=0, ge=0, le=10)

    rigor: int = Field(default=0, ge=0, le=10)

    seo: int = Field(default=0, ge=0, le=10)

    legal: int = Field(default=0, ge=0, le=10)

    originalidad: int = Field(default=0, ge=0, le=10)

    engagement: int = Field(default=0, ge=0, le=10)

    valor: int = Field(default=0, ge=0, le=10)

    imagen: int = Field(default=0, ge=0, le=10)

    comentarios: str = ""

    @property
    def total(self):

        return (
            self.claridad
            + self.rigor
            + self.seo
            + self.legal
            + self.originalidad
            + self.engagement
            + self.valor
            + self.imagen
        )

    #########################################################################
# Resultado Investigación Mercado
#########################################################################

class MarketResearch(BaseModel):

    tema: str = ""

    resumen: str = ""

    #tendencias: List[str] = []
    #noticias: List[str] = []
    #empresas: List[str] = []
    #competidores: List[str] = []
    #casos_uso: List[str] = []
    #keywords: List[str] = []
    #hashtags: List[str] = []
    #referencias: List[str] = []

    tendencias: List[str] = Field(default_factory=list)
    noticias: List[str] = Field(default_factory=list)
    empresas: List[str] = Field(default_factory=list)
    competidores: List[str] = Field(default_factory=list)
    casos_uso: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    hashtags: List[str] = Field(default_factory=list)
    referencias: List[str] = Field(default_factory=list)




    #########################################################################
# Resultado SEO
#########################################################################

class SEOResult(BaseModel):

    hook: str = ""

    titulo: str = ""

    cta: str = ""

    #hashtags: List[str] = []
    #keywords: List[str] = []
    hashtags: List[str] = Field(default_factory=list)

    keywords: List[str] = Field(default_factory=list)

    prompt_imagen: str = ""

#########################################################################
# Resultado Legal
#########################################################################

class LegalReview(BaseModel):

    aprobado: bool = False

    #observaciones: List[str] = []

    #riesgos: List[str] = []

    #recomendaciones: List[str] = []
    observaciones: List[str] = Field(default_factory=list)

    riesgos: List[str] = Field(default_factory=list)

    recomendaciones: List[str] = Field(default_factory=list)



#########################################################################
# Revisión Técnica IA
#########################################################################

class TechnicalReview(BaseModel):

    aprobado: bool = False

    #errores: List[str] = []

    #mejoras: List[str] = []

    errores: List[str] = Field(default_factory=list)

    mejoras: List[str] = Field(default_factory=list)

#########################################################################
# Estado principal
#########################################################################

class LinkedinState(TypedDict):

    ############################################################
    # Tema
    ############################################################

    tema: str

    audiencia: str

    objetivo: str

    ############################################################
    # Estado del Workflow
    ############################################################

    workflow_status: WorkflowStatus

    ############################################################
    # Arquitecto
    ############################################################

    arquitectura_contenido: Dict[str, Any]

    ############################################################
    # Mercado
    ############################################################

    mercado: MarketResearch

    ############################################################
    # Publicación
    ############################################################

    borrador: str

    borrador_anterior: str

    version_final: str
    comentarios_editor: List[str]
    ############################################################
    # SEO
    ############################################################

    seo: SEOResult
    seo_raw: Dict[str, Any]
    ############################################################
    # Legal
    ############################################################

    legal: LegalReview
    legal_raw: Dict[str, Any]
    ############################################################
    # Técnico
    ############################################################

    tecnico: TechnicalReview
    technical_raw: Dict[str, Any]
    ############################################################
    # Imagen
    ############################################################

    prompt_imagen: str

    imagen_url: str
    ############################################################
    # Salida
    ############################################################

    linkedin_url: str

    image_path: str
    ############################################################
    # Editor
    ############################################################

    score: ScoreCard

    editor: Dict[str, Any]

    decision: ReviewDecision

    ############################################################
    # Control
    ############################################################

    iteracion: int
    fecha_inicio: str

    fecha_fin: str
    max_iteraciones: int

    aprobado: bool

    publicado: bool

    ############################################################
    # Historial
    ############################################################

    historial: List[Dict[str, Any]]

    ############################################################
    # Logs
    ############################################################

    mensajes: List[str]

    errores: List[str]

