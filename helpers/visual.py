import random
import streamlit as st
import numpy as np


def show_GIF(gif_type: str, st_structure=st, msg: str = None):
    working_gifs = ['https://media.giphy.com/media/VekcnHOwOI5So/giphy.gif',
                    'https://media.giphy.com/media/13rQ7rrTrvZXlm/giphy.gif',
                    'https://media.giphy.com/media/toXKzaJP3WIgM/giphy.gif',
                    'https://media.giphy.com/media/5Zesu5VPNGJlm/giphy.gif',
                    'https://media.giphy.com/media/xiAqCzbB3eZvG/giphy.gif',
                    'https://media.giphy.com/media/tn3kTJo4P4y1G/giphy.gif']
    error_gifs = ['https://media.giphy.com/media/3BlItBedmyoAU/giphy.gif',
                  'https://media.giphy.com/media/AhjXalGPAfJg4/giphy.gif',
                  'https://media.giphy.com/media/8EmeieJAGjvUI/giphy.gif',
                  'https://media.giphy.com/media/6AaB96ZVrUN0I/giphy.gif',
                  'https://media.giphy.com/media/MZocLC5dJprPTcrm65/giphy.gif',
                  'https://media.giphy.com/media/ljtfkyTD3PIUZaKWRi/giphy.gif',
                  'https://media.giphy.com/media/0DhHqfExMMT7VdeqIr/giphy.gif']
    success_gifs = ['https://media.giphy.com/media/tkApIfibjeWt1ufWwj/giphy.gif',
                    'https://media.giphy.com/media/cXblnKXr2BQOaYnTni/giphy.gif',
                    'https://media.giphy.com/media/IwAZ6dvvvaTtdI8SD5/giphy.gif',
                    'https://media.giphy.com/media/4xpB3eE00FfBm/giphy.gif']
    gifs = {'working': working_gifs,
            'error': error_gifs,
            'success': success_gifs}

    msg_type = {'info': '' if msg is None else msg,
                'working': 'Aún no terminamos de trabajar en esta nueva característica de la plataforma, pero prometemos terminar pronto...' if msg is None else msg,
                'error': 'Algo ha salido mal 😥, por favor contactar a Data Service para notificar problema.' if msg is None else msg,
                'success': 'Todo resultó bien!' if msg is None else msg}
    _, c, _ = st_structure.columns([3, 4, 3])
    c.image(random.choice(gifs[gif_type]), use_column_width=True)

    if gif_type == 'info':
        c.info(msg_type[gif_type])
    elif gif_type == 'working':
        c.warning(msg_type[gif_type])
    elif gif_type == 'error':
        c.error(msg_type[gif_type])
    elif gif_type == 'success':
        c.success(msg_type[gif_type])


def highlight_column(bgcolor="lightblue", color="black"):
    return f'background-color: {bgcolor}; color: {color};'


def highlight_with_function(value, function, bgcolor="#f9aeae", color="black"):
    if function(value):
        return f'background-color: {bgcolor}; color: {color};'
    else:
        return ""


def highlight_invalid_trip(s, bgcolor="#f9aeae", color="black"):
    is_invalid = pd.Series(data=False, index=s.index)
    is_invalid['is_valid'] = s.loc['is_valid'] is False
    return [f'background-color: {bgcolor}; color: {color};' if is_invalid.any() else '' for v in is_invalid]


def highlight_missing_values(value, bgcolor="#f9aeae", color="black"):
    if type(value) == type("") and value == "":
        return f'background-color: {bgcolor}; color: {color};'
    elif type(value) in [type(np.nan)] and np.isnan(value):
        return f'background-color: {bgcolor}; color: {color};'
    else:
        return ""