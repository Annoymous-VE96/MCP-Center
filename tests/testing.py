from domains.news.tools import url_shortner

url = "https://www.espn.in/football/story/_/id/49145571/fifa-world-cup-2026-stats-lionel-messi-all-goalscorer-18-kylian-mbappe-miroslav-klose-16-record-100-haaland"
alias = "Accenture Launches Accenture Edge to Help Mid-Market Companies Harness AI and Reinvent How They Operate - Accenture"

response = url_shortner(url,alias)
print(response)