import requests
from langchain.tools import Tool
from config.config import NVD_API_KEY   # adjust path

def search_cve(query: str):
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    headers = {
        "apiKey": NVD_API_KEY
    }

    params = {
        "keywordSearch": query,
        "resultsPerPage": 3
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        results = []

        for item in data.get("vulnerabilities", []):
            cve = item["cve"]
            cve_id = cve["id"]
            desc = cve["descriptions"][0]["value"]

            results.append(f"{cve_id}: {desc[:200]}")

        return "\n\n".join(results) if results else "No CVEs found."

    except Exception as e:
        return f"CVE API Error: {str(e)}"


cve_tool = Tool(
    name="CVE_Search",
    func=search_cve,
    description="Use for CVEs, vulnerabilities, exploits, severity, latest security issues."
)