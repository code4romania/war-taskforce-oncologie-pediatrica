import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import plotly.express as px

from django.apps import apps
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import pandas as pd

PatientRequest = apps.get_model("dispatch", "PatientRequest")

app = DjangoDash("OncoPedAdminDash")

# app.scripts.append_script({"external_url": "https://cdn.plot.ly/plotly-locale-ro-latest.js"})


def layout():
    min_date = PatientRequest.objects.earliest("created_at").created_at.date()

    return html.Div(
        [
            dbc.Row(
                dbc.Col(
                    [
                        dcc.DatePickerRange(
                            id="date-range",
                            number_of_months_shown=3,
                            min_date_allowed=min_date,
                            max_date_allowed=timezone.localtime().date(),
                            initial_visible_month=min_date,
                            clearable=True,
                            display_format="DD MMM YY"
                            # start_date_placeholder_text=str(_("Start Date")),
                            # end_date_placeholder_text=str( _("End Date")),
                        ),
                    ],
                    className="d-flex justify-content-start align-items-center",
                ),
                className="mb-4"
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Row(dbc.Col(html.Div(id="graphs"))),
                        # className="col-10 d-flex justify-content-center align-items-center",
                        className="col-10",
                    ),
                    dbc.Col(
                        dbc.Row(dbc.Col(html.Div(id="counters"))),
                        className="col-2 d-flex justify-content-center align-items-center",
                    ),
                ]
            ),
        ],
        className="container-fluid",
    )


app.layout = layout()


@app.callback(
    [
        Output("graphs", "children"),
        Output("counters", "children"),
    ],
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def build_dashboard(start_date, end_date, *args, **kwargs):

    # q = PatientRequest.objects

    # if start_date and end_date:
    #     q = q.filter(created_at__gte=start_date, created_at__lte=end_date)
    # if start_date and not end_date:
    #     q = q.filter(created_at__gte=start_date)
    # if not start_date and end_date:
    #     q = q.filter(created_at__lte=end_date)

    from datetime import date
    from random import randint, choice

    df = pd.DataFrame(
        # q.values(
        #     "id",
        #     "created_at",
        # )
        [
            {"id": 1, "created_at": date(2022, 3, i), "category": choice(["Alpha", "Beta", "Gamma"])}
            for i in range(11, 19)
            for x in range(randint(0, 38))
        ]
    )
    # df.created_at = df.created_at.dt.date
    df = df.groupby(["created_at", "category"], as_index=False).count()
    df.rename(columns={"created_at": "Dată", "id": "Solicitări", "category": "Categorie"}, inplace=True)
    print(df)

    fig = px.area(
        df,
        x=df["Dată"],
        y=df["Solicitări"],
        color=df["Categorie"],
        markers=True
        # text=df["Solicitări"],
    )
    fig.layout.template = "plotly_white"
    fig.layout.hovermode = "x"
    fig.layout.title = "Evoluție Solicitări"
    # fig.layout.font.size = 14
    fig.layout.margin.t = 40
    fig.layout.margin.b = 15
    fig.layout.margin.l = 10
    fig.layout.margin.r = 30
    fig.update_layout(title_x=0.5)

    graph = [
        dcc.Graph(
            id="requests-line",
            responsive=True,
            figure={
                        'data': [
                            {
                                'type': 'area',
                                'mode': 'markers+lines',
                                'x': df["Dată"],
                                'y': df["Solicitări"],
                                # 'color': df["Categorie"],
                                # 'split_lines': df["Categorie"],
                                'showlegend': False,
                                "fill": "tozeroy"
                            }
                        ],
                        'layout': {
                            'title': "Evoluție Solicitări",
                            # 'margin': {
                            #     't': 40,
                            #     'b': 15,
                            #     'l': 10,
                            #     'r': 30,
                            # },
                            # 'legend': {
                            #     'x': 0.6,
                            #     'y': 1
                            # },
                        }
                    },
            config={"displayModeBar": False},
            # style={"height": "70vh"},
        )
    ]

    return html.P(graph), html.P(end_date)
