import streamlit as st
from streamlit_option_menu import option_menu
import home
import map

st.set_page_config(layout="wide")

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title="Podering",
                options=["home", "map"],
                icons=["house-fill", "person-circle"],
                menu_icon="chart-text-fill",
                default_index=1,
            )

   
        if app == "home":
          home.app() 

        elif app == "map":
          map.app()  

if __name__ == "__main__":
    app = MultiApp()
    app.run()
