import os
import json
from pathlib import Path
from typing import List, Dict, Optional

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import ijson  # streaming JSON parser

DATA_ROOT = Path("camara/legislaturas")

# ---------- JSON HELPERS ----------

def fetch_json(filepath: Path):
    try:
        with filepath.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error for {filepath}: {e}")
        return None


def read_ndjson_limited(path: Path, max_entries: int) -> List[Dict]:
    results = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= max_entries:
                break
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                results.append(obj)
            except json.JSONDecodeError:
                continue
    return results


def read_json_array_limited(path: Path, max_entries: int, key: Optional[str] = None) -> List[Dict]:
    results = []
    with path.open("r", encoding="utf-8") as f:
        prefix = f"{key}.item" if key else "item"
        for obj in ijson.items(f, prefix):
            results.append(obj)
            if len(results) >= max_entries:
                break
    return results


def scan_info_files_limited(leg: int, max_entries: int):
    info_dir = DATA_ROOT / str(leg) / "proposicoes"
    results = []
    if not info_dir.exists():
        return results
    for i, entry in enumerate(sorted(info_dir.iterdir())):
        if i >= max_entries:
            break
        info_file = entry / "info.json"
        if info_file.exists():
            data = fetch_json(info_file)
            if not data:
                continue
            dados = data.get("dados") if isinstance(data, dict) and "dados" in data else data
            results.append(dados)
    return results


# ---------- LOAD FUNCTIONS ----------

def load_proposicoes_list(legislatura: int, max_entries: int = 1000) -> List[Dict]:
    summary_path = DATA_ROOT / str(legislatura) / "proposicoes.json"
    if not summary_path.exists():
        return scan_info_files_limited(legislatura, max_entries)

    with summary_path.open("r", encoding="utf-8") as f:
        first_bytes = f.read(2048)
    if "\n" in first_bytes and not first_bytes.lstrip().startswith(("{", "[")):
        return read_ndjson_limited(summary_path, max_entries)

    try:
        return read_json_array_limited(summary_path, max_entries, key="dados")
    except Exception:
        return read_json_array_limited(summary_path, max_entries, key=None)


def load_proposicoes_dataframe(legislatura: int, max_entries: int = 1000) -> pd.DataFrame:
    items = load_proposicoes_list(legislatura, max_entries)
    enriched = []

    for item in items:
        row = {
            "id": item.get("id"),
            "siglaTipo": item.get("siglaTipo"),
            "codTipo": item.get("codTipo"),
            "numero": item.get("numero"),
            "ano": item.get("ano"),
            "ementa": item.get("ementa") or "",
            "descricaoTipo": item.get("descricaoTipo", ""),
            "ementaDetalhada": None,
            "dataApresentacao": None,
            "descricaoTramitacao": None,
            "despacho": None,
            # "urlInteiroTeor": None,  # COMMENTED OUT
        }

        if row["id"] is not None:
            info_path = DATA_ROOT / str(legislatura) / "proposicoes" / str(row["id"]) / "info.json"
            info = fetch_json(info_path)
            if info:
                dados = info.get("dados") if isinstance(info, dict) and "dados" in info else info
                if isinstance(dados, dict):
                    row["ementaDetalhada"] = dados.get("ementaDetalhada") or row["ementa"]
                    row["dataApresentacao"] = dados.get("dataApresentacao")
                    status = dados.get("statusProposicao") or {}
                    if isinstance(status, dict):
                        row["descricaoTramitacao"] = status.get("descricaoTramitacao") or status.get("descricaoSituacao")
                        row["despacho"] = status.get("despacho")
                    # row["urlInteiroTeor"] = dados.get("urlInteiroTeor")  # COMMENTED OUT
                    if dados.get("descricaoTipo"):
                        row["descricaoTipo"] = dados.get("descricaoTipo")

        enriched.append(row)

    if not enriched:
        return pd.DataFrame()

    df = pd.DataFrame(enriched)
    df = df.sort_values(by=["ano", "numero"], ascending=[False, False], na_position="last").reset_index(drop=True)
    return df


# ---------- DASH APP ----------

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard: Proposições na Câmara dos Deputados"),
    html.Label("Selecione a Legislatura:"),
    dcc.Dropdown(
        id='leg-dropdown',
        options=[{'label': str(x), 'value': x} for x in (53, 54, 55, 56, 57)],
        value=57,
        clearable=False
    ),
    html.Label("Limite de proposições:"),
    dcc.Input(id='max-entries', type='number', value=1000, min=10, step=100),

    dcc.Graph(id='proposicoes-graph'),
    html.Div(id='tabela-proposicoes')
])


@app.callback(
    [Output('proposicoes-graph', 'figure'),
     Output('tabela-proposicoes', 'children')],
    [Input('leg-dropdown', 'value'),
     Input('max-entries', 'value')]
)
def update_proposicoes_dashboard(legislatura, max_entries):
    df = load_proposicoes_dataframe(legislatura, max_entries)

    if df.empty:
        fig = px.bar(title=f"Nenhum dado disponível para a legislatura {legislatura}")
        return fig, html.P("Erro ao carregar dados ou nenhum dado encontrado.")

    # Prepare bar chart: X = siglaTipo, hover shows descricaoTipo
    count_df = df.groupby(['siglaTipo', 'descricaoTipo']).size().reset_index(name='Contagem')
    fig = px.bar(
        count_df,
        x='siglaTipo',  # short sigla on axis
        y='Contagem',
        color='siglaTipo',
        text='Contagem',
        hover_data={'descricaoTipo': True, 'siglaTipo': True},
        title=f"Contagem de Proposições por Tipo (Leg. {legislatura}, máx. {max_entries})"
    )
    fig.update_traces(textposition='outside')

    # Table (without urlInteiroTeor)
    table_df = df[[
        "id", "siglaTipo", "descricaoTipo", "numero", "ano",
        "ementa", "ementaDetalhada", "dataApresentacao",
        "descricaoTramitacao", "despacho"
    ]].copy()

    # Shorten text
    table_df["ementa"] = table_df["ementa"].apply(lambda x: x if len(x) <= 120 else x[:120] + "...")
    table_df["ementaDetalhada"] = table_df["ementaDetalhada"].apply(lambda x: x if x and len(x) <= 200 else (x[:200] + "..." if x else ""))

    # DataTable with sorting
    table = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in table_df.columns],
        data=table_df.to_dict("records"),
        sort_action="native",
        page_size=200,
        style_table={'overflowX': 'auto', 'width': '100%'},
        style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto'},
        style_header={'fontWeight': 'bold'},
    )

    return fig, table


if __name__ == "__main__":
    app.run(debug=True)
