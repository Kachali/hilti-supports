import psycopg2
import pandas as pd
import os

def connection_to_postgress(sys, user):
    specifications = psycopg2.connect(dbname="support_user_database", host=os.environ.get('DB_HOST'), user="support_user_database_user", password=os.environ.get('DB_PASSWORD'), port="5432")
    spec_df = pd.read_sql_query("SELECT * FROM specifications", specifications)
    system_df = spec_df.loc[(spec_df['system'] == sys) & (spec_df['status'] == 'В работе') &
                            (spec_df['author_id'] == user.id)].reset_index(drop=True)
    return (system_df)




