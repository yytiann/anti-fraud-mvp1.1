import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import random
import os

st.title("🕸 团伙关系图谱")

data = pd.read_csv("data_sample.csv")

report_id = st.text_input("请输入报案号")

if st.button("查询关系网络"):

    row = data[data["report_id"] == report_id]

    if row.empty:
        st.error("未找到案件")
    else:
        row = row.iloc[0]

        # 构造当前客户
        current_customer = f"客户_{row['report_id']}"
        current_hospital = f"医院_{random.randint(1,5)}"
        current_agent = f"代理人_{random.randint(1,3)}"

        # 创建图
        G = nx.Graph()

        # 添加当前节点
        G.add_node(current_customer, type="customer", risk=row["label"])
        G.add_node(current_hospital, type="hospital")
        G.add_node(current_agent, type="agent")

        G.add_edge(current_customer, current_hospital)
        G.add_edge(current_customer, current_agent)

        # 找同医院的其他客户（模拟）
        same_hospital_cases = data.sample(5)

        for _, r in same_hospital_cases.iterrows():
            other_customer = f"客户_{r['report_id']}"
            G.add_node(other_customer, type="customer", risk=r["label"])
            G.add_edge(other_customer, current_hospital)

        # 创建可视化网络
        net = Network(height="650px", width="100%", bgcolor="#111111", font_color="white")

        for node, attr in G.nodes(data=True):

            if attr.get("type") == "customer":
                if attr.get("risk") == 1:
                    color = "red"
                else:
                    color = "gray"
            elif attr.get("type") == "hospital":
                color = "blue"
            else:
                color = "green"

            size = 30 if node == current_customer else 15

            net.add_node(node, label=node, color=color, size=size)

        for edge in G.edges():
            net.add_edge(edge[0], edge[1])

        net.save_graph("graph.html")

        with open("graph.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        st.components.v1.html(html_content, height=700)

        st.info("红色节点 = 高风险客户，灰色 = 正常客户")