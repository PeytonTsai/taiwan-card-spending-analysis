import sqlite3
import pandas as pd

#抓取資料庫
db_path = "data/spending.db"

#建立連線
conn = sqlite3.connect(db_path)

print("檢查資料表是否成功寫入")
tables = ["Dim_Time","Dim_Location","Dim_Industry","Fact_Consumption"]

for table in tables:
    count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table}", conn).iloc[0]['cnt']
    print(f"{table.ljust(10)}:{count:6d} 筆數據")

print("測試跨表關聯join查詢模擬tableau讀取")

#測試sql關聯是否正常
test_query="""
SELECT
    t.year || '年' || t.month || '月' AS 消費年月,
    l.city_name AS 縣市名稱,
    i.industry_name AS 產業類別,
    f.transaction_count AS 交易筆數,
    f.transaction_amount AS 交易金額,
    f.avg_ticket_value AS 客單價
FROM Fact_Consumption f
JOIN Dim_Time t ON f.time_key = t.time_key
JOIN Dim_location l ON f.location_id = l.location_id
JOIN Dim_Industry i ON f.industry_id = i.industry_id
LIMIT 10;
"""
df_preview = pd.read_sql(test_query, conn)
print(df_preview.to_string(index=False))
conn.close()
print("\n資料庫檢查完成")