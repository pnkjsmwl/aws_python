import requests


def get_call():
    # url = "http://localhost:8080/get"
    # r = requests.get(url=url)
    # print(r.content)

    url2 = "https://localhost:9002/get"
    r = requests.get(url=url2, verify=False)
    print(r.content)

    url3 = "https://localhost:9002/post"
    payload = 'Pankaj'
    r = requests.post(url=url3, verify=False, data=payload)
    print(r.content)


def main():
    get_call()


if __name__ == "__main__":
    main()
