import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sentimen", page_icon="📈", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('dataset.csv')
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df[(df['created_at'] >= '2025-09-01') & (df['created_at'] <= '2025-11-30')]
    return df

@st.cache_data
def classify_sentiment(text):
    if pd.isna(text):
        return 'Netral'
    text = str(text).lower()
    negative_words = ['attack', 'malicious', 'hack', 'breach', 'vulnerable', 'threat', 'risk', 'danger', 'compromised', 'exploit', 'malware', 'worm']
    positive_words = ['safe', 'secure', 'protect', 'fix', 'patch', 'solution', 'resolved', 'update', 'defend']
    neg_count = sum(1 for word in negative_words if word in text)
    pos_count = sum(1 for word in positive_words if word in text)
    if neg_count > pos_count:
        return 'Negatif'
    elif pos_count > neg_count:
        return 'Positif'
    return 'Netral'

df = load_data()
df['sentiment'] = df['full_text'].apply(classify_sentiment)
sentiment_counts = df['sentiment'].value_counts()

st.sidebar.info(f"**Periode:** Sep - Nov 2025\n**Total Data:** {len(df):,} tweets")

st.title("📈 Sentimen")
st.caption("Analisis polaritas sentimen publik menggunakan Lexicon-based Classification")
st.markdown("---")

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("😊 Positif", f"{sentiment_counts.get('Positif', 0):,}", 
              f"{sentiment_counts.get('Positif', 0)/len(df)*100:.1f}%")
with col2:
    st.metric("😐 Netral", f"{sentiment_counts.get('Netral', 0):,}", 
              f"{sentiment_counts.get('Netral', 0)/len(df)*100:.1f}%")
with col3:
    st.metric("😟 Negatif", f"{sentiment_counts.get('Negatif', 0):,}", 
              f"{sentiment_counts.get('Negatif', 0)/len(df)*100:.1f}%")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🥧 Distribusi Proporsi Sentimen")
    st.markdown("**🎯 Tujuan:** Visualisasi proporsi sentimen secara keseluruhan")
    st.markdown("**🔬 Metode:** Pie chart dengan color mapping kategorikal")
    
    fig = px.pie(values=sentiment_counts.values, names=sentiment_counts.index,
                 color_discrete_map={'Positif': '#2ecc71', 'Netral': '#95a5a6', 'Negatif': '#e74c3c'},
                 hole=0.4, title='Proporsi Sentimen')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, width='stretch')
    
    st.markdown(f"""
    **📊 Hasil:**
    - Sentimen dominan: **{sentiment_counts.idxmax()}** ({sentiment_counts.max()/len(df)*100:.1f}%)
    - Total terklasifikasi: **{len(df):,} tweet**
    
    **💡 Insight:**
    Dominasi sentimen netral menunjukkan bahwa mayoritas diskusi bersifat **informatif dan objektif**, 
    bukan emosional. Komunitas developer cenderung fokus pada **fakta dan solusi** daripada panic atau blame.
    
    **🎯 Implikasi:**
    Respons yang tenang dan rasional ini menunjukkan **kematangan ekosistem open-source** dalam menghadapi krisis keamanan.
    """)

