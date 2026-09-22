# 🛠️ 工具 TA Python 訓練計畫(八週)—— 詳細版

針對工具 / 管線 Technical Artist 的實際工作與面試設計。每天 30–45 分鐘,與作品集和投遞並行,不是前置條件。

🧭 **設計依據:** 四年實務經驗已經有,缺的是三樣——(1)資料在函式之間怎麼流的習慣、(2)沒有被別人 review 過的程式碼、(3)學的是工作需要什麼而不是系統性補弱點。這份計畫只針對這三樣,不練其他。

---

## ⏱️ 零、每天的流程(每次都照這個走)

| 分鐘 | 做什麼 |
|---|---|
| 0–5 | 讀題。**不開編輯器。** 在紙上或純文字檔寫下:輸入是什麼、輸出長什麼樣、中間要幾步、每步吃什麼吐什麼 |
| 5–10 | 開編輯器,**只寫函式簽名和 docstring**,不寫內容。每個函式一行說明:進什麼、出什麼 |
| 10–35 | 填內容。卡住超過 15 分鐘才查文件。查完在筆記寫一句「我當時不知道的是 ___」 |
| 35–40 | 用題目附的測試資料跑。然後問三個問題:空輸入會怎樣?路徑不存在會怎樣?資料乘十會怎樣?能修就修,不能修就寫下來 |
| 40–45 | 存檔,檔名加日期(`day01_texture_check.py`)。**不覆蓋舊版本。** |

📏 **規則:**

1. 練習時段不開 AI。工作上照用,這半小時不用。
2. 先簽名、再內容。這一條專門治「中間空白」。
3. 卡住 15 分鐘再查。不到 15 分鐘就查,練不到拆解。
4. 每週日把這週的程式碼發給一位工程師,問一句「哪裡寫得怪」。不用他細改。
5. 「我當時不知道的是 ___」這份清單,第八週要用。

---

## 🧱 一、第 1–2 週:資料流與核心語法

### 📚 這兩週會用到的東西(全部在標準庫,不用裝任何套件)

| 東西 | 用來做什麼 | 什麼時候查 |
|---|---|---|
| `pathlib.Path` | 列資料夾、拆路徑、判斷存在 | 第 1 天 |
| `Path.iterdir()` / `.glob()` / `.rglob()` | 列一層 / 按模式列 / 遞迴列 | 第 1、3 天 |
| `Path.stem` / `.suffix` / `.name` / `.parent` | 檔名不含副檔名 / 副檔名 / 完整檔名 / 上層目錄 | 第 1 天 |
| `str.rsplit(sep, maxsplit)` | 從右邊切,只切 N 次 | 第 1 天 |
| `str.endswith()` / `.startswith()` / `.lower()` | 比對結尾 / 開頭 / 轉小寫 | 第 1、2 天 |
| `dict` 當分組容器 | key 是資產名,value 是它有的類型 | 第 1 天 |
| `set` 差集 `a - b` | 「應該有的」減「實際有的」= 缺的 | 第 1、7 天 |
| `collections.defaultdict(list)` | 分組時不用先檢查 key 存不存在 | 第 1、8 天 |
| `collections.Counter` | 數東西出現幾次 | 第 6 天 |
| `json.load()` / `json.dump(obj, f, indent=2, ensure_ascii=False)` | 讀寫設定與報告 | 第 3、9 天 |
| `hashlib.md5()` / `.sha256()` | 算檔案內容的指紋 | 第 4 天 |
| `csv.DictReader` | 讀 CSV,每行變 dict | 第 8 天 |
| `argparse` | 命令列參數 | 第 10 天 |
| `logging` | 取代 print,分等級、可寫檔 | 第 10 天 |

不用先背。到那一天再查那一行。

---

### 📌 第 1 天:貼圖完整性檢查

🎯 **目標:** 建立「篩選 → 解析 → 分組 → 比對 → 報告」這條資料流。這是整份計畫的地基。

🧪 **測試資料(自己建這些空檔案):**
```
Crate_BaseColor.png    Crate_Normal.png      Crate_Roughness.png   Crate_Metallic.png
Barrel_BaseColor.png   Barrel_normal.png     Barrel_Roughness.png
Pipe_BaseColor.png     Pipe_Normal.png       Pipe_Roughness.png    Pipe_Metallic.png   Pipe_AO.png
readme.txt
Wall_Section_A_BaseColor.png
```

📥 **輸入:** 一個資料夾路徑
📤 **輸出:** 印出(1)每個資產有哪些、缺哪些;(2)不合規的檔名清單

