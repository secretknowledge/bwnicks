from stats import HypixelAPI

api = HypixelAPI("3ae7e469-f78e-474e-9d0c-1ee6c4378127")

while True:
    prompt = input("Is (n)ick, (f)kdr, or (q)uit: ")

    if prompt == "n":
        print(api.nick(input("Player IGN: ")))
    elif prompt == "f":
        print(api.fkdr(input("Player IGN: ")))
    elif prompt == "q":
        break
    else:
        print("Invalid input.")