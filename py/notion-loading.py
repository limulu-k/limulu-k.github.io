import requests
import json
import os
import time


# Notion API 설정
NOTION_API_KEY = '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'  # Integration에서 발급받은 토큰
PAGE_ID = '153e8cfac68c804bb7e1ee19089fcca7'  # 가져오려는 페이지의 ID

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# ✅ 이미지 저장 디렉토리 생성
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# ✅ 특정 페이지의 모든 블록 가져오기 (Pagination 처리)
def get_page_blocks(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    all_blocks = []
    
    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            all_blocks.extend(data.get("results", []))
            url = data.get("next_cursor")  # 다음 페이지가 있으면 계속 요청
            if url:
                url = f"https://api.notion.com/v1/blocks/{page_id}/children?start_cursor={url}"
        else:
            print(f"🚨 오류 발생: {response.status_code}, {response.text}")
            return None
    
    return all_blocks

# ✅ Notion 내부 이미지 다운로드 함수
def download_image(image_url, block_id):
    """ Notion 내부 파일 URL을 다운로드하여 저장 """
    response = requests.get(image_url, headers=HEADERS, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(IMAGE_DIR, f"{block_id}.jpg")  # 저장 경로
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"✅ 이미지 저장 완료: {file_path}")
        return file_path
    else:
        print(f"❌ 이미지 다운로드 실패: {image_url}")
        return None

# ✅ 재귀적으로 하위 페이지 및 모든 블록 가져오기
def extract_notion_data(page_id, depth=0):
    data = get_page_blocks(page_id)
    if not data:
        return None
    
    notion_data = []

    for block in data:
        block_id = block["id"]
        block_type = block["type"]
        text_content = ""

        # ✅ **모든 블록 타입에서 `block_data`를 초기화**
        block_data = {
            "id": block_id,
            "type": block_type,
            "has_children": block["has_children"]
        }

        # ✅ 안전한 `rich_text` 데이터 추출 (KeyError 방지)
        def extract_text(rich_text_list):
            if not rich_text_list:
                return ""
            return " ".join([rt.get("text", {}).get("content", "") for rt in rich_text_list if "text" in rt])

        # ✅ 텍스트 포함 블록 추출
        if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item", "to_do"]:
            text_content = extract_text(block[block_type].get("rich_text", []))

        # ✅ 이미지 처리 (내부 이미지 다운로드 & 원본 URL 유지)
        elif block_type == "image":
            image_url = block["image"].get("file", {}).get("url") or block["image"].get("external", {}).get("url")
            block_data["notion_url"] = image_url  # ✅ 원본 Notion 이미지 URL 저장

            if "amazonaws.com" in image_url:  # ✅ Notion 내부 이미지 (S3)
                local_path = download_image(image_url, block_id)  # ✅ 이미지 다운로드
                block_data["local_path"] = local_path  # ✅ 로컬 저장 경로 추가
                text_content = f"이미지 (로컬 저장: {local_path}, 원본 URL: {image_url})"
            else:
                text_content = f"이미지 URL: {image_url}"

        # ✅ 코드 블록 처리
        elif block_type == "code":
            code_text = extract_text(block["code"].get("rich_text", []))
            code_language = block["code"]["language"]
            text_content = f"```{code_language}\n{code_text}\n```"

        # ✅ 테이블 처리 (⚠️ 기존 오류 해결)
        elif block_type == "table":
            text_content = f"테이블 (열 개수: {block['table']['table_width']})"

        elif block_type == "table_row":
            # ✅ `cells`는 리스트의 리스트 구조이므로, 한 단계 더 접근해야 함.
            row_content = [
                extract_text(cell) if isinstance(cell, list) else ""  # 리스트인 경우만 처리
                for cell in block["table_row"].get("cells", [])
            ]
            text_content = f"테이블 행: {row_content}"

        # ✅ 토글 처리
        elif block_type == "toggle":
            toggle_text = extract_text(block["toggle"].get("rich_text", []))
            text_content = f"▶ {toggle_text}"

        # ✅ 블록 내용 추가
        block_data["content"] = text_content

        # ✅ 하위 블록이 있으면 재귀적으로 가져옴
        if block["has_children"] and depth < 5:
            time.sleep(0.5)
            block_data["children"] = extract_notion_data(block_id, depth + 1)

        notion_data.append(block_data)

    return notion_data



# ✅ JSON 저장
def save_json(data, filename="notion_output.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ JSON 파일 저장 완료: {filename}")

# ✅ 실행
notion_data = extract_notion_data(PAGE_ID)
save_json(notion_data)