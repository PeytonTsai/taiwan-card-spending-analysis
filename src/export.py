import sqlite3
import pandas as pd

#連接資料庫
conn = sqlite3.connect("data/spending.db")

#匯出整理好的資料
query = """
SELECT 
    t.year || '年' || t.month || '月' AS 消費年月,
    l.city_name AS 縣市名稱,
    i.industry_name AS 產業類別,
    f.transaction_count AS 交易筆數,
    f.transaction_amount AS 交易金額,
    f.avg_ticket_value AS 客單價
FROM Fact_Consumption f
JOIN Dim_Time t ON f.time_key = t.time_key
JOIN Dim_Location l ON f.location_id = l.location_id
JOIN Dim_Industry i ON f.industry_id = i.industry_id; 
"""

df=pd.read_sql(query,conn)
df.to_csv("data/spending_export.csv",index=False,encoding="utf-8-sig")
conn.close()
print("資料已匯出至 data/spending_export.csv")