import streamlit as st
import pandas as pd
import joblib
from xgboost import XGBClassifier
from rules import strong_rules
import numpy as np
from datetime import datetime

# 加载数据
data = pd.read_csv("data_sample.csv")
# 如果列不存在则初始化
if "manual_decision" not in data.columns:
    data["manual_decision"] = ""

if "decision_time" not in data.columns:
    data["decision_time"] = ""

if "feedback_label" not in data.columns:
    data["feedback_label"] = ""

# 模拟客户姓名和险种字段（演示）
names = ["张三", "李四", "王五", "赵六", "陈七"]
insurance_types = ["重疾险", "医疗险", "意外险", "寿险"]

data["客户姓名"] = np.random.choice(names, size=len(data))
data["险种"] = np.random.choice(insurance_types, size=len(data))
data["报案时间"] = pd.to_datetime("2024-01-01") + pd.to_timedelta(
    np.random.randint(0, 60, len(data)), unit="D"
)

# 加载模型
model = XGBClassifier()
model.load_model("model.json")
feature_columns = joblib.load("feature_columns.pkl")

st.title("📋 案件管理")

# 如果来自跳转
if "selected_report_id" in st.session_state:
    report_id = st.session_state["selected_report_id"]
else:
    report_id = ""

report_id = st.text_input("请输入报案号", value=report_id)

if st.button("查询案件"):

    row = data[data["report_id"] == report_id]

    if row.empty:
        st.error("未找到案件")
    else:
        row = row.iloc[0]

        # 模型评分
        score = model.predict_proba(
            row[feature_columns].values.reshape(1, -1)
        )[0][1]

        # 风险等级
        if score > 0.8:
            risk_level = "高风险"
            risk_color = "🔴"
        elif score > 0.5:
            risk_level = "中风险"
            risk_color = "🟠"
        else:
            risk_level = "低风险"
            risk_color = "🟢"

        # 规则命中
        rule_hits = strong_rules(row)

        # 决策建议
        if rule_hits:
            decision = "建议提调（规则触发）"
        elif score > 0.7:
            decision = "建议提调（模型高风险）"
        else:
            decision = "无需提调"

        st.divider()

        # =========================
        # 案件基础信息
        # =========================

        st.markdown(f"""
        **报案号：** {row['report_id']}  
        **客户姓名：** {row['客户姓名']}  
        **险种：** {row['险种']}  
        **报案时间：** {row['报案时间'].date()}  
        """)

        st.divider()

        # =========================
        # 风险评分
        # =========================

        st.markdown(f"""
        {risk_color} **风险等级：{risk_level}（{round(score,3)}）**
        """)

        st.markdown(f"**系统建议：{decision}**")

        st.divider()

        # =========================
        # 风险原因
        # =========================

        st.subheader("📌 风险原因")

        if rule_hits:
            for i, reason in enumerate(rule_hits, 1):
                st.write(f"{i}. {reason}")
        else:
            st.write("未触发强规则，主要依据模型评分。")

        st.divider()

        # =========================
        # 风险分构成（模拟）
        # =========================

        st.subheader("📊 风险分构成")

        with st.expander("点击展开风险分构成"):

            time_risk = round(score * np.random.uniform(0.3, 0.4), 2)
            behavior_risk = round(score * np.random.uniform(0.2, 0.3), 2)
            money_risk = round(score * np.random.uniform(0.2, 0.3), 2)

            st.write(f"- 时间风险：{time_risk}")
            st.write(f"- 行为风险：{behavior_risk}")
            st.write(f"- 金额风险：{money_risk}")

        st.divider()

        # =========================
        # 操作按钮
        # =========================

        col1, col2, col3 = st.columns(3)

        # =========================
        # 操作按钮（带闭环写入）
        # =========================

        col1, col2, col3 = st.columns(3)

        if col1.button("发起调查"):
            data.loc[data["report_id"] == report_id, "manual_decision"] = "调查"
            data.loc[data["report_id"] == report_id, "decision_time"] = datetime.now()
            data.loc[data["report_id"] == report_id, "feedback_label"] = 1

            data.to_csv("data_sample.csv", index=False)
            st.success("已提交调查申请，并写入反馈数据")

        if col2.button("人工通过"):
            data.loc[data["report_id"] == report_id, "manual_decision"] = "通过"
            data.loc[data["report_id"] == report_id, "decision_time"] = datetime.now()
            data.loc[data["report_id"] == report_id, "feedback_label"] = 0

            data.to_csv("data_sample.csv", index=False)
            st.success("案件已人工通过，并写入反馈数据")

        if col3.button("标记误判"):
            data.loc[data["report_id"] == report_id, "manual_decision"] = "误判"
            data.loc[data["report_id"] == report_id, "decision_time"] = datetime.now()
            data.loc[data["report_id"] == report_id, "feedback_label"] = 0

            data.to_csv("data_sample.csv", index=False)
            st.warning("已标记为误判样本，数据已更新")