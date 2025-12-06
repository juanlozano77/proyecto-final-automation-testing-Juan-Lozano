# utils/generate_summary_html.py

from pathlib import Path
import xml.etree.ElementTree as ET
import html

def save_html_safely(html_path, html_content):
    p = Path(html_path)

    # Crear carpeta
    p.parent.mkdir(parents=True, exist_ok=True)

    # Si existe, eliminar (soluciona PermissionError)
    if p.exists():
        try:
            p.unlink()
        except Exception:
            pass

    # Guardar archivo
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_content)

def extraer_esperado_obtenido(message: str):
    """
    Intenta extraer 'Resultado esperado' y 'Resultado obtenido' del mensaje
    de error usando las cadenas 'Esperado' y 'Obtenido' que pusimos en los asserts.

    Si no encuentra nada, devuelve textos genéricos.
    """
    if not message:
        return "", ""

    # Normalizamos un poco
    msg = message.replace("\r\n", "\n")

    esperado = ""
    obtenido = ""

    # Buscar la línea donde aparece 'Esperado'
    for line in msg.split("\n"):
        line_stripped = line.strip()
        if line_stripped.lower().startswith("esperado"):
            # Ej: "Esperado: X" o "Esperado que contenga: 'X'"
            esperado = line_stripped
        if line_stripped.lower().startswith("obtenido"):
            obtenido = line_stripped

    # Si no encontramos, dejamos algo genérico
    if not esperado and "Esperado" in msg:
        esperado = "Esperado (ver detalle en mensaje de error)"
    if not obtenido and "Obtenido" in msg:
        obtenido = "Obtenido (ver detalle en mensaje de error)"

    return esperado, obtenido


def generate_html_from_junit(xml_path: str, html_path: str):
    xml_file = Path(xml_path)
    if not xml_file.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {xml_file}")

    tree = ET.parse(xml_file)
    root = tree.getroot()

    rows = []

    # Maneja tanto un testsuite raíz como múltiples
    for testcase in root.iter("testcase"):
        name = testcase.get("name", "")
        classname = testcase.get("classname", "")
        time = testcase.get("time", "0")

        status = "passed"
        failure_msg = ""
        skipped_msg = ""

        for child in testcase:
            if child.tag in ("failure", "error"):
                status = "failed"
                failure_msg = child.text or ""
                break
            if child.tag == "skipped":
                status = "skipped"
                skipped_msg = child.text or ""
                break

        # Extraer esperado / obtenido si falló
        esperado = ""
        obtenido = ""
        if status == "failed":
            esperado, obtenido = extraer_esperado_obtenido(failure_msg)

        # Si pasó, ponemos un texto genérico
        if status == "passed":
            esperado = "El sistema se comportó según lo esperado."
            obtenido = "Resultado conforme (sin desvíos detectados)."

        if status == "skipped":
            esperado = "El test fue marcado como 'skipped' (omitido)."
            obtenido = skipped_msg or "No se ejecutó este caso de prueba."

        rows.append(
            {
                "module": classname,
                "name": name,
                "status": status,
                "time": time,
                "esperado": esperado,
                "obtenido": obtenido,
            }
        )

    # Generar HTML
    html_lines = [
        "<html>",
        "<head>",
        "<meta charset='utf-8'>",
        "<title>Resumen de Casos de Prueba</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; margin: 20px; }",
        "h1 { margin-bottom: 10px; }",
        "table { border-collapse: collapse; width: 100%; font-size: 14px; }",
        "th, td { border: 1px solid #ccc; padding: 6px 8px; text-align: left; vertical-align: top; }",
        "th { background-color: #f5f5f5; }",
        ".passed { background-color: #d4edda; }",
        ".failed { background-color: #f8d7da; }",
        ".skipped { background-color: #fff3cd; }",
        ".status { font-weight: bold; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Resumen de Casos de Prueba</h1>",
        "<p>Este resumen muestra, para cada caso de prueba, el módulo, el nombre, el estado, la duración y, cuando aplica, el resultado esperado y el resultado obtenido.</p>",
        "<table>",
        "<tr>",
        "<th>Módulo</th>",
        "<th>Nombre del test</th>",
        "<th>Estado</th>",
        "<th>Duración (s)</th>",
        "<th>Resultado esperado</th>",
        "<th>Resultado obtenido</th>",
        "</tr>",
    ]

    for r in rows:
        status_class = r["status"]
        html_lines.append(
            f"<tr class='{status_class}'>"
            f"<td>{html.escape(r['module'])}</td>"
            f"<td>{html.escape(r['name'])}</td>"
            f"<td class='status'>{html.escape(r['status'].upper())}</td>"
            f"<td>{html.escape(r['time'])}</td>"
            f"<td>{html.escape(r['esperado'])}</td>"
            f"<td>{html.escape(r['obtenido'])}</td>"
            f"</tr>"
        )

    html_lines.extend(["</table>", "</body>", "</html>"])

    Path(html_path).write_text("\n".join(html_lines), encoding="utf-8")
    print(f"Resumen generado en: {html_path}")


if __name__ == "__main__":
    generate_html_from_junit("reports/junit_results.xml", "reports/resumen_casos.html")

