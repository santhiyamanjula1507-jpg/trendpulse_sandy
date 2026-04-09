import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = sns.load_dataset("tips")
# Matplotlib / Seaborn charts
st.subheader("Bill Distribution by Day")
fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(data=df, x="day", y="total_bill", ax=ax, palette="muted")
ax.set_xlabel("Day of Week")
ax.set_ylabel("Total Bill ($)")
plt.tight_layout()
st.pyplot(fig) # Pass the figure object directly
plt.close(fig)