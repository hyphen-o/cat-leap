class MileStastics:
    def set_data(self, miles_data):
        self.__MILES_DATA = miles_data

    def get_length(self):
        list_len = []
        for USER_MILES in self.__MILES_DATA:
            list_len.append(len(USER_MILES) - 1)

        return list_len

    def get_duplication(self):
        list_duplication = []
        for USER_MILES in self.__MILES_DATA:
            for MILE, index in USER_MILES:
                if index == len(USER_MILES) - 1:
                    break

                if index != len(USER_MILES) - 2:
                    list_duplication.append(
                        [
                            {**MILE["Before"], "IsRemix": MILE["IsRemix"]},
                            {
                                **USER_MILES[index + 1]["Before"],
                                "IsRemix": USER_MILES[index + 1]["IsRemix"],
                            },
                        ]
                    )
                else:
                    list_duplication.append(
                        [{**MILE["Before"], "IsRemix": MILE["IsRemix"]}, "NEXT_LEVEL"]
                    )
