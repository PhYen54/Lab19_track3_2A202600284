import wikipediaapi
import json
from datetime import datetime

# 1. Khởi tạo Wikipedia API 
# Lưu ý quan trọng: Wikipedia hiện yêu cầu User-Agent rõ ràng. Hãy đổi email mẫu dưới đây thành email của bạn.
user_agent = "GraphRAG_CorpusBuilder/1.0 (phuongyen303@gmail.com)"
wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='en')

# 2. Danh sách n bài báo cần crawl (Bạn có thể thêm bớt tùy ý)
companies = [
    "Apple Inc.",
    "Microsoft",
    "Alphabet Inc.",
    "Amazon (company)",
    "Meta Platforms",
    "NVIDIA",
    "Samsung Electronics",
    "Taiwan Semiconductor Manufacturing Company",
    "Tesla, Inc.",
    "Broadcom"
]

print(f"Tổng số công ty: {len(companies)}")
def build_corpus(titles, output_filename):
    corpus = []
    crawl_date = datetime.now().strftime("%Y-%m-%d")

    print(f"Bắt đầu crawl {len(titles)} bài báo từ Wikipedia...")

    for i, title in enumerate(titles):
        print(f"[{i+1}/{len(titles)}] Đang lấy dữ liệu: {title}...")
        
        # Gọi API lấy bài viết
        page = wiki.page(title)

        if page.exists():
            # Tạo object JSON chứa metadata và nội dung
            doc = {
                "doc_id": f"wiki_company_{i:03d}",
                "title": page.title,
                "url": page.fullurl,
                "category": "Tech & AI Company",
                "crawl_date": crawl_date,
                "content": page.text  # .text tự động lọc bỏ thẻ HTML, trả về văn bản thuần
            }
            corpus.append(doc)
        else:
            print(f"  -> Cảnh báo: Không tìm thấy bài viết có tên '{title}'")

    # 3. Lưu toàn bộ mảng dictionary ra file JSON
    with open(output_filename, 'w', encoding='utf-8') as f:
        # ensure_ascii=False để không bị lỗi font nếu có ký tự unicode
        # indent=4 để file JSON được format đẹp, dễ đọc bằng mắt thường
        json.dump(corpus, f, ensure_ascii=False, indent=4)

    print(f"\nHoàn tất! Đã lưu {len(corpus)} tài liệu vào file '{output_filename}'.")

if __name__ == "__main__":
    # Đặt tên file đầu ra
    output_file = "ai_companies_corpus_10.json"
    build_corpus(companies, output_file)