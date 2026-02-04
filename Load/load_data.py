import pandas as pd
from sqlalchemy.engine import Engine


def load_to_sqlite(df: pd.DataFrame, engine: Engine, table_name: str = "vgsales") -> None:
    df.to_sql(table_name, engine, if_exists="replace", index=False)
