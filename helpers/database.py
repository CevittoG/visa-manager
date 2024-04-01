import streamlit as st
import pandas as pd
from supabase import create_client, Client
from typing import List, Union, Tuple


@st.cache_resource
def db_init_conn() -> Client:
    url = st.secrets["SUPABASE_PROJECT_URL"]
    key = st.secrets["SUPABASE_API_KEY"]

    # Create client
    supabase_client = create_client(url, key)
    # Create session from client
    supabase_session = supabase_client.auth.sign_in_with_password({'email': st.secrets['SUPABASE_ADMIN_USER'], 'password': st.secrets['SUPABASE_ADMIN_PASS']})

    return supabase_client


# @st.experimental_memo(ttl=600, show_spinner=False)
def db_select(_conn: Client, table_name: str, columns: Union[List[str], str] = '*', query_filter: Tuple[str, str, str] = None):
    sel_col = ', '.join(columns) if isinstance(columns, list) else columns

    try:
        if query_filter is not None:
            query = _conn.table(table_name).select(sel_col).filter(column=query_filter[0], operator=query_filter[1], criteria=query_filter[2])
        else:
            query = _conn.table(table_name).select(sel_col)

        response = query.execute()
        return response
    except:
        return False


# @st.experimental_memo(ttl=600, show_spinner=False)
def db_insert(_conn: Client, table_name: str, json_data: Union[dict, List[dict]]):
    query = _conn.table(table_name).insert(json_data)
    try:
        response = query.execute()
    except Exception as e:
        response = e
    return response.message


# @st.experimental_memo(ttl=600, show_spinner=False)
def db_update(_conn: Client, table_name: str, json_data: Union[dict, list], query_filter: Tuple[str, str, str]):
    try:
        query = _conn.table(table_name).update(json_data).filter(column=query_filter[0], operator=query_filter[1], criteria=query_filter[2])
        response = query.execute()
        return response
    except:
        return False