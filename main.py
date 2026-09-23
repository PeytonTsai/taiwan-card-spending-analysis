import os
from src.downloader import fetch_clean_data
from src.db_loader import init_db_load

def main():
    #如果沒有data資料夾，自動建立
    os.makedirs("data",exist_ok=True)

    try:
        #執行下載跟檔案清洗
        df_cleaned=fetch_clean_data()

        #寫入sqlite資料庫(生成data/spending.db)
        init_db_load(df_cleaned,db_path="data/spending.db")

        print("\n ---後端流程全部完成")
        print("可以開始執行Tableau連接")

    except Exception as e:
        print(f"執行過程錯誤: {e}")

if __name__=="__main__":
    main()
