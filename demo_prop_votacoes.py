import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from io import StringIO
import ijson

import dash
from dash import dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

DATA_LEG_ROOT = Path("camara/legislaturas")

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
            if i >= max_entries: break
            line = line.strip()
            if not line: continue
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return results

def read_json_array_limited(path: Path, max_entries: int, key: Optional[str] = None) -> List[Dict]:
    results = []
    with path.open("r", encoding="utf-8") as f:
        prefix = f"{key}.item" if key else "item"
        try:
            for obj in ijson.items(f, prefix):
                results.append(obj)
                if len(results) >= max_entries: break
        except ijson.common.IncompleteJSONError as e:
            print(f"Warning: Incomplete JSON file at {path}. Processed {len(results)} items. Error: {e}")
    return results

def scan_info_files_limited(info_dir: Path, max_entries: int):
    results = []
    if not info_dir.exists(): return results
    for i, entry in enumerate(sorted(info_dir.iterdir())):
        if i >= max_entries: break
        data = fetch_json(entry / "info.json")
        if not data: continue
        dados = data.get("dados") if isinstance(data, dict) and "dados" in data else data
        results.append(dados)
    return results

# ---------- DATA LOAD FUNCTIONS ----------
def load_proposicoes_list(legislatura: int, max_entries: int = 6000) -> List[Dict]:
    summary_path = DATA_LEG_ROOT / str(legislatura) / "proposicoes.json"
    if not summary_path.exists():
        return scan_info_files_limited(DATA_LEG_ROOT / str(legislatura) / "proposicoes", max_entries)
    with summary_path.open("r", encoding="utf-8") as f:
        first_bytes = f.read(2048)
    if "\n" in first_bytes and not first_bytes.lstrip().startswith(("{", "[")):
        return read_ndjson_limited(summary_path, max_entries)
    try: return read_json_array_limited(summary_path, max_entries, key="dados")
    except Exception: return read_json_array_limited(summary_path, max_entries, key=None)

def load_proposicoes_dataframe(legislatura: int, max_entries: int = 6000) -> pd.DataFrame:
    items = load_proposicoes_list(legislatura, max_entries)
    enriched = []
    for item in items:
        if not isinstance(item, dict): continue
        row = { "id": item.get("id"), "siglaTipo": item.get("siglaTipo"), "codTipo": item.get("codTipo"), "numero": item.get("numero"), "ano": item.get("ano"), "ementa": item.get("ementa") or "", "descricaoTipo": item.get("descricaoTipo", ""), "ementaDetalhada": None, "dataApresentacao": None, "descricaoTramitacao": None, "despacho": None ,}
        if row["id"] is not None:
            info_path = DATA_LEG_ROOT / str(legislatura) / "proposicoes" / str(row["id"]) / "info.json"
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
                    if dados.get("descricaoTipo"): row["descricaoTipo"] = dados.get("descricaoTipo")
        enriched.append(row)
    if not enriched: return pd.DataFrame()
    df = pd.DataFrame(enriched)
    return df.sort_values(by=["ano", "numero"], ascending=[False, False], na_position="last").reset_index(drop=True)

def load_votacoes_list(legislatura: int, max_entries: int = 6000) -> List[Dict]:
    summary_path = DATA_LEG_ROOT / str(legislatura) / "votacoes.json"
    if not summary_path.exists():
        return scan_info_files_limited(DATA_LEG_ROOT / str(legislatura) / "votacoes", max_entries)
    with summary_path.open("r", encoding="utf-8") as f:
        first_bytes = f.read(2048)
    if "\n" in first_bytes and not first_bytes.lstrip().startswith(("{", "[")):
        return read_ndjson_limited(summary_path, max_entries)
    try: return read_json_array_limited(summary_path, max_entries, key="dados")
    except Exception: return read_json_array_limited(summary_path, max_entries, key=None)

