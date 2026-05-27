import requests
from langchain.tools import Tool

CISA_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

def get_cisa_data(_: str):
    try:
        res = requests.get(CISA_URL)
        data = res.json()

        vulns = data.get("vulnerabilities", [])[:5]

        output = []
        for v in vulns:
            output.append(f"{v['cveID']} - {v['vulnerabilityName']}")

        return "\n".join(output)

    except Exception as e:
        return f"CISA Error: {str(e)}"


cisa_tool = Tool(
    name="CISA_Threat_Feed",
    func=get_cisa_data,
    description="Use for real-time exploited vulnerabilities and latest threats."
)