import os
from dotenv import load_dotenv
import json
import urllib.parse
from pathlib import Path
from typing import List, Dict, Optional, Any
from io import StringIO
from functools import reduce
import dash
from dash import dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import sqlalchemy

load_dotenv()


# ---------- CONFIGURAÇÃO DO BANCO DE DADOS ----------
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PWD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME")
}

# Criar a string de conexão e o engine do SQLAlchemy
try:
    db_connection_str = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    db_engine = sqlalchemy.create_engine(db_connection_str)
    print("Conexão com o banco de dados estabelecida com sucesso.")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    db_engine = None

# ---------- FUNÇÕES AUXILIARES ----------
def get_legislatura_years(legislatura: int) -> List[int]:
    """Mapeia o número da legislatura para um range de anos."""
    start_year_map = {
        53: 2007,
        54: 2011,
        55: 2015,
        56: 2019,
        57: 2023,
    }
    start_year = start_year_map.get(legislatura)
    if not start_year:
        return []
    return list(range(start_year, start_year + 4))

def _process_votacoes_rows(items: List[Dict], legislatura: Optional[int] = None) -> List[Dict]:
    """Processa as linhas de votações, principalmente a coluna de proposições."""
    enriched = []
    for item in items:
        # A coluna proposicoesAfetadas vem como uma string JSON do banco de dados
        proposicoes_afetadas = item.get('proposicoesAfetadas')
        
        # Parseia a string JSON para uma lista de dicionários
        if isinstance(proposicoes_afetadas, str):
            try:
                proposicoes_list = json.loads(proposicoes_afetadas)
            except json.JSONDecodeError:
                proposicoes_list = []
        elif isinstance(proposicoes_afetadas, list): # Caso o driver já converta
             proposicoes_list = proposicoes_afetadas
        else:
            proposicoes_list = []

        item['proposicoesAfetadas'] = proposicoes_list if proposicoes_list else []
        
        if proposicoes_list:
            item['proposicoesAfetadas_resumo'] = f"{len(proposicoes_list)} proposição(ões) afetada(s)"
        else:
            item['proposicoesAfetadas_resumo'] = "Nenhuma proposição afetada"
            
        enriched.append(item)
    return enriched

# ---------- CONFIGURAÇÃO DOS TIPOS DE DADOS E QUERIES SQL ----------
DATA_TYPE_CONFIG = {
    "proposicoes": {
        "display_name": "Proposições",
        "sort_by": ["ano", "numero"],
        "sort_ascending": [False, False],
        "graph_column_x": "siglaTipo",
        "graph_hover_data": ["descricaoTipo"],
        "query_template": """
            WITH latest_status AS (
                SELECT DISTINCT ON (proposicao_id)
                    proposicao_id,
                    descricao_tramitacao,
                    despacho
                FROM proposicoes_status
                ORDER BY proposicao_id, data_hora DESC
            )
            SELECT
                p.id,
                p.sigla_tipo AS "siglaTipo",
                p.cod_tipo AS "codTipo",
                p.numero,
                p.ano,
                p.ementa,
                p.ementa_detalhada AS "ementaDetalhada",
                p.data_apresentacao AS "dataApresentacao",
                p.descricao_tipo AS "descricaoTipo",
                ls.descricao_tramitacao AS "descricaoTramitacao",
                ls.despacho
            FROM
                proposicoes p
            LEFT JOIN
                latest_status ls ON p.id = ls.proposicao_id
            WHERE
                p.ano IN ({years_tuple})
            ORDER BY
                p.ano DESC, p.numero DESC
            LIMIT {max_entries};
        """
    },
    "votacoes": {
        "display_name": "Votações",
        "processor": _process_votacoes_rows,
        "sort_by": ["dataHoraRegistro"],
        "sort_ascending": [False],
        "graph_column_x": "aprovacao",
        "graph_hover_data": ["siglaOrgao"],
        "query_template": """
            SELECT
                v.id,
                v.data_hora_registro AS "dataHoraRegistro",
                v.sigla_orgao AS "siglaOrgao",
                v.descricao,
                CASE
                    WHEN v.aprovacao = 1 THEN 'Aprovada'
                    WHEN v.aprovacao = 0 THEN 'Rejeitada/Outro'
                    ELSE 'Indefinido'
                END AS aprovacao,
                (
                    SELECT json_agg(
                        json_build_object(
                            'id', p.id,
                            'text', p.sigla_tipo || ' ' || p.numero || '/' || p.ano,
                            'details', p.ementa
                        )
                    )
                    FROM votacoes_proposicoes vp
                    JOIN proposicoes p ON vp.proposicao_id = p.id
                    WHERE vp.votacao_id = v.id
                ) AS "proposicoesAfetadas"
            FROM
                votacoes v
            WHERE
                EXTRACT(YEAR FROM v.data_hora_registro) IN ({years_tuple})
            ORDER BY
                v.data_hora_registro DESC
            LIMIT {max_entries};
        """
    }
}

