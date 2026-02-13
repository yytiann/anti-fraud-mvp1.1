import streamlit as st
import pandas as pd
import joblib
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import numpy as np
import time

st.title("📈 模型管理中心（中台版）")

st.markdown("""
模型管理中心用于展示模型版本、性能指标、特征重要性及版本切换能力。  
当前为演示级中台版本。
""")

# =========================
# 1️⃣ 模型版本区
# =========================

st.subheader("🧠 模型版本信息")

available_versions = ["v1.0-生产版", "v1.1-优化版", "v2.0-实验版"]
selected_version = st.selectbox("选择模型版本", available_versions)

# 模拟指标（演示用）
training_samples = 10000
auc_score = round(np.random.uniform(0.82, 0.90), 3)
ks_score = round(np.random.uniform(0.40, 0.60), 3)

col1, col2, col3 = st.columns(3)
col1.metric("当前版本", selected_version)
col2.metric("AUC", auc_score)
col3.metric("KS", ks_score)

# =========================
# 2️⃣ 特征重要性展示
# =========================

st.subheader("📊 特征重要性")

try:
    model = XGBClassifier()
    model.load_model("model.json")
    feature_columns = joblib.load("feature_columns.pkl")

    importances = model.feature_importances_

    importance_df = pd.DataFrame({
        "feature": feature_columns,
        "importance": importances
    }).sort_values(by="importance", ascending=False)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(importance_df["feature"], importance_df["importance"])
    ax.invert_yaxis()
    ax.set_xlabel("Importance Score")
    ax.set_title("Feature Importance")

    st.pyplot(fig)

except Exception as e:
    st.warning("未检测到模型文件，请确认 model.json 和 feature_columns.pkl 存在。")
    st.text(str(e))

# =========================
# 3️⃣ 模型重训练模拟
# =========================

st.subheader("🔄 模型重训练")

if st.button("启动模型重训练（模拟）"):
    with st.spinner("模型训练中..."):
        time.sleep(2)
    st.success("模型训练完成，已生成新版本 v2.1（模拟）")

# =========================
# 4️⃣ 模型说明
# =========================

st.subheader("📌 模型说明")

st.markdown("""
- 模型类型：XGBoost 二分类模型  
- 输入特征：时间类、金额类、频率类、行为类特征  
- 输出结果：风险评分（0~1）  
- 决策逻辑：规则优先 + 模型评分融合  
- 支持版本管理  
- 支持A/B测试  
- 支持灰度发布与回滚机制  
""")