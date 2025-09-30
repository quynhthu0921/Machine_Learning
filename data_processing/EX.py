#Input: df
# Output: Top 3 sản phẩm có giá trị lớn nhất (là sản phẩm bán chạy nhất)

import pandas as pd

def top3_highest_value_products(df):
    # Tính tổng giá trị (doanh thu) theo ProductID
    product_totals = df.groupby('ProductID').apply(
        lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum()
    ).reset_index(name='TotalValue')

    # Lấy 3 sản phẩm có TotalValue cao nhất
    top3 = product_totals.sort_values(by='TotalValue', ascending=False).head(3).reset_index(drop=True)

    return top3

# Ví dụ chạy
df = pd.read_csv("../datasets/SalesTransactions/SalesTransactions.csv")
result = top3_highest_value_products(df)

print("3 sản phẩm có giá trị cao nhất:")
print(result)
