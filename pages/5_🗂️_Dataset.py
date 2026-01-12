import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dataset", page_icon="🗂️", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('dataset.csv')
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df[(df['created_at'] >= '2025-09-01') & (df['created_at'] <= '2025-11-30')]
    return df

df = load_data()

st.sidebar.info(f"**Periode:** Sep - Nov 2025\n**Total Data:** {len(df):,} tweets")

st.title("🗂️ Eksplorasi Data Mentah")
st.caption("Akses dan filter data hasil pemrosesan")
st.markdown("---")

st.markdown("### 🔍 Filter Data")

col1, col2 = st.columns(2)
with col1:
    search_term = st.text_input("🔎 Cari kata kunci dalam tweet:", placeholder="Contoh: malware, attack, security")
with col2:
    min_engagement = st.slider("📊 Minimum total engagement (likes + retweets):", 0, 100, 0)

# Apply filters
filtered_df = df.copy()
if search_term:
    filtered_df = filtered_df[filtered_df['full_text'].str.contains(search_term, case=False, na=False)]

filtered_df['total_engagement'] = filtered_df['favorite_count'] + filtered_df['retweet_count']
filtered_df = filtered_df[filtered_df['total_engagement'] >= min_engagement]

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Tweet Ditampilkan", f"{len(filtered_df):,}")
with col2:
    st.metric("❤️ Total Likes", f"{filtered_df['favorite_count'].sum():,}")
with col3:
    st.metric("🔄 Total Retweets", f"{filtered_df['retweet_count'].sum():,}")
with col4:
    st.metric("💬 Avg Engagement", f"{filtered_df['total_engagement'].mean():.1f}")

st.markdown("---")

# Data table
st.markdown("### 📋 Tabel Data")
display_cols = ['created_at', 'username', 'full_text', 'favorite_count', 'retweet_count', 'total_engagement']

st.dataframe(
    filtered_df[display_cols].sort_values('total_engagement', ascending=False),
    width='stretch',
    height=650,
    column_config={
        "created_at": st.column_config.DateColumn("Tanggal", format="DD/MM/YYYY"),
        "username": "Username",
        "full_text": st.column_config.TextColumn("Tweet", width="large"),
        "favorite_count": st.column_config.NumberColumn("Likes", format="%d"),
        "retweet_count": st.column_config.NumberColumn("Retweets", format="%d"),
        "total_engagement": st.column_config.NumberColumn("Total Engagement", format="%d")
    }
)

# Download
st.markdown("### 📥 Unduh Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Data (CSV)",
    data=csv,
    file_name=f"npm-tweet-dataset-filtered_{len(filtered_df)}.csv",
    mime="text/csv",
    help="Unduh data yang telah difilter dalam format CSV"
)
st.download_button(
    label="📥 Download Raw Dataset (CSV)",
    data=csv,
    file_name=f"npm-tweet-dataset.csv",
    mime="text/csv",
    help="Unduh data mentah dalam format CSV"
)
