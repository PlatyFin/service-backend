#### class defination ####
class LandingPageUtilities():
    def getStrategiesList(self):
        try:
            strategies = ["darkflow"]

            return strategies
        except Exception as e:
            print("Error while treading up : {} ".format(e))