import streamlit as st

from utils import APP_NAME, PAGES, RED, TEAL, header, inject_css

st.set_page_config(page_title=f"{APP_NAME} · Group 5", layout="wide")

pages = [
    st.Page(path, title=label, default=(i == 0))
    for i, (path, label) in enumerate(PAGES)
]

page = st.navigation(pages, position="hidden")
active = [p.title for p in pages].index(page.title)

inject_css(accent=RED if page.title == "Messy Data" else TEAL, active=active)
header()
page.run()
