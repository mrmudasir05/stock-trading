import pandas as pd
import streamlit as st



def display_response_as_table(res, sort: bool = True):
    if res.ok:
        data = res.json()

        def show_df(df):
            if not df.empty and sort:
                # sort by first column
                first_col = df.columns[0]
                df = df.sort_values(by=first_col, ascending=True).reset_index(drop=True)
            st.dataframe(df, use_container_width=True)

        # If dict with list inside (like {"trades": [...]})
        if isinstance(data, dict) and any(isinstance(v, list) for v in data.values()):
            for key, value in data.items():
                if isinstance(value, list):
                    df = pd.DataFrame(value)
                    st.subheader(key.capitalize())
                    show_df(df)
                    return

        # If dict → single row
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
            show_df(df)

        # If list of dicts → multiple rows
        elif isinstance(data, list):
            df = pd.DataFrame(data)
            show_df(df)

        else:
            st.write(data)
    else:
        st.error(res.text)
