
"""
Modern Animals
 └── Species

Dinosaurs
 └── Species
"""
import numpy as np
import pandas as pd
import plotly.express as px

data = [
    ["modern animal", "Primates",     "Homo sapiens",                              1420, 83],
    ["modern animal", "Cetacea",      "Porpoise (Phocaena phocaena)",              1735, 142.43],
    ["modern animal", "Primates",     "Chimpanzee (Troglodytes niger)",            440,  56.69],
    ["modern animal", "Marsupials",   "Baboon (Papio cynocephalus)",               175,  19.51],  # 如要严格生物学，可改成 Primates
    ["modern animal", "Aves",         "Crow (Corvus brachyrhynchos)",              9.3,  0.337],
    ["modern animal", "Proboscidea",  "Elephant (Loxodonta africana knochenhaueri)",5712, 6654],
    ["modern animal", "Cetacea",      "Whale, Blue (Balaenoptera musculus)",       6800, 58059],
    ["modern animal", "Marsupials",   "Opossum (Didelphus marsupialis etensis)",   4.8,  1.147],
    ["modern animal", "Fish",         "Goldfish (Carassius auratus)",              0.10, 0.00952],
    ["modern animal", "Aves",         "Ostrich, Masai (Struthio camelus massaicus)",42.11,123],
    ["modern animal", "Fish",         "Tuna (Thunus secundodorsalis)",             3.09, 5.21],
    ["modern animal", "Reptiles",     "Alligator (Alligator mississippiensis)",    14.08,205],
    ["Dinosaurs",     "Carnosaur",    "Allosaurus",                                167.5,2300],
    ["Dinosaurs",     "Ornithopod",   "Anatosaurus",                               150,  3400],
    ["Dinosaurs",     "Sauropod",     "Brachiosaurus",                             154.5,87000],
    ["Dinosaurs",     "Ornithopod",   "Camptosaurus",                              23,   400],
]

df = pd.DataFrame(data, columns=["Class", "Group", "Species", "Brain mass (g)", "Body wt (kg)"])

def treemap1():
    # 用脑重当面积，用体重当颜色
    fig = px.treemap(
        df,
        path=["Class", "Species"],          # 层级：先按现代/恐龙，再到具体物种
        values="Brain mass (g)",            # 矩形面积 = 体重
        color="Body wt (kg)",               # 颜色 = 脑重量
        color_continuous_scale="RdYlGn",    # 绿-黄-红配色
        title="Brain and Body Weight: Modern Animals vs Dinosaurs"
    )
    fig.update_layout(margin=dict(t=60, l=10, r=10, b=10))
    fig.show()

    # fig = px.treemap(
    #     df,
    #     path=["Class", "Species"],
    #     values="Log Body Weight",      # ✅ 用对数面积
    #     color="Brain mass (g)",
    #     color_continuous_scale="RdYlGn",
    #     title="Brain and Body Weight (Log-Scaled Area): Modern Animals vs Dinosaurs"
    # )
    # fig.update_layout(margin=dict(t=60, l=10, r=10, b=10))
    # fig.show()

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
def plot():
    # =========================
    # 2. 对数变换（防止数量级过大）
    # =========================
    X = np.column_stack([
        np.log10(df["Brain mass (g)"] + 1),
        np.log10(df["Body wt (kg)"] + 1)
    ])

    # =========================
    # 3. K-Means 聚类（k = 2）
    # =========================
    kmeans = KMeans(n_clusters=2, n_init=10, random_state=42)
    df["Cluster"] = kmeans.fit_predict(X)

    # =========================
    # 4. 画聚类散点图（不指定颜色）
    # =========================
    plt.figure()

    markers = ["o", "s"]  # 用不同形状表示不同簇

    for i, cluster_id in enumerate(sorted(df["Cluster"].unique())):
        subset = df[df["Cluster"] == cluster_id]

        plt.scatter(
            np.log10(subset["Brain mass (g)"] + 1),
            np.log10(subset["Body wt (kg)"] + 1),
            marker=markers[i]
        )

        # 标注物种名称
        for _, row in subset.iterrows():
            plt.text(
                np.log10(row["Brain mass (g)"] + 1),
                np.log10(row["Body wt (kg)"] + 1),
                row["Species"],
                fontsize=8
            )

    plt.xlabel("Log Brain Mass (g)")
    plt.ylabel("Log Body Weight (kg)")
    plt.title("K-Means Clustering of Species Based on Brain and Body Weight")
    plt.grid(True)
    plt.show()
# plot()


