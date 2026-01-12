import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Tren", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('dataset.csv')
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df[(df['created_at'] >= '2025-09-01') & (df['created_at'] <= '2025-11-30')]
    return df

df = load_data()

st.sidebar.info(f"**Periode:** Sep - Nov 2025\n**Total Data:** {len(df):,} tweets")

st.title("📊 Tren")
st.caption("Analisis pola waktu diskusi publik terkait NPM Supply Chain Attack")
st.markdown("---")

daily_counts = df.groupby(df['created_at'].dt.date).size().reset_index()
daily_counts.columns = ['date', 'count']

# Chart 1: Line Chart
st.markdown("### 📈 Tren Volume Tweet Harian")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🎯 Tujuan:** Mengidentifikasi pola intensitas diskusi publik per hari")
    st.markdown("**🔬 Metode:** Agregasi time-series dengan grouping harian")
with col2:
    st.metric("Puncak Aktivitas", f"{daily_counts['count'].max()} tweet")
    st.caption(f"Tanggal: {daily_counts.loc[daily_counts['count'].idxmax(), 'date']}")

fig = px.line(daily_counts, x='date', y='count', 
              labels={'date': 'Tanggal', 'count': 'Jumlah Tweet'},
              title='Volume Tweet Harian')
fig.update_traces(line_color='#1f77b4', line_width=2.5)
fig.update_layout(hovermode='x unified', height=600)
st.plotly_chart(fig, width='stretch')

st.markdown(f"""
**📊 Hasil Analisis:**
- Puncak aktivitas terjadi pada **{daily_counts.loc[daily_counts['count'].idxmax(), 'date']}** dengan **{daily_counts['count'].max()} tweet**
- Rata-rata volume harian: **{daily_counts['count'].mean():.0f} tweet**
- Total hari dengan aktivitas: **{len(daily_counts)} hari**

**💡 Kesimpulan:**
Lonjakan aktivitas pada tanggal puncak mengindikasikan adanya **momen kritis** dalam insiden NPM supply chain attack. 
Hal ini menunjukkan bahwa komunitas developer sangat responsif terhadap isu keamanan yang mengancam ekosistem JavaScript.

**🎯 Implikasi:**
Pola temporal ini menunjukkan bahwa **early warning system** dan **rapid response** dari komunitas sangat penting 
untuk memitigasi dampak serangan supply chain di masa depan.
""")

st.markdown("---")

# Chart 2: Weekly Bar
st.markdown("### 📊 Volume Tweet per Minggu")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🎯 Tujuan:** Menganalisis tren jangka menengah dengan agregasi mingguan")
    st.markdown("**🔬 Metode:** Grouping berdasarkan periode mingguan (week period)")
with col2:
    df_weekly = df.copy()
    df_weekly['week'] = df_weekly['created_at'].dt.to_period('W').astype(str)
    weekly_counts = df_weekly.groupby('week').size().reset_index(name='count')
    st.metric("Rata-rata Mingguan", f"{weekly_counts['count'].mean():.0f} tweet")
    st.caption(f"Total: {len(weekly_counts)} minggu")

fig = px.bar(weekly_counts, x='week', y='count', 
             labels={'week': 'Minggu', 'count': 'Jumlah Tweet'},
             title='Distribusi Volume per Minggu')
fig.update_traces(marker_color='#3498db')
fig.update_layout(height=600)
st.plotly_chart(fig, width='stretch')

