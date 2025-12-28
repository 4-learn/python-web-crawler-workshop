import json
import os

class LawDataManager:
    def __init__(self, json_file_path="laws_data.json"):
        self.json_file_path = json_file_path
        self.laws_data = []

    def save_to_json(self):
        """將法律資料儲存到 JSON 檔案"""
        with open(self.json_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.laws_data, f, ensure_ascii=False, indent=2)
        print(f"\n資料已儲存到 {self.json_file_path}")
        print(f"總共儲存 {len(self.laws_data)} 筆資料")

    def load_from_json(self):
        """從 JSON 檔案載入法律資料"""
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                self.laws_data = json.load(f)
            print(f"已從 {self.json_file_path} 載入 {len(self.laws_data)} 筆資料")
        else:
            print(f"檔案 {self.json_file_path} 不存在")

    def show_laws_data(self, limit=5):
        """顯示法律資料（預設顯示前 5 筆）"""
        print(f"\n顯示前 {limit} 筆資料：")
        print("=" * 60)

        for i, law in enumerate(self.laws_data[:limit], 1):
            print(f"\n第 {i} 筆：")
            print(f"章節: {law.get('chapter', 'N/A')}")
            print(f"條文編號: {law.get('article_number', 'N/A')}")
            print(f"條文連結: {law.get('article_link', 'N/A')}")
            print(f"內容: {law.get('content', 'N/A')[:100]}...")
            print("-" * 60)
