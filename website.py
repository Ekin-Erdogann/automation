import sys
import webbrowser

Urls={"work":["https://www.google.com","https://www.linkedin.com"], "social":["https://www.instagram.com/","https://www.youtube.com"]}

def open_page(urls):
    for url in urls:
        webbrowser.open_new_tab(url)

if __name__=="__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in Urls:
        print("Usage: python script.py <setName>")
        print("Available sets:")
        for setName in Urls.keys():
            print(f"- {setName}")
        sys.exit(1)
    setName= sys.argv[1]
    urls=Urls[setName]
    open_page(urls=urls)