import os

index_path = r"c:\ameva\AMEVA-Dead-Internet-Threatre\src\ui\templates\index.html"
js_path = r"c:\ameva\AMEVA-Dead-Internet-Threatre\src\ui\static\js\app.js"

with open(index_path, "r", encoding="utf-8") as f:
    html_content = f.read()

start_idx = html_content.find("<script>")
end_idx = html_content.find("</script>", start_idx)

if start_idx != -1 and end_idx != -1:
    script_content = html_content[start_idx + len("<script>"):end_idx].strip()
    
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(script_content)
        
    new_html = html_content[:start_idx] + '<script src="/static/js/app.js"></script>' + html_content[end_idx + len("</script>"):]
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_html)
        
print("Extracted JS to app.js")
