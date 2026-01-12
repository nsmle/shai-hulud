import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="Analisis NPM Supply Chain Attack",
    layout="wide",
    page_icon="🔒",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('dataset.csv')
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df[(df['created_at'] >= '2025-09-01') & (df['created_at'] <= '2025-11-30')]
    return df

df = load_data()

# Sidebar
st.sidebar.info(f"**Periode:** Sep - Nov 2025\n**Total Data:** {len(df):,} tweets")


# Main Page
st.title("Analisis Dinamika Sentimen dan Respons Publik")
st.subheader("Serangan Supply Chain pada Node Package Manager (NPM)")
st.caption("Periode: September - November 2025")

st.markdown("---")

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Total Tweet", f"{len(df):,}")
with col2:
    st.metric("📅 Rentang Waktu", f"{(df['created_at'].max() - df['created_at'].min()).days} hari")
with col3:
    st.metric("❤️ Total Likes", f"{df['favorite_count'].sum():,}")
with col4:
    st.metric("🔄 Total Retweets", f"{df['retweet_count'].sum():,}")

st.markdown("---")

# Sumber Dataset
st.markdown("### 📊 Sumber Dataset")
st.markdown(f"""
Dataset yang digunakan adalah hasil **crawling Twitter** menggunakan library `tweet-harvest` 
dengan kata kunci: **NPM Supply Chain Attack**, **Shai-Hulud**, **Worm Malware**, dan **Malicious Package NPM**.

**Data yang diambil berupa:**
1. **Username** - Identitas pengguna Twitter
2. **Created At** - Waktu tweet dibuat
3. **Full Text** - Isi lengkap tweet
4. **Favorite Count** - Jumlah likes
5. **Retweet Count** - Jumlah retweets

Data yang diolah sebanyak **{len(df):,}** baris data dari periode **September - November 2025**.
""")

st.markdown("---")

# Tentang Penelitian
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Tentang Penelitian")
    st.markdown("""
    Dashboard ini menyajikan hasil **pemrosesan dan visualisasi data** Twitter terkait serangan 
    *supply chain* pada ekosistem Node Package Manager (NPM) periode September-November 2025.
    
    **Tujuan Penelitian:**
    - Menganalisis sentimen publik terhadap insiden keamanan NPM
    - Mengidentifikasi topik dominan dalam diskusi
    - Memetakan pola temporal respons publik
    - Menyajikan visualisasi informatif untuk interpretasi data
    """)

with col2:
    st.markdown("### 🔬 Metodologi")
    st.markdown("""
    **Pemrosesan Data:**
    - Data Cleaning
    - Preprocessing
    - Feature Selection
    
    **Analisis:**
    - Lexicon-based Sentiment
    - Temporal Analysis
    - Keyword Extraction
    
    **Visualisasi:**
    - Time Series Charts
    - Distribution Charts
    - Word Frequency
    """)
