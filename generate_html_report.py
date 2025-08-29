import json
from pathlib import Path
from datetime import datetime

# Diretórios
PROJECT_ROOT = Path(__file__).parent
JSON_FILE = PROJECT_ROOT / "reports" / "result.json"
HTML_FILE = PROJECT_ROOT / "reports" / "report.html"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"

# Carregar resultados do JSON
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# HTML básico
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Test Report</title>
<style>
  body {{ font-family: Arial, sans-serif; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
  th {{ background-color: #f2f2f2; }}
  tr.pass {{ background-color: #d4edda; }}
  tr.fail {{ background-color: #f8d7da; }}
</style>
</head>
<body>
<h2>Test Report</h2>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<table>
<tr>
<th>Status</th>
<th>Test</th>
<th>Screenshot</th>
</tr>
"""

# Preencher tabela
for test in data.get("tests", []):
    status = test.get("outcome", "unknown")
    nodeid = test.get("nodeid", "")
    
    # Se existir screenshot
    screenshot_name = test.get("extra_screenshot")  # ajuste conforme a chave usada no JSON
    if screenshot_name and (SCREENSHOTS_DIR / screenshot_name).exists():
        screenshot_link = f'<a href="../screenshots/{screenshot_name}">View</a>'
    else:
        screenshot_link = "—"
    
    row_class = "pass" if status == "passed" else "fail"
    html_content += f"<tr class='{row_class}'><td>{status}</td><td>{nodeid}</td><td>{screenshot_link}</td></tr>\n"

html_content += """
</table>
</body>
</html>
"""

# Salvar arquivo HTML
HTML_FILE.parent.mkdir(parents=True, exist_ok=True)
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML report generated: {HTML_FILE}")