🧩 **拆解(先寫這五步的簽名,再寫內容):**

1. `列出所有檔案(資料夾) -> list[Path]`
2. `解析檔名(一個檔名) -> (資產名, 類型) 或 None` —— None 代表不合規
3. `分組(解析結果的清單) -> dict[資產名, set[類型]]`
4. `找缺的(某資產有的類型, 必要類型) -> set[類型]`
5. `印報告(分組結果, 不合規清單)`

⚠️ **四個陷阱(先自己找,找不到再看下面):**

- `readme.txt` —— 副檔名不是 `.png`
- `Pipe_AO.png` —— `AO` 不在四種類型裡
- `Barrel_normal.png` —— 小寫 `n`。你要決定:算錯,還是算對但要修?先算錯,第 2 天處理
- `Wall_Section_A_BaseColor.png` —— **資產名含底線。** `split('_')` 會切成四段,壞掉。解法有兩條:(a)`rsplit('_', 1)` 只切最後一個底線;(b)不切,拿四種類型一個一個 `endswith('_BaseColor.png')` 比,中了就把後綴砍掉。兩條都對,選一條

✅ **完成標準:**
- Crate 完整、Barrel 缺 Normal 和 Metallic(因為 `normal` 小寫被判不合規)、Pipe 完整、Wall_Section_A 缺三個
- 不合規清單:`readme.txt`、`Pipe_AO.png`、`Barrel_normal.png`
- 資料夾不存在時不會 crash,會印一句清楚的錯誤

❌ **常見錯誤:** 把解析和分組寫在同一個迴圈裡。可以動,但第 9 天要換設定檔的時候你會發現拆不開。現在就拆。

---

### 📌 第 2 天:命名規範驗證器 + `--fix`

🎯 **目標:** 學「預覽再執行」這個模式。任何會改檔案的工具都要有它。

📥 **輸入:** 資料夾路徑、`--fix` 旗標(有就真的改,沒有就只印出會改什麼)
📤 **輸出:** 列出每個要改的檔名,舊 → 新。有 `--fix` 才真的改

🧩 **拆解:**
1. 沿用第 1 天的解析函式
2. `建議修正(壞檔名) -> 新檔名 或 None` —— 只修大小寫;`Pipe_AO.png` 修不了,回 None
3. `執行改名(舊, 新, dry_run: bool)` —— dry_run 為真只印不做

🔍 **邊界情況:** 修正後的檔名已經存在怎麼辦?(例如同時有 `Barrel_normal.png` 和 `Barrel_Normal.png`)—— 不能覆蓋,要跳過並報告。這一條一定要處理。

✅ **完成標準:** 沒加 `--fix` 跑一次,資料夾一個檔案都沒變。加了再跑,`Barrel_normal.png` 變 `Barrel_Normal.png`。

---

### 📌 第 3 天:資料夾樹 → JSON manifest

🎯 **目標:** 遞迴遍歷、巢狀資料結構、寫 JSON。

📥 **輸入:** 根目錄
📤 **輸出:** 一個 `manifest.json`,每個檔案一筆:相對路徑、大小(bytes)、副檔名、最後修改時間

🧩 **拆解:**
1. `遞迴列出所有檔案(根) -> list[Path]` —— 用 `rglob('*')`,過濾掉資料夾
2. `一個檔案 -> 一筆記錄(dict)`
3. `所有記錄 -> 寫 JSON`

🔍 **邊界情況:** 路徑要用**相對路徑**存,不然 manifest 換台電腦就沒用。`Path.relative_to(根)`。

✅ **完成標準:** 用你 O'Neill cylinder 專案的 Content 資料夾跑一次,JSON 能被 `json.load` 讀回來。

---

### 📌 第 4 天:找重複檔案

🎯 **目標:** 用內容當 key 分組,不是用名字。

📥 **輸入:** 資料夾
📤 **輸出:** 每組重複的檔案列在一起

🧩 **拆解:**
1. `算指紋(檔案) -> str` —— 讀檔案內容進 hashlib,回 hexdigest。**大檔案要分塊讀**,不要一次 `read()`
2. `分組(所有檔案) -> dict[指紋, list[Path]]`
3. 只印 value 長度 > 1 的組

🔍 **邊界情況:** 空檔案的指紋都一樣,要不要算重複?你決定,但要有意識地決定。

✅ **完成標準:** 複製幾個檔案改名放進去,能抓到。

---

### 📌 第 5 天:批次改名

🎯 **目標:** 字串處理 + dry-run 再一次(這個模式要練到反射)。

