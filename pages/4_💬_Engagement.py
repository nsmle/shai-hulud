import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

st.set_page_config(page_title="Engagement & Hashtag", page_icon="💬", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('dataset.csv')
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df[(df['created_at'] >= '2025-09-01') & (df['created_at'] <= '2025-11-30')]
    return df

@st.cache_data
def extract_hashtags(df):
    all_hashtags = []
    for text in df['full_text'].dropna():
        hashtags = re.findall(r'#(\w+)', str(text))
        all_hashtags.extend([tag.lower() for tag in hashtags])
    return Counter(all_hashtags).most_common(15)

df = load_data()
df['total_engagement'] = df['favorite_count'] + df['retweet_count']

st.sidebar.info(f"**Periode:** Sep - Nov 2025\n**Total Data:** {len(df):,} tweets")

st.title("💬 Analisis Engagement & Hashtag")
st.caption("Analisis interaksi publik dan kategorisasi topik dalam diskusi NPM supply chain attack")
st.markdown("---")

st.markdown("## 📊 Analisis Engagement")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Likes", f"{df['favorite_count'].sum():,}")
with col2:
    st.metric("Total Retweets", f"{df['retweet_count'].sum():,}")
with col3:
    st.metric("Avg Engagement", f"{df['total_engagement'].mean():.1f}")
with col4:
    engagement_rate = (df[df['total_engagement'] > 0].shape[0] / len(df) * 100)
    st.metric("Engagement Rate", f"{engagement_rate:.1f}%")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Distribusi Engagement")
    st.markdown("**🎯 Tujuan:** Menganalisis pola distribusi engagement untuk memahami variasi respons publik")
    st.markdown("**🔬 Metode:** Histogram distribusi total engagement (likes + retweets)")
    
    fig = px.histogram(df, x='total_engagement', nbins=30, title='Distribusi Total Engagement',
                      labels={'total_engagement': 'Total Engagement', 'count': 'Frekuensi'})
    fig.update_traces(marker_color='#8e44ad', marker_line_color='#6c3483', marker_line_width=1.5)
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown(f"""
    **📊 Hasil:**
    - Median: **{df['total_engagement'].median():.0f}**
    - Mean: **{df['total_engagement'].mean():.1f}**
    - Max: **{df['total_engagement'].max():,}**
    
    **💡 Kesimpulan:**
    Distribusi **long-tail** menunjukkan mayoritas tweet memiliki engagement rendah, 
    sementara beberapa tweet viral mendapat perhatian ekstrem dari komunitas.
    """)

with col2:
    st.markdown("### 📈 Tren Engagement Temporal")
    st.markdown("**🎯 Tujuan:** Mengidentifikasi momen peak interest dan pola engagement sepanjang waktu")
    st.markdown("**🔬 Metode:** Time series agregasi engagement harian")
    
    daily_engagement = df.groupby(df['created_at'].dt.date).agg({
        'favorite_count': 'sum', 
        'retweet_count': 'sum'
    }).reset_index()
    daily_engagement.columns = ['date', 'likes', 'retweets']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily_engagement['date'], y=daily_engagement['likes'], 
                            name='Likes', line=dict(color='#c0392b', width=3), 
                            mode='lines+markers', marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=daily_engagement['date'], y=daily_engagement['retweets'], 
                            name='Retweets', line=dict(color='#2874a6', width=3),
                            mode='lines+markers', marker=dict(size=6)))
    fig.update_layout(title='Tren Engagement Harian', height=400, hovermode='x unified')
    st.plotly_chart(fig, width='stretch')
    
    peak_date = daily_engagement.loc[daily_engagement['likes'].idxmax(), 'date']
    st.markdown(f"""
    **📊 Hasil:**
    - Peak engagement: **{daily_engagement.loc[daily_engagement['likes'].idxmax(), 'date']}**
    - Total likes: **{daily_engagement['likes'].sum():,}**
    - Total retweets: **{daily_engagement['retweets'].sum():,}**
    
    **💡 Kesimpulan:**
    Pola engagement mengikuti volume tweet, menunjukkan **konsistensi minat publik** 
    sepanjang periode insiden NPM supply chain attack.
    """)

