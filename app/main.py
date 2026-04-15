import time

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = FastAPI(title="TaskFlow", version="1.0.0")

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"],
)

TASKS = [
    {"id": 1, "title": "Prepare CI/CD demo", "done": False},
    {"id": 2, "title": "Write infrastructure docs", "done": True},
]


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    endpoint = request.url.path
    method = request.method
    start = time.perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=str(status_code)).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(time.perf_counter() - start)


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.get("/api/tasks")
async def list_tasks() -> JSONResponse:
    return JSONResponse({"items": TASKS})


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    html = """
    <!doctype html>
    <html lang='en'>
      <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>TaskFlow</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            margin: 2rem;
            background: #f7f9fb;
            color: #1f2937;
          }
          .card {
            max-width: 720px;
            background: white;
            padding: 1.5rem;
            border-radius: 14px;
            box-shadow: 0 6px 24px rgba(0,0,0,.08);
          }
          h1 { margin-top: 0; }
          li.done { text-decoration: line-through; color: #6b7280; }
          .badge {
            display: inline-block;
            padding: .3rem .6rem;
            border-radius: 999px;
            background: #e0f2fe;
            color: #0369a1;
            font-size: .8rem;
          }
        </style>
      </head>
      <body>
        <div class='card'>
          <span class='badge'>FastAPI • Docker • Kubernetes</span>
          <h1>TaskFlow</h1>
          <p>Simple task tracker used to demonstrate a full DevOps lifecycle.</p>
          <ul id='tasks'></ul>
        </div>
        <script>
          fetch('/api/tasks')
            .then(r => r.json())
            .then(data => {
              const list = document.getElementById('tasks');
              data.items.forEach(task => {
                const li = document.createElement('li');
                li.className = task.done ? 'done' : '';
                li.textContent = task.title;
                list.appendChild(li);
              });
            });
        </script>
      </body>
    </html>
    """
    return HTMLResponse(html)


@app.get("/metrics")
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