📥 **輸入:** 資料夾、以下三選一:`--prefix X`、`--suffix X`、`--replace 舊 新`;加 `--fix`
📤 **輸出:** 舊 → 新清單

🔍 **邊界情況:** 副檔名不能被動到(`--suffix _v2` 要變 `Crate_v2.png`,不是 `Crate.png_v2`)。用 `Path.stem` 和 `Path.suffix` 分開處理。改名後衝突同第 2 天。

---

### 📌 第 6 天:log 錯誤統計

🎯 **目標:** `Counter`、排序、讀文字檔。

🧪 **測試資料(自己寫一個 `build.log`,二三十行):**
```
[INFO] Loading asset Crate
[ERROR] MissingTexture: Crate_Metallic.png not found
[WARN] LOD count below recommended for Barrel
[ERROR] MissingTexture: Pipe_AO.png not found
[ERROR] InvalidName: Barrel_normal.png
...
```

📤 **輸出:** 每種錯誤類型出現幾次,依次數由多到少

🧩 **拆解:**
1. `逐行讀`
2. `一行 -> 錯誤類型 或 None` —— 只看 `[ERROR]` 行,類型是冒號前那個詞
3. `Counter` 數,`.most_common()` 排

---

### 📌 第 7 天:兩個清單比對

🎯 **目標:** `set` 運算解決「什麼變了」。

📥 **輸入:** 兩個 JSON manifest(用第 3 天的工具產生,中間改幾個檔案)
📤 **輸出:** 新增的、刪除的、改過的(路徑相同但大小或時間不同)

🧩 **拆解:**
1. 兩個 manifest 各轉成 `dict[相對路徑, 記錄]`
2. `新增 = 新的 keys - 舊的 keys`;`刪除 = 舊 - 新`;`共同 = 舊 & 新`
3. 共同的裡面逐一比大小和時間

---

### 📌 第 8 天:CSV 分組摘要

📥 **輸入:** 一個 `assets.csv`(自己編,欄位:name, category, size_bytes, lod_count)
📤 **輸出:** 每個 category 有幾個資產、總大小、平均 LOD 數

🧩 **拆解:** `csv.DictReader` → `defaultdict(list)` 按 category 收 → 每組算數字

🔍 **邊界情況:** `size_bytes` 讀進來是字串,要轉 `int`。有一行是空的或壞的怎麼辦?跳過並記下行號。

---

### 📌 第 9 天:設定驅動

🎯 **目標:** 把寫死的東西搬出程式碼。

把第 1 天的工具改成:必要貼圖類型從 `config.json` 讀。

```json
{
  "required_types": ["BaseColor", "Normal", "Roughness", "Metallic"],
  "extension": ".png",
  "case_sensitive": false
}
```

✅ **完成標準:** 改 JSON 不改程式碼,能讓 `AO` 變成合規類型。`case_sensitive` 切成 false 的時候 `Barrel_normal.png` 變合規。

**這一天你會知道第 1 天有沒有拆對。** 拆對了改幾行就好,拆錯了要重寫一半。

---

### 📌 第 10 天:從腳本到工具

把第 1 天的工具**第三次重寫**,這次要求:

- `argparse`:`資料夾` 為必要位置參數,`--config` 預設 `config.json`,`--json-out` 可選,有的話輸出 JSON 而不是印
- `logging` 取代所有 `print`:報告用 `INFO`,不合規檔名用 `WARNING`,資料夾不存在用 `ERROR`
- `except` 只抓具體例外(`FileNotFoundError`、`json.JSONDecodeError`),不寫 `except Exception`
- 所有函式有型別提示

**做完把第 1、9、10 天的三個版本並排開。** 看三件事:函式數量變了沒、每個函式的長度、哪些東西從程式碼搬到設定檔了。寫三句話總結。**這三句話就是面試時「你怎麼成長的」的答案。**

---

## 🏗️ 二、第 3–4 週:工具的設計習慣

### 📚 這兩週會用到的東西

| 東西 | 用來做什麼 |
|---|---|
| `argparse` 子命令(`add_subparsers`) | 一個工具多個動作:`tool export`、`tool validate` |
| `logging.FileHandler` | log 寫進檔案 |
| `dataclasses.dataclass` | 定義「一筆資產記錄」長什麼樣,取代散的 dict |
| 型別提示 `list[str]`、`dict[str, Path]`、`Optional[X]` | 讓簽名自己說明輸入輸出 |
| `subprocess.run([...], capture_output=True, text=True, check=False)` | 呼叫 Blender / UE 命令列,抓輸出,看 return code |
| `if __name__ == "__main__":` | 讓檔案既能直接跑,也能被 import |

