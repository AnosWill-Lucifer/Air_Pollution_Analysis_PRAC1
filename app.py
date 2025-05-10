import streamlit as st
from my_page.summary import show as show_summary
from my_page.processing import show as show_processing
from my_page.visualization import show as show_visualization
from my_page.modeling import show as show_modeling
from my_page.summary_insight import show as show_summary_insight

# Multipage navigation
def main():
    st.sidebar.title("🗂️ Navigation")
    pages = {
        "1️⃣ Project & Data Summary": show_summary,
        "2️⃣ Theory & Processing": show_processing,
        "3️⃣ Visualization": show_visualization,
        "4️⃣ Modeling & Prediction": show_modeling,
        "5️⃣ Summary & Insights": show_summary_insight
    }
    choice = st.sidebar.radio("Go to", list(pages.keys()))
    pages[choice]()

if __name__ == "__main__":
    main()