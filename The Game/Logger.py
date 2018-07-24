class Logger(object):

    def __init__(self, obstacleNumber):
        self.file = open("data" + str(obstacleNumber), "a+")

    def logData(self, obstacleNumber, speed, action, distance):
        self.file.write(str(obstacleNumber) + "," + str(speed) + "," + str(action) + "," + str(distance) + "\n")
        #pass
