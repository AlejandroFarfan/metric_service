class data_keeper():

    def __init__(self) :
        print("data_keeper")
        self.users = []

    def feed_data(self, log: str):
        print("feed "+log)
        if "user" in log :
            pass