with col2:
    st.markdown("### 📊 Jumlah Absolut per Sentimen")
    st.markdown("**🎯 Tujuan:** Menampilkan jumlah tweet per kategori sentimen")
    st.markdown("**🔬 Metode:** Bar chart vertikal dengan color mapping")
    
    fig = px.bar(x=sentiment_counts.index, y=sentiment_counts.values,
                 labels={'x': 'Sentimen', 'y': 'Jumlah Tweet'},
                 color=sentiment_counts.index,
                 color_discrete_map={'Positif': '#2ecc71', 'Netral': '#95a5a6', 'Negatif': '#e74c3c'},
                 title='Distribusi Jumlah Tweet')
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown(f"""
    **📊 Hasil:**
    - Positif: **{sentiment_counts.get('Positif', 0):,}** tweet ({sentiment_counts.get('Positif', 0)/len(df)*100:.1f}%)
    - Netral: **{sentiment_counts.get('Netral', 0):,}** tweet ({sentiment_counts.get('Netral', 0)/len(df)*100:.1f}%)
    - Negatif: **{sentiment_counts.get('Negatif', 0):,}** tweet ({sentiment_counts.get('Negatif', 0)/len(df)*100:.1f}%)
    
    **💡 Insight:**
    Meskipun terjadi serangan keamanan, sentimen negatif relatif rendah. Ini menunjukkan bahwa komunitas 
    **tidak panik berlebihan** dan lebih fokus pada **mitigasi dan pembelajaran** dari insiden ini.
    """)

st.markdown("---")

# Chart 3 & 4: Sunburst and Treemap
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌅 Sunburst Chart Sentimen")
    st.markdown("**🎯 Tujuan:** Visualisasi hierarki proporsi sentimen")
    st.markdown("**🔬 Metode:** Sunburst chart dengan struktur hierarkis")
    
    sentiment_df = pd.DataFrame({
        'Sentimen': sentiment_counts.index,
        'Jumlah': sentiment_counts.values,
        'Kategori': ['Sentimen'] * len(sentiment_counts)
    })
    
    fig = px.sunburst(sentiment_df, path=['Kategori', 'Sentimen'], values='Jumlah',
                     color='Sentimen',
                     color_discrete_map={'Positif': '#2ecc71', 'Netral': '#95a5a6', 'Negatif': '#e74c3c'},
                     title='Hierarki Sentimen')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("**📊 Hasil:** Visualisasi hierarkis menunjukkan struktur distribusi sentimen secara interaktif.")

with col2:
    st.markdown("### 🗺️ Treemap Sentimen")
    st.markdown("**🎯 Tujuan:** Perbandingan proporsi dengan area persegi")
    st.markdown("**🔬 Metode:** Treemap dengan color mapping sentimen")
    
    fig = px.treemap(sentiment_df, path=['Kategori', 'Sentimen'], values='Jumlah',
                    color='Sentimen',
                    color_discrete_map={'Positif': '#2ecc71', 'Netral': '#95a5a6', 'Negatif': '#e74c3c'},
                    title='Treemap Distribusi Sentimen')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("**📊 Hasil:** Area persegi merepresentasikan proporsi relatif setiap kategori sentimen.")

st.markdown("---")

# Chart 5: Sentiment over Time
st.markdown("### 📅 Tren Sentimen Harian")
st.markdown("**🎯 Tujuan:** Melihat evolusi sentimen dari waktu ke waktu")
st.markdown("**🔬 Metode:** Stacked area chart sentimen per hari")

df_sentiment_daily = df.groupby([df['created_at'].dt.date, 'sentiment']).size().reset_index(name='count')
df_sentiment_daily.columns = ['date', 'sentiment', 'count']

fig = px.area(df_sentiment_daily, x='date', y='count', color='sentiment',
              labels={'date': 'Tanggal', 'count': 'Jumlah', 'sentiment': 'Sentimen'},
              color_discrete_map={'Positif': '#2ecc71', 'Netral': '#95a5a6', 'Negatif': '#e74c3c'},
              title='Evolusi Sentimen Harian')
fig.update_layout(height=600)
st.plotly_chart(fig, width='stretch')

st.markdown("""
**📊 Hasil:**
Stacked area chart menunjukkan **dinamika sentimen** sepanjang periode. Dominasi warna abu-abu (netral) 
konsisten mengindikasikan **stabilitas diskusi objektif** tanpa fluktuasi emosional ekstrem.

**💡 Kesimpulan:**
Tidak ada lonjakan sentimen negatif yang signifikan, menunjukkan komunitas **responsif namun tenang** 
dalam menghadapi krisis keamanan.
""")
