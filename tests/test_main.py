from main import create_initial_state
from state import WorkflowStatus, ReviewDecision


def test_create_initial_state():
    state = create_initial_state("Prueba")

    assert state["tema"] == "Prueba"
    assert state["workflow_status"] == WorkflowStatus.RESEARCH
    assert state["decision"] == ReviewDecision.REJECTED
    assert state["iteracion"] == 1
    assert isinstance(state["historial"], list)
    assert state["errores"] == []
