import streamlit as st
import pandas as pd
import joblib
from xgboost import XGBClassifier
import numpy as np
from datetime import datetime

st.title("📋 批量案件列表")

# 读取数据
data = pd.read_csv("data_sample.csv")

# 初始化反馈列
if "manual_decision" not in data.columns:
    data["manual_decision"] = ""

if "decision_time" not in data.columns:
    data["decision_time"] = ""

if "feedback_label" not in data.columns:
    data["feedback_label"] = ""

# 加载模型
model = XGBClassifier()
model.load_model("model.json")
feature_columns = joblib.load("feature_columns.pkl")

# 计算风险分
scores = model.predict_proba(data[feature_columns])[:, 1]
data["risk_score"] = scores

# 风险等级
def risk_level(score):
    if score > 0.8:
        return "🔴 高风险"
    elif score > 0.5:
        return "🟠 中风险"
    else:
        return "🟢 低风险"

data["risk_level"] = data["risk_score"].apply(risk_level)

# =========================
# 筛选区
# =========================

st.subheader("🔍 筛选条件")

col1, col2 = st.columns(2)

risk_filter = col1.selectbox(
    "风险等级",
    ["全部", "🔴 高风险", "🟠 中风险", "🟢 低风险"]
)

process_filter = col2.selectbox(
    "处理状态",
    ["全部", "未处理", "已处理"]
)

filtered_data = data.copy()

if risk_filter != "全部":
    filtered_data = filtered_data[filtered_data["risk_level"] == risk_filter]

if process_filter == "未处理":
    filtered_data = filtered_data[filtered_data["manual_decision"] == ""]
elif process_filter == "已处理":
    filtered_data = filtered_data[filtered_data["manual_decision"] != ""]

filtered_data = filtered_data.sort_values(by="risk_score", ascending=False)

st.divider()

# =========================
# 批量操作区
# =========================

st.subheader("☑ 批量选择案件")

selected_cases = st.multiselect(
    "选择需要发起调查的案件",
    filtered_data["report_id"].tolist()
)

if st.button("批量发起调查"):
    if selected_cases:
        data.loc[data["report_id"].isin(selected_cases), "manual_decision"] = "调查"
        data.loc[data["report_id"].isin(selected_cases), "decision_time"] = datetime.now()
        data.loc[data["report_id"].isin(selected_cases), "feedback_label"] = 1

        data.to_csv("data_sample.csv", index=False)
        st.success(f"已对 {len(selected_cases)} 个案件发起调查")
    else:
        st.warning("请先选择案件")

st.divider()

# =========================
# 案件表展示
# =========================

display_columns = [
    "report_id",
    "risk_level",
    "risk_score",
    "manual_decision"
]

# 生成可点击链接
filtered_data["查看详情"] = filtered_data["report_id"]

st.dataframe(
    filtered_data[display_columns],
    use_container_width=True
)

st.info(f"当前展示案件数量：{len(filtered_data)}")

st.divider()

# =========================
# 导出 Excel
# =========================

st.subheader("⬇ 导出数据")

excel_data = filtered_data.to_excel("export.xlsx", index=False)

with open("data_sample.csv", "rb") as file:
    st.download_button(
        label="导出当前筛选结果为CSV",
        data=file,
        file_name="案件列表导出.csv",
        mime="text/csv"
    )