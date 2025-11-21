# Minimal PyPI Stats API Wrapper

A lightweight FastAPI service that proxies requests to the official **PyPIStats API**.

This wrapper simplifies interaction with `pypistats.org/api` by providing clean, documented endpoints with automatic parameter forwarding and consistent error handling.

---

## 🚀 Features

* FastAPI-powered microservice
* Proxies multiple PyPIStats endpoints
* Simple query parameter passthrough
* Automatic HTTP error forwarding
* Interactive API docs via **Swagger UI** at `/docs`

---

## 📦 Requirements

* Python 3.10+
* `fastapi`
* `uvicorn`
* `httpx`

Install dependencies:

```bash
pip install fastapi uvicorn httpx
```

---

## ▶️ Running the Server

Start the API locally using Uvicorn:

```bash
uvicorn api.index:app --reload
```

By default, the API will run at:

```
http://127.0.0.1:8000
```

Swagger UI will be available at:

```
http://127.0.0.1:8000/docs
```

---

## 📡 Available Endpoints

### Root

`GET /`
Returns basic metadata and route references.

---

### 🔢 Download Statistics

#### **Recent Downloads**

`GET /api/packages/{package}/recent`

Query params:

* `period`: `day`, `week`, or `month`

Example:

```
/api/packages/fastapi/recent?period=month
```

---

#### **Overall Daily Downloads**

`GET /api/packages/{package}/overall`

Query params:

* `mirrors`: `true` or `false`

Example:

```
/api/packages/httpx/overall?mirrors=false
```

---

### 🧩 Breakdown Endpoints

#### **By Python Major Version**

`GET /api/packages/{package}/python_major`

Query params:

* `version`: e.g. `3`

---

#### **By Python Minor Version**

`GET /api/packages/{package}/python_minor`

Query params:

* `version`: e.g. `3.10`

---

#### **By Operating System**

`GET /api/packages/{package}/system`

Query params:

* `os`: `Windows`, `Linux`, `Darwin`, etc.

---

## 🔧 How It Works

The proxy forwards requests directly to:

```
https://pypistats.org/api/
```

For each route:

* Incoming parameters are forwarded unchanged
* Errors from the external API are passed back to the client

Core forwarding logic:

```python
async def forward_request(endpoint: str, params: dict):
    url = f"{BASE_EXTERNAL_API}/{endpoint}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    if response.status_code != 200:
        ...
    return response.json()
```

---

## 📝 License

MIT (feel free to modify and use)

---

## 🙌 Notes

This service acts only as a thin wrapper. All data is sourced from **pypistats.org**.
