# LinkedIn AI MultiAgent

Este repositorio contiene un flujo de trabajo multiagente para generar contenido de LinkedIn usando LangGraph, Ollama y OpenAI.

## Cómo probar el proyecto

### 1. Ejecutar localmente

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

### 2. Probar en Google Colab

Abre el notebook:

https://colab.research.google.com/github/JaimeEladio-AI/linkedin-ai-agents/blob/main/run_checks.ipynb

Luego ejecuta todas las celdas. El notebook:

- clona el repositorio si no está presente
- instala dependencias
- compila `main.py`
- ejecuta pruebas con `pytest`
- lista los archivos del repositorio

## Pruebas incluidas

- `tests/test_main.py`: prueba básica de creación del estado inicial

## Notas

- El proyecto aún no tiene pruebas completas para todos los agentes.
- `run_checks.ipynb` está diseñado para verificar el entorno y las dependencias en Colab.