st.markdown("---")

st.markdown("### ⚖️ Perbandingan Likes vs Retweets")
st.markdown("**🎯 Tujuan:** Memahami tipe engagement dominan dalam respons publik")
st.markdown("**🔬 Metode:** Pie chart proporsi likes vs retweets")

col1, col2 = st.columns(2)

with col1:
    engagement_type = pd.DataFrame({
        'Type': ['Likes', 'Retweets'],
        'Count': [df['favorite_count'].sum(), df['retweet_count'].sum()]
    })
    
    fig = px.pie(engagement_type, values='Count', names='Type',
                 title='Proporsi Likes vs Retweets',
                 color='Type',
                 color_discrete_map={'Likes': '#c0392b', 'Retweets': '#2874a6'},
                 hole=0.4)
    fig.update_traces(textfont_size=16, marker=dict(line=dict(color='#ffffff', width=3)))
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')

with col2:
    likes_pct = (df['favorite_count'].sum() / df['total_engagement'].sum() * 100)
    retweets_pct = (df['retweet_count'].sum() / df['total_engagement'].sum() * 100)
    
    st.markdown(f"""
    **📊 Hasil:**
    - Likes: **{likes_pct:.1f}%** ({df['favorite_count'].sum():,})
    - Retweets: **{retweets_pct:.1f}%** ({df['retweet_count'].sum():,})
    - Rasio Likes:Retweets = **{likes_pct/retweets_pct:.2f}:1**
    
    **💡 Kesimpulan:**
    {'Likes mendominasi, menunjukkan respons **passive agreement**.' if likes_pct > retweets_pct else 'Retweets mendominasi, menunjukkan konten **shareable** dan **actionable**.'}
    
    **🎯 Implikasi:**
    {'Komunitas cenderung memberikan apresiasi tanpa menyebarkan lebih lanjut.' if likes_pct > retweets_pct else 'Komunitas aktif menyebarkan informasi, menunjukkan urgensi dan pentingnya konten.'}
    """)

st.markdown("---")

st.markdown("### 🔥 Top 10 Tweet dengan Engagement Tertinggi")
st.markdown("**🎯 Tujuan:** Identifikasi konten yang paling resonan untuk memahami jenis informasi yang viral")
st.markdown("**🔬 Metode:** Sorting berdasarkan total engagement")

top_tweets = df.nlargest(10, 'total_engagement')[['username', 'full_text', 'favorite_count', 'retweet_count', 'total_engagement']]
st.dataframe(top_tweets, width='stretch', height=400)

st.markdown(f"""
**📊 Hasil:**
- Tweet teratas: **{top_tweets.iloc[0]['total_engagement']:,}** engagement
- Top 10 total: **{top_tweets['total_engagement'].sum():,}** engagement
- Persentase dari total: **{(top_tweets['total_engagement'].sum()/df['total_engagement'].sum()*100):.1f}%**

**💡 Kesimpulan:**
Tweet dengan engagement tinggi berisi **informasi teknis**, **warning**, atau **solusi praktis** 
yang bernilai bagi komunitas developer dalam merespons ancaman keamanan.
""")

st.markdown("---")
st.markdown("---")

st.markdown("## 🔗 Analisis Hashtag")

hashtags = extract_hashtags(df)

