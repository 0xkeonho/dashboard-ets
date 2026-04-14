# MGH Analytics Dashboard

Dashboard analitik untuk Massachusetts General Hospital.

## Cara Menjalankan

### Menggunakan uv (Recommended)

```bash
git clone https://github.com/0xkeonho/dashboard-ets.git
cd dashboard-ets
uv venv && uv pip install -r requirements.txt
streamlit run app.py
```

Atau langsung:
```bash
uv run streamlit run app.py
```

### Menggunakan pip

```bash
git clone https://github.com/0xkeonho/dashboard-ets.git
cd dashboard-ets
pip install -r requirements.txt
streamlit run app.py
```

## Struktur

- `app.py` - Entry point
- `pages/` - Halaman dashboard
- `data/` - Dataset CSV
- `utils.py` - Helper functions
