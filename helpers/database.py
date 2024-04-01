import streamlit as st
import pandas as pd
from supabase import create_client, Client
from typing import List, Union, Tuple


@st.experimental_singleton
def db_init_conn() -> Client:
    url = st.secrets["SUPABASE_PROJECT_URL"]
    key = st.secrets["SUPABASE_API_KEY"]
    return create_client(url, key)


# @st.experimental_memo(ttl=600, show_spinner=False)
def db_select(_conn: Client, table_name: str, columns: Union[List[str], str] = '*', query_filter: Tuple[str, str, str] = None) -> Union[pd.DataFrame, bool]:
    sel_col = ', '.join(columns) if isinstance(columns, list) else columns

    try:
        if query_filter is not None:
            query = _conn.table(table_name).select(sel_col).filter(column=query_filter[0], operator=query_filter[1], criteria=query_filter[2])
        else:
            query = _conn.table(table_name).select(sel_col)

        response = query.execute()
        df = pd.DataFrame.from_records(response.data)
        return df
    except:
        return False


# @st.experimental_memo(ttl=600, show_spinner=False)
def db_insert(_conn: Client, table_name: str, json_data: Union[dict, List[dict]]) -> Union[pd.DataFrame, bool]:
    try:
        query = _conn.table(table_name).insert(json_data)
        response = query.execute()
        df = pd.DataFrame.from_records(response.data)
        return df
    except Exception as e:
        return e


# @st.experimental_memo(ttl=600, show_spinner=False)
def db_update(_conn: Client, table_name: str, json_data: Union[dict, list], query_filter: Tuple[str, str, str]) -> Union[pd.DataFrame, bool]:
    try:
        query = _conn.table(table_name).update(json_data).filter(column=query_filter[0], operator=query_filter[1], criteria=query_filter[2])
        response = query.execute()
        df = pd.DataFrame.from_records(response.data)
        return df
    except:
        return False