def load_votacoes_dataframe(legislatura: int, max_entries: int = 6000) -> pd.DataFrame:
    items = load_votacoes_list(legislatura, max_entries)
    enriched = []
    for item in items:
        if not isinstance(item, dict): continue
        base_row = { "id": item.get("id"), "dataHoraRegistro": item.get("dataHoraRegistro"), "siglaOrgao": item.get("siglaOrgao"), "descricao": item.get("descricao", "Descrição não disponível"), "aprovacao": item.get("aprovacao") }
        proposicoes_afetadas = []
        if base_row["id"] is not None:
            info_path = DATA_LEG_ROOT / str(legislatura) / "votacoes" / str(base_row["id"]) / "info.json"
            info = fetch_json(info_path)
            if info:
                dados = info.get("dados") if isinstance(info, dict) and "dados" in info else info
                if isinstance(dados, dict):
                    base_row["descricao"] = dados.get("descricao") or base_row["descricao"]
                    base_row["aprovacao"] = dados.get("aprovacao") if dados.get("aprovacao") is not None else base_row["aprovacao"]
                    proposicoes_afetadas = dados.get("proposicoesAfetadas", [])
        if not proposicoes_afetadas:
            row = base_row.copy(); row["proposicaoAfetada"] = "N/A"; row["proposicaoUri"] = None; enriched.append(row)
        else:
            for p in proposicoes_afetadas:
                if isinstance(p, dict):
                    row = base_row.copy(); row["proposicaoAfetada"] = f"{p.get('siglaTipo')} {p.get('numero')}/{p.get('ano')}"; row["proposicaoUri"] = p.get('uri'); enriched.append(row)
    if not enriched: return pd.DataFrame()
    df = pd.DataFrame(enriched)
    def map_resultado(aprovacao):
        if aprovacao == 1: return "Aprovada"
        if pd.isna(aprovacao): return "Indefinido"
        return "Rejeitada/Outro"
    df['resultado'] = df['aprovacao'].apply(map_resultado)
    df['dataHoraRegistro'] = pd.to_datetime(df['dataHoraRegistro'])
    return df.sort_values(by="dataHoraRegistro", ascending=False, na_position="last").reset_index(drop=True)

# --- helper para garantir que max_entries seja um inteiro válido ---
def sanitize_max_entries(max_entries, default=1000, min_allowed=10, max_allowed=1_000_000):
    try:
        if max_entries is None:
            return default
        me = int(float(max_entries))
    except (ValueError, TypeError):
        return default
    if me < min_allowed:
        return min_allowed
    if me > max_allowed:
        return max_allowed
    return me