### 🎯 唯一任務:從記憶重建 Varadise 的 Blender → UE 匯出工具

🙈 **不看舊程式碼。** 這是重點。

📆 **每天的分配:**

| 天 | 做什麼 |
|---|---|
| 11 | 只寫規格。一頁純文字:這個工具吃什麼、吐什麼、有哪幾個步驤、每步失敗了會怎樣。**不寫程式** |
| 12 | 定義資料結構。用 `dataclass` 寫出「一個要匯出的資產」有哪些欄位。寫 `config.json` 的範例 |
| 13–14 | 寫核心邏輯。一個 `core.py`,裡面全是函式,**沒有 argparse、沒有 print**,只回傳結果和拋例外 |
| 15 | 寫 `cli.py`,只負責解參數、呼叫 core、把結果印出來或寫 log |
| 16 | 加 `--dry-run`、加 logging 寫檔、把所有 `print` 清掉 |
| 17 | 冪等測試:連跑三次,結果要一樣。壞輸入測試:給它一個不存在的路徑、一個壞的 JSON、一個沒有選取物件的場景 |
| 18 | 寫 README。結構:這是什麼 / 怎麼裝 / 怎麼跑(三個範例指令)/ 設定檔每個欄位的意思 / 常見錯誤 |
| 19 | **現在才打開舊程式碼。** 並排比,寫下:(a)當年哪三處寫得糟、(b)現在哪三處寫得好、(c)有沒有當年反而更合理的地方 |
| 20 | 把第 19 天的比較整理成一頁。這一頁直接進作品集 |

☑️ **勾選清單(第 20 天全部要打勾):**

- [ ] 核心邏輯和 CLI 分開:`from core import export_assets` 能在別的腳本裡用
- [ ] 所有路徑、參數從 JSON 讀,程式碼裡搜不到寫死的路徑
- [ ] `--dry-run` 跑完,磁碟上一個檔案都沒變
- [ ] 連跑三次結果相同
- [ ] 壞輸入會報清楚是哪一筆、為什麼,不會默默跳過
- [ ] log 寫到檔案
- [ ] README 給一個沒見過你的人,他能跑起來(真的找一個人試)

---

## 🎮 三、第 5–6 週:引擎整合

### 🎮 第 5 週(第 21–25 天):UE5 專案健檢工具

📚 **要查的 API(到那天再查,不用先背):**

| 東西 | 用來做什麼 |
|---|---|
| `unreal.AssetRegistryHelpers.get_asset_registry()` | 拿到資產登錄表 |
| `asset_registry.get_assets_by_path(path, recursive=True)` | 列某路徑下所有資產 |
| `unreal.EditorAssetLibrary.load_asset(path)` | 載入一個資產 |
| `unreal.EditorAssetLibrary.rename_asset(old, new)` | 改名 |
| `StaticMesh.get_num_lods()` 或 `get_editor_property('lod_count')` | 看 LOD 數 |
| `Texture2D.blueprint_get_size_x()` / `_y()` | 看貼圖尺寸 |
| Editor Utility Widget 的 `Execute Python Script` 節點 | 從 UI 觸發 Python |

📆 **每天:**

| 天 | 做什麼 |
|---|---|
| 21 | 規格 + 資料結構。健檢報告的一筆長什麼樣(資產路徑、問題類型、嚴重度、建議修法)。用 `dataclass` |
| 22 | 寫「列出所有靜態網格,回報 LOD 數 < 2 的」 |
| 23 | 寫「列出所有貼圖,回報尺寸不是 2 的次方的」(`n & (n-1) == 0` 這個判斷值得查一下為什麼) |
| 24 | 寫「命名檢查」——沿用第 1–2 週的解析邏輯,規範從 JSON 讀。加 `--fix` 修命名 |
| 25 | 做一個最小的 Editor Utility Widget,一個按鈕觸發健檢、結果印到 Output Log。加 README |

✅ **完成標準:** 在 O'Neill cylinder 專案上跑,報告裡至少要抓到一個真問題。修掉它。

### 🧊 第 6 週(第 26–30 天):Blender 設定驅動批次匯出

📚 **要查的 API:**

| 東西 | 用來做什麼 |
|---|---|
| `bpy.context.selected_objects` | 選取的物件 |
| `obj.name` / `obj.type` / `obj.dimensions` | 物件屬性 |
| `bpy.ops.export_scene.fbx(filepath=..., use_selection=True, ...)` | 匯出 FBX,參數很多,查文件 |
| `bpy.ops.object.select_all(action='DESELECT')` + `obj.select_set(True)` | 一個一個選來匯 |
| `bpy.types.Operator` | 把腳本包成 Blender 裡的按鈕 |

