import httpx
import re
import urllib.parse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def search_business_info(name, city):
    query = f"{name} {city} phone contact"
    try:
        r = httpx.post(
            "https://html.duckduckgo.com/html/",
            data={"q": query},
            headers=headers,
            timeout=10
        )
        text = r.text
        # Look for Indian phone patterns (0257-... or 98..., 94..., etc.)
        phones = re.findall(r'(?:\+91[\-\s]?)?[6-9]\d{9}|0\d{2,4}[\-\s]?\d{6,8}', text)
        # Look for website links
        links = re.findall(r'href="//duckduckgo\.com/l/\?uddg=([^"&]+)', text)
        clean_links = [urllib.parse.unquote(l) for l in links if not any(x in l for x in ['duckduckgo', 'justdial', 'indiamart', 'facebook', 'youtube', 'wikipedia', 'google'])]
        return {
            "phones": list(set(phones))[:3],
            "possible_websites": clean_links[:2]
        }
    except Exception as e:
        return {"error": str(e)}

print("Enrichment for 'Raisoni Hospital Jalgaon':")
res = search_business_info("Raisoni Hospital", "Jalgaon")
print(res)
