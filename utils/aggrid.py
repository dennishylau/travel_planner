from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, AgGridReturn
import pandas as pd


def build_aggrid(df: pd.DataFrame) -> AgGridReturn:
    builder = GridOptionsBuilder.from_dataframe(df)
    builder.configure_default_column(
        editable=False, suppressMovable=True)
    builder.configure_columns(
        ['name'],
        rowDrag=True, width=100
    )
    builder.configure_columns(
        ['city', 'tag'],
        width=30
    )
    builder.configure_columns(
        ['date'],
        width=40
    )
    builder.configure_columns(
        ['date_order', 'lat', 'long', 'gmaps_link', 'place_id'],
        editable=True, hide=True
    )
    builder.configure_selection(
        selection_mode="multiple",
        use_checkbox=True,
        rowMultiSelectWithClick=True,
    )
    builder.configure_grid_options(
        rowDragManaged=True,
        rowDragEntireRow=True,
        rowDragMultiRow=True,
        suppressMoveWhenRowDragging=True,
    )
    go = builder.build()
    return AgGrid(
        df,
        gridOptions=go,
        fit_columns_on_grid_load=True,
        update_mode=GridUpdateMode.MANUAL,
        height=1000
    )