st.markdown(f"""
**📊 Hasil Analisis:**
- Rata-rata volume mingguan: **{weekly_counts['count'].mean():.0f} tweet**
- Minggu paling aktif: **{weekly_counts.loc[weekly_counts['count'].idxmax(), 'week']}** ({weekly_counts['count'].max()} tweet)
- Standar deviasi: **{weekly_counts['count'].std():.1f}** (menunjukkan variasi aktivitas)

**💡 Kesimpulan:**
Pola mingguan menunjukkan bahwa diskusi tentang NPM attack **tidak berlangsung singkat**, melainkan menjadi topik berkelanjutan 
yang terus dibahas oleh komunitas developer selama periode penelitian. Ini mengindikasikan tingkat **kepedulian tinggi** terhadap keamanan supply chain.

**🎯 Implikasi:**
Persistensi diskusi menunjukkan bahwa insiden ini **mengubah perilaku** komunitas developer dalam hal **dependency management** 
dan **security awareness**. Organisasi perlu mengadopsi **continuous monitoring** untuk supply chain security.
""")

st.markdown("---")

# Chart 3: Area Chart
st.markdown("### 📈 Area Chart Volume Kumulatif")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🎯 Tujuan:** Visualisasi akumulasi volume diskusi dari waktu ke waktu")
    st.markdown("**🔬 Metode:** Area chart dengan fill untuk menunjukkan volume kumulatif")
with col2:
    st.metric("Total Kumulatif", f"{daily_counts['count'].sum():,} tweet")
    st.caption("Periode Sep-Nov 2025")

fig = px.area(daily_counts, x='date', y='count',
              labels={'date': 'Tanggal', 'count': 'Jumlah Tweet'},
              title='Volume Kumulatif Harian')
fig.update_traces(line_color='#3498db', fillcolor='rgba(52, 152, 219, 0.3)')
fig.update_layout(height=600)
st.plotly_chart(fig, width='stretch')

st.markdown(f"""
**📊 Hasil:**
Area chart menunjukkan **intensitas diskusi** dengan visualisasi yang lebih jelas terhadap volume.
Total akumulasi mencapai **{daily_counts['count'].sum():,} tweet** selama periode analisis.
""")

st.markdown("---")

# Chart 4: Hourly Heatmap
st.markdown("### 🔥 Heatmap Aktivitas per Jam dan Hari")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🎯 Tujuan:** Mengidentifikasi pola aktivitas berdasarkan jam dan hari dalam seminggu")
    st.markdown("**🔬 Metode:** Heatmap dengan agregasi hour-of-day vs day-of-week")
with col2:
    df_hourly = df.copy()
    df_hourly['hour'] = df_hourly['created_at'].dt.hour
    peak_hour = df_hourly['hour'].mode()[0]
    st.metric("Jam Paling Aktif", f"{peak_hour}:00")
    st.caption(f"{len(df_hourly[df_hourly['hour']==peak_hour])} tweet")

df_heatmap = df.copy()
df_heatmap['hour'] = df_heatmap['created_at'].dt.hour
df_heatmap['day_name'] = df_heatmap['created_at'].dt.day_name()
day_order_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_order_id = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
heatmap_data = df_heatmap.groupby(['day_name', 'hour']).size().reset_index(name='count')
heatmap_pivot = heatmap_data.pivot(index='day_name', columns='hour', values='count').fillna(0)
heatmap_pivot = heatmap_pivot.reindex(day_order_en)
heatmap_pivot.index = day_order_id

fig = px.imshow(heatmap_pivot, 
                labels=dict(x="Jam", y="Hari", color="Jumlah Tweet"),
                title='Pola Aktivitas Harian',
                color_continuous_scale='Blues',
                aspect='auto',
                text_auto=True)
fig.update_layout(height=600)
st.plotly_chart(fig, width='stretch')

st.markdown(f"""
**📊 Hasil:**
- Jam paling aktif: **{peak_hour}:00** dengan **{len(df_hourly[df_hourly['hour']==peak_hour])}** tweet
- Pola menunjukkan aktivitas tertinggi pada jam kerja, mengindikasikan diskusi profesional

**💡 Insight:**
Pola temporal menunjukkan bahwa diskusi didominasi oleh **developer profesional** yang aktif pada jam kerja.
""")

st.markdown("---")

