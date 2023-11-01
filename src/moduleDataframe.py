import sys
import pandas as pd
from io import StringIO

def get_dataframe_info(df):
    original_stdout = sys.stdout
    sys.stdout = StringIO()
    df.info()
    info_output = sys.stdout.getvalue()
    sys.stdout = original_stdout
    if info_output.strip() == '':
        return "Aucune information disponible"
    return info_output

def create_dataframe(content, separator, nrows_value):
    try:
        df = pd.read_csv(StringIO(content), sep=separator, nrows=nrows_value, low_memory=False, encoding='UTF-8')
        return df
    except pd.errors.ParserError as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return None
