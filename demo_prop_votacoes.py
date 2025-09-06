import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from io import StringIO
import ijson
from functools import reduce

import dash
from dash import dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

DATA_LEG_ROOT = Path("camara/legislaturas")

# ---------- JSON HELPERS (Unchanged) ----------
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

# ---------- GENERIC DATA LOADING (NEW & REFACTORED) ----------

def get_nested_value(data: Dict, key_path: str, default: Any = None) -> Any:
    """Safely retrieves a value from a nested dictionary using a dot-separated path."""
    keys = key_path.split('.')
    try:
        return reduce(lambda d, key: d.get(key) if isinstance(d, dict) else default, keys, data)
    except (TypeError, KeyError):
        return default

def _process_votacoes_rows(items: List[Dict]) -> List[Dict]:
    """Custom processor for 'votacoes' to handle the one-to-many relationship with proposicoesAfetadas."""
    enriched = []
    for item in items:
        # Map 'aprovacao' to a readable string
        aprovacao = item.get('aprovacao')
        if aprovacao == 1:
            item['resultado'] = "Aprovada"
        elif pd.isna(aprovacao):
            item['resultado'] = "Indefinido"
        else:
            item['resultado'] = "Rejeitada/Outro"
        
        proposicoes_afetadas = get_nested_value(item, 'proposicoesAfetadas', []) or []
        
        if not proposicoes_afetadas:
            row = item.copy()
            row["proposicaoAfetada"] = "N/A"
            row["proposicaoUri"] = None
            enriched.append(row)
        else:
            for p in proposicoes_afetadas:
                if isinstance(p, dict):
                    row = item.copy()
                    row["proposicaoAfetada"] = f"{p.get('siglaTipo')} {p.get('numero')}/{p.get('ano')}"
                    row["proposicaoUri"] = p.get('uri')
                    enriched.append(row)
    return enriched

# --- Configuration for each data type ---
DATA_TYPE_CONFIG = {
    "proposicoes": {
        "display_name": "Proposições",
        "base_fields": ["id", "siglaTipo", "codTipo", "numero", "ano", "ementa", "descricaoTipo"],
        "enrichment_fields": {
            # "target_column_name": "path.to.value.in.info_json"
            "ementaDetalhada": "ementaDetalhada",
            "dataApresentacao": "dataApresentacao",
            "descricaoTramitacao": "statusProposicao.descricaoTramitacao",
            "despacho": "statusProposicao.despacho"
        },
        "sort_by": ["ano", "numero"],
        "sort_ascending": [False, False],
        "graph_column_x": "siglaTipo", # Column to plot on the x-axis
        "graph_hover_data": ["descricaoTipo"],
    },
    "votacoes": {
        "display_name": "Votações",
        "base_fields": ["id", "dataHoraRegistro", "siglaOrgao", "descricao", "aprovacao"],
        "enrichment_fields": {
            "proposicoesAfetadas": "proposicoesAfetadas",
        },
        "processor": _process_votacoes_rows, # Custom function for complex transformations
        "sort_by": ["dataHoraRegistro"],
        "sort_ascending": [False],
        "graph_column_x": "resultado",
        "graph_hover_data": ["siglaOrgao"],
    }
    # To add a new data type, e.g., 'frentes', just add a new dictionary here.
    # "frentes": { ... }
}

def load_summary_list(data_type: str, legislatura: int, max_entries: int) -> List[Dict]:
    """Generic function to load the initial list of items from a summary file or by scanning."""
    summary_path = DATA_LEG_ROOT / str(legislatura) / f"{data_type}.json"
    if not summary_path.exists():
        return scan_info_files_limited(DATA_LEG_ROOT / str(legislatura) / data_type, max_entries)
    
    with summary_path.open("r", encoding="utf-8") as f:
        first_bytes = f.read(2048)
    
    if "\n" in first_bytes and not first_bytes.lstrip().startswith(("{", "[")):
        return read_ndjson_limited(summary_path, max_entries)
    
    try: 
        return read_json_array_limited(summary_path, max_entries, key="dados")
    except Exception: 
        return read_json_array_limited(summary_path, max_entries, key=None)

