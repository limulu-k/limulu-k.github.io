import requests

NOTION_API_KEY = "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"
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28"
}

# ✅ 워크스페이스 내 검색 (Integration이 접근할 수 있는 데이터 확인)
url = "https://api.notion.com/v1/search"

response = requests.post(url, headers=HEADERS, json={"query": ""})

print(response.json())  # Integration이 접근 가능한 페이지 목록 출력
