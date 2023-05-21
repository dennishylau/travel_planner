import pandas as pd


def update_date_order(df: pd.DataFrame, travel_dates: list[str]) -> bool:
    '''
    Update date order if needed, and return True if actually updated
    '''
    updated = False
    for date in travel_dates:
        num_rows = df.loc[df.date == date].shape[0]
        predicate = (
            df.date == date) & (
            df.tag.isin(['Backlog'])
        )
        if num_rows > 0:
            order = list(range(1, num_rows + 1))
            order_changed = df.loc[predicate].date_order.tolist() != order
            if order_changed:
                df.loc[predicate, ['date_order']] = order
                updated = True
    df.sort_values(by=['date', 'date_order'], na_position='last', inplace=True)
    return updated