# ---------- DASH APP ----------
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Store(id='proposicoes-data-store'), dcc.Store(id='votacoes-data-store'),
    html.H1("Dashboard: Câmara dos Deputados"),
    html.Div([
        html.Label("Selecione a Legislatura:"),
        dcc.Dropdown(id='leg-dropdown', options=[{'label': str(x), 'value': x} for x in (53, 54, 55, 56, 57)], value=57, clearable=False, style={'width': '200px', 'marginRight': '20px'}),
        html.Label("Limite de entradas:"),
        dcc.Input(id='max-entries', type='number', value=1000, min=10, step=100, style={'width': '150px'}, debounce=True),
    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),
    dcc.Tabs(id="tabs-main", value='tab-proposicoes', children=[
        dcc.Tab(label='Proposições', value='tab-proposicoes', children=[
            dcc.Graph(id='proposicoes-graph'),
            html.Button('Limpar Filtro', id='clear-proposicoes-filter-btn', n_clicks=0, style={'marginTop': '10px'}),
            html.Div(id='tabela-proposicoes')
        ]),
        dcc.Tab(label='Votações', value='tab-votacoes', children=[
            html.Div([
                dcc.Graph(id='votacoes-graph-pie', style={'flex': 1, 'minWidth': '300px'}),
                html.Div([
                    dcc.RadioItems(id='votacoes-bar-filter-radio',
                                   options=[{'label': 'Todas', 'value': 'Todas'},
                                            {'label': 'Aprovadas', 'value': 'Aprovada'},
                                            {'label': 'Rejeitadas/Outro', 'value': 'Rejeitada/Outro'}],
                                   value='Todas', labelStyle={'display': 'inline-block', 'marginRight': '10px'}),
                    dcc.Graph(id='votacoes-graph-bar', style={'height': '560px', 'minWidth': '420px'})
                ], style={'flex': 1.5, 'minWidth': '420px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'stretch'})
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start'}),
            html.Button('Limpar Filtro da Tabela', id='clear-votacoes-filter-btn', n_clicks=0, style={'marginTop': '10px'}),
            html.Div(id='tabela-votacoes')
        ]),
    ])
])

# --- CALLBACKS ---
@app.callback(
    [Output('proposicoes-data-store', 'data'), Output('proposicoes-graph', 'figure')],
    [Input('leg-dropdown', 'value'), Input('max-entries', 'value')]
)
def load_proposicoes_data(legislatura, max_entries):
    max_entries = sanitize_max_entries(max_entries, default=1000)
    df = load_proposicoes_dataframe(legislatura, max_entries)
    if df.empty:
        empty_fig = px.bar(title=f"Nenhum dado de proposições para a legislatura {legislatura}")
        return None, empty_fig

    count_df = df.groupby(['siglaTipo', 'descricaoTipo']).size().reset_index(name='Contagem').sort_values(by='Contagem', ascending=False)
    fig = px.bar(count_df, x='siglaTipo', y='Contagem', color='siglaTipo', text='Contagem',
                 hover_data={'descricaoTipo': True, 'siglaTipo': False},
                 labels={'siglaTipo': 'Tipo', 'Contagem': 'Quantidade'},
                 title=f"Contagem de Proposições por Tipo (Leg. {legislatura}, máx. {max_entries})",
                 category_orders={"siglaTipo": count_df['siglaTipo'].tolist()})
    fig.update_traces(textposition='outside').update_layout(showlegend=False)
    return df.to_json(date_format='iso', orient='split'), fig

@app.callback(
    Output('tabela-proposicoes', 'children'),
    [Input('proposicoes-data-store', 'data'), Input('proposicoes-graph', 'clickData'), Input('clear-proposicoes-filter-btn', 'n_clicks')]
)
def update_proposicoes_table(json_data, clickData, n_clicks):
    if not json_data: return html.P("Selecione uma legislatura para carregar os dados.")
    
    df = pd.read_json(StringIO(json_data), orient='split')
    
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'No trigger'
    filtered_df = df
    
    if 'clear-proposicoes-filter-btn' in triggered_id:
        filtered_df = df
    elif triggered_id == 'proposicoes-graph' and clickData:
        sigla_tipo = clickData['points'][0]['x']
        filtered_df = df[df['siglaTipo'] == sigla_tipo]

    table_df = filtered_df[["id", "siglaTipo", "descricaoTipo", "numero", "ano", "ementa", "dataApresentacao", "descricaoTramitacao"]].copy()
    table_df.loc[:, "ementa"] = table_df["ementa"].apply(lambda x: (x[:120] + "...") if isinstance(x, str) and len(x) > 120 else x)
    return dash_table.DataTable(columns=[{"name": col, "id": col} for col in table_df.columns], data=table_df.to_dict("records"), sort_action="native", page_size=25, style_table={'overflowX': 'auto'}, style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto', 'minWidth': '100px', 'maxWidth': '300px'}, style_header={'fontWeight': 'bold'})

@app.callback(
    Output('votacoes-data-store', 'data'),
    [Input('leg-dropdown', 'value'), Input('max-entries', 'value')]
)
def load_votacoes_data(legislatura, max_entries):
    max_entries = sanitize_max_entries(max_entries, default=1000)
    df = load_votacoes_dataframe(legislatura, max_entries)
    if df.empty:
        return None
    return df.to_json(date_format='iso', orient='split')


@app.callback(
    [Output('votacoes-graph-pie', 'figure'), Output('votacoes-graph-bar', 'figure')],
    [Input('votacoes-data-store', 'data'), Input('votacoes-bar-filter-radio', 'value')]
)
def update_votacoes_graphs(json_data, radio_value):
    if not json_data:
        empty_fig = px.pie(title="Nenhum dado de votações disponível")
        empty_bar = px.bar(title="Nenhum dado de votações disponível")
        return empty_fig, empty_bar

    df = pd.read_json(StringIO(json_data), orient='split')
    
    pie_fig = px.pie(df, names='resultado', title="Resultado Geral das Votações",
                     color='resultado', color_discrete_map={'Aprovada': 'green', 'Rejeitada/Outro': 'red', 'Indefinido': 'grey'})
    pie_fig.update_traces(textinfo='percent+label')
    pie_fig.update_layout(height=420, margin=dict(l=20, r=20, t=40, b=20), legend={'orientation': 'h', 'y': -0.12})

    if radio_value == 'Todas':
        bar_df = df.copy()
    else:
        bar_df = df[df['resultado'] == radio_value].copy()
    
    bar_df.loc[bar_df['proposicaoAfetada'].isna(), 'proposicaoAfetada'] = 'N/A'

    deduped = bar_df[bar_df['proposicaoAfetada'] != 'N/A'].drop_duplicates(subset=['id', 'proposicaoAfetada'])
    
    TOP_N = 12
    prop_counts = (deduped.groupby('proposicaoAfetada')['id']
                           .nunique()
                           .nlargest(TOP_N)
                           .reset_index(name='Contagem'))

    if prop_counts.empty:
        bar_fig = px.bar(title=f'Top Proposições Mais Votadas ({radio_value}) - nenhum dado')
        bar_fig.update_layout(height=560, margin=dict(l=20, r=20, t=40, b=20))
        return pie_fig, bar_fig

    bar_fig = px.bar(prop_counts, x='Contagem', y='proposicaoAfetada', orientation='h',
                     title=f'Top {TOP_N} Proposições Mais Votadas ({radio_value})',
                     labels={'proposicaoAfetada': 'Proposição', 'Contagem': 'Nº de Votações'}, text='Contagem')
    bar_fig.update_traces(textposition='outside', textfont_size=12)
    bar_fig.update_layout(
        height=560, margin=dict(l=220, r=20, t=50, b=50),
        yaxis={'automargin': True}, bargap=0.18)
    bar_fig.update_yaxes(categoryorder="total ascending", tickfont=dict(size=12))

    return pie_fig, bar_fig

@app.callback(
    Output('tabela-votacoes', 'children'),
    [Input('votacoes-data-store', 'data'), Input('votacoes-graph-pie', 'clickData'), Input('votacoes-graph-bar', 'clickData'), Input('clear-votacoes-filter-btn', 'n_clicks')]
)
def update_votacoes_table(json_data, pie_click, bar_click, n_clicks):
    if not json_data: return html.P("Selecione uma legislatura para carregar os dados.")

    df = pd.read_json(StringIO(json_data), orient='split')
    df['dataHoraRegistro'] = pd.to_datetime(df['dataHoraRegistro'])
    
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'No trigger'
    
    filtered_df = df

    if 'clear-votacoes-filter-btn' in triggered_id:
        filtered_df = df
    elif triggered_id == 'votacoes-graph-pie' and pie_click:
        resultado = pie_click['points'][0]['label']
        filtered_df = df[df['resultado'] == resultado]
    elif triggered_id == 'votacoes-graph-bar' and bar_click:
        proposicao = bar_click['points'][0]['y']
        filtered_df = df[df['proposicaoAfetada'] == proposicao]
    
    table_df = filtered_df.drop_duplicates(subset=['id']).copy()
    
    table_df.loc[:, 'proposicaoAfetada'] = table_df.apply(lambda row: f"[{row['proposicaoAfetada']}]({row['proposicaoUri']})" if pd.notna(row['proposicaoUri']) else row['proposicaoAfetada'], axis=1)
    table_df.loc[:, "dataHoraRegistro"] = table_df["dataHoraRegistro"].dt.strftime('%Y-%m-%d %H:%M')
    
    return dash_table.DataTable(
        columns=[
            {"name": "ID Votação", "id": "id"}, 
            {"name": "Data/Hora", "id": "dataHoraRegistro"}, 
            {"name": "Órgão", "id": "siglaOrgao"}, 
            {"name": "Descrição", "id": "descricao"}, 
            {"name": "Resultado", "id": "resultado"}, 
            {"name": "Proposição Principal", "id": "proposicaoAfetada", "presentation": "markdown"}
        ], 
        data=table_df.to_dict("records"), 
        sort_action="native", 
        page_size=25, 
        style_table={'overflowX': 'auto'}, 
        style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto', 'minWidth': '120px'}, 
        style_header={'fontWeight': 'bold'}
    )

if __name__ == "__main__":
    app.run(debug=True)
