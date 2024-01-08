import stats


if __name__ == "__main__":
    api_client = stats.Client(stats.API_KEY)
    while True:
        ign = input("Enter player name: ")
        print(f"Player {ign} is a nickname: {api_client.nick(ign)}")