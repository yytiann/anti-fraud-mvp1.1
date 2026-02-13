import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import joblib

np.random.seed(42)

n = 10000

data = pd.DataFrame({
    "report_id": [f"R{i}" for i in range(n)],
    "days_policy_to_claim": np.random.exponential(scale=200, size=n).astype(int),
    "claim_amount": np.random.normal(20000, 10000, n).clip(1000, 100000),
    "sum_insured": np.random.choice([50000,100000,200000,500000], size=n),
    "claim_count_1y": np.random.poisson(1, n),
    "was_investigated": np.random.binomial(1, 0.1, n),
    "policy_count": np.random.randint(1,5,n)
})

risk_score = (
    (data["days_policy_to_claim"] <= 30) * 2 +
    (data["claim_count_1y"] >= 3) * 2 +
    (data["claim_amount"] > 50000) * 1 +
    (data["was_investigated"] == 1) * 2
)

prob = 1 / (1 + np.exp(-risk_score))
data["label"] = np.random.binomial(1, prob)

data.to_csv("data_sample.csv", index=False)

X = data.drop(columns=["report_id","label"])
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

model = XGBClassifier()
model.fit(X_train,y_train)
model.save_model("model.json")
#joblib.dump(model, "model.pkl")
joblib.dump(X.columns.tolist(), "feature_columns.pkl")

print("模型训练完成")