from flask import Flask, request, render_template, send_file, redirect, url_for
import csv
import io

app = Flask(__name__, template_folder='templates', static_folder='static')

# Default sample metrics for the five proposed models
DEFAULT_METRICS = [
    {"Model": "Large Language Model (LLM)", "Accuracy": "81.50", "Precision": "0.82", "Recall": "0.81", "F1-Score": "0.82"},
    {"Model": "Neural Network", "Accuracy": "85.20", "Precision": "0.86", "Recall": "0.85", "F1-Score": "0.85"},
    {"Model": "NLP Model", "Accuracy": "88.40", "Precision": "0.89", "Recall": "0.88", "F1-Score": "0.88"},
    {"Model": "Bytecode Model", "Accuracy": "92.10", "Precision": "0.93", "Recall": "0.92", "F1-Score": "0.92"},
    {"Model": "Control Flow Graph Model", "Accuracy": "94.80", "Precision": "0.95", "Recall": "0.95", "F1-Score": "0.95"},
]

def parse_csv_stream(stream) -> list:
    try:
        text = stream.read().decode('utf-8') if hasattr(stream, 'read') else stream
        reader = csv.DictReader(io.StringIO(text))
        rows = []
        for r in reader:
            # ensure keys we expect exist
            if not r.get('Model'):
                continue
            rows.append({
                'Model': r.get('Model','').strip(),
                'Accuracy': r.get('Accuracy','').strip(),
                'Precision': r.get('Precision','').strip(),
                'Recall': r.get('Recall','').strip(),
                'F1-Score': r.get('F1-Score','').strip(),
            })
        return rows
    except Exception:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    metrics = DEFAULT_METRICS.copy()
    message = None
    if request.method == 'POST':
        # file upload
        f = request.files.get('file')
        if f and f.filename:
            parsed = parse_csv_stream(f.stream)
            if parsed:
                metrics = parsed
                message = f"Loaded {len(parsed)} rows from {f.filename}"
            else:
                message = "Uploaded file could not be parsed. Ensure CSV with header: Model,Accuracy,Precision,Recall,F1-Score"
        else:
            # manual form fields
            rows = []
            i = 0
            while True:
                prefix = f"row_{i}_model"
                if prefix not in request.form:
                    break
                m = request.form.get(f"row_{i}_model",""
                    ).strip()
                if not m:
                    break
                rows.append({
                    'Model': m,
                    'Accuracy': request.form.get(f"row_{i}_acc",""),
                    'Precision': request.form.get(f"row_{i}_prec",""),
                    'Recall': request.form.get(f"row_{i}_rec",""),
                    'F1-Score': request.form.get(f"row_{i}_f1",""),
                })
                i += 1
            if rows:
                metrics = rows
                message = f"Loaded {len(rows)} rows from form"
    return render_template('index.html', metrics=metrics, message=message)

@app.route('/sample')
def sample():
    csv_text = 'Model,Accuracy,Precision,Recall,F1-Score\n'
    for r in DEFAULT_METRICS:
        csv_text += f"{r['Model']},{r['Accuracy']},{r['Precision']},{r['Recall']},{r['F1-Score']}\n"
    return (csv_text, 200, {'Content-Type': 'text/csv; charset=utf-8', 'Content-Disposition': 'attachment; filename="sample_metrics.csv"'})

if __name__ == '__main__':
    # Run locally: open http://127.0.0.1:5000/
    app.run(host='127.0.0.1', port=5000, debug=True)
