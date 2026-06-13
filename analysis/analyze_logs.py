import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("logs/aura_logs.csv", sep=",")

print("\n===== BASIC INFO =====")
print(df.head())
print("\nLabel Counts:\n", df["label"].value_counts())

# -------------------------------
#  1. Label Distribution (Bar Chart)
# -------------------------------
plt.figure()
df["label"].value_counts().plot(kind="bar")
plt.title("Environment Distribution")
plt.xlabel("Label")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------------------------------
#  2. Environment Proportion (Pie Chart)
# -------------------------------
plt.figure()
df["label"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Environment Proportion")
plt.ylabel("")
plt.tight_layout()
plt.show()

# -------------------------------
#  3. VAD vs Environment (Stacked Bar)
# -------------------------------
vad_env = df.groupby(["label", "vad"]).size().unstack(fill_value=0)

vad_env.plot(kind="bar", stacked=True)
plt.title("VAD Activity per Environment")
plt.xlabel("Environment")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------------------------------
#  4. Smoothed Timeline (Over Time)
# -------------------------------
label_map = {
    "quiet": 0,
    "conversational": 1,
    "music": 2,
    "noisy": 3,
    "traffic": 4
}

df["label_num"] = df["label"].map(label_map)

# Rolling smoothing
df["smoothed"] = df["label_num"].rolling(window=5).mean()

plt.figure()
plt.plot(df["smoothed"])
plt.yticks(list(label_map.values()), list(label_map.keys()))
plt.title("Smoothed Environment Over Time")
plt.xlabel("Time Step")
plt.ylabel("Environment")
plt.tight_layout()
plt.show()

# -------------------------------
#  5. Confidence Distribution (Box Plot)
# -------------------------------
plt.figure()
df.boxplot(column="confidence", by="label")
plt.title("Confidence by Environment")
plt.suptitle("")  # removes default title
plt.xlabel("Label")
plt.ylabel("Confidence")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()