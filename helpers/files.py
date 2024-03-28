import pandas as pd
from typing import List, Tuple, Union
from helpers.config import COUNTRIES


def csv_to_list(trips_df: pd.DataFrame) -> Union[List[Tuple], str]:
    expected_columns = ['country', 'entry_date', 'exit_date']

    # Check columns
    if set(expected_columns).issubset(set(trips_df.columns)):
        trips_df = trips_df[expected_columns]
        # Check for missing values
        if trips_df.isnull().sum().sum() == 0:
            # Check formats
            valid_format = True
            try:
                trips_df = trips_df.astype({'country': 'str',
                                            'entry_date': 'datetime64[ns]',
                                            'exit_date': 'datetime64[ns]'})
                for c in ['entry_date', 'exit_date']:
                    trips_df[c] = trips_df[c].dt.date
            except:
                valid_format = False
            if valid_format:

                # Check country values
                if all(trips_df['country'].isin(COUNTRIES)):
                    return list(trips_df.itertuples(index=False, name=None))
                else:
                    countries_str_list = '\n- '.join(COUNTRIES)
                    return f"Country must be:\n\n- {countries_str_list}"
            else:
                return f"Columns must have the following formats: \n\n- country: str\n- entry_date: date\n- exit_date: date"
        else:
            return f"Mandatory columns: {', '.join(expected_columns)}"
    else:
        return f"File must have columns: {', '.join(expected_columns)}"
