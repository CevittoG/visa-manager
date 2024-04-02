import streamlit as st
import pandas as pd
from supabase import create_client, Client
from typing import List, Union, Tuple, Literal


# --------------------------------------------------------------------------- DB CONNECTION
@st.cache_resource
def db_init_conn() -> Client:
    url = st.secrets["SUPABASE_PROJECT_URL"]
    key = st.secrets["SUPABASE_API_KEY"]

    # Create client
    supabase_client = create_client(url, key)
    # Create session from client
    supabase_session = supabase_client.auth.sign_in_with_password({'email': st.secrets['SUPABASE_ADMIN_USER'], 'password': st.secrets['SUPABASE_ADMIN_PASS']})

    return supabase_client


# --------------------------------------------------------------------------- DB QUERIES
def db_select(_conn: Client, table_name: str, columns: Union[List[str], str] = '*', query_filter: Tuple[str, Literal['eq', 'neq', 'gr', 'gte', 'lt', 'lte', 'like', 'ilike', 'is', 'in', 'contains'], Union[str, List]] = None):
    sel_col = ', '.join(columns) if isinstance(columns, list) else columns
    if query_filter is not None:
        query = _conn.table(table_name).select(sel_col).filter(column=query_filter[0], operator=query_filter[1], criteria=query_filter[2])
    else:
        query = _conn.table(table_name).select(sel_col)

    try:
        response = query.execute()
        return response.data
    except Exception as e:
        return e.message


def db_insert(_conn: Client, table_name: str, json_data: Union[dict, List[dict]]):
    query = _conn.table(table_name).insert(json_data)
    try:
        response = query.execute()
        return response.data
    except Exception as e:
        return e.message


def db_update(_conn: Client, table_name: str, json_data: Union[dict, list], query_filter: Tuple[str, str, str]):
    try:
        query = _conn.table(table_name).update(json_data).filter(column=query_filter[0], operator=query_filter[1], criteria=query_filter[2])
        response = query.execute()
        return response.data
    except Exception as e:
        return e.message


def db_upsert(_conn: Client, table_name: str, json_data: Union[dict, List[dict]]):
    query = _conn.table(table_name).insert(json_data)
    try:
        response = query.execute()
        return response.data
    except Exception as e:
        return e.message


# --------------------------------------------------------------------------- DATA EXTRACTION BY USER ID
def user_sing_up(_conn: Client, username, password):
    # Creates User
    insert_user = db_insert(_conn, 'users', {'username': username, 'password': password})
    # Check for errors
    if isinstance(insert_user, str):
        if insert_user == 'duplicate key value violates unique constraint "users_username_key"':
            return 'Username already exist, please select another username.'
        else:
            if st.secrets['DEBUG']:
                return insert_user
            else:
                return 'Unknown error, please refresh the page and try again. If this keeps happening please wait a few minutes, the services might be down.'
    else:
        # Creates TravelHistory
        insert_th = db_insert(_conn, 'travel_history', {'user_id': insert_user[0]['id']})
        # Check for errors
        if isinstance(insert_th, str):
            if st.secrets['DEBUG']:
                return insert_th
            else:
                return 'Unknown error, please refresh the page and try again. If this keeps happening please wait a few minutes, the services might be down.'

        else:
            return insert_user[0]['id'], insert_user[0]['username'], insert_th[0]['id']  # user_id, username, th_id


def get_user_trips(_conn, th_id):
    # Get current TravelHistory from db for user
    travel_history_trips = db_select(_conn, 'travel_history_trips', 'trip_id', ('travel_history_id', 'eq', str(th_id)))

    if not travel_history_trips:
        # There is no data for travel_history_id
        return False
    else:
        # Get current TravelHistory-Trips from db for user
        trips = db_select(_conn, 'trips', ['country', 'entry_date', 'exit_date'], ('trips', 'in', str(th_id)))  # ToDo
        return trips

    # bulk upsert
    # [{'id': idx, 'country': t.country, 'entry_date': t.entry_date, 'exit_date': t.exit_date} for t in self.trips]
