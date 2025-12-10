import pytest
import utils.generate_summary_html as generate_html
# Lista de archivos de pruebas a ejecutar
test_files = [
    "tests/api/test_api_with_faker.py",
	"./tests/api/test_reqres_api.py",                            
	"./tests/api/test_reqres_api.py",
	"./tests/api/test_reqres_api.py",
	"./tests/ui/test_checkout_flow.py",
	"./tests/ui/test_checkout_negative.py",
	"./tests/ui/test_demo_failure.py",
	"./tests/ui/test_inventory.py",
	"./tests/ui/test_login.py"
]

# Argumentos para ejecutar las pruebas: archivos + reporte HTML
pytest_args = test_files + ["--html=reports/report.html","--self-contained-html","-v"]
pytest.main(pytest_args)
generate_html.generate_html_from_junit ("reports/junit_results.xml", "reports/resumen_casos.html")