# ---------- CARREGAMENTO DE DADOS DO BANCO ----------
def load_generic_dataframe(data_type: str, legislatura: int, max_entries: int) -> pd.DataFrame:
    if not db_engine:
        print("Erro: Conexão com o banco de dados não está disponível.")
        return pd.DataFrame()

    config = DATA_TYPE_CONFIG.get(data_type)
    if not config:
        print(f"Error: No configuration found for data type '{data_type}'")
        return pd.DataFrame()

    years = get_legislatura_years(legislatura)
    if not years:
        print(f"Erro: Anos para a legislatura {legislatura} não definidos.")
        return pd.DataFrame()
    
    # Formata a tupla de anos para a cláusula IN do SQL
    years_tuple_str = ', '.join(map(str, years))
    
    query = config["query_template"].format(
        years_tuple=years_tuple_str,
        max_entries=max_entries
    )

    try:
        with db_engine.connect() as connection:
            df = pd.read_sql_query(sqlalchemy.text(query), connection)
    except Exception as e:
        print(f"Erro ao executar a query para '{data_type}': {e}")
        return pd.DataFrame()

    if df.empty:
        return pd.DataFrame()

    # Aplica o processador pós-query, se houver (para 'votacoes')
    if 'processor' in config:
        # O processador espera uma lista de dicionários
        processed_data = config['processor'](df.to_dict('records'), legislatura=legislatura)
        if not processed_data:
            return pd.DataFrame()
        df = pd.DataFrame(processed_data)

    # Garante a ordenação final, se especificada
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

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# O restante do código (layout e callbacks do Dash) permanece o mesmo
# ... (cole o restante do seu código original aqui, sem alterações)
# app.index_string = ...
# app.layout = ...
# def get_display_columns(df): ...
# def create_table(df, max_entries): ...
# @app.callback(...)
# def render_output_area(...): ...
# ... e assim por diante
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            
            .main-container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 16px;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                margin: 0;
                font-size: 2.5rem;
                font-weight: 700;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            
            .header p {
                margin: 10px 0 0 0;
                font-size: 1.1rem;
                opacity: 0.9;
                font-weight: 300;
            }
            
            .controls-section {
                background: #f8fafc;
                padding: 25px 30px;
                border-bottom: 1px solid #e2e8f0;
            }
            
            .control-group {
                display: flex;
                flex-wrap: wrap;
                gap: 25px;
                align-items: end;
            }
            
            .control-item {
                display: flex;
                flex-direction: column;
                min-width: 150px;
            }
            
            .control-item label {
                font-weight: 600;
                color: #374151;
                margin-bottom: 8px;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .warning-card {
                background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                border: 1px solid #f59e0b;
                border-radius: 12px;
                padding: 15px;
                margin: 20px 30px;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .warning-icon {
                width: 24px;
                height: 24px;
                background: #f59e0b;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                flex-shrink: 0;
                font-size: 14px;
            }
            
            .content-section {
                padding: 30px;
            }
            
            .stats-card {
                background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
                border: 1px solid #10b981;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 25px;
                text-align: center;
            }
            
            .chart-container {
                background: white;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 25px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            .table-section {
                background: white;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            .section-title {
                font-size: 1.5rem;
                font-weight: 600;
                color: #1f2937;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #e5e7eb;
            }
            
            .filter-info {
                background: #eff6ff;
                border: 1px solid #3b82f6;
                border-radius: 8px;
                padding: 12px 16px;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .reset-button {
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                margin-bottom: 15px;
            }
            
            .reset-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    dcc.Store(id='generic-data-store'),
    dcc.Store(id='modal-content-store'),
    
    html.Div([
        # Header Section
        html.Div([
            html.H1("Dashboard Câmara dos Deputados"),
            html.P("Análise de Proposições e Votações Legislativas")
        ], className="header"),
        
        # Controls Section
        html.Div([
            html.Div([
                html.Div([
                    html.Label("Legislatura"),
                    dcc.Dropdown(
                        id='leg-dropdown', 
                        options=[{'label': f'{x}ª Legislatura', 'value': x} for x in (53, 54, 55, 56, 57)], 
                        value=57, 
                        clearable=False,
                        style={'minWidth': '160px'}
                    )
                ], className="control-item"),

                html.Div([
                    html.Label("Tipo de Dados"),
                    dcc.Dropdown(
                        id='data-type-dropdown',
                        options=[{'label': f'{v["display_name"]}', 'value': k} for k, v in DATA_TYPE_CONFIG.items()],
                        value='proposicoes',
                        clearable=False,
                        style={'minWidth': '200px'}
                    )
                ], className="control-item"),
                
                html.Div([
                    html.Label("Limite de Registros"),
                    dcc.Input(
                        id='max-entries', 
                        type='number', 
                        value=1000, 
                        min=10, 
                        step=100, 
                        style={'width': '150px', 'padding': '8px', 'border': '1px solid #d1d5db', 'borderRadius': '8px'}, 
                        debounce=True
                    )
                ], className="control-item"),
            ], className="control-group")
        ], className="controls-section"),

        # Warning Section
        html.Div(id='loading-warning-container'),

        # Content Section
        html.Div([
            dcc.Loading(
                id='loading-output',
                type='circle',
                color='#3b82f6',
                children=[html.Div(id='output-area')]
            )
        ], className="content-section"),
        
    ], className="main-container"),

    html.Div(
        id='proposicoes-modal',
        style={
            'display': 'none',
            'position': 'fixed',
            'zIndex': '3000',
            'left': 0,
            'top': 0,
            'width': '100%',
            'height': '100%',
            'overflow': 'auto',
            'backgroundColor': 'rgba(0,0,0,0.6)',
            'padding': '20px'
        },
        children=html.Div(
            id='proposicoes-modal-content',
            style={
                'backgroundColor': 'white',
                'margin': 'auto',
                'padding': '0',
                'borderRadius': '16px',
                'maxWidth': '1200px',
                'boxShadow': '0 25px 50px -12px rgba(0,0,0,0.25)',
                'overflow': 'hidden'
            },
            children=[
                # Modal Header
                html.Div([
                    html.Div([
                        html.H3("Proposições Afetadas & Contexto", style={'margin': 0, 'color': '#1f2937', 'fontSize': '1.5rem'}),
                        html.P("Detalhes da votação e proposições relacionadas", style={'margin': '5px 0 0 0', 'color': '#6b7280', 'fontSize': '0.9rem'})
                    ]),
                    html.Div([
                        html.Button("Copiar", id='modal-copy-button', n_clicks=0, 
                                  style={'marginRight': '8px', 'padding': '8px 16px', 'background': '#10b981', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'cursor': 'pointer'}),
                        html.A("JSON", id='modal-open-json', href='#', target='_blank', 
                               style={'marginRight': '8px', 'padding': '8px 16px', 'background': '#3b82f6', 'color': 'white', 'textDecoration': 'none', 'borderRadius': '6px'}),
                        html.Button("✕", id='modal-close-button', n_clicks=0,
                                  style={'padding': '8px 12px', 'background': '#ef4444', 'color': 'white', 'border': 'none', 'borderRadius': '6px', 'cursor': 'pointer'})
                    ], style={'display': 'flex', 'alignItems': 'center'})
                ], style={
                    'display': 'flex', 
                    'justifyContent': 'space-between', 
                    'alignItems': 'center',
                    'padding': '20px 25px',
                    'borderBottom': '1px solid #e5e7eb',
                    'background': '#f9fafb'
                }),
                
                # Search Section
                html.Div([
                    html.Div([
                        dcc.Input(
                            id='modal-search', 
                            placeholder='Filtrar proposições por texto, sigla, número ou palavras da ementa...', 
                            type='text', 
                            style={
                                'width': '100%', 
                                'padding': '12px 16px', 
                                'border': '2px solid #e5e7eb', 
                                'borderRadius': '8px',
                                'fontSize': '14px',
                                'outline': 'none'
                            }
                        ),
                        html.Span(id='modal-count', style={'marginTop': '8px', 'fontSize': '0.9rem', 'color': '#6b7280', 'fontWeight': '500'})
                    ])
                ], style={'padding': '20px 25px', 'borderBottom': '1px solid #e5e7eb'}),
                
                # Content Grid
                html.Div([
                    html.Div([
                        html.H4("Resumo da Votação", style={'margin': '0 0 15px 0', 'color': '#374151', 'fontSize': '1.1rem'}),
                        html.Div(id='modal-row-summary')
                    ], style={
                        'background': '#f8fafc',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'maxHeight': '60vh', 
                        'overflowY': 'auto'
                    }),
                    
                    html.Div([
                        html.H4("Proposições Detalhadas", style={'margin': '0 0 15px 0', 'color': '#374151', 'fontSize': '1.1rem'}),
                        html.Div(id='modal-body')
                    ], style={
                        'maxHeight': '60vh', 
                        'overflowY': 'auto',
                        'padding': '20px'
                    })
                ], style={
                    'display': 'grid', 
                    'gridTemplateColumns': '400px 1fr', 
                    'gap': '0'
                })
            ]
        )
    ),
])

def get_display_columns(df):
    cols = list(df.columns)
    if 'proposicoesAfetadas_resumo' in cols:
        if 'proposicoesAfetadas' in cols:
            cols.remove('proposicoesAfetadas')
    return cols

def create_table(df, max_entries):
    display_columns = get_display_columns(df)
    
    if df.empty:
        return html.Div([
            html.Div([
                html.H3("Nenhum Dado Encontrado", style={'textAlign': 'center', 'color': '#6b7280', 'margin': '40px 0 20px 0'}),
                html.P("Tente ajustar os filtros ou selecionar outra legislatura.", style={'textAlign': 'center', 'color': '#9ca3af'})
            ], style={'padding': '40px', 'background': '#f9fafb', 'borderRadius': '12px', 'border': '2px dashed #d1d5db'})
        ])

    if 'ementa' in display_columns:
        df['ementa'] = df['ementa'].astype(str).apply(lambda x: (x[:120] + '...') if len(x) > 120 else x)
    if 'descricao' in display_columns:
        df['descricao'] = df['descricao'].astype(str).apply(lambda x: (x[:120] + '...') if len(x) > 120 else x)

    columns = []
    for col in display_columns:
        if col == 'proposicoesAfetadas_resumo':
            columns.append({
                "name": "Proposições Afetadas",
                "id": col,
            })
        elif col == 'aprovacao':
            columns.append({
                "name": "Resultado",
                "id": col,
            })
        elif col == 'siglaTipo':
            columns.append({
                "name": "Tipo",
                "id": col,
            })
        elif col == 'dataHoraRegistro':
            columns.append({
                "name": "Data/Hora",
                "id": col,
            })
        elif col == 'siglaOrgao':
            columns.append({
                "name": "Órgão",
                "id": col,
            })
        else:
            columns.append({"name": col.title(), "id": col})

    data_for_table = df[display_columns].to_dict("records")

    return dash_table.DataTable(
        id='generic-table',
        columns=columns,
        data=data_for_table,
        sort_action="native",
        page_size=max(int(sanitize_max_entries(max_entries) / 10), 10),
        style_table={
            'overflowX': 'auto',
            'border': '1px solid #e5e7eb',
            'borderRadius': '12px',
        },
        style_cell={
            'textAlign': 'left',
            'whiteSpace': 'normal',
            'height': 'auto',
            'minWidth': '120px',
            'maxWidth': '350px',
            'padding': '12px',
            'fontFamily': 'Inter, sans-serif',
            'fontSize': '14px',
            'border': '1px solid #f3f4f6',
        },
        style_header={
            'fontWeight': '600',
            'backgroundColor': '#f8fafc',
            'color': '#374151',
            'textTransform': 'uppercase',
            'fontSize': '12px',
            'letterSpacing': '0.5px',
            'border': '1px solid #e5e7eb',
        },
        style_data_conditional=[
            {
                'if': {'column_id': 'proposicoesAfetadas_resumo'},
                'color': '#2563eb',
                'textDecoration': 'underline',
                'cursor': 'pointer',
                'fontWeight': '500',
            },
            {
                'if': {'column_id': 'aprovacao', 'filter_query': '{aprovacao} = Aprovada'},
                'backgroundColor': '#dcfce7',
                'color': '#166534',
                'fontWeight': '600',
            },
            {
                'if': {'column_id': 'aprovacao', 'filter_query': '{aprovacao} contains Rejeitada'},
                'backgroundColor': '#fef2f2',
                'color': '#dc2626',
                'fontWeight': '600',
            },
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f9fafb'
            }
        ],
        style_data={
            'border': '1px solid #f3f4f6',
        }
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
            html.Div([
                html.H3("Nenhum Dado Encontrado", style={'textAlign': 'center', 'margin': '0 0 15px 0', 'color': '#374151'}),
                html.P(f"Não foram encontrados dados para '{DATA_TYPE_CONFIG[data_type]['display_name']}' na {legislatura}ª legislatura.", 
                      style={'textAlign': 'center', 'color': '#6b7280', 'margin': '0 0 15px 0'}),
                html.P("Verifique a conexão com o banco de dados ou ajuste os filtros.", 
                      style={'textAlign': 'center', 'color': '#9ca3af', 'fontSize': '0.9rem'})
            ], style={
                'padding': '60px 40px',
                'background': 'linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%)',
                'borderRadius': '16px',
                'border': '2px dashed #d1d5db',
                'textAlign': 'center'
            })
        ])
    
    df = pd.read_json(StringIO(json_data), orient='split')
    config = DATA_TYPE_CONFIG[data_type]

    # Stats Card
    total_records = len(df)
    stats_card = html.Div([
        html.Div([
            html.Div([
                html.H3(f"{total_records:,}", style={'margin': '0', 'fontSize': '2.5rem', 'fontWeight': '700', 'color': '#059669'}),
                html.P(f"Total de {config['display_name']} Carregados", style={'margin': '5px 0 0 0', 'color': '#065f46', 'fontWeight': '500'})
            ], style={'textAlign': 'center'}),
            html.Div([
                html.Span(f"Legislatura {legislatura}", style={'background': '#dbeafe', 'color': '#1d4ed8', 'padding': '4px 12px', 'borderRadius': '20px', 'fontSize': '0.85rem', 'fontWeight': '500'}),
                html.Span(f"Limite: {sanitize_max_entries(max_entries):,}", style={'background': '#fef3c7', 'color': '#92400e', 'padding': '4px 12px', 'borderRadius': '20px', 'fontSize': '0.85rem', 'fontWeight': '500', 'marginLeft': '10px'})
            ], style={'textAlign': 'center', 'marginTop': '15px'})
        ])
    ], className="stats-card")

    # Graph
    graph_col_x = config.get('graph_column_x')
    graph_component = html.Div()
    
    if graph_col_x and graph_col_x in df.columns:
        counts = df.groupby(graph_col_x).size().reset_index(name='Contagem')
        hover_cols = config.get('graph_hover_data', [])
        
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
        
        color_discrete_map = {}
        if data_type == 'votacoes':
            color_discrete_map = {
                'Aprovada': '#10b981',
                'Rejeitada/Outro': '#ef4444',
                'Indefinido': '#6b7280'
            }
        
        fig = px.bar(
            count_df, 
            x=graph_col_x, 
            y='Contagem', 
            color=graph_col_x,
            color_discrete_map=color_discrete_map if color_discrete_map else None,
            hover_data=config.get('graph_hover_data', []),
            labels={graph_col_x: 'Categoria', 'Contagem': 'Quantidade'},
            title=f"Distribuição: {config['display_name']} - {legislatura}ª Legislatura",
            text='Contagem'
        )
        
        fig.update_traces(
            textposition='outside',
            textfont=dict(size=12, color='#374151'),
            hovertemplate='<b>%{x}</b><br>Quantidade: %{y}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12, color='#374151'),
            title=dict(font=dict(size=16, color='#1f2937')),
            xaxis=dict(
                gridcolor='#f3f4f6',
                title_font=dict(size=14, color='#6b7280')
            ),
            yaxis=dict(
                gridcolor='#f3f4f6',
                title_font=dict(size=14, color='#6b7280')
            ),
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        graph_component = html.Div([
            dcc.Graph(id='generic-graph', figure=fig)
        ], className="chart-container")
    else:
        fig = px.bar(title="Não é possível gerar o gráfico: coluna de agregação não definida.")
        graph_component = html.Div([
            dcc.Graph(id='generic-graph', figure=fig)
        ], className="chart-container")

    return html.Div([
        stats_card,
        graph_component,
        html.Div([
            html.H4("Dados Detalhados", className="section-title"),
            html.Button("Resetar Filtro", id='reset-filter-button', n_clicks=0, className="reset-button"),
            html.Div(id='table-container', children=create_table(df, max_entries))
        ], className="table-section")
    ])

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
    return df.to_json(date_format='iso', orient='split')

@app.callback(
    Output('loading-warning-container', 'children'),
    Input('max-entries', 'value')
)
def update_loading_warning(max_entries):
    max_entries = sanitize_max_entries(max_entries)
    if max_entries > 20000: # Aumentado o limite pois o DB é mais rápido
        return html.Div([
            html.Div([
                html.Div("!", className="warning-icon"),
                html.Div([
                    html.Strong("Atenção: Consulta Grande"),
                    html.Br(),
                    f"Limite de {max_entries:,} registros selecionado. A consulta pode ser mais lenta."
                ], style={'flex': '1'})
            ], className="warning-card")
        ])
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
            html.Div([
                html.Span("Filtro:", style={'marginRight': '8px'}),
                html.Strong(f"Filtrado por: {clicked_category}"),
                html.Span(f" ({len(filtered_df)} registros)", style={'color': '#6b7280', 'marginLeft': '8px'})
            ], className="filter-info"),
            create_table(filtered_df, max_entries)
        ])
    
    return html.Div([
        html.Div([
            html.Span("Todos:", style={'marginRight': '8px'}),
            html.Strong("Mostrando todos os dados"),
            html.Span(f" ({len(df)} registros)", style={'color': '#6b7280', 'marginLeft': '8px'})
        ], className="filter-info"),
        create_table(df, max_entries)
    ])

