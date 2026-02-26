import streamlit as st
import pandas as pd
import plotly.express as px

# 1️⃣ إعدادات الصفحة
st.set_page_config(page_title="SQL Performance Dashboard", layout="wide")
st.title("🚀 SQL Performance Tuning Dashboard")

@st.cache_data
def load_data():
    path = r"C:\Users\Marwan\Test Data\SQL_Performance_Analysis.csv"
    df = pd.read_csv(path)
    
    # --- تصحيح عمود Index Used بناءً على صورتك ---
    # أي حاجة فيها كلمة PRIMARY أو رقم أكبر من 0 نعتبرها 1
    def fix_index(val):
        val_str = str(val).upper()
        if "PRIMARY" in val_str or "1" in val_str:
            return 1
        return 0
    
    df['index_used_numeric'] = df['index_used'].apply(fix_index)

    # --- تصحيح الكفاءة (Efficiency) ---
    # هنحول الأعمدة لأرقام الأول
    df['rows_returned'] = pd.to_numeric(df['rows_returned'], errors='coerce').fillna(0)
    df['rows_examined'] = pd.to_numeric(df['rows_examined'], errors='coerce').fillna(0)
    
    # المعادلة: لو الـ examined بصفر، هنخلي الكفاءة 1 (100%) عشان الرقم ميبقاش آلاف
    def calc_efficiency(row):
        if row['rows_examined'] <= 0:
            return 1.0 if row['rows_returned'] > 0 else 0.0
        eff = row['rows_returned'] / row['rows_examined']
        return min(eff, 1.0) # عشان ميزيدش عن 100%

    df['efficiency_ratio_fixed'] = df.apply(calc_efficiency, axis=1)
    
    return df

try:
    df = load_data()

    # --- 4️⃣ حساب الـ KPIs ---
    col1, col2, col3, col4 = st.columns(4)

    total_q = len(df)
    avg_lat = df["execution_time_ms"].mean()
    idx_usage = (df["index_used_numeric"].mean() * 100)
    avg_eff = (df["efficiency_ratio_fixed"].mean() * 100)

    col1.metric("Total Queries", f"{total_q}")
    col2.metric("Avg Latency", f"{avg_lat:.2f} ms")
    col3.metric("Index Usage", f"{idx_usage:.1f}%")
    col4.metric("Avg Efficiency", f"{avg_eff:.2f}%")

    st.divider()

    # --- 5️⃣ الرسومات ---
    left_c, right_c = st.columns(2)
    with left_c:
        st.subheader("📊 Latency Distribution")
        fig1 = px.histogram(df, x="execution_time_ms", nbins=20, color_discrete_sequence=["#636EFA"])
        st.plotly_chart(fig1, use_container_width=True)

    with right_c:
        st.subheader("🎯 Efficiency vs Rows Examined")
        fig2 = px.scatter(df, x="rows_examined", y="execution_time_ms", 
                         size="rows_returned", color="efficiency_ratio_fixed",
                         color_continuous_scale="RdYlGn")
        st.plotly_chart(fig2, use_container_width=True)

    # --- 6️⃣ الجدول ---
    st.subheader("🚨 Top 10 Slowest Queries")
    top_10 = df.nlargest(10, "execution_time_ms")[["sql_text", "execution_time_ms", "index_used"]]
    st.dataframe(top_10, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error: {e}")