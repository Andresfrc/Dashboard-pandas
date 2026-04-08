import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, dash_table, dcc, html
from flask import has_request_context

from database import obtener_estudiantes


def fig_vacia(mensaje="Sin datos suficientes"):
    fig = go.Figure()
    fig.add_annotation(
        text=mensaje,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color="#7f8c8d"),
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="#f9f9f9",
        plot_bgcolor="#f9f9f9",
    )
    return fig


def creartablero(server):
    appnotas = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix="/tablero/",
        suppress_callback_exceptions=True,
    )

    def serve_layout():
        dataf = obtener_estudiantes()
        if dataf.empty:
            min_edad = 0
            max_edad = 0
            min_prom = 0.0
            max_prom = 5.0
            carreras = []
        else:
            min_edad = int(dataf["edad"].min())
            max_edad = int(dataf["edad"].max())
            min_prom = float(dataf["promedio"].min())
            max_prom = float(dataf["promedio"].max())
            carreras = dataf["carrera"].dropna().unique()

        if has_request_context():
            from flask import session

            nombre = session.get("nombre", "Invitado")
            rol = session.get("rol", "")
        else:
            nombre = "Invitado"
            rol = ""

        return html.Div(
            [
                html.Div(
                    [
                        html.H1(
                            "TABLERO AVANZADO",
                            style={
                                "margin": "0",
                                "fontSize": "24px",
                                "color": "#2c3e50",
                                "fontFamily": "Poppins, sans-serif",
                            },
                        ),
                        html.Div(
                            [
                                html.Span(
                                    f"Usuario: {nombre}",
                                    style={
                                        "marginRight": "15px",
                                        "color": "#2c3e50",
                                        "fontFamily": "Poppins, sans-serif",
                                        "fontWeight": "bold",
                                    },
                                ),
                                html.Span(
                                    f"Rol: {rol}",
                                    style={
                                        "color": "#7f8c8d",
                                        "fontFamily": "Poppins, sans-serif",
                                        "fontSize": "13px",
                                        "marginRight": "15px",
                                    },
                                ),
                                html.A(
                                    "Registrar estudiante",
                                    href="/insertar_estudiante/",
                                    style={
                                        "backgroundColor": "#ff7a59",
                                        "color": "white",
                                        "padding": "7px 14px",
                                        "borderRadius": "999px",
                                        "fontFamily": "Poppins, sans-serif",
                                        "fontSize": "13px",
                                        "fontWeight": "bold",
                                        "textDecoration": "none",
                                        "marginRight": "12px",
                                        "boxShadow": "0 8px 16px rgba(255, 122, 89, 0.25)",
                                    },
                                ),
                                html.A(
                                    "Cerrar sesion",
                                    href="/logout",
                                    style={
                                        "color": "#c0392b",
                                        "fontFamily": "Poppins, sans-serif",
                                        "fontSize": "13px",
                                        "fontWeight": "bold",
                                        "textDecoration": "none",
                                    },
                                ),
                            ]
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "backgroundColor": "#ecf0f1",
                        "padding": "15px 30px",
                        "borderRadius": "10px",
                        "marginBottom": "25px",
                        "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "Buscar por nombre:",
                                    style={
                                        "fontFamily": "Poppins, sans-serif",
                                        "fontWeight": "bold",
                                    },
                                ),
                                dcc.Input(
                                    id="buscar-nombre",
                                    type="text",
                                    placeholder="Ej: Maria",
                                    debounce=True,
                                    style={
                                        "width": "100%",
                                        "padding": "8px 10px",
                                        "borderRadius": "6px",
                                        "border": "1px solid #bdc3c7",
                                        "fontFamily": "Poppins, sans-serif",
                                    },
                                ),
                            ],
                            style={"flex": "1", "minWidth": "200px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Actualizar datos:",
                                    style={
                                        "fontFamily": "Poppins, sans-serif",
                                        "fontWeight": "bold",
                                    },
                                ),
                                html.Button(
                                    "Actualizar",
                                    id="btn-refrescar",
                                    n_clicks=0,
                                    style={
                                        "width": "100%",
                                        "padding": "8px 10px",
                                        "borderRadius": "6px",
                                        "border": "1px solid #bdc3c7",
                                        "fontFamily": "Poppins, sans-serif",
                                        "backgroundColor": "#ecf0f1",
                                        "cursor": "pointer",
                                    },
                                ),
                            ],
                            style={"flex": "0.6", "minWidth": "150px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Filtrar por carrera:",
                                    style={
                                        "fontFamily": "Poppins, sans-serif",
                                        "fontWeight": "bold",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="filtro-carrera",
                                    options=[{"label": "Todas", "value": "__TODAS__"}]
                                    + [{"label": c, "value": c} for c in carreras],
                                    value="__TODAS__",
                                    clearable=True,
                                    placeholder="Todas las carreras",
                                ),
                            ],
                            style={"flex": "1", "minWidth": "200px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Rango de edades:",
                                    style={
                                        "fontFamily": "Poppins, sans-serif",
                                        "fontWeight": "bold",
                                    },
                                ),
                                dcc.RangeSlider(
                                    id="rango-edades",
                                    min=min_edad,
                                    max=max_edad,
                                    step=1,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                    value=[
                                        min_edad,
                                        max_edad,
                                    ],
                                ),
                            ],
                            style={"flex": "2", "minWidth": "250px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Rango de promedio:",
                                    style={
                                        "fontFamily": "Poppins, sans-serif",
                                        "fontWeight": "bold",
                                    },
                                ),
                                dcc.RangeSlider(
                                    id="rango-promedio",
                                    min=min_prom,
                                    max=max_prom,
                                    step=0.1,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                    value=[
                                        min_prom,
                                        max_prom,
                                    ],
                                ),
                            ],
                            style={"flex": "2", "minWidth": "250px"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "30px",
                        "flexWrap": "wrap",
                        "backgroundColor": "#f9f9f9",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "marginBottom": "20px",
                        "boxShadow": "0 2px 6px rgba(0,0,0,0.07)",
                    },
                ),
                html.Div(
                    id="kpis",
                    style={
                        "display": "flex",
                        "justifyContent": "space-around",
                        "marginBottom": "20px",
                        "gap": "15px",
                    },
                ),
                html.Div(
                    id="aviso-seleccion",
                    style={
                        "textAlign": "center",
                        "color": "#e67e22",
                        "fontFamily": "Poppins, sans-serif",
                        "marginBottom": "10px",
                        "fontWeight": "bold",
                    },
                ),
                
                
                
                dcc.Loading(
                    dash_table.DataTable(
                        id="tabla",
                        row_selectable="multi",
                        filter_action="native",
                        sort_action="native",
                        page_action="native",
                        page_size=10,
                        selected_rows=[],
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "textAlign": "center",
                            "padding": "10px",
                            "fontFamily": "Poppins, sans-serif",
                            "backgroundColor": "#ecf0f1",
                            "color": "#2c3e50",
                            "border": "1px solid #bdc3c7",
                        },
                        style_header={
                            "backgroundColor": "#2c3e50",
                            "color": "white",
                            "fontWeight": "bold",
                            "fontFamily": "Poppins, sans-serif",
                        },
                        style_data_conditional=[
                            {
                                "if": {"state": "selected"},
                                "backgroundColor": "#d5e8d4",
                                "border": "1px solid #82b366",
                            }
                        ],
                    ),
                    type="circle",
                ),
                html.Br(),
                dcc.Loading(dcc.Graph(id="grafico-detallado"), type="default"),
                html.Br(),
                dcc.Tabs(
                    [
                        dcc.Tab(label="Histograma", children=dcc.Graph(id="histograma")),
                        dcc.Tab(label="Dispersion", children=dcc.Graph(id="dispersion")),
                        dcc.Tab(label="Pie Edad", children=dcc.Graph(id="pie")),
                        dcc.Tab(
                            label="Barras Desempeno",
                            children=dcc.Graph(id="barras"),
                        ),
                    ],
                    style={"fontFamily": "Poppins, sans-serif"},
                ),
            ],
            style={
                "padding": "30px",
                "backgroundColor": "#ffffff",
                "minHeight": "100vh",
            },
            
                        
            
        )

    appnotas.layout = serve_layout

    @appnotas.callback(
        Output("tabla", "data"),
        Output("kpis", "children"),
        Output("tabla", "columns"),
        Output("grafico-detallado", "figure"),
        Output("histograma", "figure"),
        Output("dispersion", "figure"),
        Output("pie", "figure"),
        Output("barras", "figure"),
        Output("aviso-seleccion", "children"),
        Input("buscar-nombre", "value"),
        Input("btn-refrescar", "n_clicks"),
        Input("filtro-carrera", "value"),
        Input("rango-edades", "value"),
        Input("rango-promedio", "value"),
        Input("tabla", "selected_rows"),
    )
    def actualizar_comp(
        nombre_busqueda,
        _n_clicks,
        carrera,
        rangoedad,
        rangoprome,
        selected_rows,
    ):
        dataf = obtener_estudiantes()
        dataf["edad"] = pd.to_numeric(dataf["edad"], errors="coerce")
        dataf["promedio"] = pd.to_numeric(dataf["promedio"], errors="coerce")

        filtro = dataf[
            (dataf["edad"] >= rangoedad[0])
            & (dataf["edad"] <= rangoedad[1])
            & (dataf["promedio"] >= rangoprome[0])
            & (dataf["promedio"] <= rangoprome[1])
        ].copy()

        if carrera not in (None, "", "__TODAS__"):
            filtro = filtro[filtro["carrera"] == carrera].copy()
        if nombre_busqueda:
            texto = str(nombre_busqueda).strip()
            if texto:
                filtro = filtro[
                    filtro["nombre"].astype(str).str.contains(texto, case=False, na=False)
                ].copy()

        if selected_rows:
            filas_validas = [i for i in selected_rows if i < len(filtro)]
            filtro_grafico = filtro.iloc[filas_validas].copy()
            aviso = (
                f"Mostrando graficos para {len(filas_validas)} estudiante(s). "
                "Desmarca para ver todos."
            )
        else:
            filtro_grafico = filtro.copy()
            aviso = ""

        promedio = (
            round(filtro_grafico["promedio"].mean(), 2)
            if not filtro_grafico.empty
            else "-"
        )
        total = len(filtro_grafico)
        maximo = (
            round(filtro_grafico["promedio"].max(), 2)
            if not filtro_grafico.empty
            else "-"
        )

        if filtro_grafico.empty:
            fig_detalle = fig_vacia("Sin datos para el filtro seleccionado")
            fig_hist = fig_vacia("Sin datos para el filtro seleccionado")
            fig_disp = fig_vacia("Sin datos para el filtro seleccionado")
            fig_pie = fig_vacia("Sin datos para el filtro seleccionado")
            fig_barras = fig_vacia("Sin datos para el filtro seleccionado")
        else:
            fig_detalle = px.box(
                filtro_grafico,
                x="carrera",
                y="promedio",
                title="Distribucion de promedios",
                template="plotly_white",
            )
            fig_hist = px.histogram(
                filtro_grafico,
                x="promedio",
                color="carrera",
                nbins=15,
                title="Histograma de promedios",
                template="plotly_white",
            )
            fig_disp = px.scatter(
                filtro_grafico,
                x="edad",
                y="promedio",
                color="carrera",
                size="promedio",
                title="Dispersion edad vs promedio",
                template="plotly_white",
            )

            fg = filtro_grafico.copy()
            fg["Rango Edad"] = pd.cut(
                fg["edad"],
                bins=[0, 20, 22, 25, 30, 100],
                labels=["<=20", "21-22", "23-25", "26-30", "30+"],
            )
            edad_prom = (
                fg.groupby("Rango Edad", observed=True)["promedio"].mean().reset_index()
            )
            edad_prom = edad_prom.dropna()

            if edad_prom.empty:
                fig_pie = fig_vacia("No hay variedad de edades suficiente")
            else:
                fig_pie = px.pie(
                    edad_prom,
                    names="Rango Edad",
                    values="promedio",
                    title="Promedio por rango de edad",
                )

            if "desempenio" in filtro_grafico.columns:
                conteo = filtro_grafico["desempenio"].value_counts().reset_index()
                conteo.columns = ["Desempeno", "Cantidad"]
                fig_barras = px.bar(
                    conteo,
                    x="Desempeno",
                    y="Cantidad",
                    color="Desempeno",
                    title="Distribucion de desempeno",
                    template="plotly_white",
                    category_orders={"Desempeno": ["Bajo", "Medio", "Alto"]},
                )
            else:
                fig_barras = fig_vacia("Columna 'desempenio' no encontrada")

        def kpi_card(titulo, valor, color):
            return html.Div(
                [
                    html.H6(
                        titulo,
                        style={
                            "color": "#7f8c8d",
                            "marginBottom": "5px",
                            "fontFamily": "Poppins, sans-serif",
                            "fontSize": "13px",
                            "margin": "0 0 5px 0",
                        },
                    ),
                    html.H3(
                        str(valor),
                        style={
                            "color": color,
                            "margin": "0",
                            "fontFamily": "Poppins, sans-serif",
                        },
                    ),
                ],
                style={
                    "backgroundColor": "#ecf0f1",
                    "padding": "20px 30px",
                    "borderRadius": "10px",
                    "textAlign": "center",
                    "flex": "1",
                    "boxShadow": "0 2px 6px rgba(0,0,0,0.08)",
                },
            )

        kpis = html.Div(
            [
                kpi_card("Promedio General", promedio, "#2c3e50"),
                kpi_card("Total Estudiantes", total, "#27ae60"),
                kpi_card("Promedio Maximo", maximo, "#e74c3c"),
            ],
            style={"display": "flex", "gap": "15px", "width": "100%"},
        )

        return (
            filtro.to_dict("records"),
            kpis,
            [{"name": col, "id": col} for col in filtro.columns],
            fig_detalle,
            fig_hist,
            fig_disp,
            fig_pie,
            fig_barras,
            aviso,
        )

    return appnotas