# Chart 5: Monthly Comparison
st.markdown("### 📅 Perbandingan Volume Bulanan")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🎯 Tujuan:** Membandingkan volume diskusi antar bulan")
    st.markdown("**🔬 Metode:** Bar chart dengan breakdown per bulan")
    
    df_monthly = df.copy()
    df_monthly['month'] = df_monthly['created_at'].dt.to_period('M').astype(str)
    monthly_counts = df_monthly.groupby('month').size().reset_index(name='count')
    
    fig = px.bar(monthly_counts, x='month', y='count',
                 labels={'month': 'Bulan', 'count': 'Jumlah Tweet'},
                 title='Distribusi Volume per Bulan',
                 text='count')
    fig.update_traces(marker_color='#e74c3c', textposition='outside')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown(f"""
    **📊 Hasil:**
    - Bulan paling aktif: **{monthly_counts.loc[monthly_counts['count'].idxmax(), 'month']}**
    - Total: **{monthly_counts['count'].max():,}** tweet
    """)

with col2:
    st.markdown("**🎯 Tujuan:** Visualisasi proporsi kontribusi per bulan")
    st.markdown("**🔬 Metode:** Pie chart distribusi bulanan")
    
    fig = px.pie(monthly_counts, values='count', names='month',
                 title='Proporsi Volume per Bulan',
                 hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown(f"""
    **📊 Hasil:**
    - Distribusi menunjukkan evolusi diskusi sepanjang periode
    - Bulan dengan proporsi tertinggi: **{monthly_counts.loc[monthly_counts['count'].idxmax(), 'month']}**
    """)

st.markdown("---")

# Chart 6: Moving Average
st.markdown("### 📉 Tren dengan Moving Average")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🎯 Tujuan:** Menghaluskan fluktuasi harian untuk melihat tren jangka panjang")
    st.markdown("**🔬 Metode:** Line chart dengan 7-day moving average")
with col2:
    ma_window = st.selectbox("Window MA:", [3, 7, 14], index=1)
    st.caption(f"Moving average {ma_window} hari")

daily_counts['MA'] = daily_counts['count'].rolling(window=ma_window, min_periods=1).mean()

fig = go.Figure()
fig.add_trace(go.Scatter(x=daily_counts['date'], y=daily_counts['count'], 
                         name='Volume Harian', line=dict(color='#9930ff', width=1),
                         opacity=0.5))
fig.add_trace(go.Scatter(x=daily_counts['date'], y=daily_counts['MA'], 
                         name=f'MA-{ma_window}', line=dict(color='#e74c3c', width=3)))
fig.update_layout(title=f'Tren Volume dengan {ma_window}-Day Moving Average',
                  xaxis_title='Tanggal', yaxis_title='Jumlah Tweet',
                  hovermode='x unified', height=600)
st.plotly_chart(fig, width='stretch')

st.markdown(f"""
**📊 Hasil:**
Moving average menunjukkan **tren umum** tanpa noise fluktuasi harian, memudahkan identifikasi pola jangka panjang.

**💡 Kesimpulan:**
Tren yang dihaluskan menunjukkan pola **pertumbuhan** atau **penurunan** diskusi secara konsisten.
""")

st.markdown("---")

# Chart 7: Cumulative Growth
st.markdown("### 📈 Pertumbuhan Kumulatif")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🎯 Tujuan:** Melihat akumulasi total tweet dari waktu ke waktu")
    st.markdown("**🔬 Metode:** Line chart kumulatif sum")
with col2:
    growth_rate = ((daily_counts['count'].sum() / len(daily_counts)) / daily_counts['count'].iloc[0] - 1) * 100 if daily_counts['count'].iloc[0] > 0 else 0
    st.metric("Growth Rate", f"{growth_rate:.1f}%")
    st.caption("Rata-rata pertumbuhan")

daily_counts['cumulative'] = daily_counts['count'].cumsum()

fig = px.line(daily_counts, x='date', y='cumulative',
              labels={'date': 'Tanggal', 'cumulative': 'Total Kumulatif'},
              title='Pertumbuhan Kumulatif Tweet')
fig.update_traces(line_color='#2ecc71', line_width=3, fill='tozeroy')
fig.update_layout(hovermode='x unified', height=600)
st.plotly_chart(fig, width='stretch')

st.markdown(f"""
**📊 Hasil:**
- Total akhir: **{daily_counts['cumulative'].iloc[-1]:,}** tweet
- Pertumbuhan menunjukkan **momentum diskusi** yang konsisten sepanjang periode

**💡 Insight:**
Kurva kumulatif yang **smooth** menunjukkan diskusi berkelanjutan tanpa periode vakum.
""")

st.markdown("---")

# Chart 8: Day of Week Analysis
st.markdown("### 📆 Analisis Berdasarkan Hari dalam Seminggu")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🎯 Tujuan:** Mengidentifikasi pola aktivitas berdasarkan hari kerja vs weekend")
    st.markdown("**🔬 Metode:** Bar chart agregasi per hari dalam seminggu")
    
    df_dow = df.copy()
    df_dow['day_name'] = df_dow['created_at'].dt.day_name()
    dow_counts = df_dow.groupby('day_name').size().reset_index(name='count')
    dow_counts['day_name'] = pd.Categorical(dow_counts['day_name'], 
                                            categories=day_order_en, 
                                            ordered=True)
    dow_counts = dow_counts.sort_values('day_name')
    dow_counts['day_name_id'] = dow_counts['day_name'].map(dict(zip(day_order_en, day_order_id)))
    
    fig = px.bar(dow_counts, x='day_name_id', y='count',
                 labels={'day_name_id': 'Hari', 'count': 'Jumlah Tweet'},
                 title='Distribusi per Hari dalam Seminggu',
                 text='count')
    fig.update_traces(marker_color='#7733cc', textposition='outside')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    st.markdown(f"""
    **📊 Hasil:**
    - Hari paling aktif: **{dow_counts.loc[dow_counts['count'].idxmax(), 'day_name_id']}**
    - Total: **{dow_counts['count'].max():,}** tweet
    """)

with col2:
    st.markdown("**🎯 Tujuan:** Perbandingan aktivitas weekday vs weekend")
    st.markdown("**🔬 Metode:** Pie chart kategori hari")
    
    df_dow['is_weekend'] = df_dow['created_at'].dt.dayofweek.isin([5, 6])
    weekend_counts = df_dow.groupby('is_weekend').size().reset_index(name='count')
    weekend_counts['category'] = weekend_counts['is_weekend'].map({True: 'Weekend', False: 'Weekday'})
    
    fig = px.pie(weekend_counts, values='count', names='category',
                 title='Weekday vs Weekend',
                 color='category',
                 color_discrete_map={'Weekday': '#3498db', 'Weekend': '#e67e22'},
                 hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    weekday_pct = weekend_counts[weekend_counts['category']=='Weekday']['count'].values[0] / len(df) * 100
    st.markdown(f"""
    **📊 Hasil:**
    - Weekday: **{weekday_pct:.1f}%**
    - Weekend: **{100-weekday_pct:.1f}%**
    
    **💡 Insight:**
    Dominasi aktivitas pada weekday menunjukkan diskusi bersifat **profesional** dan terkait pekerjaan.
    """)

st.markdown("---")

# Summary Statistics
st.markdown("### 📊 Ringkasan Statistik Temporal")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Median Harian", f"{daily_counts['count'].median():.0f}")
    st.caption("Tweet per hari")
with col2:
    st.metric("Std Deviasi", f"{daily_counts['count'].std():.1f}")
    st.caption("Variabilitas")
with col3:
    st.metric("Koef. Variasi", f"{(daily_counts['count'].std()/daily_counts['count'].mean()*100):.1f}%")
    st.caption("Relative variability")
with col4:
    st.metric("Range", f"{daily_counts['count'].max() - daily_counts['count'].min()}")
    st.caption("Max - Min")