def test_treemap_log_log():
    # 1. 手动输入你的数据（以 kg 为主，g 后面用公式算）
    data = [
        # Group,        Species,                                      Brain_mass_g, Body_wt_kg
        ("Primates",     "Homo sapiens",                              1420,         83),
        ("Cetacea",      "Porpoise (Phocaena phocaena)",              1735,         142.43),
        ("Primates",     "Chimpanzee (Troglodytes niger)",            440,          56.69),
        ("Marsupials",   "Baboon (Papio cynocephalus)",               175,          19.51),
        ("Aves",         "Crow (Corvus brachyrhynchos)",              9.3,          0.337),
        ("Proboscidea",  "Elephant (Loxodonta africana knochenhaueri)",5712,        6654),
        ("Cetacea",      "Whale, Blue (Balaenoptera musculus)",       6800,         58059),
        ("Marsupials",   "Opossum (Didelphus marsupialis etensis)",   4.8,          1.147),
        ("Fish",         "Goldfish (Carassius auratus)",              0.10,         0.00952),
        ("Aves",         "Ostrich, Masai (Struthio camelus massaicus)",42.11,       123),
        ("Fish",         "Tuna (Thunus secundodorsalis)",             3.09,         5.21),
        ("Reptiles",     "Alligator (Alligator mississippiensis)",    14.08,        205),

        # Dinosaurs（注意 Group 这里用统一的大类 "Dinosaurs"，Subtype 可以另外加一列）
        ("Dinosaurs",    "Allosaurus (Carnosaur)",                    167.5,        2300),
        ("Dinosaurs",    "Anatosaurus (Ornithopod)",                  150,          3400),
        ("Dinosaurs",    "Brachiosaurus (Sauropod)",                  154.5,        87000),
        ("Dinosaurs",    "Camptosaurus (Ornithopod)",                 23,           400),
        ("Dinosaurs",    "Diplodocus (Sauropod)",                     50,           11700),
    ]

    df = pd.DataFrame(data, columns=["Group", "Species", "Brain_mass_g", "Body_wt_kg"])

    # 派生列：把体重变成 g，顺便算一下脑体比
    df["Body_mass_g"] = df["Body_wt_kg"] * 1000
    df["Brain_body_ratio"] = df["Brain_mass_g"] / df["Body_mass_g"]

    print(df)

    # =======================
    # 图 1：Treemap（Group -> Species，按脑重量面积）
    # =======================
    fig_treemap = px.treemap(
        df,
        path=["Group", "Species"],      # 层级路径
        values="Brain_mass_g",          # 决定面积
        color="Group",                  # 颜色按 Group 区分
        title="Treemap of Brain Mass by Group and Species"
    )
    fig_treemap.show()

    # =======================
    # 图 2：对数散点图 Body mass vs Brain mass
    # =======================
    key_species = [
        "Homo sapiens",
        "Whale, Blue (Balaenoptera musculus)",
        "Elephant (Loxodonta africana knochenhaueri)",
        "Brachiosaurus (Sauropod)"
    ]

    df["Label"] = df["Species"].where(df["Species"].isin(key_species), "")

    fig_scatter = px.scatter(
        df,
        x="Body_mass_g",
        y="Brain_mass_g",
        color="Group",
        hover_name="Species",

        text="Species",              # ✅ 关键：显示物种名
        size="Brain_mass_g",
        size_max=35,          # ✅ 限制最大气泡大小（关键！）

        log_x=True,
        log_y=True,
        title="Brain Mass vs Body Mass (log-log scale)"
    )
    # ✅ 控制文字位置（避免压在点正中间）
    fig_scatter.update_traces(
        textposition="top center",
        textfont=dict(size=10)   # ✅ 这里控制物种名的字号
    )
    fig_scatter.update_xaxes(range=[0, 9])
    fig_scatter.update_yaxes(range=[-1, 4])
    fig_scatter.update_traces(marker=dict(line=dict(width=0.5)))
    fig_scatter.show()


def plot2_with_regression():
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression

    # =========================
    # 1. 对数变换
    # =========================
    df["log_brain"] = np.log10(df["Brain mass (g)"] + 1)
    df["log_body"] = np.log10(df["Body wt (kg)"] + 1)

    # =========================
    # 2. 分组
    # =========================
    modern = df[df["Class"] == "modern animal"]
    dino = df[df["Class"] == "Dinosaurs"]

    # =========================
    # 3. 拟合回归模型
    # =========================
    model_modern = LinearRegression()
    model_dino = LinearRegression()

    X_modern = modern["log_brain"].values.reshape(-1, 1)
    y_modern = modern["log_body"].values
    X_dino = dino["log_brain"].values.reshape(-1, 1)
    y_dino = dino["log_body"].values

    model_modern.fit(X_modern, y_modern)
    model_dino.fit(X_dino, y_dino)

    # 回归线范围
    x_line = np.linspace(df["log_brain"].min(), df["log_brain"].max(), 100).reshape(-1, 1)

    y_modern_pred = model_modern.predict(x_line)
    y_dino_pred = model_dino.predict(x_line)

    # =========================
    # 4. 作图
    # =========================
    plt.figure(figsize=(10, 7))

    plt.scatter(modern["log_brain"], modern["log_body"], label="Modern Animals")
    plt.scatter(dino["log_brain"], dino["log_body"], label="Dinosaurs", marker="s")

    # ✅ 回归线
    plt.plot(x_line, y_modern_pred, linestyle="--", label=f"Modern Regression (slope={model_modern.coef_[0]:.2f})")
    plt.plot(x_line, y_dino_pred, linestyle="--", label=f"Dinosaur Regression (slope={model_dino.coef_[0]:.2f})")

    # ✅ 标注物种名
    for _, row in df.iterrows():
        plt.text(row["log_brain"], row["log_body"], row["Species"], fontsize=8)

    plt.xlabel("Log Brain Mass (g)")
    plt.ylabel("Log Body Weight (kg)")
    plt.title("Modern Animals vs Dinosaurs: Log-Log Regression of Brain and Body Size")
    plt.legend()
    plt.grid(True)
    plt.show()

