import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from io import StringIO
from functools import reduce
import dash
from dash import dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import ijson


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
    for i, entry in enumerate(info_dir.iterdir()):
        if i >= max_entries: break
        data = fetch_json(entry / "info.json")
        if not data: continue
        dados = data.get("dados") if isinstance(data, dict) and "dados" in data else data
        results.append(dados)
    return results

# ---------- GENERIC DATA LOADING ----------
def get_nested_value(data: Dict, key_path: str, default: Any = None) -> Any:
    keys = key_path.split('.')
    try:
        return reduce(lambda d, key: d.get(key) if isinstance(d, dict) else default, keys, data)
    except (TypeError, KeyError):
        return default

def _process_votacoes_rows(items: List[Dict], legislatura: Optional[int] = None) -> List[Dict]:
    enriched = []
    for item in items:
        aprovacao = item.get('aprovacao')
        if aprovacao == 1:
            item['aprovacao'] = "Aprovada"
        elif aprovacao == 0:
            item['aprovacao'] = "Rejeitada/Outro"
        else:
            item['aprovacao'] = "Indefinido"

        proposicoes_afetadas = get_nested_value(item, 'proposicoesAfetadas', []) or []
        
        if proposicoes_afetadas and legislatura:
            enriched_proposicoes = []
            for prop_summary in proposicoes_afetadas:
                if not isinstance(prop_summary, dict): continue
                
                prop_id = prop_summary.get('id')
                # Cria um texto base com as informações do sumário
                display_text = f"{prop_summary.get('siglaTipo', '')} {prop_summary.get('numero', '')}/{prop_summary.get('ano', '')}"
                details = "Ementa não encontrada."

                if prop_id:
                    # Constrói o caminho para o info.json da proposição específica
                    prop_info_path = DATA_LEG_ROOT / str(legislatura) / "proposicoes" / str(prop_id) / "info.json"
                    prop_info_data = fetch_json(prop_info_path)
                    
                    if prop_info_data:
                        prop_dados = prop_info_data.get("dados", {})
                        ementa = prop_dados.get("ementa", details)
                        details = ementa if ementa else "Ementa não disponível."
                
                # Armazena um dicionário com o texto de exibição e os detalhes
                enriched_proposicoes.append({
                    "text": display_text,
                    "details": details
                })
            
            # A coluna principal agora armazena a lista de dicionários enriquecidos
            item['proposicoesAfetadas'] = enriched_proposicoes
            item['proposicoesAfetadas_resumo'] = f"{len(enriched_proposicoes)} proposição(ões) afetada(s)"
        else:
            # Fallback caso não haja proposições ou a legislatura não seja fornecida
            item['proposicoesAfetadas'] = []
            item['proposicoesAfetadas_resumo'] = "Nenhuma proposição afetada"
            
        enriched.append(item)
    return enriched

DATA_TYPE_CONFIG = {
    "proposicoes": {
        "display_name": "Proposições",
        "base_fields": ["id", "siglaTipo", "codTipo", "numero", "ano", "ementa"],
        "enrichment_fields": {
            "ementaDetalhada": "ementaDetalhada",
            "dataApresentacao": "dataApresentacao",
            "descricaoTramitacao": "statusProposicao.descricaoTramitacao",
            "despacho": "statusProposicao.despacho",
            "descricaoTipo": "descricaoTipo",
        },
        "sort_by": ["ano", "numero"],
        "sort_ascending": [False, False],
        "graph_column_x": "siglaTipo",
        "graph_hover_data": ["descricaoTipo"],
    },
    "votacoes": {
        "display_name": "Votações",
        "base_fields": ["id", "dataHoraRegistro", "siglaOrgao", "descricao", "aprovacao"],
        "enrichment_fields": {
             # Este campo agora carrega a lista completa, que será usada pelo modal
            "proposicoesAfetadas": "proposicoesAfetadas",
        },
        "processor": _process_votacoes_rows, # O processador cria o campo de resumo
        "sort_by": ["dataHoraRegistro"],
        "sort_ascending": [False],
        "graph_column_x": "aprovacao",
        "graph_hover_data": ["siglaOrgao"],
    }
}

