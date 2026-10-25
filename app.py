from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from src.data_cleaning import clean_data

st.set_page_config(page_title="TransitIQ | Passenger Analytics", page_icon="🚌", layout="wide", initial_sidebar_state="expanded")

# ---------- Design system ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --ink:#172b4d; --muted:#70809a; --teal:#12b8a6; --navy:#10213a; --paper:#f4f7fb; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: #f4f7fb; color:var(--ink); }
[data-testid="stHeader"] { background:rgba(244,247,251,.9); }
.block-container { padding-top:1.5rem; padding-bottom:2.5rem; max-width:1500px; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#10213a 0%,#172f50 100%); }
[data-testid="stSidebar"] * { color:#eef5ff !important; }
[data-testid="stSidebar"] [data-testid="stFileUploader"] section { background:#1d385a; border:1px dashed #5d7898; }
[data-testid="stSidebar"] hr { border-color:#38506e; }
.hero { background:linear-gradient(115deg,#10213a 0%,#173c5d 62%,#087e83 100%); padding:30px 34px; border-radius:22px; color:white; margin:0 0 22px 0; position:relative; overflow:hidden; box-shadow:0 12px 30px rgba(18,43,77,.13); }
.hero:after { content:'↗'; position:absolute; right:36px; top:8px; font-size:100px; color:rgba(255,255,255,.09); font-weight:800; }
.hero-kicker { color:#72e2d5; text-transform:uppercase; letter-spacing:2px; font-size:11px; font-weight:800; margin-bottom:9px; }
.hero h1 { color:white; font-family:Manrope,sans-serif; font-size:30px; line-height:1.2; margin:0 0 9px 0; font-weight:800; }
.hero p { color:#d7e7f5; font-size:14px; margin:0; max-width:760px; }
.section-head { font-family:Manrope,sans-serif; font-size:20px; font-weight:800; color:#172b4d; margin:14px 0 4px 0; }
.section-sub { color:#77869b; font-size:12px; margin:0 0 15px 0; }
.kpi { background:white; padding:18px 20px; border-radius:16px; border:1px solid #e7edf5; box-shadow:0 5px 18px rgba(24,48,80,.035); min-height:124px; }
.kpi-label { color:#7b8aa0; font-size:12px; font-weight:700; letter-spacing:.4px; text-transform:uppercase; }
.kpi-value { color:#172b4d; font-family:Manrope,sans-serif; font-size:28px; font-weight:800; margin-top:7px; }
.kpi-foot { color:#0c9f92; font-size:11px; margin-top:4px; font-weight:600; }
.panel { background:white; border:1px solid #e7edf5; border-radius:17px; padding:14px 16px 6px 16px; box-shadow:0 5px 18px rgba(24,48,80,.035); }
div[data-testid="stPlotlyChart"] { background:transparent; }
.stButton button, .stDownloadButton button { border-radius:10px; font-weight:700; }
.stDownloadButton button { background:#10213a; color:white; border:0; }
[data-testid="stDataFrame"] { border:1px solid #e7edf5; border-radius:12px; overflow:hidden; }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

path = Path(__file__).parent / "data" / "public_transport_data.csv"
with st.sidebar:
    st.markdown("<div style='font-size:12px;letter-spacing:2px;color:#72e2d5;font-weight:800;margin:12px 0 4px'>TRANSITIQ</div><div style='font-size:22px;font-weight:800;line-height:1.2'>Mobility<br>Intelligence</div><div style='font-size:12px;color:#b9cce0;margin-top:8px'>Passenger demand • Route insights</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("**WORKSPACE**")
    page = st.radio("Navigate", ["Overview", "Passenger Analytics", "Explore Data", "Data Quality", "About Project"], label_visibility="collapsed")
    st.divider()
    st.markdown("**DATA SOURCE**")
    upload = st.file_uploader("Upload your transport CSV", type=["csv"], help="Required columns: route, stop, date, hour, passengers. vehicle_capacity is optional.")
    st.caption("Demo dataset is synthetic. Upload official data for real-world analysis.")

try:
    raw = pd.read_csv(upload) if upload else pd.read_csv(path)
except Exception as e:
    st.error(f"Unable to load data: {e}")
    st.stop()

df = clean_data(raw)
required = {"route", "stop", "date", "hour", "passengers"}
if not required.issubset(df.columns):
    st.error("CSV must contain: route, stop, date, hour, passengers. vehicle_capacity is optional.")
    st.stop()
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["hour"] = pd.to_numeric(df["hour"], errors="coerce").fillna(0).clip(0, 23).astype(int)
df["passengers"] = pd.to_numeric(df["passengers"], errors="coerce").fillna(0)

st.markdown("<div class='hero'><div class='hero-kicker'>DATA MODELING & VISUALIZATION · MINI PROJECT</div><h1>Public Transport & Passenger<br>Traffic Analytics</h1><p>Turn passenger records into clear operational insights. Explore route performance, peak-hour demand, stop activity and daily travel patterns in one interactive workspace.</p></div>", unsafe_allow_html=True)

# Global filters
with st.container():
    st.markdown("<div class='section-head'>Your analytics workspace</div><div class='section-sub'>Filter the dataset to focus on routes and dates that matter.</div>", unsafe_allow_html=True)
    f1, f2, f3 = st.columns([1.2, 1.2, 1])
    all_routes = sorted(df.route.dropna().astype(str).unique().tolist())
    with f1:
        selected_routes = st.multiselect("Routes", all_routes, default=all_routes, key="routes_filter")
    valid_dates = df["date"].dropna()
    with f2:
        if not valid_dates.empty:
            min_d, max_d = valid_dates.min().date(), valid_dates.max().date()
            date_range = st.date_input("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
        else:
            date_range = ()
    with f3:
        hour_options = ["All day", "Morning peak (6–10)", "Midday (10–16)", "Evening peak (16–21)"]
        hour_filter = st.selectbox("Time of day", hour_options)

filtered = df[df.route.astype(str).isin(selected_routes)].copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[filtered.date.dt.date.between(date_range[0], date_range[1])]
if hour_filter == "Morning peak (6–10)": filtered = filtered[filtered.hour.between(6, 9)]
elif hour_filter == "Midday (10–16)": filtered = filtered[filtered.hour.between(10, 15)]
elif hour_filter == "Evening peak (16–21)": filtered = filtered[filtered.hour.between(16, 20)]

if filtered.empty:
    st.warning("No records match these filters. Try selecting more routes or a wider date range.")
    st.stop()

# Common chart theme
def polish(fig, height=330):
    fig.update_layout(height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="DM Sans, sans-serif", color="#6e7e94", size=11),
                      title=dict(font=dict(family="Manrope, sans-serif", size=15, color="#172b4d"), x=0.02),
                      margin=dict(l=12, r=12, t=54, b=12), legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0))
    fig.update_xaxes(showgrid=False, linecolor="#e9eef5", tickfont=dict(size=10))
    fig.update_yaxes(showgrid=True, gridcolor="#edf1f6", zeroline=False, linecolor="rgba(0,0,0,0)", tickfont=dict(size=10))
    return fig

def kpi(label, value, foot):
    st.markdown(f"<div class='kpi'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div><div class='kpi-foot'>↗ &nbsp;{foot}</div></div>", unsafe_allow_html=True)

if page == "Overview":
    total = int(filtered.passengers.sum())
    avg = int(filtered.passengers.mean()) if len(filtered) else 0
    busiest = filtered.groupby("route").passengers.sum().idxmax() if len(filtered) else "—"
    peak = filtered.groupby("hour").passengers.sum().idxmax() if len(filtered) else 0
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Passenger records", f"{total:,}", "passenger counts in selection")
    with c2: kpi("Active routes", f"{filtered.route.nunique():,}", "routes in selected view")
    with c3: kpi("Stops covered", f"{filtered.stop.nunique():,}", "unique stops represented")
    with c4: kpi("Peak hour", f"{int(peak):02d}:00", f"{int(filtered[filtered.hour == peak].passengers.sum()):,} passengers recorded")
    st.markdown("<div class='section-head'>Demand at a glance</div><div class='section-sub'>A quick view of route usage and how passenger activity changes through the day.</div>", unsafe_allow_html=True)
    left,right = st.columns([1.05,1])
    route = filtered.groupby("route", as_index=False).passengers.sum().sort_values("passengers", ascending=True)
    fig = px.bar(route, x="passengers", y="route", orientation="h", title="Passenger volume by route", color="passengers", color_continuous_scale=["#bdeee8", "#10a99a"])
    fig.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Passenger count")
    with left: st.markdown("<div class='panel'>", unsafe_allow_html=True); st.plotly_chart(polish(fig, 340), use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)
    hourly = filtered.groupby("hour", as_index=False).passengers.sum().sort_values("hour")
    fig2 = px.area(hourly, x="hour", y="passengers", title="Hourly passenger demand", markers=True)
    fig2.update_traces(line_color="#10a99a", fillcolor="rgba(18,184,166,.15)", marker=dict(size=5, color="#087e83"))
    fig2.update_xaxes(dtick=2, title="Hour of day", tickmode="linear")
    fig2.update_yaxes(title="Passenger count")
    with right: st.markdown("<div class='panel'>", unsafe_allow_html=True); st.plotly_chart(polish(fig2, 340), use_container_width=True); st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-head'>Route performance snapshot</div><div class='section-sub'>Routes ranked by recorded passenger volume.</div>", unsafe_allow_html=True)
    summary = filtered.groupby("route", as_index=False).agg(passengers=("passengers","sum"), records=("passengers","size"), stops=("stop","nunique"), avg_per_record=("passengers","mean")).sort_values("passengers", ascending=False)
    summary["avg_per_record"] = summary["avg_per_record"].round(1)
    st.dataframe(summary.rename(columns={"route":"Route", "passengers":"Passenger count", "records":"Records", "stops":"Unique stops", "avg_per_record":"Avg. per record"}), use_container_width=True, hide_index=True)

elif page == "Passenger Analytics":
    st.markdown("<div class='section-head'>Passenger demand intelligence</div><div class='section-sub'>Identify busy stops, daily patterns and route-by-hour hotspots.</div>", unsafe_allow_html=True)
    a,b = st.columns(2)
    stop = filtered.groupby("stop", as_index=False).passengers.sum().sort_values("passengers", ascending=False).head(12).sort_values("passengers")
    fig = px.bar(stop, x="passengers", y="stop", orientation="h", title="Top stops by passenger count", color="passengers", color_continuous_scale=["#c7d9f5","#4c78c8"])
    fig.update_layout(coloraxis_showscale=False, xaxis_title="Passenger count", yaxis_title="")
    with a: st.plotly_chart(polish(fig, 390), use_container_width=True)
    daily = filtered.dropna(subset=["date"]).groupby("date", as_index=False).passengers.sum()
    fig = px.line(daily, x="date", y="passengers", title="Daily passenger trend", markers=True)
    fig.update_traces(line_color="#7c5ce0", marker=dict(size=6))
    fig.update_layout(xaxis_title="Date", yaxis_title="Passenger count")
    with b: st.plotly_chart(polish(fig, 390), use_container_width=True)
    heat = filtered.pivot_table(index="route", columns="hour", values="passengers", aggfunc="sum", fill_value=0)
    fig = px.imshow(heat, aspect="auto", title="Route × hour demand heatmap", labels={"x":"Hour of day", "y":"Route", "color":"Passengers"}, color_continuous_scale="Teal")
    st.plotly_chart(polish(fig, max(300, 35 * len(heat) + 100)), use_container_width=True)
    st.info("Interpretation tip: darker heatmap cells indicate higher recorded passenger counts for a route and hour. These sample records are synthetic and should not be treated as official ridership statistics.")

elif page == "Explore Data":
    st.markdown("<div class='section-head'>Explore the records</div><div class='section-sub'>Inspect, search and export the filtered passenger dataset.</div>", unsafe_allow_html=True)
    search = st.text_input("Search route or stop", placeholder="e.g. R1, Central Station")
    view = filtered.copy()
    if search:
        mask = view.route.astype(str).str.contains(search, case=False, na=False) | view.stop.astype(str).str.contains(search, case=False, na=False)
        view = view[mask]
    st.caption(f"Showing {len(view):,} of {len(filtered):,} filtered records")
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.download_button("⬇ Download filtered CSV", view.to_csv(index=False).encode("utf-8"), "filtered_transport_data.csv", "text/csv")
    st.markdown("<div class='section-head'>Dataset structure</div>", unsafe_allow_html=True)
    schema = pd.DataFrame({"Column":df.columns, "Data type":[str(x) for x in df.dtypes], "Missing values":[int(df[c].isna().sum()) for c in df.columns], "Unique values":[int(df[c].nunique()) for c in df.columns]})
    st.dataframe(schema, use_container_width=True, hide_index=True)

elif page == "Data Quality":
    st.markdown("<div class='section-head'>Data quality monitor</div><div class='section-sub'>Review missing values, duplicate rows and the cleaned dataset.</div>", unsafe_allow_html=True)
    q1,q2,q3 = st.columns(3)
    with q1: kpi("Raw rows", f"{len(raw):,}", "rows loaded from source")
    with q2: kpi("Clean rows", f"{len(df):,}", "rows after cleaning")
    with q3: kpi("Rows removed", f"{max(0,len(raw)-len(df)):,}", "difference after cleaning")
    missing = raw.isna().sum().rename("Missing values").reset_index().rename(columns={"index":"Column"})
    fig = px.bar(missing, x="Column", y="Missing values", title="Missing values by column", color="Missing values", color_continuous_scale=["#c7d9f5","#e07a5f"])
    fig.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="Missing values")
    st.plotly_chart(polish(fig, 300), use_container_width=True)
    st.markdown("**Cleaned data preview**")
    st.dataframe(df.head(100), use_container_width=True, hide_index=True)
    st.download_button("⬇ Download cleaned CSV", df.to_csv(index=False).encode("utf-8"), "cleaned_transport_data.csv", "text/csv")

else:
    st.markdown("<div class='section-head'>About this project</div><div class='section-sub'>A student mini project on data modeling and interactive passenger-demand visualization.</div>", unsafe_allow_html=True)
    x,y = st.columns([1.15,1])
    with x:
        st.markdown("### Project objective")
        st.write("To organize public transport passenger records and visualize route utilization, stop activity, and peak-hour patterns through an interactive dashboard.")
        st.markdown("### Technology stack")
        st.markdown("- **Python** — data processing and analysis\n- **Pandas** — data cleaning and aggregation\n- **Plotly** — interactive charts\n- **Streamlit** — dashboard interface\n- **MySQL / SQL** — schema and sample analytical queries")
    with y:
        st.markdown("### Dashboard features")
        st.markdown("- Interactive route, date and time filters\n- KPI cards for key transport indicators\n- Route ranking and hourly demand charts\n- Stop-level and daily trend analysis\n- Route-hour heatmap\n- CSV upload, data inspection and export\n- Data-quality summary")
        st.warning("The bundled dataset is synthetic demonstration data. Use a verified public transport dataset before drawing real-world conclusions.")
    st.markdown("### Data fields")
    st.dataframe(pd.DataFrame({"Field":["route","stop","date","hour","passengers","vehicle_capacity"],"Meaning":["Route identifier","Passenger stop","Observation date","Hour of day (0–23)","Recorded passenger count","Optional vehicle capacity"]}), use_container_width=True, hide_index=True)

st.markdown("<div style='text-align:center;color:#9aa7b8;font-size:11px;padding:26px 0 0'>TRANSITIQ · Public Transport & Passenger Traffic Analytics · Academic demonstration dashboard</div>", unsafe_allow_html=True)
