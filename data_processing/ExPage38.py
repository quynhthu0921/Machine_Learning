import pandas as pd


def find_orders_within_range(df, minValue, maxValue, SortType=True):
    # Tính tổng giá trị từng hóa đơn
    order_totals = df.groupby('OrderID').apply(
        lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum()
    ).reset_index(name='Sum')

    # Lọc theo khoảng giá trị
    filtered = order_totals[
        (order_totals['Sum'] >= minValue) & (order_totals['Sum'] <= maxValue)
        ]

    # Sắp xếp theo SortType (True = tăng dần, False = giảm dần)
    filtered = filtered.sort_values(by='Sum', ascending=SortType).reset_index(drop=True)

    return filtered


# Ví dụ đọc file csv
df = pd.read_csv("../datasets/SalesTransactions/SalesTransactions.csv")

# Nhập giá trị min max
minValue = float(input("Nhập giá trị min: "))
maxValue = float(input("Nhập giá trị max: "))
SortType = input("Sắp xếp tăng dần? (y/n): ").lower() == "y"

# Chạy hàm
result = find_orders_within_range(df, minValue, maxValue, SortType)

print("Danh sách hóa đơn:")
print(result)
