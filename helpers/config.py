import operator
import pandas as pd
from datetime import date, datetime, timedelta


COUNTRIES = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'The Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus',
             'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada',
             'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Democratic Republic of the Congo', 'Republic of the Congo', 'Costa Rica', 'Côte d’Ivoire', 'Croatia', 'Cuba', 'Cyprus',
             'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor (Timor-Leste)', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia',
             'Fiji', 'Finland', 'France', 'Gabon', 'The Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India',
             'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'North Korea', 'South Korea', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia',
             'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico',
             'Micronesia, Federated States of', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar (Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger',
             'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda',
             'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore',
             'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Sudan, South', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand',
             'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'England', 'Wales', 'Scotland', 'Ireland', 'United States', 'Uruguay',
             'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
SCHENGEN_COUNTRIES = ['Austria', 'Belgium', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Italy', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta',
                      'Netherlands', 'Norway', 'Poland', 'Portugal', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland']


class Trip:
    def __init__(self, country, entry_date, exit_date):
        # input from gui
        self.country: str = country
        self.entry_date: date = entry_date
        self.exit_date: date = exit_date
        # to calculate
        self.type: str = self.get_type()
        self.days: int = self.get_duration()
        self.limit_date = 0
        self.days_left = 0
        self.entry_eval_date: date = None
        self.entry_eval_days: int = 0
        self.exit_eval_date: date = None
        self.exit_eval_days: int = 0
        self.renew_date: date = 0
        # after validation
        self.valid = True

    def __str__(self):
        return f"{self.country.title()} ({self.entry_date.strftime('%m-%d-%Y')} to {self.exit_date.strftime('%m-%d-%Y')})"

    def get_type(self):
        trip_type = 'Schengen' if self.country in SCHENGEN_COUNTRIES else 'Other'
        return trip_type

    def get_duration(self):
        difference_dates = self.exit_date - self.entry_date
        difference_days = difference_dates.days + 1
        return difference_days

    def get_entry_eval_date(self, n_days: int):
        self.entry_eval_date = self.entry_date - timedelta(days=n_days)

    def get_exit_eval_date(self, n_days: int):
        self.exit_eval_date = self.exit_date - timedelta(days=n_days)

    def get_entry_eval_days(self, trips: list):
        # Search for trips that ended before self.entry_date and after self.entry_eval_date
        trips_on_eval_period = [t for t in trips if (t.exit_date < self.entry_date) and (t.exit_date >= self.entry_eval_date)]

        if trips_on_eval_period:
            # Choose date from where to start counting days (what happened last)
            sooner_date = [(t.exit_date, max([t.entry_date, self.entry_eval_date])) for t in trips_on_eval_period]
            # Count days between dates
            days_count = [exit_d - sooner_d for exit_d, sooner_d in sooner_date]
            self.entry_eval_days = sum([dates.days + 1 for dates in days_count])
        else:
            pass

    def get_exit_eval_days(self, trips: list):
        # Search for trips that ended before self.exit_date and after self.exit_eval_date
        trips_on_eval_period = [t for t in trips if (t.exit_date <= self.exit_date) and (t.exit_date >= self.exit_eval_date)]

        if trips_on_eval_period:
            # Choose date from where to start counting days (what happened last)
            sooner_date = ((t.exit_date, max([t.entry_date, self.exit_eval_date])) for t in trips_on_eval_period)
            # Count days between dates
            days_count = (exit_d - sooner_d for exit_d, sooner_d in sooner_date)
            self.exit_eval_days = sum((dates.days + 1 for dates in days_count))
        else:
            pass

    def update_days_count(self):
        self.days_left = 90 - self.exit_eval_days
        self.limit_date = self.exit_date + timedelta(days=self.days_left)
        self.renew_date = self.entry_date + timedelta(days=180)

    def validate(self, value: bool):
        self.valid = value


class TravelHistory:
    def __init__(self):
        self.trips: list = []
        self.last_trip: Trip = None

    def add_trip(self, trip: Trip):
        self.last_trip = trip
        self.trips.append(trip)
        self.trips = sorted(self.trips, key=operator.attrgetter('entry_date'))
        self.validation()

    def validation(self):
        val_functions = {'Schengen': self.schengen_validation}
        if self.last_trip.type == 'Other':
            pass
        else:
            val_functions[self.last_trip.type]()

    def schengen_validation(self):
        # Selection of schengen trips
        schengen_trips = [t for t in self.trips if t.country in SCHENGEN_COUNTRIES]
        for trip in schengen_trips:
            # Evaluation Visa Dates (180 days before each event)
            trip.get_entry_eval_date(180)
            trip.get_exit_eval_date(180)
            # Compare with other Schengen trips
            if len(schengen_trips) > 0:
                # Days in Schengen zone before eval dates
                trip.get_entry_eval_days(schengen_trips)
                trip.get_exit_eval_days(schengen_trips)
                # Other
                trip.update_days_count()
            # Validate trip
            is_valid = (trip.days <= 30) & (trip.days_left >= 0) & (trip.entry_eval_days <= 90) & (trip.exit_eval_days <= 90)
            trip.validate(is_valid)

    def to_df(self) -> pd.DataFrame:
        records_aux = [{
            'type': t.type,
            'country': t.country,
            'entry_date': t.entry_date,
            'exit_date': t.exit_date,
            'days': t.days,
            'limit_date': t.limit_date,
            'days_left': t.days_left,
            'entry_eval_date': t.entry_eval_date,
            'entry_eval_days': t.entry_eval_days,
            'exit_eval_date': t.exit_eval_date,
            'exit_eval_days': t.exit_eval_days,
            'renew_date': t.renew_date,
            'is_valid': t.valid,
        } for t in self.trips]

        return pd.DataFrame.from_records(records_aux)

    def update_trips(self, edited_trips: pd.DataFrame) -> list:
        # Check for differences
        cols_to_compare = ['country', 'entry_date', 'exit_date']
        current_df = self.to_df()[cols_to_compare]
        edited_df = edited_trips.loc[:, edited_trips.columns != 'remove'][cols_to_compare]
        diff_idx = list(current_df.compare(edited_df, result_names=("current", "edited"), keep_equal=True).index)

        changes = []

        # Add edited trips
        for idx in diff_idx:
            new_trip = Trip(edited_trips.iloc[idx]['country'], edited_trips.iloc[idx]['entry_date'], edited_trips.iloc[idx]['exit_date'])
            changes.append((f"{new_trip}", '✏️'))
            self.add_trip(new_trip)

        # Remove selected trips
        for idx in list(edited_trips[edited_trips['remove'] == True].index):
            changes.append((f"{self.trips[idx]}", '🗑️'))
            self.trips.pop(idx)

        # list of changes to print
        return changes