def load_summary_list(data_type: str, legislatura: int, max_entries: int) -> List[Dict]:
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
    config = DATA_TYPE_CONFIG.get(data_type)
    if not config:
        print(f"Error: No configuration found for data type '{data_type}'")
        return pd.DataFrame()

    items = load_summary_list(data_type, legislatura, max_entries)
    enriched = []

    for item in items:
        if not isinstance(item, dict): continue

        row = {key: item.get(key) for key in config["base_fields"]}

        item_id = row.get("id")
        if item_id and config.get("enrichment_fields"):
            info_path = DATA_LEG_ROOT / str(legislatura) / data_type / str(item_id) / "info.json"
            info = fetch_json(info_path)
            if info:
                dados = info.get("dados") if isinstance(info, dict) and "dados" in info else info
                if isinstance(dados, dict):
                    for target_col, key_path in config["enrichment_fields"].items():
                        value = get_nested_value(dados, key_path)
                        if value is not None:
                            row[target_col] = value

        enriched.append(row)

    if not enriched:
        return pd.DataFrame()

    if 'processor' in config:
        processed_data = config['processor'](enriched, legislatura=legislatura)
    else:
        processed_data = enriched

    if not processed_data:
        return pd.DataFrame()

    df = pd.DataFrame(processed_data)

    if 'sort_by' in config:
        for col in config['sort_by']:
            if 'data' in col.lower() or 'time' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')

        df = df.sort_values(
            by=config['sort_by'],
            ascending=config.get('sort_ascending', False),
            na_position="last"
        ).reset_index(drop=True)

    return df

def sanitize_max_entries(max_entries, default=1000, min_allowed=10, max_allowed=1_000_000):
    try:
        if max_entries is None: return default
        me = int(float(max_entries))
    except (ValueError, TypeError): return default
    return max(min_allowed, min(me, max_allowed))

# ---------- DASH APP ----------
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Store(id='generic-data-store'),
    dcc.Store(id='modal-content-store'),
    html.H1("Dashboard Genérico: Câmara dos Deputados"),

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

    html.Div(id='loading-warning', style={'color': 'orange', 'marginBottom': '10px'}),

    dcc.Loading(
        id='loading-output',
        type='default',
        children=[html.Div(id='output-area')]
    ),
    
    # dcc.ConfirmDialog é uma maneira simples de criar um modal de texto.
    dcc.ConfirmDialog(
        id='proposicoes-modal',
        message='', # O conteúdo será preenchido via callback
    ),
])


def get_display_columns(df):
    """Determina quais colunas exibir na tabela."""
    cols = list(df.columns)
    # Se a coluna de resumo existir, use-a no lugar da lista completa
    if 'proposicoesAfetadas_resumo' in cols:
        # Remove a coluna da lista original se ela existir
        if 'proposicoesAfetadas' in cols:
            cols.remove('proposicoesAfetadas')
    return cols

