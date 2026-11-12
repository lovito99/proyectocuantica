PYTHON ?= .venv/bin/python

.PHONY: all instalar pruebas experimento informe presentacion ppt overleaf

all: pruebas experimento informe presentacion overleaf

instalar:
	uv venv --python 3.12 .venv
	uv pip install --python $(PYTHON) -r requirements.txt

pruebas:
	$(PYTHON) -m pytest -q

experimento:
	$(PYTHON) -m proyecto.experimento

informe:
	latexmk -cd -pdf -interaction=nonstopmode -halt-on-error informe/latex/main.tex
	$(PYTHON) -c "from shutil import copyfile; copyfile('informe/latex/main.pdf', 'informe/avance_circuitos_reversibles.pdf')"

presentacion:
	latexmk -cd -pdf -interaction=nonstopmode -halt-on-error ppt/diapositivas.tex

ppt: presentacion

overleaf:
	$(PYTHON) herramientas/preparar_overleaf.py
