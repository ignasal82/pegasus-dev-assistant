"""Pruebas de chunking: sin red."""

from rag import config
from rag.chunking import MAX_CHARS, chunk_file, split_markdown


def test_documento_con_headings_genera_varios_chunks():
    text = "# Título\n\nIntro corta.\n\n## Sección A\n\nContenido A.\n\n## Sección B\n\nContenido B."
    chunks = split_markdown(text, "doc/prueba.md")
    assert len(chunks) >= 3
    headings = [c.heading for c in chunks]
    assert "Sección A" in headings
    assert "Sección B" in headings


def test_chunks_conservan_source():
    text = "## Único\n\nAlgo."
    chunks = split_markdown(text, "doc/conocimiento/faq.md")
    assert all(c.source == "doc/conocimiento/faq.md" for c in chunks)


def test_seccion_larga_se_parte_con_limite():
    parrafos = "\n\n".join(f"Párrafo {i} " + "x" * 200 for i in range(12))
    text = f"## Larga\n\n{parrafos}"
    chunks = split_markdown(text, "doc/prueba.md")
    assert len(chunks) > 1
    # margen por el solapamiento
    assert all(len(c.text) <= MAX_CHARS + 300 for c in chunks)


def test_documento_sin_headings_no_se_pierde():
    text = "Texto plano sin encabezados."
    chunks = split_markdown(text, "doc/plano.md")
    assert len(chunks) == 1
    assert chunks[0].text == text


def test_chunk_file_usa_ruta_relativa_posix():
    faq = config.KNOWLEDGE_DIR / "faq.md"
    chunks = chunk_file(faq, config.REPO_ROOT)
    assert chunks, "faq.md debería producir fragmentos"
    assert chunks[0].source == "doc/conocimiento/faq.md"


def test_kb_completa_produce_fragmentos_de_las_cinco_fuentes():
    sources = set()
    for path in config.knowledge_files():
        for chunk in chunk_file(path, config.REPO_ROOT):
            sources.add(chunk.source)
    assert len(sources) == 5
