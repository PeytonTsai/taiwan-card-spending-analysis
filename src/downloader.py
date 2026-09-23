#下載與清洗檔案
import pandas as pd
import numpy as np
import requests
import io

def fetch_clean_data():
    """
    1. 串接 - 自動從政府開放平台下載最新的信用卡消費CSV檔案
    2. 清洗 - 資料型態轉換與計算
    """
    #1.串接下載
    csv_url = "https://www.nccc.com.tw/dataDownload/Billing%20Address/BANK_LCSUM_IDSUM_BA.CSV"
    print("正在串接下載資料...")
    response = requests.get(csv_url)
    if response.status_code !=200:
        raise Exception(f"無法下載，錯誤碼:{response.status_code}")
    #2.資料轉換
    #指定utf-8-sig避免亂碼，自動偵測並剔除開頭的BOM標籤
    df_raw=pd.read_csv(io.StringIO(response.content.decode("utf-8-sig")))
    print("開始資料清洗與計算...")

    #建立一份檔案來清洗資料
    df_cleaned=df_raw.copy()
    amt_col="信用卡交易金額[新臺幣]"
    cnt_col="信用卡交易筆數"

    #將資料轉為數字，非數字轉為NaN，把NaN補0後轉為整數
    df_cleaned[amt_col]=pd.to_numeric(df_cleaned[amt_col],errors="coerce").fillna(0).astype("Int64")
    df_cleaned[cnt_col]=pd.to_numeric(df_cleaned[cnt_col],errors="coerce").fillna(0).astype("Int64")

    #客單價計算（平均每筆消費金額）
    #如果筆數 > 0 則計算金額/筆數並四捨五入到2位，否則為 0
    df_cleaned["客單價"] = np.where(
        df_cleaned[cnt_col] > 0,
        (df_cleaned[amt_col] / df_cleaned[cnt_col]).round(2),
        0.0
    )

    #時間拆為年分與月份表示
    df_cleaned["年份"]=df_cleaned["年月"].astype(str).str[:4].astype(int)
    df_cleaned["月份"]=df_cleaned["年月"].astype(str).str[4:].astype(int)

    #地區代碼對照中文名稱
    location_map ={
        '63000000': '臺北市', '64000000': '高雄市', '65000000': '新北市', 
        '66000000': '臺中市', '67000000': '臺南市', '68000000': '桃園市', 
        '10002000': '宜蘭縣', '10004000': '新竹縣', '10005000': '苗栗縣', 
        '10007000': '彰化縣', '10008000': '南投縣', '10009000': '雲林縣', 
        '10010000': '嘉義縣', '10020000': '嘉義市', '10013000': '屏東縣', 
        '10014000': '臺東縣', '10015000': '花蓮縣', '10016000': '澎湖縣', 
        '10017000': '基隆市', '10018000': '新竹市', '09020000': '金門縣', 
        '09007000': '連江縣'
    }
    df_cleaned["地區"]=df_cleaned["地區"].astype(str).str.zfill(8)
    df_cleaned["縣市"]=df_cleaned["地區"].map(location_map).fillna("未知地區")

    print(f"完成處理 {len(df_cleaned)} 筆消費數據")
    return df_cleaned


#%%查看資料
if __name__ == "__main__":
    df = fetch_clean_data()
    # 查看清洗後的資料前 5 筆
    print(df[["年份", "月份", "縣市", "客單價"]].head())