if len(hashtags) > 0:
    hashtag_df = pd.DataFrame(hashtags, columns=['Hashtag', 'Frekuensi'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Hashtag Unik", len(hashtags))
    with col2:
        st.metric("Hashtag Teratas", f"#{hashtag_df.iloc[0]['Hashtag']}")
        st.caption(f"{hashtag_df.iloc[0]['Frekuensi']} kali")
    with col3:
        st.metric("Total Penggunaan", f"{hashtag_df['Frekuensi'].sum():,}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Top 15 Hashtag")
        st.markdown("**🎯 Tujuan:** Identifikasi tagar populer untuk memahami kategorisasi topik")
        st.markdown("**🔬 Metode:** Regex extraction dan frequency counting")
        
        fig = px.bar(hashtag_df, x='Frekuensi', y='Hashtag', orientation='h',
                     title='Most Used Hashtags')
        fig.update_traces(marker_color='#16a085', marker_line_color='#117a65', marker_line_width=1.5)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=500)
        st.plotly_chart(fig, width='stretch')
        
        st.markdown(f"""
        **📊 Hasil:**
        - Hashtag teratas: **#{hashtag_df.iloc[0]['Hashtag']}** ({hashtag_df.iloc[0]['Frekuensi']} kali)
        - Top 5 total: **{hashtag_df.head(5)['Frekuensi'].sum():,}** penggunaan
        
        **💡 Kesimpulan:**
        Hashtag dominan menunjukkan **tema utama** yang digunakan komunitas 
        untuk mengorganisir dan mengkategorisasi diskusi.
        """)
    
    with col2:
        st.markdown("### 🎯 Treemap Hashtag")
        st.markdown("**🎯 Tujuan:** Visualisasi proporsi penggunaan hashtag")
        st.markdown("**🔬 Metode:** Treemap dengan color gradient")
        
        fig = px.treemap(hashtag_df, path=['Hashtag'], values='Frekuensi',
                         title='Hashtag Distribution',
                         color='Frekuensi', color_continuous_scale='Tealgrn')
        fig.update_traces(marker=dict(line=dict(color='#ffffff', width=2)))
        fig.update_layout(height=500)
        st.plotly_chart(fig, width='stretch')
        
        top_10_pct = (hashtag_df.head(10)['Frekuensi'].sum() / hashtag_df['Frekuensi'].sum() * 100)
        st.markdown(f"""
        **📊 Hasil:**
        - Total hashtag unik: **{len(hashtags)}**
        - Konsentrasi top 10: **{top_10_pct:.1f}%**
        
        **💡 Insight:**
        Hashtag membantu **information discovery** dan **community coordination** 
        dalam merespons insiden keamanan NPM.
        """)
    
    st.markdown("---")
    
    st.markdown("### 📋 Ringkasan Analisis Engagement & Hashtag")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**💬 Engagement Metrics**")
        st.markdown(f"""
        - Total engagement: **{df['total_engagement'].sum():,}**
        - Engagement rate: **{engagement_rate:.1f}%**
        - Avg per tweet: **{df['total_engagement'].mean():.1f}**
        - Likes ratio: **{likes_pct:.1f}%**
        """)
    
    with col2:
        st.markdown("**🔗 Hashtag Metrics**")
        st.markdown(f"""
        - Total hashtag: **{len(hashtags)}**
        - Total usage: **{hashtag_df['Frekuensi'].sum():,}**
        - Top hashtag: **#{hashtag_df.iloc[0]['Hashtag']}**
        - Top 10 share: **{top_10_pct:.1f}%**
        """)
    
    with col3:
        st.markdown("**🎯 Key Insights**")
        st.markdown(f"""
        - Peak date: **{peak_date}**
        - Top tweet: **{top_tweets.iloc[0]['total_engagement']:,}**
        - Distribution: **Long-tail**
        - Behavior: **{'Passive' if likes_pct > retweets_pct else 'Active'}**
        """)
    
    st.markdown("""
    **🔍 Kesimpulan Utama:**
    
    1. **Engagement Pattern**: Distribusi long-tail menunjukkan beberapa tweet viral mendominasi perhatian publik
    2. **Temporal Consistency**: Engagement mengikuti volume tweet, menunjukkan minat publik yang konsisten
    3. **Hashtag Usage**: Komunitas menggunakan hashtag untuk kategorisasi dan koordinasi diskusi
    4. **Content Type**: Tweet dengan informasi teknis dan solusi praktis mendapat engagement tertinggi
    
    **💡 Implikasi untuk Penelitian:**
    Pola engagement menunjukkan **respons publik yang terstruktur** dengan konten berkualitas tinggi 
    mendapat perhatian maksimal. Hashtag memfasilitasi **information discovery** dan membantu 
    komunitas developer mengorganisir diskusi tentang ancaman keamanan NPM secara efektif.
    """)
    
else:
    st.info("📊 Tidak ada hashtag yang ditemukan dalam dataset. Diskusi bersifat **organik** tanpa kategorisasi formal menggunakan hashtag.")
