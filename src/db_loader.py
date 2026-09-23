import os
import sqlite3
import pandas as pd

def init_db_load(df_cleaned, db_path="data/spending.db"):
    """
    1. 自動建立sqlite3
    2. 對齊欄位名稱，寫入資料
    """
    print(f"正在初始化資料庫:{db_path}")

    # 確保資料夾存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    #建立連線
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #啟用外鍵約束
    cursor.execute("PRAGMA foreign_keys = ON;")

    #跨行編寫建立資料表
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Dim_Time(
            time_key INTEGER PRIMARY KEY,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Dim_Location(
            location_id TEXT PRIMARY KEY,
            city_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Dim_Industry(
            industry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            industry_name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS Fact_Consumption(
        fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
        time_key INTEGER NOT NULL,
        location_id TEXT,
        industry_id INTEGER,
        transaction_count INTEGER NOT NULL,
        transaction_amount INTEGER NOT NULL,
        avg_ticket_value REAL,
        /* 
        [外鍵關聯說明]
        - time_key: 參考 Dim_Time(time_key)，綁定年月時間資訊
        - location_id: 參考 Dim_Location(location_id)，綁定消費縣市名稱
        - industry_id: 參考 Dim_Industry(industry_id)，綁定消費產業類別
        */
        FOREIGN KEY (time_key) REFERENCES Dim_Time(time_key),
        FOREIGN KEY (location_id) REFERENCES Dim_Location(location_id),
        FOREIGN KEY (industry_id) REFERENCES Dim_Industry(industry_id)
        );
    """)
    conn.commit()
    print("正在生成並寫入資料...")

    #寫入時間資料
    time_df=df_cleaned[["年月","年份","月份"]].drop_duplicates()
    time_df.columns=["time_key","year","month"]

    #逐條寫入
    for _, row in time_df.iterrows():
        cursor.execute(
            """
            /* 將時間資料逐筆寫入 Dim_Time 表，若 time_key 重複則忽略 */
            INSERT OR IGNORE INTO Dim_Time (time_key,year,month) VALUES (?,?,?)
            """,
            (int(row["time_key"]),int(row["year"]),int(row["month"]))
        )

    #寫入地區資料
    locations_df = df_cleaned[["地區","縣市"]].drop_duplicates()
    for _, row in locations_df.iterrows():
        cursor.execute(
            """
            INSERT OR IGNORE INTO  Dim_Location (location_id,city_name) VALUES(?,?)
            """,
            (str(row["地區"]),str(row["縣市"]))
        )

    #寫入產業別資料，取得不重複的值-->.unique()
    industries = df_cleaned["信用卡產業別"].unique()
    for ind in industries :
        cursor.execute(
            """
            INSERT OR IGNORE INTO Dim_Industry (industry_name) VALUES(?)
            """,
            (str(ind).strip(),) #防呆去頭尾空白.strip()
        )

    conn.commit()

    print("正在處理與寫入表格...")

    industry_table=pd.read_sql("SELECT industry_id, industry_name FROM Dim_Industry",conn)

    df_fact= df_cleaned.merge(industry_table,left_on="信用卡產業別",right_on="industry_name",how="left")
    df_fact_final=df_fact[["年月","地區","industry_id","信用卡交易筆數","信用卡交易金額[新臺幣]","客單價"]]
    df_fact_final.columns=["time_key","location_id","industry_id","transaction_count","transaction_amount","avg_ticket_value"]

    # 批次寫入事實表 Fact_Consumption
    df_fact_final.to_sql("Fact_Consumption", conn, if_exists="append", index=False)
    conn.commit()

    # 關閉資料庫連線
    conn.close()
    print("-> 所有數據成功寫入 SQLite 資料庫！")

    