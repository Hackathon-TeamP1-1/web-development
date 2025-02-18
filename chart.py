import streamlit as st
import pandas as pd
import plotly.express as px

# إعداد الصفحة في Streamlit
st.set_page_config(page_title="Renewable Energy Consumption Tracker", layout="wide")

# عنوان التطبيق
st.title("📊 Renewable Energy Consumption Tracker")
st.markdown("### تصور بياني لاستهلاك الطاقة المتجددة حسب الأشهر")

# تحميل ملف CSV
df = pd.read_csv("all_variables_merged_interpolated.csv")

# تحويل رقم الشهر إلى أسماء
df["Month"] = df["MO"].map({
    1: "January", 2: "February", 3: "March", 4: "April", 
    5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 
    10: "October", 11: "November", 12: "December"
})

# اختيار عمود استهلاك الطاقة
df["Energy Consumption (MWh)"] = df["ALLSKY_SFC_SW_DWN"]

# إزالة القيم غير الصالحة (مثلاً، القيم السالبة أو غير المحددة)
df = df[df["Energy Consumption (MWh)"] > 0]

# تجميع القيم حسب الشهر (متوسط الاستهلاك لكل شهر)
df_grouped = df.groupby("Month", as_index=False)["Energy Consumption (MWh)"].mean()

# رسم البيانات باستخدام Plotly
fig = px.bar(df_grouped, x="Month", y="Energy Consumption (MWh)", 
             title="استهلاك الطاقة المتجددة حسب الأشهر",
             color="Energy Consumption (MWh)", 
             color_continuous_scale="Viridis")

# تحسين المظهر
fig.update_layout(
    xaxis_title="الشهر",
    yaxis_title="استهلاك الطاقة (MWh)",
    template="plotly_dark"
)

# عرض المخطط في Streamlit
st.plotly_chart(fig, use_container_width=True)