def load_generic_dataframe(data_type: str, legislatura: int, max_entries: int) -> pd.DataFrame:
    """
    Generic data loader that uses the DATA_TYPE_CONFIG to build a DataFrame.
    """
    config = DATA_TYPE_CONFIG.get(data_type)
    if not config:
        print(f"Error: No configuration found for data type '{data_type}'")
        return pd.DataFrame()

    items = load_summary_list(data_type, legislatura, max_entries)
    enriched = []

    for item in items:
        if not isinstance(item, dict): continue
        
        # 1. Extract base fields from the summary list item
        row = {key: item.get(key) for key in config["base_fields"]}
        
        # 2. Enrich with data from individual info.json file
        item_id = row.get("id")
        if item_id and config.get("enrichment_fields"):
            info_path = DATA_LEG_ROOT / str(legislatura) / data_type / str(item_id) / "info.json"
            info = fetch_json(info_path)
            if info:
                dados = info.get("dados") if isinstance(info, dict) and "dados" in info else info
                if isinstance(dados, dict):
                    for target_col, source_path in config["enrichment_fields"].items():
                        value = get_nested_value(dados, source_path)
                        # Only update if the new value is not None, to avoid overwriting good data with nothing
                        if value is not None:
                            row[target_col] = value
        
        enriched.append(row)

    if not enriched:
        return pd.DataFrame()
    
    # 3. Apply custom processor if defined (for complex transformations)
    if 'processor' in config:
        processed_data = config['processor'](enriched)
    else:
        processed_data = enriched
        
    if not processed_data:
        return pd.DataFrame()

    df = pd.DataFrame(processed_data)
    
    # 4. Sort the DataFrame
    if 'sort_by' in config:
        # Convert date/time columns before sorting
        for col in config['sort_by']:
            if 'data' in col.lower() or 'time' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')

        df = df.sort_values(
            by=config['sort_by'],
            ascending=config.get('sort_ascending', False),
            na_position="last"
        ).reset_index(drop=True)

    return df

# --- helper para garantir que max_entries seja um inteiro válido ---
def sanitize_max_entries(max_entries, default=1000, min_allowed=10, max_allowed=1_000_000):
    try:
        if max_entries is None: return default
        me = int(float(max_entries))
    except (ValueError, TypeError): return default
    return max(min_allowed, min(me, max_allowed))



# ---------- DASH APP (REFACTORED) ----------
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Store(id='generic-data-store'),
    html.H1("Dashboard Genérico: Câmara dos Deputados"),
    
    # --- Controls ---
    html.Div([
        html.Label("Selecione a Legislatura:"),
        dcc.Dropdown(id='leg-dropdown', options=[{'label': str(x), 'value': x} for x in (53, 54, 55, 56, 57)], value=57, clearable=False, style={'width': '150px'}),
        
        html.Label("Tipo de Dado:", style={'marginLeft': '20px'}),
        dcc.Dropdown(
            id='data-type-dropdown',
            options=[{'label': v['display_name'], 'value': k} for k, v in DATA_TYPE_CONFIG.items()],
            value='proposicoes',
            clearable=False,
            style={'width': '200px'}
        ),

        html.Label("Limite de entradas:", style={'marginLeft': '20px'}),
        dcc.Input(id='max-entries', type='number', value=1000, min=10, step=100, style={'width': '150px'}, debounce=True),
    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),
    
    # --- Dynamic Output Area ---
    html.Div(id='output-area')
])

# --- CALLBACKS (REFACTORED) ---

