# recipes/services/planejamento_mt_correntes.py
from io import BytesIO
import pandas as pd

def excel_para_html(uploaded_file, max_rows=1000):
    """
    Lê o Excel enviado e devolve um dict com:
      - tabela_html: HTML da tabela (até max_rows linhas)
      - sheet: aba lida
      - sheet_names: todas as abas
      - rows_total / rows_shown / columns
    """
    xls = pd.ExcelFile(uploaded_file)
    sheet = xls.sheet_names[0]  # primeira aba (ajuste se quiser escolher)
    df = pd.read_excel(xls, sheet_name=sheet)

    rows_total = len(df)
    if rows_total > max_rows:
        df_view = df.head(max_rows)
    else:
        df_view = df

    tabela_html = df_view.to_html(index=False, border=0, classes="tbl")
    return {
        "tabela_html": tabela_html,
        "sheet": sheet,
        "sheet_names": xls.sheet_names,
        "rows_total": rows_total,
        "rows_shown": len(df_view),
        "columns": df.columns.tolist(),
    }
