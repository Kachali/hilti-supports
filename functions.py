import psycopg2
import pandas as pd

def connection_to_postgress(sys, user):
    specifications = psycopg2.connect(dbname="support_user_database",
                                      host="dpg-civ600diuiedpv0lrnm0-a.oregon-postgres.render.com",
                                      user="support_user_database_user",
                                      password="6giJ3AG6hvMP8DoMyvx1LYooCJA35j2u",
                                      port="5432")
    spec_df = pd.read_sql_query("SELECT * FROM specifications", specifications)
    system_df = spec_df.loc[(spec_df['system'] == sys) & (spec_df['status'] == 'В работе') & (
                spec_df['author_id'] == user.id)].reset_index(drop=True)
    return (len(system_df), system_df)