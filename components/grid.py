import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd


def render_grid(
    df: pd.DataFrame,
    key: str,
    title: str = None,
    page_size: int = 10,
):
    if title:
        st.subheader(title)

    # 🔎 Busca global
    search = st.text_input("🔎 Busca global", key=f"{key}_search")
    if search:
        df = df[
            df.astype(str)
            .apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
        ]

    # 👁️ Colunas visíveis
    visible_columns = st.multiselect(
        "Colunas visíveis",
        df.columns.tolist(),
        default=df.columns.tolist(),
        key=f"{key}_columns"
    )
    df = df[visible_columns]

    # 🧹 Limpar filtros
    if st.button("🧹 Limpar filtros", key=f"{key}_clear"):
        st.rerun()

    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_grid_options(
        domLayout="autoHeight",
        defaultColDef={
            "filter": True,
            "floatingFilter": True,
            "sortable": True,
            "resizable": True,
        },
        pagination=True,
        paginationPageSize=page_size,
        paginationPageSizeSelector=[5, 10, 20, 50, 100],
        rowSelection="multiple",
        localeText={
            # Paginação
            "page": "Página",
            "to": "até",
            "of": "de",
            "next": "Próximo",
            "last": "Último",
            "first": "Primeiro",
            "previous": "Anterior",

            # Grid
            "loadingOoo": "Carregando...",
            "noRowsToShow": "Nenhum registro encontrado",

            # Filtros
            "filterOoo": "Filtrar...",
            "equals": "Igual",
            "notEqual": "Diferente",
            "lessThan": "Menor que",
            "greaterThan": "Maior que",
            "contains": "Contém",
            "notContains": "Não contém",
            "startsWith": "Começa com",
            "endsWith": "Termina com",
            "inRange": "Entre",
            "applyFilter": "Aplicar",
            "clearFilter": "Limpar",

            # Colunas
            "columns": "Colunas",
            "selectAll": "Selecionar tudo",
            "searchOoo": "Pesquisar...",

            # Outros
            "blank": "Vazio",
            "notBlank": "Não vazio",
        },
    )

    grid = AgGrid(
        df,
        gridOptions=gb.build(),
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        enable_enterprise_modules=False,
        key=key,
        reload_data=True,
    )

    # 📤 Exportação FREE
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Exportar CSV",
        csv,
        f"{key}.csv",
        "text/csv",
        key=f"{key}_export"
    )

    return grid
