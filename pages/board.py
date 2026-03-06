import json
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import streamlit as st
from support import download_get_url

load_dotenv()

with st.container(border=True):
    st.image("pictures/vodous_tmavy_main.png", width="stretch")

url_base = os.getenv("FAST_API_URL_BASE")
url_statistics = os.getenv("FAST_API_URL_STATISTICS_WEEKLY")
url = url_base + url_statistics
statistics_responce = download_get_url(url)
if statistics_responce["status"] == 200:
    statistics_data = json.loads(statistics_responce["data"])["data"]
else:
    statistics_data = []

stat_data = pd.DataFrame(statistics_data["data"])
# wide -> long
df_long = stat_data.melt(
    id_vars="date_serial",
    value_vars=[
        "word_rating_count_by_date",
        "storytelling_story_count_by_date",
        "storytelling_result_count_by_date",
    ],
    var_name="metric",
    value_name="count"
)

df_long["metric"] = df_long["metric"].replace({
    "word_rating_count_by_date": "Word rating",
    "storytelling_story_count_by_date": "Storytelling story",
    "storytelling_result_count_by_date": "Storytelling result",
})

fig = px.bar(
    df_long,
    x="date_serial",
    y="count",
    color="metric",
    barmode="group",   # důležité: sloupce vedle sebe
    labels={
        "date_serial": "",
        "count": "Count",
        "metric": "Typ akce",
    }
)
fig.update_layout(
    legend=dict(
        orientation="h",
        y=-0.2,
        x=0.5,
        xanchor="center"
    )
)

fig.update_layout(legend_title_text="")

st.plotly_chart(fig)
