"""
==============================================================================
Proyecto:
LinkedIn AI MultiAgent

Archivo:
tools/scoring.py

Descripción
-----------

Motor de evaluación de publicaciones LinkedIn.

Este componente calcula un puntaje objetivo para decidir si una
publicación puede ser aprobada o debe regresar al Agente Creador
para una nueva iteración.

El puntaje máximo es 100 puntos.

==============================================================================

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from tools.logger import LOG

##########################################################################
# Criterio de evaluación
##########################################################################

@dataclass(slots=True)
class ScoreCriterion:

    """
    Representa un criterio de evaluación.
    """

    name: str

    weight: int

    passed: bool

    observations: str = ""

##########################################################################

@dataclass(slots=True)
class ScoreResult:

    total: int

    maximum: int

    percentage: float

    approved: bool

    observations: List[str]

##########################################################################

class ScoreEngine:

    """
    Calcula el puntaje de una publicación.
    """

    PASS_SCORE = 85

    ######################################################################

    def calculate(

        self,

        criteria: List[ScoreCriterion],

    ) -> ScoreResult:

        total = 0

        maximum = 0

        observations = []

        for criterion in criteria:

            maximum += criterion.weight

            if criterion.passed:

                total += criterion.weight

            elif criterion.observations:

                observations.append(

                    criterion.observations

                )

        percentage = round(

            total / maximum * 100,

            2,

        )

        approved = (

            percentage >= self.PASS_SCORE

        )

        LOG.info(

            f"Score: {percentage}%"

        )

        return ScoreResult(

            total=total,

            maximum=maximum,

            percentage=percentage,

            approved=approved,

            observations=observations,

        )

##########################################################################

SCORING = ScoreEngine()

