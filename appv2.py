import streamlit as st

st.set_page_config(
    page_title="保险反欺诈决策平台",
    page_icon="🛡",
    layout="wide"
)

st.title("🛡 保险反欺诈决策平台")

st.markdown("""
本系统为报案后风险识别模块 MVP，  
采用规则 + 模型融合架构， 
贯穿“销售—承保—理赔—调查”核心业务场景。 
支持可解释决策输出。
""")


st.markdown("""
1.降低赔付率
2.提升理赔效率
3.降低人工成本
4.提高模型可解释性
5.形成可复用风险资产
""")

st.info("请从左侧菜单进入功能页面。")