📆 **每天:**

| 天 | 做什麼 |
|---|---|
| 26 | 規格。`export_config.json` 長什麼樣:全域預設(比例、軸向)+ 每個物件可覆寫 |
| 27 | 寫「對每個選取物件,單獨匯出一個 FBX,檔名 = 物件名」 |
| 28 | 加設定檔:每個物件從 JSON 找自己的設定,找不到用預設 |
| 29 | 匯出後產生 `manifest.json`:每個匯出的檔案、來源物件、用了什麼設定、尺寸。**格式要跟第 5 週的健檢工具吃得進去** |
| 30 | 包成 Operator,Blender 裡 F3 搜得到。README |

✅ **完成標準:** Blender 匯出 → manifest → UE 端讀 manifest 做健檢,一條線通。這條線就是作品集的核心敘事。

---

## 🔁 四、第 7–8 週:回饋與輸出

### 🎤 第 7 週(第 31–35 天)

| 天 | 做什麼 |
|---|---|
| 31 | 挑三個最好的工具(建議:第 10 天的、第 20 天的、第 5+6 週合起來的那條線)。每個開一頁 |
| 32–33 | 每頁用四段寫:**問題**(誰痛、痛在哪、以前怎麼做)/ **做法**(拆成幾步、每步做什麼)/ **取捨**(我也考慮過 X,沒選是因為 Y)/ **結果**(省了多少時間、抓到多少問題)。**取捨那段最重要**,那是分辨「會寫」和「會判斷」的地方 |
| 34 | 每個工具錄一段**兩分鐘**口頭講解。手機錄就好。聽回來,標出講不清楚的地方 |
| 35 | 重錄一次 |

🎤 **兩分鐘講解的結構:** 十秒說問題 → 三十秒說怎麼拆 → 三十秒說最難的一個決定 → 二十秒說結果 → 三十秒說如果重做會改什麼。

### 🔍 第 8 週(第 36–40 天)

| 天 | 做什麼 |
|---|---|
| 36–37 | 請工程師做**完整** code review,不是看一眼。把他說的每一條寫下來,不辯解 |
| 38 | 照 review 改。改不動的寫下為什麼 |
| 39 | 找一個自己不熟的 Blender addon 原始碼(GitHub 上隨便一個星星幾百的)。不改它,只讀。寫下:它怎麼分檔案、怎麼處理設定、怎麼報錯、跟你的做法差在哪 |
| 40 | 回頭看第 5 條規則累積的「我當時不知道的是 ___」清單。分兩類:**查了就會**(語法、API 名稱)和**概念缺口**(不知道有這種做法)。後者才是下一輪要練的 |

---

## 🚫 五、不要碰的

- LeetCode、演算法題 —— TA 面試幾乎不考
- C++ —— 已排除
- 新框架(Django、FastAPI、任何 web 東西)
- 教學影片 —— 看了會有進步的錯覺
- 第二個語言
- 把標準庫從頭過一遍

---

## 📅 六、時間對照

| 週次 | 訓練 | 主線 |
|---|---|---|
| 1–2 | 資料流與核心語法 | 作品集收尾(九月底) |
| 3–4 | 重建匯出工具 | 開始投遞(十月) |
| 5–6 | UE5 / Blender 真工具 | 投遞中;十月中更新作品集時把這兩個補進去 |
| 7–8 | 回饋、整理、口頭練習 | 面試準備 |

🚀 **投遞不等這份計畫。它是並行的,不是前置的。**

---

## ✅ 七、過關的標準

不是「寫得快」,是這六條:

1. 拿到一個需求,動手之前能列出幾個函式、各自的輸入輸出
2. 測試之前能想到至少一半的邊界情況
3. 自己的工具,一行一行能解釋為什麼這樣寫
4. 需求改了,能改,不用整個重寫
5. 工具壞了,能找到哪裡壞
6. 沒見過你的人,靠 README 能跑起來

六條都能,「白紙寫不出來」就可以放下——缺的只是語法記憶,查就有。

---

## 🔧 八、如果中間斷了

斷幾天很正常。不要從頭開始,從斷的那一天接著做。這份計畫的順序有依賴(第 9 天靠第 1 天、第 29 天靠第 25 天),但每一週內部可以調。

如果某一題卡了兩天還沒出來,跳過,做下一題,週末回來。卡住的那一題記進「我當時不知道的是 ___」清單。
