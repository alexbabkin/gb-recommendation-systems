import numpy as np
import pandas as pd

def prefilter_items(data, item_features, top_n=5000, bottom_n=1000, weeks_ago_to_delete=52, hight_cost=5000, low_cost=60, department_item_count=150):
    df_copy = data.copy()

    # Уберем самые популярные
    popularity = df_copy.groupby('item_id')['quantity'].sum().reset_index()
    top = popularity.sort_values('quantity', ascending=False).head(top_n)['item_id'].tolist()
    df_copy.loc[df_copy['item_id'].isin(top), 'item_id'] = 999999

    # Уберем самые непопулряные
    bottom = popularity.sort_values('quantity').head(bottom_n)['item_id'].tolist()
    df_copy.loc[df_copy['item_id'].isin(bottom), 'item_id'] = 999999

    # Уберем товары, которые не продавались за последние n недель
    items_ago = df_copy.loc[df_copy['week_no'] > weeks_ago_to_delete]['item_id'].tolist()
    df_copy.loc[df_copy['item_id'].isin(items_ago), 'item_id'] = 999999

    # Уберем не интересные для рекоммендаций категории (department)
    department_size = item_features.groupby('department')['item_id'].nunique().sort_values(ascending=False).reset_index()
    departments = department_size[department_size['item_id'] < department_item_count].department.tolist()
    items_in_deparmments = item_features[item_features.department.isin(departments)]['item_id'].unique().tolist()
    df_copy.loc[df_copy['item_id'].isin(items_in_deparmments), 'item_id'] = 999999


    # Уберем слишком дорогие и слишком дешевые
    df_copy['price'] = df_copy['sales_value'] / df_copy['quantity']

    df_copy.loc[df_copy['price'] < low_cost, 'item_id'] = 999999
    df_copy.loc[df_copy['price'] > hight_cost, 'item_id'] = 999999

    df_copy.drop('price', axis=1)

    return df_copy