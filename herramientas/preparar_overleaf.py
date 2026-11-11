"""Empaqueta solo los archivos necesarios para compilar el artículo en Overleaf."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "informe/latex"
TARGET = ROOT / "informe/avance_overleaf.zip"


def main():
    files = [SOURCE / "main.tex", SOURCE / "referencias.bib"]
    files.extend(sorted((SOURCE / "resultados").glob("*")))
    if not (SOURCE / "resultados/resultados.tex").is_file():
        raise SystemExit("Primero ejecuta: python -m proyecto.experimento")
    with ZipFile(TARGET, "w", ZIP_DEFLATED) as archive:
        for path in files:
            if path.is_file():
                archive.write(path, path.relative_to(SOURCE))
        archive.writestr("LEEME.txt", "Archivo principal: main.tex\n"
                         "Compilador: pdfLaTeX; bibliografia: BibTeX (IEEEtran).\n"
                         "Los resultados ya estan incluidos; no es necesario ejecutar Python en Overleaf.\n")
    print(f"Paquete de Overleaf: {TARGET}")


if __name__ == "__main__":
    main()