def create_table(df, max_entries):
    display_columns = get_display_columns(df)
    
    if df.empty:
        return dash_table.DataTable(
            id='generic-table',
            columns=[{"name": col, "id": col} for col in display_columns],
            data=[],
            page_size=20,
        )

    # Truncate long text columns
    if 'ementa' in display_columns: # Verifique se a coluna existe antes de tentar modificar
        df['ementa'] = df['ementa'].astype(str).apply(lambda x: (x[:120] + '...') if len(x) > 120 else x)
    if 'descricao' in display_columns: # Verifique se a coluna existe antes de tentar modificar
        df['descricao'] = df['descricao'].astype(str).apply(lambda x: (x[:120] + '...') if len(x) > 120 else x)

    # Configuração de colunas para o modal
    columns = []
    for col in display_columns:
        if col == 'proposicoesAfetadas_resumo':
            columns.append({
                "name": "Proposições Afetadas",
                "id": col,
            })
        else:
            columns.append({"name": col, "id": col})

    data_for_table = df[display_columns].to_dict("records")

    return dash_table.DataTable(
        id='generic-table',
        columns=columns,
        data=data_for_table, # <<< USAMOS OS DADOS FILTRADOS AQUI
        sort_action="native",
        page_size=max(int(sanitize_max_entries(max_entries) / 10), 10),
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'whiteSpace': 'normal',
            'height': 'auto',
            'minWidth': '120px',
            'maxWidth': '350px',
        },
        style_header={'fontWeight': 'bold'},
        style_data_conditional=[
            {
                'if': {'column_id': 'proposicoesAfetadas_resumo'},
                'color': 'blue',
                'textDecoration': 'underline',
                'cursor': 'pointer',
            }
        ]
    )

@app.callback(
    Output('output-area', 'children'),
    Input('generic-data-store', 'data'),
    State('data-type-dropdown', 'value'),
    State('leg-dropdown', 'value'),
    State('max-entries', 'value'),
)
def render_output_area(json_data, data_type, legislatura, max_entries):
    if not json_data:
        return html.Div([
            html.H3(f"Nenhum dado encontrado para '{DATA_TYPE_CONFIG[data_type]['display_name']}' na legislatura {legislatura}."),
            html.P("Tente ajustar o limite de entradas ou selecionar outra legislatura.")
        ])
    df = pd.read_json(StringIO(json_data), orient='split')
    config = DATA_TYPE_CONFIG[data_type]

    graph_col_x = config.get('graph_column_x')
    graph_component = html.Div() # Componente vazio por padrão
    if graph_col_x and graph_col_x in df.columns:
        counts = df.groupby(graph_col_x).size().reset_index(name='Contagem')
        hover_cols = config.get('graph_hover_data', [])
        
        # Corrigido: merge para hover_data
        if hover_cols:
            mapping_cols = [graph_col_x] + [col for col in hover_cols if col in df.columns]
            if len(mapping_cols) > 1:
                hover_map = df[mapping_cols].drop_duplicates()
                count_df = pd.merge(counts, hover_map, on=graph_col_x, how='left')
            else:
                count_df = counts
        else:
            count_df = counts

        count_df = count_df.sort_values(by='Contagem', ascending=False)
        fig = px.bar(count_df, x=graph_col_x, y='Contagem', color=graph_col_x,
                     hover_data=config.get('graph_hover_data', []),
                     labels={graph_col_x: 'Categoria', 'Contagem': 'Quantidade'},
                     title=f"Contagem por Categoria: {config['display_name']} (Leg. {legislatura}, máx. {sanitize_max_entries(max_entries)})",
                     text='Contagem')
        fig.update_traces(textposition='outside').update_layout(showlegend=False)
        graph_component = dcc.Graph(id='generic-graph', figure=fig)
    else:
        fig = px.bar(title="Não é possível gerar o gráfico: coluna de agregação não definida ou não encontrada.")
        graph_component = dcc.Graph(id='generic-graph', figure=fig)


    return html.Div([
        graph_component,
        html.Hr(),
        html.H4("Dados Detalhados"),
        html.Button("Resetar Filtro", id='reset-filter-button', n_clicks=0),
        html.Div(id='table-container', children=create_table(df, max_entries))
    ])


# ---------- CALLBACKS ----------
@app.callback(
    Output('generic-data-store', 'data'),
    Input('leg-dropdown', 'value'),
    Input('data-type-dropdown', 'value'),
    Input('max-entries', 'value')
)
def load_data_to_store(legislatura, data_type, max_entries):
    max_entries = sanitize_max_entries(max_entries)
    df = load_generic_dataframe(data_type, legislatura, max_entries)
    if df.empty:
        return None
    # Armazenar com orient='split' é eficiente e preserva os tipos de dados
    return df.to_json(date_format='iso', orient='split')


