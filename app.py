import json
import requests
import urllib3

# 關閉 SSL 憑證警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def run_check():
    base_url = "https://www.rtmpcdn.com/live/qq{}.m3u8"
    stream_entries = []

    print("正在檢查 qq1 到 qq10 的連線與跳轉狀況...")
    for i in range(1, 11):
        stream_name = f"qq{i}"
        url = base_url.format(i)
        try:
            response = requests.get(url, timeout=5, allow_redirects=True, verify=False)
            if response.status_code == 200 and len(response.history) > 0:
                final_url = response.url
                print(f"[有跳轉] {stream_name} -> {final_url}")
                stream_entries.append({
                    "name": stream_name,
                    "url": final_url,
                })
        except requests.exceptions.RequestException:
            pass

    formatted_json = json.dumps(stream_entries, indent=2, ensure_ascii=False)

    # 輸出 streams.js
    js_content = f"const streamUrls = {formatted_json};"
    with open("streams.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    # 另存一份 streams.json
    with open("streams.json", "w", encoding="utf-8") as f:
        f.write(formatted_json)

    print(f"已完成！共寫入 {len(stream_entries)} 筆資料至 streams.js 與 streams.json")


if __name__ == "__main__":
    run_check()