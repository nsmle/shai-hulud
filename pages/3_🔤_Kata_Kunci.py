import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re
from itertools import combinations

st.set_page_config(page_title="Kata Kunci", page_icon="🔤", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('dataset.csv')
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df[(df['created_at'] >= '2025-09-01') & (df['created_at'] <= '2025-11-30')]
    return df

@st.cache_data
def extract_keywords(texts, top_n=15):
    stopwords = {'the', 'and', 'for', 'are', 'with', 'this', 'that', 'from', 'was', 'has', 'have', 
                 'been', 'not', 'but', 'can', 'will', 'all', 'more', 'https', 'com', 'via', 'new', 'get', 'one', 'now', 'use'}
    words = []
    for text in texts:
        if pd.notna(text):
            text = str(text).lower()
            text = re.sub(r'http\S+|www\S+|@\S+|#\S+', '', text)
            tokens = re.findall(r'\b[a-z]{3,}\b', text)
            words.extend([w for w in tokens if w not in stopwords])
    return Counter(words).most_common(top_n)

@st.cache_data
def categorize_keywords(keywords_list):
    categories = {
        'Security': ['security', 'malicious', 'attack', 'vulnerability', 'threat', 'breach', 'exploit', 'malware', 'worm'],
        'Technical': ['npm', 'package', 'node', 'javascript', 'code', 'library', 'dependency', 'install', 'version'],
        'Supply Chain': ['supply', 'chain', 'dependencies', 'upstream', 'downstream'],
        'Action': ['update', 'fix', 'patch', 'remove', 'check', 'scan', 'monitor', 'protect']
    }
    
    categorized = {cat: [] for cat in categories}
    uncategorized = []
    
    for word, freq in keywords_list:
        assigned = False
        for cat, keywords in categories.items():
            if word in keywords:
                categorized[cat].append((word, freq))
                assigned = True
                break
        if not assigned:
            uncategorized.append((word, freq))
    
    return categorized, uncategorized

@st.cache_data
def extract_keyword_cooccurrence(texts, top_keywords, top_n=10):
    keyword_set = set([k[0] for k in top_keywords])
    cooccurrence = Counter()
    
    for text in texts:
        if pd.notna(text):
            text = str(text).lower()
            text = re.sub(r'http\S+|www\S+|@\S+|#\S+', '', text)
            tokens = set(re.findall(r'\b[a-z]{3,}\b', text))
            found_keywords = tokens & keyword_set
            
            if len(found_keywords) >= 2:
                for pair in combinations(sorted(found_keywords), 2):
                    cooccurrence[pair] += 1
    
    return cooccurrence.most_common(top_n)

@st.cache_data
def extract_keywords_temporal(df, top_n=10):
    df_temp = df.copy()
    df_temp['date'] = df_temp['created_at'].dt.date
    
    stopwords = {'the', 'and', 'for', 'are', 'with', 'this', 'that', 'from', 'was', 'has', 'have', 
                 'been', 'not', 'but', 'can', 'will', 'all', 'more', 'https', 'com', 'via', 'new', 'get', 'one', 'now', 'use'}
    
    daily_keywords = {}
    for date, group in df_temp.groupby('date'):
        words = []
        for text in group['full_text']:
            if pd.notna(text):
                text = str(text).lower()
                text = re.sub(r'http\S+|www\S+|@\S+|#\S+', '', text)
                tokens = re.findall(r'\b[a-z]{3,}\b', text)
                words.extend([w for w in tokens if w not in stopwords])
        daily_keywords[date] = Counter(words).most_common(top_n)
    
    return daily_keywords

df = load_data()
keywords = extract_keywords(df['full_text'], top_n=20)
keywords_df = pd.DataFrame(keywords, columns=['Kata Kunci', 'Frekuensi'])
keywords_df['Persentase'] = (keywords_df['Frekuensi'] / keywords_df['Frekuensi'].sum() * 100).round(2)
categorized, uncategorized = categorize_keywords(keywords)
cooccurrence = extract_keyword_cooccurrence(df['full_text'], keywords, top_n=15)
daily_keywords = extract_keywords_temporal(df, top_n=5)

st.sidebar.info(f"**Periode:** Sep - Nov 2025\n**Total Data:** {len(df):,} tweets")

st.title("🔤 Kata Kunci")
st.caption("Ekstraksi dan kata-kata dominan dalam diskusi")
st.markdown("---")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### 📊 Top 15 Kata Kunci Dominan")
    st.markdown("**🎯 Tujuan:** Identifikasi istilah teknis yang paling sering muncul")
    st.markdown("**🔬 Metode:** Frequency counting dengan stopword removal")
with col2:
    st.metric("Total Kata Unik", f"{len(set([w for text in df['full_text'] if pd.notna(text) for w in str(text).lower().split()])):,}")
    st.metric("Kata Teratas", keywords_df.iloc[0]['Kata Kunci'])
    st.caption(f"Frekuensi: {keywords_df.iloc[0]['Frekuensi']} kali")

fig = px.bar(keywords_df, x='Frekuensi', y='Kata Kunci', orientation='h',
             title='Distribusi Frekuensi Kata Kunci',
             labels={'Kata Kunci': 'Kata Kunci', 'Frekuensi': 'Frekuensi Kemunculan'})
fig.update_traces(marker_color='#3498db', texttemplate='%{x}', textposition='outside')
fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
st.plotly_chart(fig, width='stretch')

st.markdown(f"""
**📊 Hasil Analisis:**
- Kata paling dominan: **"{keywords_df.iloc[0]['Kata Kunci']}"** ({keywords_df.iloc[0]['Frekuensi']} kemunculan)
- Kata kedua: **"{keywords_df.iloc[1]['Kata Kunci']}"** ({keywords_df.iloc[1]['Frekuensi']} kemunculan)
- Kata ketiga: **"{keywords_df.iloc[2]['Kata Kunci']}"** ({keywords_df.iloc[2]['Frekuensi']} kemunculan)

**💡 Kesimpulan:**
Kata-kata dominan seperti **"npm", "attack", "supply", "chain", "package"** menunjukkan bahwa diskusi 
sangat **fokus pada isu teknis** terkait keamanan ekosistem NPM. Kata **"security"** dan **"malicious"** 
yang sering muncul mengindikasikan tingginya **awareness** komunitas terhadap ancaman supply chain.

**🎯 Implikasi:**
Temuan ini menunjukkan bahwa komunitas developer JavaScript memiliki **literasi keamanan yang baik** 
dan aktif mendiskusikan solusi preventif untuk mencegah serangan serupa di masa depan.
""")

st.markdown("---")

# Chart 2: Treemap
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🗺️ Proporsi Kata Kunci")
    st.markdown("**🎯 Tujuan:** Visualisasi proporsi kata kunci dengan area")
    st.markdown("**🔬 Metode:** Treemap dengan color gradient berdasarkan frekuensi")
    
    fig = px.treemap(keywords_df, path=['Kata Kunci'], values='Frekuensi',
                    title='Proporsi Kata Kunci (Treemap)',
                    color='Frekuensi',
                    color_continuous_scale='Blues')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("**📊 Hasil:** Area persegi merepresentasikan frekuensi relatif setiap kata kunci.")

with col2:
    st.markdown("### 🎯 Distribusi Kata Kunci")
    st.markdown("**🎯 Tujuan:** Analisis distribusi frekuensi kata kunci")
    st.markdown("**🔬 Metode:** Scatter plot dengan size mapping")
    
    keywords_df['rank'] = range(1, len(keywords_df) + 1)
    fig = px.scatter(keywords_df, x='rank', y='Frekuensi',
                    size='Frekuensi', color='Frekuensi',
                    hover_data=['Kata Kunci'],
                    title='Distribusi Ranking Kata Kunci',
                    labels={'rank': 'Ranking', 'Frekuensi': 'Frekuensi'},
                    color_continuous_scale='Viridis')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("**📊 Hasil:** Scatter plot menunjukkan pola distribusi power-law pada frekuensi kata kunci.")

st.markdown("---")

# Chart 3: Polar Chart
st.markdown("### 🎪 Top 10 Kata Kunci")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🎯 Tujuan:** Visualisasi radial untuk perbandingan kata kunci")
    st.markdown("**🔬 Metode:** Polar bar chart dengan mapping frekuensi ke radius")
with col2:
    st.metric("Top 10 Total", f"{keywords_df.head(10)['Frekuensi'].sum():,}")
    st.caption(f"{keywords_df.head(10)['Frekuensi'].sum()/keywords_df['Frekuensi'].sum()*100:.1f}% dari total")

fig = px.bar_polar(keywords_df.head(10), r='Frekuensi', theta='Kata Kunci',
                  title='Distribusi Radial Kata Kunci Dominan',
                  color='Frekuensi',
                  color_continuous_scale='Blues')
fig.update_layout(height=500)
st.plotly_chart(fig, width='stretch')

st.markdown("""
**📊 Hasil:**
Polar chart memberikan perspektif alternatif untuk membandingkan kata kunci. Top 10 kata kunci 
merepresentasikan mayoritas diskusi, menunjukkan **konsentrasi topik** yang tinggi.

**💡 Insight:**
Konsentrasi pada beberapa kata kunci utama menunjukkan bahwa diskusi **sangat terfokus** pada 
isu-isu spesifik terkait keamanan NPM, bukan tersebar ke topik yang tidak relevan.
""")

st.markdown("---")

# Chart 4: Keyword Categories
st.markdown("### 🏷️ Kategorisasi Kata Kunci")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🎯 Tujuan:** Mengelompokkan kata kunci berdasarkan tema untuk analisis kontekstual")
    st.markdown("**🔬 Metode:** Rule-based categorization dengan predefined categories")
with col2:
    total_categorized = sum(len(v) for v in categorized.values())
    st.metric("Kata Terkategorisasi", total_categorized)
    st.caption(f"{len(uncategorized)} tidak terkategorisasi")

# Create category dataframe
cat_data = []
for cat, words in categorized.items():
    for word, freq in words:
        cat_data.append({'Kategori': cat, 'Kata': word, 'Frekuensi': freq})

if cat_data:
    cat_df = pd.DataFrame(cat_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sunburst chart
        fig = px.sunburst(cat_df, path=['Kategori', 'Kata'], values='Frekuensi',
                         title='Hierarki Kategori Kata Kunci',
                         color='Frekuensi',
                         color_continuous_scale='Reds')
        fig.update_layout(height=450)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Category distribution
        cat_summary = cat_df.groupby('Kategori')['Frekuensi'].sum().reset_index()
        cat_summary = cat_summary.sort_values('Frekuensi', ascending=True)
        
        fig = px.bar(cat_summary, x='Frekuensi', y='Kategori', orientation='h',
                    title='Distribusi Frekuensi per Kategori',
                    text='Frekuensi')
        fig.update_traces(marker_color='#e74c3c', textposition='outside')
        fig.update_layout(height=450)
        st.plotly_chart(fig, width='stretch')
    
    st.markdown(f"""
    **📊 Hasil Kategorisasi:**
    - **Security**: {len(categorized['Security'])} kata - fokus pada ancaman dan keamanan
    - **Technical**: {len(categorized['Technical'])} kata - terminologi teknis NPM/JavaScript
    - **Supply Chain**: {len(categorized['Supply Chain'])} kata - konteks serangan supply chain
    - **Action**: {len(categorized['Action'])} kata - tindakan mitigasi dan respons
    
    **💡 Insight:**
    Dominasi kategori Security menunjukkan bahwa diskusi **sangat concern** terhadap aspek keamanan.
    Kehadiran kategori Action mengindikasikan komunitas **proaktif** mencari solusi.
    """)
else:
    st.info("Tidak ada kata kunci yang dapat dikategorisasi.")

st.markdown("---")

# Chart 5: Co-occurrence Network
st.markdown("### 🔗 Analisis Co-occurrence Kata Kunci")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🎯 Tujuan:** Mengidentifikasi kata kunci yang sering muncul bersamaan")
    st.markdown("**🔬 Metode:** Pairwise co-occurrence analysis dalam tweet yang sama")
with col2:
    st.metric("Total Pasangan", len(cooccurrence))
    st.caption("Top 15 co-occurrence")

if cooccurrence:
    cooc_df = pd.DataFrame([
        {'Pasangan': f"{pair[0]} + {pair[1]}", 'Kata 1': pair[0], 'Kata 2': pair[1], 'Frekuensi': freq}
        for pair, freq in cooccurrence
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(cooc_df, x='Frekuensi', y='Pasangan', orientation='h',
                    title='Top 15 Pasangan Kata yang Sering Muncul Bersama',
                    text='Frekuensi')
        fig.update_traces(marker_color='#9b59b6', textposition='outside')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Heatmap-style visualization
        top_words = list(set([w for pair, _ in cooccurrence[:10] for w in pair]))
        matrix_data = []
        
        for w1 in top_words:
            row = []
            for w2 in top_words:
                if w1 == w2:
                    row.append(0)
                else:
                    pair = tuple(sorted([w1, w2]))
                    freq = next((f for p, f in cooccurrence if p == pair), 0)
                    row.append(freq)
            matrix_data.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix_data,
            x=top_words,
            y=top_words,
            colorscale='Purples',
            text=matrix_data,
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
        fig.update_layout(title='Heatmap Co-occurrence Matrix', height=500)
        st.plotly_chart(fig, width='stretch')
    
    st.markdown(f"""
    **📊 Hasil:**
    - Pasangan teratas: **"{cooc_df.iloc[0]['Kata 1']}" + "{cooc_df.iloc[0]['Kata 2']}"** ({cooc_df.iloc[0]['Frekuensi']} kali)
    - Total {len(cooccurrence)} pasangan kata yang sering muncul bersama
    
    **💡 Insight:**
    Co-occurrence menunjukkan **konteks semantik** dan **topik terkait** yang dibahas bersamaan.
    Pasangan kata mengungkap **narasi dominan** dalam diskusi NPM supply chain attack.
    """)
else:
    st.info("Tidak ada co-occurrence yang signifikan ditemukan.")

st.markdown("---")

# Chart 6: Temporal Evolution
st.markdown("### 📅 Evolusi Temporal Kata Kunci")
st.markdown("**🎯 Tujuan:** Melihat perubahan kata kunci dominan dari waktu ke waktu")
st.markdown("**🔬 Metode:** Daily keyword extraction dan tracking frequency changes")

# Get top 5 overall keywords
top_5_keywords = [k[0] for k in keywords[:5]]

# Create temporal dataframe
temporal_data = []
for date, kw_list in daily_keywords.items():
    for word, freq in kw_list:
        if word in top_5_keywords:
            temporal_data.append({'Tanggal': date, 'Kata': word, 'Frekuensi': freq})

if temporal_data:
    temporal_df = pd.DataFrame(temporal_data)
    
    fig = px.line(temporal_df, x='Tanggal', y='Frekuensi', color='Kata',
                 title='Tren Temporal Top 5 Kata Kunci',
                 labels={'Frekuensi': 'Frekuensi Harian', 'Kata': 'Kata Kunci'})
    fig.update_layout(hovermode='x unified', height=600)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("""
    **📊 Hasil:**
    Line chart menunjukkan **dinamika temporal** kata kunci dominan sepanjang periode.
    Fluktuasi mengindikasikan **pergeseran fokus** diskusi dari waktu ke waktu.
    
    **💡 Insight:**
    - Kata kunci yang **konsisten tinggi** = topik inti yang terus dibahas
    - **Spike** pada tanggal tertentu = momen kritis atau breaking news
    - **Penurunan bertahap** = topik mulai mereda atau teratasi
    """)
else:
    st.info("Data temporal tidak tersedia.")

st.markdown("---")

# Summary Statistics
st.markdown("### 📊 Ringkasan Statistik Kata Kunci")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Kata Unik", f"{len(set([w for text in df['full_text'] if pd.notna(text) for w in str(text).lower().split()])):,}")
    st.caption("Dalam dataset")
with col2:
    st.metric("Avg Frekuensi", f"{keywords_df['Frekuensi'].mean():.1f}")
    st.caption("Top 20 keywords")
with col3:
    st.metric("Konsentrasi Top 5", f"{keywords_df.head(5)['Persentase'].sum():.1f}%")
    st.caption("Dari total frekuensi")
with col4:
    st.metric("Diversity Index", f"{(1 - (keywords_df['Frekuensi'].std() / keywords_df['Frekuensi'].mean())):.2f}")
    st.caption("Coefficient of variation")
