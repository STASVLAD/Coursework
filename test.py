def main():
    response = {
        "version": 0,
        "session": 1,
        "response": {
            "end_session": False
        }
    }

    inner(response)
    print(response)


def inner(response):
    response["session"] = 2
    response["new"] = 2


main()
