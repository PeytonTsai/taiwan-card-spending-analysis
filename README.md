# 台灣信用卡消費數據分析 (Taiwan Card Spending Analysis)

本專案旨在透過 Python 自動化擷取台灣信用卡消費相關開放資料，進行清洗、結構化處理並儲存至 SQLite 資料庫與 CSV 檔案中，最後透過 Tableau 視覺化儀表板呈現台灣消費趨勢與區域分佈分析。

---

## 🛠️ 技術堆棧 (Tech Stack)

* **數據處理與 ETL**：Python (`pandas`, `requests`, `sqlite3`)
* **資料庫管理**：SQLite
* **數據視覺化 (BI)**：Tableau Desktop / Public Edition
* **版本控制**：Git & GitHub

---

## 📊 分析儀表板預覽 (Dashboard Screenshots)

以下為專案之 Tableau 視覺化報表截圖：

### 1. 全台消費市場總覽 (Executive Overview)
![主頁(Home Dashboard)](img/螢幕擷取畫面%202026-09-23%20103357.png)
* **核心功能**：即時監控全台總交易金額、筆數與客單價 MoM 成長率。
* **視覺亮點**：地圖與淡旺季時間軸趨勢連動。

### 2. 產業與區域交叉矩陣分析 (Industry Analysis)
![分析(Analysis Dashboard)](img/螢幕擷取畫面%202026-09-23%20103808.png)
* **核心功能**：透過四象限散佈圖區分「高單價/低頻率」與「低單價/高頻率」產業特性。

### 3. 區域深入探索與動態下潛 (Regional Drill-down)
![區域(Location Dashboard)](img/螢幕擷取畫面%202026-09-23%20103913.png)
* **核心功能**：點擊地圖任意縣市，右側 Top 5 產業與下方時間軸動態切換為該縣市數據。

---

## 💡 關鍵商業洞察 (Key Business Insights)

1. **季節性消費爆發點**：全台消費高度集中於年末（12月）及暑期（5~7月），呈現明顯的節慶與假期效應。
2. **區域消費結構差異**：四象限矩陣顯示雙北地區以高頻率日常消費為主，竹苗區域則呈現較高之客單價表現。
3. **縣市 Top 5 產業下潛**：透過動態 Set 過濾，「百貨」與「文教康樂」類別普遍佔據多數縣市前三大消費來源。

---

## 🚀 快速開始 (Quick Start)

### 1. 複製專案庫 (Clone Repository)
```bash
git clone https://github.com/PeytonTsai/taiwan-card-spending-analysis.git
cd taiwan-card-spending-analysis
```

### 2. 執行 ETL 流程 (Run Pipeline)
```bash
python main.py
```
(執行完成後數據將自動下載、清洗並更新至 data/spending_export.csv 與 SQLite 資料庫中)

## 🛠️ 專案架構與檔案說明 (Project Structure)
```bash
taiwan-card-spending-analysis/
│
├── data/
│   └── spending_export.csv    # 導出的消費處理資料集
│
├── src/
│   ├── downloader.py          # 開放資料自動化下載模組
│   ├── db_loader.py           # 資料清洗與寫入 SQLite 模組
│   ├── check_db.py            # 資料庫驗證與查詢工具
│   └── export.py              # 資料匯出處理模組
│
├── img/                       # tableau 視覺化報表截圖資料夾
├── main.py                    # 專案主執行程式
├── README.md                  # 專案說明文件
└── .gitignore                 # Git 版本控制忽略設定
```
