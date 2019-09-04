import requests


def get_call():
    url = "http://localhost:8080/check"
    r = requests.get(url=url)
    print(r.content)
    url2 = "https://localhost:9002/check"
    r = requests.get(url=url2, verify=False)
    print(r.content)


def main():
    get_call()


if __name__ == "__main__":
    main()