@app.callback(
    Output('generic-data-store', 'data'),
    [Input('leg-dropdown', 'value'),
     Input('data-type-dropdown', 'value'),
     Input('max-entries', 'value')]
)
def load_data_to_store(legislatura, data_type, max_entries):
    """Loads data based on user selection and stores it as JSON."""
    max_entries = sanitize_max_entries(max_entries)
    df = load_generic_dataframe(data_type, legislatura, max_entries)
    if df.empty:
        return None
    return df.to_json(date_format='iso', orient='split')

@app.callback(
    Output('output-area', 'children'),
    [Input('generic-data-store', 'data')],
    [State('data-type-dropdown', 'value'),
     State('leg-dropdown', 'value'),
     State('max-entries', 'value')]
)

def render_output_area(json_data, data_type, legislatura, max_entries):
    """Renders the graph and table based on the data in the store."""
    if not json_data:
        return html.Div([
            html.H3(f"Nenhum dado encontrado para '{DATA_TYPE_CONFIG[data_type]['display_name']}' na legislatura {legislatura}."),
            html.P("Tente ajustar o limite de entradas ou selecionar outra legislatura.")
        ])

    df = pd.read_json(StringIO(json_data), orient='split')
    config = DATA_TYPE_CONFIG[data_type]
    
    # --- Generic Graph Generation (REVISED & ROBUST) ---
    graph_col_x = config.get('graph_column_x')
    if graph_col_x and graph_col_x in df.columns:
        
        # Step 1: Get the primary counts by grouping only by the x-axis column.
        # This gives us the correct total height for each bar.
        counts = df.groupby(graph_col_x).size().reset_index(name='Contagem')

        # Step 2: Add the hover data back in a controlled way.
        hover_cols = config.get('graph_hover_data', [])
        if hover_cols:
            # Create a list of columns needed for the mapping (x-axis + hover columns)
            mapping_cols = [graph_col_x] + [col for col in hover_cols if col in df.columns]
            
            # Create a unique mapping from the x-axis value to its hover text(s)
            hover_map = df[mapping_cols].drop_duplicates()
            
            # Merge the hover data into our counts dataframe.
            # For the 1-to-1 case ('proposicoes'), this is a simple join.
            # For the 1-to-many case ('votacoes'), this correctly duplicates
            # the total count for each hover category, which px.bar can handle.
            count_df = pd.merge(counts, hover_map, on=graph_col_x, how='left')
        else:
            count_df = counts

        count_df = count_df.sort_values(by='Contagem', ascending=False)

        fig = px.bar(count_df, x=graph_col_x, y='Contagem', color=graph_col_x,
                     hover_data=hover_cols, # Now hover_cols exist in count_df
                     labels={graph_col_x: 'Categoria', 'Contagem': 'Quantidade'},
                     title=f"Contagem por Categoria: {config['display_name']} (Leg. {legislatura}, máx. {sanitize_max_entries(max_entries)})",
                     text='Contagem')
        fig.update_traces(textposition='outside').update_layout(showlegend=False)
    else:
        fig = px.bar(title="Não é possível gerar o gráfico: coluna de agregação não definida ou não encontrada.")
    display_columns = list(df.columns) 
    
    if 'ementa' in df.columns:
        df['ementa'] = df['ementa'].astype(str).apply(lambda x: (x[:120] + '...') if len(x) > 120 else x)
    if 'descricao' in df.columns:
         df['descricao'] = df['descricao'].astype(str).apply(lambda x: (x[:120] + '...') if len(x) > 120 else x)

    
    # Converte colunas com listas ou dicionários para strings legíveis
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
            df[col] = df[col].apply(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x)

    table = dash_table.DataTable(
        id='generic-table',
        columns=[{"name": col, "id": col} for col in display_columns],
        data=df.to_dict("records"),
        sort_action="native",
        page_size=20,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto', 'minWidth': '120px', 'maxWidth': '350px'},
        style_header={'fontWeight': 'bold'}
    )
    
    return html.Div([
        dcc.Graph(id='generic-graph', figure=fig),
        html.Hr(),
        html.H4("Dados Detalhados"),
        table
    ])
if __name__ == "__main__":
    app.run(debug=True)
