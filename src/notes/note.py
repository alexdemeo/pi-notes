import datetime


def record(text):
    from src import DIR
    t = datetime.datetime.now().strftime("%b%d-%I:%M:%S%p")
    file = DIR + "resources/notes/" + t + ".txt"
    f = open(file, "w")
    f.write(text)
    print("Recorded to", file, ":", text)
    f.close()


if __name__ == '__main__':
    record("yoyo man")
