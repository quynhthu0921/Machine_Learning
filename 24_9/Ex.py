import sqlite3
import pandas as pd

DB_PATH = '../databases/Chinook_Sqlite.sqlite'

def top_n_customers_by_value(n: int, method: str = "invoice_total") -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if method == "invoice_total":
        query = """
        SELECT
            c.CustomerId,
            ROUND(SUM(i.Total), 2) AS TotalValue
        FROM Customer c
        JOIN Invoice i ON i.CustomerId = c.CustomerId
        GROUP BY c.CustomerId
        ORDER BY TotalValue DESC, c.CustomerId
        LIMIT ?
        """
        cur.execute(query, (n,))
    else:
        query = """
        SELECT
            c.CustomerId,
            ROUND(SUM(il.UnitPrice * il.Quantity), 2) AS TotalValue
        FROM Customer c
        JOIN Invoice i ON i.CustomerId = c.CustomerId
        JOIN InvoiceLine il ON il.InvoiceId = i.InvoiceId
        GROUP BY c.CustomerId
        ORDER BY TotalValue DESC, c.CustomerId
        LIMIT ?
        """
        cur.execute(query, (n,))

    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    df = pd.DataFrame(rows, columns=cols)

    conn.close()
    return df

if __name__ == "__main__":
    N = int(input("Nhập top n mà bạn muốn: "))
    print(f"Top {N} khách hàng theo tổng giá trị (dùng Invoice.Total):")
    df_top = top_n_customers_by_value(N, method="invoice_total")
    print(df_top)