@app.callback(
    Output('loading-warning', 'children'),
    Input('max-entries', 'value')
)
def update_loading_warning(max_entries):
    max_entries = sanitize_max_entries(max_entries)
    if max_entries > 5000:
        return f"Aviso: Limite grande ({max_entries}) selecionado. O carregamento pode demorar vários segundos ou minutos devido ao processamento de arquivos."
    return ""

@app.callback(
    Output('table-container', 'children'),
    Input('generic-graph', 'clickData'),
    Input('reset-filter-button', 'n_clicks'),
    State('generic-data-store', 'data'),
    State('data-type-dropdown', 'value'),
    State('max-entries', 'value')
)
def update_table_on_click(click_data, n_clicks, json_data, data_type, max_entries):
    if not json_data:
        return create_table(pd.DataFrame(), max_entries)

    df = pd.read_json(StringIO(json_data), orient='split')
    config = DATA_TYPE_CONFIG[data_type]
    graph_col_x = config.get('graph_column_x')

    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    if triggered_id == 'generic-graph' and click_data and graph_col_x in df.columns:
        clicked_category = click_data['points'][0]['x']
        filtered_df = df[df[graph_col_x] == clicked_category]
        return html.Div([
            html.P(f"Filtrado por: {clicked_category}", style={'fontWeight': 'bold'}),
            create_table(filtered_df, max_entries)
        ])
    
    return html.Div([
        html.P("Mostrando todos os dados", style={'fontWeight': 'bold'}),
        create_table(df, max_entries)
    ])


@app.callback(
    Output('modal-content-store', 'data'),
    Input('generic-table', 'active_cell'),
    State('generic-data-store', 'data')
)
def store_modal_content(active_cell, json_data):
    if not active_cell or not json_data:
        return None

    # O `active_cell` se refere ao índice da view da tabela.
    # Para ser robusto com ordenação e paginação, idealmente a tabela teria uma coluna de ID.
    # Como não tem, vamos precisar mapear o índice da linha da tabela de volta para o DataFrame.
    # Isso pode ser complexo. A forma mais simples que funciona sem filtro/sort do usuário é:
    df = pd.read_json(StringIO(json_data), orient='split')
    row_idx = active_cell['row']
    col_id = active_cell['column_id']

    if col_id == 'proposicoesAfetadas_resumo':
        # `df.iloc[row_idx]` funciona se a tabela não foi reordenada pelo usuário.
        # Para uma solução mais robusta, seria necessário um callback mais complexo
        # que considerasse os estados `sort_by` e `filter_query` da tabela.
        # Por enquanto, esta abordagem é suficiente para a demonstração.
        if row_idx < len(df):
            row = df.iloc[row_idx]
            proposicoes_list = row.get('proposicoesAfetadas', [])

            if isinstance(proposicoes_list, list) and proposicoes_list:
                modal_lines = []
                for prop_data in proposicoes_list:
                    if isinstance(prop_data, dict):
                        text = prop_data.get('text', 'Proposição não identificada')
                        details = prop_data.get('details', 'Sem detalhes.')
                        # Trunca a ementa para não criar um modal gigantesco
                        details_truncated = (details[:350] + '...') if len(details) > 350 else details
                
                        modal_lines.append(f"• {text}\n  Ementa: {details_truncated}")
                # Junta tudo com duas quebras de linha para espaçamento
                return "\n\n".join(modal_lines)

    return None

@app.callback(
    Output('proposicoes-modal', 'displayed'),
    Output('proposicoes-modal', 'message'),
    Input('modal-content-store', 'data')
)
def show_modal(content):
    if content:
        return True, content
    return False, ""

if __name__ == "__main__":
    app.run(debug=True)
