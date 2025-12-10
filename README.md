# 🧪 Trabajo Final Integrador – Framework de Automatización de Pruebas

## 🎯 Propósito del Proyecto
Este proyecto implementa un framework completo de automatización que integra:
- Pruebas de UI con Selenium WebDriver sobre SauceDemo.
- Pruebas de API con Requests utilizando JSONPlaceholder.
- Arquitectura escalable con Page Object Model (POM).
- Gestión de datos (CSV/JSON), logs, screenshots automáticos y reportes HTML + XML.
- Casos positivos, negativos e intencionalmente fallidos para validar el comportamiento del framework frente a errores.

## 🛠️ Tecnologías Utilizadas
- Python 3.10+
- Selenium WebDriver + WebDriver Manager
- Requests
- Faker (datos dinámicos)
- Pytest
- pytest-html y JUnit XML
- Page Object Model (POM)

## 📂 Estructura del Proyecto
sauce-automation/

├── pages/ (POM)

├── tests/

│   ├── ui/

│   └── api/

├── utils/

├── resources/

│   └── test_data/

├── screenshots/

├── logs/

├── reports/

├── conftest.py

├── pytest.ini

├── requirements.txt

└── README.md


## 📦 Instalación
```
pip install -r requirements.txt
```

## ▶️ Ejecución de Pruebas
```
python run_test.py
```

## 🔍 Tipos de Pruebas
### ✔ UI Positivas
- Login correcto  
- Ordenamiento de productos  
- Flujo completo de compra  

### ❌ UI Negativas
- Login inválido  
- Checkout sin completar datos  

### 🧨 Test UI que falla intencionalmente
`test_demo_failure.py` — Diseñado para fallar y demostrar:
- Screenshot automático  
- Log de error  
- Evidencia en HTML  

### 🌐 Pruebas de API
✔ GET / POST con JSONPlaceholder  
✔ POST con Faker (datos dinámicos)  
❌ DELETE inválido  
🧨 Test API que falla intencionalmente  

## 📸 ¿Qué ocurre cuando algo falla?
El framework captura:
1. **Screenshot automático** — guardado en `/screenshots/`  
2. **Registro detallado en logs** — `/logs/execution.log`  
3. **Reporte HTML enriquecido con evidencia visual**  
4. Mensajes claros: *Esperado vs Obtenido*  

## 📊 Interpretación de Reportes
### Reporte HTML (`report.html`)
Incluye:
- Estado del test (PASSED/FAILED)  
- Capturas de pantalla  
- Log asociado  
- Trazas y detalles  

### Reporte XML (JUnit)
- Compatible con CI/CD  
- Base para reportes ejecutivos  

### Reporte Ejecutivo (`resumen_casos.html`)
- Tabla con: nombre del test, estado y duración  
- Ideal para presentaciones  

## 👨‍💻 Autor
**Juan Lozano**  
Proyecto Final – Automatización de Pruebas

### Agradecimientos 🙏 

Profesor: ***José Montezuma*** 

Mentora: ***Valentina Lembo** 
