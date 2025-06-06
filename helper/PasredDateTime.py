from datetime import datetime

def parseDateFormats(label):
    label = str(label).strip()
    for fmt in ("%d %b %Y","%d %B %Y", "%B %Y", "%b %Y"):
        try:
            return datetime.strptime(label, fmt)
        except Exception as ex:
            print(ex)
    return None  