# plot2_with_regression()

def dataset2_plot():
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go

    # =========================
    # 1. 构建数据
    # =========================
    data = [
        # Order/Suborder, Genus, Investment_22, Projected_23  （单位：百万美元）
        ("Carnosaur", "Allosaurus", 5, 1),
        ("Ornithopod", "Anatosaurus", 3, 2),
        ("Sauropod", "Brachiosaurus", 4, 3),
        ("Ornithopod", "Camptosaurus", 6, 4),
        ("Sauropod", "Diplodocus", 5, 2),
        ("Ornithopod", "Iguanodon", 3, 1),
        ("Ceratopsian", "Protoceratops", 4, 2),
        ("Stegosaur", "Stegosaurus", 4, 1),
        ("Ceratopsian", "Triceratops", 6, 4),
        ("Theropod", "Tyrannosaurus", 9, 5),
    ]

    df = pd.DataFrame(
        data,
        columns=["Order", "Genus", "Investment_22", "Projected_23"]
    )

    print(df)

    # =========================
    # 2. Treemap：2022 投资结构
    # =========================
    fig_treemap = px.treemap(
        df,
        path=["Order", "Genus"],  # 层级：Order → Genus
        values="Investment_22",  # 面积 = 2022 投资额
        color="Order",  # 颜色按 Order 区分
        title="Biosyn Dinosaur Portfolio: 2022 Investment Treemap"
    )
    fig_treemap.show()

    # =========================
    # 3. Benchmark 图：2022 基准 vs 2023 预算
    #    做法：柱子 = 2023；折线 = 2022 基准线
    # =========================
    fig_benchmark = go.Figure()

    # 2023 预算作为柱子
    fig_benchmark.add_trace(
        go.Bar(
            x=df["Genus"],
            y=df["Projected_23"],
            name="Projected Investment 2023 ($M)"
        )
    )

    # 2022 投资作为基准线
    fig_benchmark.add_trace(
        go.Scatter(
            x=df["Genus"],
            y=df["Investment_22"],
            mode="lines+markers",
            name="Investment 2022 Benchmark ($M)"
        )
    )

    fig_benchmark.update_layout(
        title="Biosyn Dinosaur Investment: 2023 vs 2022 Benchmark",
        xaxis_title="Dinosaur Genus",
        yaxis_title="Investment ($M)",
        barmode="group"
    )

    fig_benchmark.show()

    # =========================
    # 4. Sankey Diagram：2022 → Genus → 2023
    #    Stage1:  2022 Total
    #    Stage2:  每个 Genus
    #    Stage3:  2023 Total
    #    这样可以看到：
    #      - 从 2022 总池子流向各恐龙的粗细
    #      - 再从各恐龙流回 2023 总池子的粗细（对比削减）
    # =========================

    # 定义节点标签
    genus_list = df["Genus"].tolist()
    nodes = ["2022 Total Investment"] + genus_list + ["2023 Total Investment"]

    # 节点索引映射
    node_index = {name: i for i, name in enumerate(nodes)}

    sources = []
    targets = []
    values = []

    # 2022 总池子 -> 各 Genus （用 2022 投资）
    for _, row in df.iterrows():
        sources.append(node_index["2022 Total Investment"])
        targets.append(node_index[row["Genus"]])
        values.append(row["Investment_22"])

    # 各 Genus -> 2023 总池子（用 2023 预计）
    for _, row in df.iterrows():
        sources.append(node_index[row["Genus"]])
        targets.append(node_index["2023 Total Investment"])
        values.append(row["Projected_23"])

    fig_sankey = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(width=0.5),
                    label=nodes
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values
                )
            )
        ]
    )

    fig_sankey.update_layout(
        title_text="Biosyn Dinosaur Investment Flow: 2022 to 2023",
        font=dict(size=12)
    )

    fig_sankey.show()
dataset2_plot()