@app.callback(
    Output('modal-content-store', 'data', allow_duplicate=True),
    Input('generic-table', 'active_cell'),
    State('generic-data-store', 'data'),
    prevent_initial_call=True
)
def store_modal_content(active_cell, json_data):
    if not active_cell or not json_data:
        return None

    df = pd.read_json(StringIO(json_data), orient='split')
    row_idx = active_cell['row']
    col_id = active_cell['column_id']

    if col_id == 'proposicoesAfetadas_resumo':
        if row_idx < len(df):
            row = df.iloc[row_idx]
            proposicoes_list = row.get('proposicoesAfetadas', [])

            if isinstance(proposicoes_list, list) and proposicoes_list:
                try:
                    # Garantir que Timestamps sejam convertidos para string
                    row_dict = row.to_dict()
                    for k, v in row_dict.items():
                        if isinstance(v, pd.Timestamp):
                            row_dict[k] = v.isoformat()
                except Exception:
                    row_dict = {k: str(v) for k, v in row.items()}
                return {
                    "row": row_dict,
                    "proposicoes": proposicoes_list
                }

    return None

@app.callback(
    Output('proposicoes-modal', 'style'),
    Output('modal-body', 'children'),
    Output('modal-row-summary', 'children'),
    Output('modal-count', 'children'),
    Input('modal-content-store', 'data'),
    Input('modal-search', 'value')
)  
def show_modal(content, search_value):
    hidden_style = {'display': 'none'}
    if not content:
        return hidden_style, "", "", ""

    row = content.get('row', {})
    props = content.get('proposicoes', []) or []

    if search_value:
        sv = search_value.strip().lower()
        filtered = [p for p in props if sv in (p.get('text','').lower() + " " + p.get('details','').lower())]
    else:
        filtered = props

    summary_rows = []
    keys_to_show = [
        ('ID', 'id', 'ID'),
        ('Data', 'dataHoraRegistro', 'Data/Hora'),
        ('Orgao', 'siglaOrgao', 'Órgão'),
        ('Desc', 'descricao', 'Descrição'),
        ('Result', 'aprovacao', 'Resultado')
    ]
    
    for icon, key, label in keys_to_show:
        if key in row:
            value = str(row.get(key, ''))
            if key == 'descricao' and len(value) > 100:
                value = value[:100] + '...'
            summary_rows.append(
                html.Tr([
                    html.Td([
                        html.Span(icon, style={'marginRight': '8px'}),
                        html.Strong(label)
                    ], style={'padding': '8px 12px', 'verticalAlign': 'top', 'width': '40%', 'borderBottom': '1px solid #f3f4f6'}),
                    html.Td(value, style={'padding': '8px 12px', 'borderBottom': '1px solid #f3f4f6', 'wordBreak': 'break-word'})
                ])
            )

    summary_table = html.Table(
        summary_rows, 
        style={
            'width': '100%', 
            'borderCollapse': 'collapse',
            'fontSize': '0.9rem',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'overflow': 'hidden',
            'border': '1px solid #e5e7eb'
        }
    )

    prop_children = []
    for i, p in enumerate(filtered):
        text = p.get('text', 'Proposição não identificada')
        details = p.get('details', '') or "Ementa não disponível."
        details_truncated = (details[:800] + '...') if len(details) > 800 else details
        prop_json_href = "data:application/json;charset=utf-8," + urllib.parse.quote(json.dumps(p, ensure_ascii=False, indent=2))
        
        prop_children.append(
            html.Div([
                html.Details([
                    html.Summary([
                        html.Span("📄", style={'marginRight': '8px'}),
                        html.Strong(text)
                    ], style={'cursor': 'pointer', 'padding': '12px', 'background': '#f8fafc', 'borderRadius': '8px', 'border': '1px solid #e5e7eb'}),
                    html.Div([
                        html.Div(details_truncated, style={
                            'whiteSpace': 'pre-wrap', 
                            'lineHeight': '1.6',
                            'color': '#374151',
                            'background': '#f9fafb',
                            'padding': '15px',
                            'borderRadius': '8px',
                            'border': '1px solid #f3f4f6',
                            'margin': '10px 0'
                        }),
                        html.Div([
                            html.A("Abrir JSON", href=prop_json_href, target="_blank", style={
                                'background': '#3b82f6',
                                'color': 'white',
                                'padding': '6px 12px',
                                'borderRadius': '6px',
                                'textDecoration': 'none',
                                'fontSize': '0.85rem',
                                'fontWeight': '500'
                            }),
                        ], style={'marginTop': '10px'})
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginBottom': '15px'})
            ])
        )

    body_children = prop_children if prop_children else [
        html.Div([
            html.Div("🧐", style={'fontSize': '3rem', 'textAlign': 'center', 'color': '#d1d5db', 'marginBottom': '15px'}),
            html.P("Nenhuma proposição encontrada para o filtro atual.", style={'textAlign': 'center', 'color': '#6b7280'})
        ], style={'padding': '40px', 'textAlign': 'center'})
    ]

    modal_style = {
        'display': 'block',
        'position': 'fixed',
        'zIndex': '3000',
        'left': 0,
        'top': 0,
        'width': '100%',
        'height': '100%',
        'overflow': 'auto',
        'backgroundColor': 'rgba(0,0,0,0.6)',
        'padding': '20px'
    }

    count_text = f"{len(filtered)} de {len(props)} proposição(ões) encontrada(s)"

    return modal_style, body_children, summary_table, count_text

@app.callback(
    Output('modal-content-store', 'data'),
    Input('modal-close-button', 'n_clicks'),
    prevent_initial_call=True
)
def close_modal(n_clicks):
    return None

@app.callback(
    Output('modal-open-json', 'href'),
    Input('modal-content-store', 'data')
)
def update_json_link(content):
    if not content:
        return '#'
    payload = json.dumps(content, ensure_ascii=False, indent=2)
    return "data:application/json;charset=utf-8," + urllib.parse.quote(payload)

@app.callback(
    Output('modal-copy-button', 'children'),
    Input('modal-copy-button', 'n_clicks'),
    State('modal-content-store', 'data'),
    prevent_initial_call=True
)
def copy_modal_text(n_clicks, content):
    if not content:
        return "Copiar resumo"
    return "Use 'Abrir JSON' para copiar"

if __name__ == "__main__":
    if db_engine:
        app.run(debug=True)
    else:
        print("\n\n*** A APLICAÇÃO NÃO PODE INICIAR. VERIFIQUE AS CONFIGURAÇÕES DO BANCO DE DADOS. ***\n\n")
