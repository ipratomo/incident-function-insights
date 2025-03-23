
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
from collections import Counter
import re

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("pareto_keywords.csv")
    by_function = pd.read_json("function_keywords.json")
    incidents = pd.read_csv("incident_chronology_sample.csv")
    return df, by_function, incidents

pareto_df, function_keywords, incident_examples = load_data()

st.title("🛡️ Incident Insights by Function")

st.header("🔧 Overall Pareto Problems from Incident Chronology")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=pareto_df, x="keyword", y="count", ax=ax, palette="Blues_d")
ax.set_title("Top 15 Keywords in Incident Chronology")
ax.set_ylabel("Frequency")
ax.set_xlabel("Keyword")
st.pyplot(fig)

st.divider()
st.header("📊 Word Cloud by Function")

selected_function = st.selectbox("Choose a function", list(function_keywords.keys()))
keywords = function_keywords[selected_function]

# Generate word cloud
word_freq = {item['keyword']: item['count'] for item in keywords}
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
ax_wc.imshow(wordcloud, interpolation='bilinear')
ax_wc.axis("off")
st.pyplot(fig_wc)

st.divider()
st.header("📝 Sample Incident Chronology per Function")
func_filter = st.selectbox("Select function to view incidents", incident_examples['function'].unique())
keyword_filter = st.text_input("Optional: Filter by keyword (e.g., 'unit', 'jalan')").lower()

filtered = incident_examples[incident_examples['function'] == func_filter]
if keyword_filter:
    filtered = filtered[filtered['kronologis'].str.contains(keyword_filter, case=False)]

st.dataframe(filtered[['inc_id', 'function', 'job_title', 'nama', 'kronologis']].reset_index(drop=True), use_container_width=True)
