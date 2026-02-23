#Necessary imports

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

#Page config - not yet responsive :(
st.set_page_config(
    page_title="Medical NER Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS- should've added a seperate file. in next push--->should change it
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap');


    html, body, .stApp {
        background: #0a0e1a;
        color: #e2e8f0;
        font-family: 'DM Sans', sans-serif;
    }

    .stApp > header { background: transparent; }


    .block-container {
        padding-top: 2rem;
        padding-bottom: 0;
        max-width: 1200px;
    }

 
    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        margin-bottom: 1rem;
    }
    .hero h1 {
        font-family: 'DM Sans', sans-serif;
        font-size: 2.6rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    .hero .accent {
        background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero p {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 0.6rem;
        font-weight: 400;
    }


    .metric-row {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
        justify-content: center;
        flex-wrap: wrap;
    }
    .metric-card {
        background: linear-gradient(145deg, #111827, #1e293b);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 1.4rem 2rem;
        text-align: center;
        min-width: 180px;
        flex: 1;
        max-width: 250px;
        transition: transform 0.2s, border-color 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #334155;
    }
    .metric-card .value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.3rem;
    }
    .metric-card .label {
        font-size: 0.82rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 500;
    }


    .clr-condition  { color: #f87171; }
    .clr-symptom    { color: #fbbf24; }
    .clr-medication { color: #34d399; }
    .clr-procedure  { color: #60a5fa; }
    .clr-total      { color: #c4b5fd; }

 
    .section-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.35rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 2.5rem 0 0.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #1e293b;
    }

  
    .chat-container {
        background: #111827;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .chat-q {
        background: #1e293b;
        border-radius: 12px;
        padding: 0.8rem 1.1rem;
        margin: 0.5rem 0;
        color: #e2e8f0;
        font-size: 0.95rem;
        border-left: 3px solid #60a5fa;
    }
    .chat-a {
        background: #0f172a;
        border-radius: 12px;
        padding: 0.8rem 1.1rem;
        margin: 0.5rem 0;
        color: #cbd5e1;
        font-size: 0.95rem;
        border-left: 3px solid #34d399;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        white-space: pre-wrap;
    }


    .code-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: #111827;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #1e293b;
        margin: 1rem 0;
    }
    .code-table th {
        background: #1e293b;
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 0.8rem 1rem;
        text-align: left;
        border-bottom: 1px solid #334155;
    }
    .code-table td {
        padding: 0.65rem 1rem;
        font-size: 0.88rem;
        color: #e2e8f0;
        border-bottom: 1px solid #1e293b;
    }
    .code-table tr:last-child td { border-bottom: none; }
    .code-table tr:hover td { background: #1e293b44; }

    .badge {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-condition  { background: #f8717122; color: #f87171; }
    .badge-symptom    { background: #fbbf2422; color: #fbbf24; }
    .badge-medication { background: #34d39922; color: #34d399; }
    .badge-procedure  { background: #60a5fa22; color: #60a5fa; }
    .badge-exact      { background: #34d39922; color: #34d399; }
    .badge-approx     { background: #fbbf2422; color: #fbbf24; }
    .badge-notfound   { background: #f8717122; color: #f87171; }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #111827;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid #1e293b;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 0.5rem 1.2rem;
    }
    .stTabs [aria-selected="true"] {
        background: #1e293b;
        color: #f1f5f9;
    }


    .stTextInput > div > div > input {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        color: #e2e8f0;
        font-family: 'DM Sans', sans-serif;
        padding: 0.7rem 1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 2px #60a5fa33;
    }

    .footer {
        text-align: center;
        padding: 3rem 0 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid #1e293b;
    }
    .footer p {
        color: #64748b;
        font-size: 0.88rem;
        margin: 0;
    }
    .footer .heart {
        color: #f472b6;
        font-size: 1rem;
    }
    .footer .name {
        color: #c4b5fd;
        font-weight: 600;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


#Load checkpoint from local machine
@st.cache_data
def load_dashboard_data():
    """Load the checkpoint CSV."""
    paths = [
        'checkpoints/dashboard_data.csv',
        'dashboard_data.csv',
    ]
    for p in paths:
        if os.path.exists(p):
            return pd.read_csv(p)
    st.error(" `dashboard_data.csv` not found.")
    st.stop()

df = load_dashboard_data()


COLORS = {
    'condition': '#f87171',
    'symptom': '#fbbf24',
    'medication': '#34d399',
    'procedure': '#60a5fa',
}
CAT_ORDER = ['condition', 'symptom', 'medication', 'procedure']
CAT_EMOJI = {'condition': '🔴', 'symptom': '🟡', 'medication': '🟢', 'procedure': '🔵'}


#hero
st.markdown("""
<div class="hero">
    <h1> Medical <span class="accent">Named Entity</span> Dashboard</h1>
</div>
""", unsafe_allow_html=True)


total = df['record_count'].sum()


#cards_metric
col0, col1, col2, col3, col4 = st.columns(5)

with col0:
    st.markdown(f"""
    <div class="metric-card">
        <div class="value clr-total">{len(df)}</div>
        <div class="label">Entities Tracked</div>
    </div>
    """, unsafe_allow_html=True)

with col1:
    cnt = df[df['category'] == 'condition']['record_count'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="value clr-condition">{cnt:,}</div>
        <div class="label">🔴 Conditions</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    cnt = df[df['category'] == 'symptom']['record_count'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="value clr-symptom">{cnt:,}</div>
        <div class="label">🟡 Symptoms</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    cnt = df[df['category'] == 'medication']['record_count'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="value clr-medication">{cnt:,}</div>
        <div class="label">🟢 Medications</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    cnt = df[df['category'] == 'procedure']['record_count'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="value clr-procedure">{cnt:,}</div>
        <div class="label">🔵 Procedures</div>
    </div>
    """, unsafe_allow_html=True)


#Tabs ---->need to work on it more later
tab_chart, tab_table, tab_chat = st.tabs(["Dashboard", "Code Reference", "Ask me about data"])
with tab_chart:
    st.markdown('<div class="section-header">Top 10 Entities by Category</div>', unsafe_allow_html=True)

    for cat in CAT_ORDER:
        sub = df[df['category'] == cat].sort_values('record_count')

        hovers = [
            f"<b>{r['entity'].title()}</b><br>"
            f"Records: {r['record_count']}<br>"
            f"Code: {r['code']} ({r['code_system']})<br>"
            f"Match: {r['confidence']}"
            for _, r in sub.iterrows()
        ]

        fig = go.Figure(go.Bar(
            x=sub['record_count'],
            y=sub['entity'].str.title(),
            orientation='h',
            marker=dict(
                color=COLORS[cat],
                line=dict(color='rgba(255,255,255,0.05)', width=0.5),
            ),
            hovertext=hovers,
            hoverinfo='text',
            text=[f'  {rc}' for rc in sub['record_count']],
            textposition='outside',
            textfont=dict(size=11, color='#94a3b8'),
            showlegend=False,
        ))

        fig.update_layout(
            title=dict(
                text=f"<b>{CAT_EMOJI[cat]}  {cat.capitalize()}s</b>",
                x=0.0,
                font=dict(size=15, color='white'),
            ),
            height=340,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#111827',
            font=dict(color='#e2e8f0', family='DM Sans, sans-serif'),
            margin=dict(t=50, b=20, l=220, r=60),
            xaxis=dict(
                gridcolor='#1e293b',
                title='Records',
                title_font=dict(size=10, color='#64748b'),
                tickfont=dict(color='#94a3b8'),
                zeroline=False,
            ),
            yaxis=dict(
                gridcolor='#1e293b',
                tickfont=dict(size=12, color='#cbd5e1'),
            ),
            hoverlabel=dict(
                bgcolor='#1e293b',
                bordercolor='#334155',
                font=dict(color='#e2e8f0', size=12),
            ),
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

#dash+code
with tab_table:
    st.markdown('<div class="section-header">Standard Medical Codes Reference</div>', unsafe_allow_html=True)

    # Build HTML table
    table_html = '<table class="code-table"><thead><tr>'
    for h in ['Category', 'Entity', 'Records', 'Code', 'System', 'Description', 'Match']:
        table_html += f'<th>{h}</th>'
    table_html += '</tr></thead><tbody>'

    df_sorted = df.sort_values(['category', 'record_count'], ascending=[True, False])
    for _, r in df_sorted.iterrows():
        cat = r['category']
        conf = r['confidence']
        conf_class = 'exact' if conf == 'exact' else ('approx' if conf == 'approximate' else 'notfound')
        conf_label = '✅ Exact' if conf == 'exact' else ('🟡 Approx' if conf == 'approximate' else '❌ N/A')

        table_html += '<tr>'
        table_html += f'<td><span class="badge badge-{cat}">{cat.capitalize()}</span></td>'
        table_html += f'<td style="font-weight:500;">{r["entity"].title()}</td>'
        table_html += f'<td style="font-family:JetBrains Mono,monospace;color:#c4b5fd;">{r["record_count"]}</td>'
        table_html += f'<td style="font-family:JetBrains Mono,monospace;">{r["code"]}</td>'
        table_html += f'<td style="color:#94a3b8;">{r["code_system"]}</td>'
        table_html += f'<td style="color:#94a3b8;font-size:0.83rem;">{r["description"]}</td>'
        table_html += f'<td><span class="badge badge-{conf_class}">{conf_label}</span></td>'
        table_html += '</tr>'

    table_html += '</tbody></table>'
    st.markdown(table_html, unsafe_allow_html=True)


#chat(without llm implimentation)
with tab_chat:
    st.markdown('<div class="section-header">Ask Questions About the Data</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#94a3b8; font-size:0.88rem; margin-bottom:1rem; line-height:1.6;">
        Try: <code style="background:#1e293b;padding:2px 6px;border-radius:4px;color:#60a5fa;">top conditions</code> ·
        <code style="background:#1e293b;padding:2px 6px;border-radius:4px;color:#60a5fa;">most common</code> ·
        <code style="background:#1e293b;padding:2px 6px;border-radius:4px;color:#60a5fa;">code for aspirin</code> ·
        <code style="background:#1e293b;padding:2px 6px;border-radius:4px;color:#60a5fa;">compare</code> ·
        <code style="background:#1e293b;padding:2px 6px;border-radius:4px;color:#60a5fa;">show all</code>
    </div>
    """, unsafe_allow_html=True)

    # Session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    def process_question(q):
        """Process a user question and return an answer from the data."""
        q_lower = q.lower().strip()

        for cat in CAT_ORDER:
            if cat in q_lower:
                sub = df[df['category'] == cat].sort_values('record_count', ascending=False)
                lines = [f"Top {len(sub)} {cat}s:\n"]
                for _, r in sub.iterrows():
                    lines.append(
                        f"  {r['entity'].title():<30} {r['record_count']:>4} records    "
                        f"{r['code']} ({r['code_system']})"
                    )
                return '\n'.join(lines)

        if any(kw in q_lower for kw in ['most common', 'highest', 'top overall', 'number one', '#1']):
            top = df.sort_values('record_count', ascending=False).iloc[0]
            return (
                f"{top['entity'].title()} ({top['category']})\n"
                f"  Records: {top['record_count']}\n"
                f"  Code:    {top['code']} ({top['code_system']})"
            )

        #Code
        if 'code' in q_lower:
            results = []
            for _, r in df.iterrows():
                if r['entity'].lower() in q_lower:
                    results.append(
                        f"{r['entity'].title()}: {r['code']} ({r['code_system']})\n"
                        f"  Description: {r['description']}\n"
                        f"  Match:       {r['confidence']}"
                    )
            if results:
                return '\n\n'.join(results)
            return "Entity not found in top 40. Try the exact entity name."

        #Compare
        if any(kw in q_lower for kw in ['compare', 'summary', 'overview']):
            lines = ["Category Overview:\n"]
            for cat in CAT_ORDER:
                sub = df[df['category'] == cat]
                total_recs = sub['record_count'].sum()
                top_ent = sub.sort_values('record_count', ascending=False).iloc[0]
                lines.append(
                    f"  {cat.capitalize():<12}  {len(sub)} entities  "
                    f"{total_recs:>5} total mentions  "
                    f"top: {top_ent['entity']} ({top_ent['record_count']})"
                )
            return '\n'.join(lines)

        #Show all- kinda messy-can fix it later with better logic
        if any(kw in q_lower for kw in ['all', 'show', 'list', 'everything', 'full']):
            return df.to_string(index=False)


        return (
            "I can answer:\n"
            "  • top conditions / symptoms / medications / procedures\n"
            "  • most common — highest record count overall\n"
            "  • code for [entity] — look up a specific code\n"
            "  • compare — category overview\n"
            "  • show all — full data table"
        )

    # Chat input
    user_q = st.text_input("", placeholder="Ask something about the medical entities...", label_visibility="collapsed")

    if user_q:
        answer = process_question(user_q)
        st.session_state.chat_history.append((user_q, answer))

    #chat history----implemented for now--might delete later
    if st.session_state.chat_history:
        for q_text, a_text in reversed(st.session_state.chat_history[-10:]):
            st.markdown(f'<div class="chat-q"> {q_text}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-a">{a_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; color:#475569; padding:3rem 0;">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;"></div>
            <div>Ask a question about the medical entities above</div>
        </div>
        """, unsafe_allow_html=True)


#Footer
st.markdown("""
<div class="footer">
    <p>Made with <span class="heart">♥</span> by <span class="name">Aziz Ahmed -- Trying to survive the era of AI</span></p>
    <p style="font-size:0.75rem; margin-top:0.4rem; color:#475569;">
    </p>
</div>
""", unsafe_allow_html=True)
