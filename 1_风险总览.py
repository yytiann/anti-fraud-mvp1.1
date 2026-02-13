import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv("data_sample.csv")

st.title("📊 风险总览")

# =========================
# 1️⃣ 核心指标区
# =========================

total_cases = len(data)
high_risk = len(data[data["label"] == 1])
suggest_ratio = round(high_risk / total_cases * 100, 2)

# 模拟指标（演示）
model_hit_rate = 28
manual_hit_rate = 19

col1, col2, col3, col4 = st.columns(4)

col1.metric("本月报案总数", f"{total_cases:,}")
col2.metric("建议提调比例", f"{suggest_ratio}%")
col3.metric("模型命中率", f"{model_hit_rate}%")
col4.metric("人工命中率", f"{manual_hit_rate}%")

st.divider()

# =========================
# 2️⃣ 高风险分布饼图
# =========================

st.subheader("🥧 高风险案件分布")

labels = ["高风险", "正常案件"]
sizes = [high_risk, total_cases - high_risk]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')

st.pyplot(fig1)

st.divider()

# =========================
# 3️⃣ 月度趋势折线图（模拟）
# =========================

st.subheader("📈 月度风险趋势")

# 模拟12个月趋势数据
months = pd.date_range(start="2024-01-01", periods=12, freq="M")
monthly_cases = np.random.randint(800, 1500, 12)
monthly_high_risk = np.random.randint(100, 400, 12)

trend_df = pd.DataFrame({
    "月份": months.strftime("%Y-%m"),
    "报案总数": monthly_cases,
    "高风险案件": monthly_high_risk
})

st.line_chart(trend_df.set_index("月份"))

st.divider()

# =========================
# 4️⃣ 规则触发 Top5
# =========================

st.subheader("📌 规则触发 Top5")

rule_top5 = [
    "短期投保",
    "高频报案",
    "黑名单命中",
    "历史调查记录",
    "异常金额波动"
]

for i, rule in enumerate(rule_top5, 1):
    st.write(f"{i}. {rule}")


# =========================
# 5️⃣ 风险热力图
# =========================
st.divider()
st.subheader("🔥 风险热力图（月份 × 风险等级）")

# 构造模拟月份数据
data["月份"] = np.random.choice(
    pd.date_range("2024-01-01", periods=6, freq="M").strftime("%Y-%m"),
    size=len(data)
)

# 统计高风险数量
heatmap_data = data.groupby(["月份", "label"]).size().unstack(fill_value=0)

fig_heat, ax_heat = plt.subplots()
im = ax_heat.imshow(heatmap_data.values)

ax_heat.set_xticks(range(len(heatmap_data.columns)))
ax_heat.set_xticklabels(["正常", "高风险"])

ax_heat.set_yticks(range(len(heatmap_data.index)))
ax_heat.set_yticklabels(heatmap_data.index)

ax_heat.set_title("风险热力分布")

plt.colorbar(im)
st.pyplot(fig_heat)

# =========================
# 6️⃣ 按险种分类分布图
# =========================
st.divider()
st.subheader("📊 按险种分类风险分布")

# 模拟险种字段（演示用）
insurance_types = ["重疾险", "医疗险", "意外险", "寿险"]
data["险种"] = np.random.choice(insurance_types, size=len(data))

risk_by_type = data.groupby("险种")["label"].sum()

fig_type, ax_type = plt.subplots()
ax_type.bar(risk_by_type.index, risk_by_type.values)
ax_type.set_title("各险种高风险案件数量")
ax_type.set_xlabel("险种")
ax_type.set_ylabel("高风险数量")

st.pyplot(fig_type)