# my-todo

簡單的命令列待辦事項工具，以 Python 3 標準庫實作，資料存於單一 JSON 檔案。

## 需求

- Python 3.10 以上
- 無需安裝任何外部套件

## 快速開始

```bash
git clone <此專案>
cd my-todo
python todo.py --help
```

## 指令說明

### 新增任務

```bash
python todo.py add 買牛奶
python todo.py add "今天要完成的報告"
```

### 列出所有任務

```bash
python todo.py list
```

輸出範例：

```
  任務清單  （1/3 已完成）
  ────────────────────────────────────
  ✓    1.  買牛奶
  ○    2.  今天要完成的報告
  ○    3.  繳電費
```

### 標記任務為完成

```bash
python todo.py done 2
```

### 刪除任務

```bash
python todo.py delete 3
```

### 查看子指令說明

```bash
python todo.py --help
python todo.py add --help
```

## 資料儲存

任務存於同目錄下的 `todos.json`，格式如下：

```json
[
  { "id": 1, "title": "買牛奶", "done": true },
  { "id": 2, "title": "今天要完成的報告", "done": false }
]
```

可直接編輯此檔案，或將其加入版本控制。

## 檔案結構

```
my-todo/
├── todo.py      # 主程式
├── todos.json   # 資料檔（執行後自動建立）
└── README.md
```
