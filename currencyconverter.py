import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# Page Configure
st.set_page_config(
    page_title="Currency Intelligence System",
    page_icon="💱",
    layout="wide"
)

# constants
CURRENCIES = ["USD", "INR", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY"]

if "page" not in st.session_state:
    st.session_state.page = "Home"

page = st.session_state.page

# Home Page
if page == "Home":

    # ---------- CUSTOM CSS ----------
    st.markdown("""
    <style>

    /* ---------- PAGE BACKGROUND ---------- */
    .stApp {
        background: linear-gradient(135deg, #667eea, #764ba2);
    }

    /* ---------- HERO ---------- */
    .hero-title {
        text-align: center;
        font-size: 56px;
        font-weight: 900;
        color: white;
        text-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }

    .hero-sub {
        text-align: center;
        font-size: 19px;
        color: #e0e0e0;
        margin-top: -8px;
    }

    /* ---------- CARDS ---------- */
    .card {
        border-radius: 26px;
        padding: 34px;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
        color: white;
        box-shadow: 0 20px 45px rgba(0,0,0,0.25);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }

    /* Glow animation */
    .card::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15), transparent 60%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .card:hover::before {
        opacity: 1;
    }

    .card:hover {
        transform: translateY(-14px) scale(1.05);
        box-shadow: 0 35px 70px rgba(0,0,0,0.45);
    }

    .card h3 {
        font-size: 28px;
        margin-bottom: 12px;
    }

    .card p {
        font-size: 17px;
        line-height: 1.6;
        opacity: 0.95;
    }

    /* ---------- CARD COLORS ---------- */
    .card.converter {
        background: linear-gradient(135deg, #00c6ff, #0072ff);
    }

    .card.analysis {
        background: linear-gradient(135deg, #f7971e, #ffd200);
        color: #1a1a1a;
    }

    .card.compare {
        background: linear-gradient(135deg, #ff512f, #dd2476);
    }

    /* ---------- BUTTON ---------- */
    .stButton > button {
        width: 100%;
        border-radius: 18px;
        padding: 15px 0;
        font-size: 16px;
        font-weight: 700;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        color: #002b36;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: scale(1.08);
        box-shadow: 0 15px 40px rgba(0,242,254,0.7);
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------- HERO ----------
    st.markdown("<div class='hero-title'>Currency Intelligence System</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-sub'>Smart currency conversion and analytics in one powerful dashboard</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ---------- CARDS ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card converter">
            <div>
                <h3>💱 Currency Converter</h3>
                <p>Instant real-time currency conversion with global accuracy</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Converter ➜", key="conv"):
            st.session_state.page = "Converter"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card analysis">
            <div>
                <h3>📊 Historical Analysis</h3>
                <p>Multi-year trends, volatility insights, and smart analytics</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Analysis ➜", key="analysis"):
            st.session_state.page = "Analysis"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="card compare">
            <div>
                <h3>📈 Currency Comparison</h3>
                <p>Visualize and compare currency strength instantly</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Comparison ➜", key="compare"):
            st.session_state.page = "Comparison"
            st.rerun()


# CURRENCY CONVERTER PAGE
elif page == "Converter":

    if st.button("⬅ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

    st.title("💱 Real-Time Currency Converter")

    amount = st.number_input("Enter Amount", min_value=0.0, value=1.0)

    col1, col2 = st.columns(2)
    base = col1.selectbox("From Currency", CURRENCIES)
    target = col2.selectbox("To Currency", CURRENCIES)

    if st.button("Convert 💰"):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base}"
            response = requests.get(url).json()
            rate = response["rates"][target]

            st.success(f"{amount} {base} = {amount * rate:.2f} {target}")
            st.caption(f"1 {base} = {rate:.4f} {target}")
            st.caption(f"Last Updated: {response['date']}")

        except Exception:
            st.error("Error fetching exchange rate data")

# Analysis page
elif page == "Analysis":

    if st.button("⬅ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

    st.title("📊 Historical Currency Analysis")

    # ---------------- INPUTS ----------------
    col1, col2 = st.columns(2)
    base = col1.selectbox("Base Currency", CURRENCIES)
    target = col2.selectbox("Target Currency", CURRENCIES)

    col3, col4 = st.columns(2)
    start_year = col3.selectbox("From Year", range(2005, datetime.now().year))
    end_year = col4.selectbox("To Year", range(start_year, datetime.now().year + 1))

    if st.button("Analyze 📈"):
        dates, rates = [], []

        with st.spinner("Fetching historical data..."):
            for year in range(start_year, end_year + 1):
                url = f"https://api.frankfurter.app/{year}-01-01..{year}-12-31?from={base}&to={target}"
                data = requests.get(url).json()

                for d, r in data["rates"].items():
                    dates.append(d)
                    rates.append(r[target])

        # ---------------- DATAFRAME ----------------
        df = pd.DataFrame({
            "Date": pd.to_datetime(dates),
            "Rate": rates
        }).sort_values("Date")

        # ---------------- MAIN TREND ----------------
        st.subheader("📈 Exchange Rate Trend")

        fig_main = px.line(
            df,
            x="Date",
            y="Rate",
            title=f"{base} → {target} Exchange Rate Trend"
        )
        st.plotly_chart(fig_main, use_container_width=True)

        # ---------------- METRICS ----------------
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Highest", f"{df['Rate'].max():.2f}")
        c2.metric("Lowest", f"{df['Rate'].min():.2f}")
        c3.metric("Average", f"{df['Rate'].mean():.2f}")
        c4.metric("Volatility", f"{df['Rate'].std():.2f}")

        # ---------------- YEARLY ANALYSIS ----------------
        st.subheader("📆 Year-wise Performance")

        df["Year"] = df["Date"].dt.year
        yearly_avg = df.groupby("Year")["Rate"].mean().reset_index()

        fig_year = px.bar(
            yearly_avg,
            x="Year",
            y="Rate",
            title="Average Exchange Rate per Year",
            text_auto=".2f"
        )
        st.plotly_chart(fig_year, use_container_width=True)

        best_year = yearly_avg.loc[yearly_avg["Rate"].idxmax()]
        worst_year = yearly_avg.loc[yearly_avg["Rate"].idxmin()]

        colA, colB = st.columns(2)
        colA.success(f"📈 Best Year: {int(best_year['Year'])} (Avg: {best_year['Rate']:.2f})")
        colB.error(f"📉 Worst Year: {int(worst_year['Year'])} (Avg: {worst_year['Rate']:.2f})")

        # ---------------- INSIGHTS ----------------
        st.subheader("Key Insights")

        st.info(f"""
        • The **strongest performance** was observed in **{int(best_year['Year'])}**.  
        • The **weakest year** was **{int(worst_year['Year'])}**.  
        """)

        # ---------------- DOWNLOAD ----------------
        st.download_button(
            "Download Full Analysis (CSV)",
            df.to_csv(index=False),
            file_name="historical_currency_analysis.csv",
            mime="text/csv"
        )

# Comparison page
elif page == "Comparison":

    if st.button("⬅ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

    st.title("📈 Currency Strength Comparison")

    # ---------------- INPUTS ----------------
    base = st.selectbox("Base Currency", CURRENCIES)
    targets = st.multiselect(
        "Select Currencies to Compare",
        [c for c in CURRENCIES if c != base],
        default=["INR", "EUR", "GBP"]
    )

    col1, col2 = st.columns(2)
    start_year = col1.selectbox("From Year", range(2010, datetime.now().year))
    end_year = col2.selectbox("To Year", range(start_year, datetime.now().year + 1))

    if st.button("Analyze Comparison 📊"):
        if not targets:
            st.warning("Please select at least one currency to compare.")
        else:
            try:
                # ============================================================
                # 1) CURRENT SNAPSHOT DATA (RESTORES YOUR OLD VALUE BOX)
                # ============================================================
                url = f"https://api.exchangerate-api.com/v4/latest/{base}"
                data = requests.get(url).json()

                rates = [data["rates"][c] for c in targets]

                df_snapshot = pd.DataFrame({
                    "Currency": targets,
                    "Current Exchange Rate": rates
                }).sort_values("Current Exchange Rate", ascending=False)

                st.subheader("📌 Current Exchange Rates")
                st.dataframe(df_snapshot, use_container_width=True)

                fig_bar = px.bar(
                    df_snapshot,
                    x="Currency",
                    y="Current Exchange Rate",
                    title=f"Current Currency Strength vs {base}",
                    text_auto=".4f"
                )
                st.plotly_chart(fig_bar, use_container_width=True)

                strongest_now = df_snapshot.iloc[-1]["Currency"]
                weakest_now = df_snapshot.iloc[0]["Currency"]

                colA, colB = st.columns(2)
                colA.success(f"Strongest (Current): {strongest_now}")
                colB.error(f"Weakest (Current): {weakest_now}")

                # ============================================================
                # 2) HISTORICAL MULTI-CURRENCY COMPARISON
                # ============================================================
                all_data = []

                with st.spinner("Fetching historical comparison data..."):
                    for currency in targets:
                        dates, hist_rates = [], []

                        for year in range(start_year, end_year + 1):
                            url = f"https://api.frankfurter.app/{year}-01-01..{year}-12-31?from={base}&to={currency}"
                            hist_data = requests.get(url).json()

                            if "rates" in hist_data:
                                for d, r in hist_data["rates"].items():
                                    dates.append(d)
                                    hist_rates.append(r[currency])

                        if dates and hist_rates:
                            df_temp = pd.DataFrame({
                                "Date": pd.to_datetime(dates),
                                "Rate": hist_rates
                            }).sort_values("Date")

                            df_temp["Currency"] = currency
                            df_temp["Normalized"] = (df_temp["Rate"] / df_temp["Rate"].iloc[0]) * 100
                            all_data.append(df_temp)

                if all_data:
                    df_all = pd.concat(all_data, ignore_index=True)

                    # ---------------- LINE TREND ----------------
                    st.subheader("📈 Historical Exchange Rate Trend")

                    fig_line = px.line(
                        df_all,
                        x="Date",
                        y="Rate",
                        color="Currency",
                        title=f"Historical Exchange Rate Trend vs {base}"
                    )
                    st.plotly_chart(fig_line, use_container_width=True)

                    # ---------------- NORMALIZED PERFORMANCE ----------------
                    st.subheader("⚖️ Relative Performance (Normalized Index)")

                    fig_norm = px.line(
                        df_all,
                        x="Date",
                        y="Normalized",
                        color="Currency",
                        title="Relative Currency Performance (Starting Point = 100)"
                    )
                    st.plotly_chart(fig_norm, use_container_width=True)

                    # ---------------- VOLATILITY COMPARISON ----------------
                    st.subheader("📊 Volatility Comparison")

                    volatility_df = (
                        df_all.groupby("Currency")["Rate"]
                        .std()
                        .reset_index()
                        .rename(columns={"Rate": "Volatility"})
                        .sort_values("Volatility", ascending=False)
                    )

                    fig_vol = px.bar(
                        volatility_df,
                        x="Currency",
                        y="Volatility",
                        title="Currency Volatility Comparison",
                        text_auto=".4f"
                    )
                    st.plotly_chart(fig_vol, use_container_width=True)

                    # ---------------- YEARLY AVERAGE COMPARISON ----------------
                    st.subheader("📅 Year-wise Average Exchange Rate Comparison")

                    df_all["Year"] = df_all["Date"].dt.year
                    yearly_avg = (
                        df_all.groupby(["Year", "Currency"])["Rate"]
                        .mean()
                        .reset_index()
                    )

                    fig_yearly = px.line(
                        yearly_avg,
                        x="Year",
                        y="Rate",
                        color="Currency",
                        markers=True,
                        title="Average Exchange Rate by Year"
                    )
                    st.plotly_chart(fig_yearly, use_container_width=True)

                    # ---------------- FINAL INSIGHTS ----------------
                    final_perf = df_all.groupby("Currency")["Normalized"].last().reset_index()
                    strongest_hist = final_perf.loc[final_perf["Normalized"].idxmax(), "Currency"]
                    weakest_hist = final_perf.loc[final_perf["Normalized"].idxmin(), "Currency"]
                    most_volatile = volatility_df.iloc[0]["Currency"]

                    st.subheader("🔍 Comparison Insights")
                    c1, c2, c3 = st.columns(3)
                    c1.success(f"💪 Best Historical Performer: {strongest_hist}")
                    c2.error(f"📉 Weakest Historical Performer: {weakest_hist}")
                    c3.warning(f"🌪 Most Volatile Currency: {most_volatile}")

                    st.info(f"""
                    **Quick Summary**
                    - **Current strongest currency** in the selected set: **{strongest_now}**
                    - **Current weakest currency** in the selected set: **{weakest_now}**
                    - **Best historical performer** over the selected period: **{strongest_hist}**
                    - **Weakest historical performer** over the selected period: **{weakest_hist}**
                    - **Most volatile currency**: **{most_volatile}**
                    """)

                    # ---------------- DOWNLOAD ----------------
                    st.download_button(
                        "Download Comparison Data (CSV)",
                        df_all.to_csv(index=False),
                        file_name="currency_comparison_analysis.csv",
                        mime="text/csv"
                    )
                else:
                    st.error("No historical comparison data available for the selected currencies.")

            except Exception as e:
                st.error("Unable to fetch comparison data")

st.markdown("---")