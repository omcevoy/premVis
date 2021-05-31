import json
from dataCollection.performanceScrape import fetchSeasonData
from dataCollection.payScrape import getPay

def writeToFile(fileName, data):
    with open(fileName, 'w') as f:
        json.dump(data, f)

def main():
    payData = getPay()
    performanceData = fetchSeasonData()
    writeToFile("payData.json", payData)
    writeToFile("performanceData.json", performanceData)


main()
