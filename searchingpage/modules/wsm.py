from pathlib import Path
import pandas as pd
import math

import os

#calculates a score based on the min and max value, linearly proportional from -0.5 to 0.5
#this function assumes min value is better
def proportionCalculationMin(min,max,value):
    return ((min+max)/2-value)/((max-min)+1)

'''
This function is assuming the user has already inputted their importance scores and selected which uni they would like to compare
'''

#importance scores in order of rent, distance, safety, early_trans, night_trans, city ddrive distance, uni drive distance, city drive time, city transit time
#range can be between 0 to 5 as some factors may not be relevant to the user at all
# importanceScores = [2,4,5,2,4,4,0,0,0] #user will normally have to input this on the frontend
# 
# university_ = "Deakin University - Burwood" #used to open file

def WSM(university_, importanceScores, maxDistance,maxRent):
    maxDistance += 999
    maxRent += 999


    file_path = os.path.dirname(os.path.abspath(__file__))+f"\dataset\{university_}.csv"
    #loads the correct file depending on which university the user chose
    suburbsDF = pd.read_csv(file_path)
    suburbsCount = len(suburbsDF) 
    scores = [] #keeps track of the scores column to add in
    safetyScores = [] #keeps track of the safety scores from 0 to 5

    #cleaning the data to get rid of unnecessary characters in the string
    suburbsDF['uni_driving_distance'] = suburbsDF['uni_driving_distance'].map(lambda x: str(x)[:-3])
    suburbsDF['city_distance'] = suburbsDF['city_distance'].map(lambda x: str(x)[:-3])
    #ensures any unis that were within 100m does not get filtered out completely
    suburbsDF['uni_driving_distance'] = suburbsDF['uni_driving_distance'].replace("","0")
    suburbsDF['city_distance'] = suburbsDF['city_distance'].replace("","0")

    #converting datatype from string to int
    suburbsDF['uni_driving_distance'] = suburbsDF['uni_driving_distance'].str.replace(",","").astype("float")
    suburbsDF['city_distance'] = suburbsDF['city_distance'].str.replace(",","").astype("float")

    #ensure all columns have the right name
    if len(suburbsDF.columns) == 15:
        suburbsDF.columns = ['index', 'id', 'geo', 'suburb','postcode','rent','distance','crime','Early_Trans_Time','Night_Trans_Time','nightPT','uni_driving_distance',
                        'city_distance','city_driving_time','city_trans_time']
    elif len(suburbsDF.columns) == 16:
        suburbsDF.columns = ['index', 'index2', 'id', 'geo', 'suburb','postcode','rent','distance','crime','Early_Trans_Time','Night_Trans_Time','nightPT','uni_driving_distance',
                        'city_distance','city_driving_time','city_trans_time']

    else:
        suburbsDF.columns = ['id', 'geo', 'suburb','postcode','rent','distance','crime','Early_Trans_Time','Night_Trans_Time','nightPT','uni_driving_distance',
                        'city_distance','city_driving_time','city_trans_time']


    ###CHANGES MADE BY AAYAN PART1###
    suburbsDF['distance'] = suburbsDF['distance'].map(lambda x: str(x)[:-3])
    suburbsDF['distance'] = suburbsDF['distance'].replace("","0")
    suburbsDF['distance'] = suburbsDF['distance'].str.replace(",","").astype("float")


    ###END OF CHANGES MADE BY AAYAN PART2###
    
    #filtering out suburbs that exceed student preferences
    resetIndexRequired = False #removing rows will impact row index, reset will be required if rows are removed
    if maxDistance!= False:
        suburbsDF = suburbsDF[suburbsDF["distance"] < maxDistance]
        resetIndexRequired = True
    if maxRent != False:
        suburbsDF = suburbsDF[suburbsDF["rent"] < maxRent]
        resetIndexRequired = True
    if resetIndexRequired == True:
        suburbsDF = suburbsDF.reset_index()
        suburbsCount = len(suburbsDF)

    #creating the inputs required for the WSM

    ###CHANGES MADE BY AAYAN PART 2, SIMON PLS CHECK

    minValues = suburbsDF.min(axis = 0)
    minRent = minValues["rent"]
    minDistance = minValues["distance"]
    minCrimeRate = math.sqrt(minValues["crime"]) #sqrt due to crime rates prone to outliers
    minEarlyTransitTime = minValues["Early_Trans_Time"]
    minNightTimeTransitTime = minValues["Night_Trans_Time"]
    #minUniDriveDistance = minValues[11]
    minCityDrivingDistance = minValues["city_distance"]
    #minCityDrivingTime = minValues[13]
    #minCityTransitTime = minValues[14]
    #max values
    maxValues = suburbsDF.max(axis = 0)
    maxRent = maxValues["rent"]
    maxDistance = maxValues["distance"]
    maxCrimeRate = math.sqrt(maxValues["crime"])
    maxEarlyTransitTime = maxValues["Early_Trans_Time"]
    maxNightTimeTransitTime = maxValues["Night_Trans_Time"]
    #maxUniDriveDistance = maxValues[11]
    maxCityDrivingDistance = maxValues["city_distance"]
    #maxCityDrivingTime = maxValues[13]
    #maxCityTransitTime = maxValues[14]


    ###END OF CHANGES MADE BY AAYAN PART 2

    #calculation of score and safety
    if suburbsCount > 1:
        for i in range(suburbsCount):
            score = 0
            scoreRent = proportionCalculationMin(minRent,maxRent,suburbsDF["rent"][i])*importanceScores[0]
            score += scoreRent
            scoreDistance = proportionCalculationMin(minDistance,maxDistance,suburbsDF["distance"][i])*importanceScores[1]
            score += scoreDistance

            #adding safety score into score
            safety = proportionCalculationMin(minCrimeRate,maxCrimeRate,math.sqrt(suburbsDF["crime"][i]))
            scoreSafety = proportionCalculationMin(minCrimeRate,maxCrimeRate,math.sqrt(suburbsDF["crime"][i])) *importanceScores[2]
            score += scoreSafety

            #calculation of safety score which is between 0 to 5
            safety = safety + 0.5
            safety = safety * 5

            scoreEarlyTransit = proportionCalculationMin(minEarlyTransitTime,maxEarlyTransitTime,suburbsDF["Early_Trans_Time"][i])*importanceScores[3]
            score += scoreEarlyTransit

            scoreNightTransit = proportionCalculationMin(minNightTimeTransitTime,maxNightTimeTransitTime,suburbsDF["Night_Trans_Time"][i])*importanceScores[4]
            score += scoreNightTransit
            #score += proportionCalculationMin(minUniDriveDistance,maxUniDriveDistance,suburbsDF["uni_driving_distance"][i])*importanceScores[6]
            scoreCityDrive = proportionCalculationMin(minCityDrivingDistance,maxCityDrivingDistance,suburbsDF["city_distance"][i])*importanceScores[5]
            score += scoreCityDrive
            #score += proportionCalculationMin(minCityDrivingTime,maxCityDrivingTime,suburbsDF["city_driving_time"][i])*importanceScores[7]
            #score += proportionCalculationMin(minCityTransitTime,maxCityTransitTime,suburbsDF["city_trans_time"][i])*importanceScores[8]

            #calculation of interaction variables where deemed necessary
            interaction1 = (scoreNightTransit + scoreSafety) * (importanceScores[2]/5) #night time transit safety
            


            scores.append(score)
            safetyScores.append(safety)
    else:
        scores.append(100)
        safetyScores.append(5)


    #adds the new scores column 
    suburbsDF["scores"] = scores
    suburbsDF["safety"] = safetyScores

    #normalizing the suburb scores
    if suburbsCount > 1: 
        minValues = suburbsDF.min(axis = 0)
        minScore = minValues[-2]
        maxValues = suburbsDF.max(axis = 0)
        maxScore = maxValues[-2]
        suburbsDF["scores"] = suburbsDF["scores"] - minScore
        suburbsDF["scores"] = suburbsDF["scores"] * (100/(-minScore+maxScore))

    # #changes the output to a dict to be used by the frontend 
    # output = {}
    # for i in range(suburbsCount):
    #     suburbInfo = {str(suburbsDF["suburb"][i]): {"suburb":suburbsDF["suburb"][i], "postcode": suburbsDF["postcode"][i], "transit_time_to_uni": str(suburbsDF["Early_Trans_Time"][i]), 
    #     "transit_time_to_2nd_transit_minutes":str(suburbsDF["city_trans_time"][i]), "night_public_transport": str(suburbsDF["nightPT"][i]), "safety": str(suburbsDF["safety"][i]),
    #     "average_rent": str(suburbsDF["rent"][i]), "suburb_score": str(suburbsDF["scores"][i]), "suburb_name_postcode":str(str(suburbsDF["suburb"][i]) + str(suburbsDF["postcode"][i]))}}
    #     output.update(suburbInfo)
        

    # return output


    #change added by Aayan to make format [{...}, {...}]

    output = []
    for i in range(suburbsCount):
        suburbInfo = {
        "suburb":suburbsDF["suburb"][i], "postcode": str(int(suburbsDF["postcode"][i])), 
        "transit_time_to_uni": str(suburbsDF["Early_Trans_Time"][i]), 
        "transit_time_to_2nd_transit_minutes":str(suburbsDF["city_trans_time"][i]), 
        "night_public_transport": str(suburbsDF["nightPT"][i]), 
        "safety": str(round(suburbsDF["safety"][i], 2)),
        "average_rent": str(round(suburbsDF["rent"][i], 2)), 
        "suburb_score": round(suburbsDF["scores"][i], 2), 
        "suburb_name_postcode":str(str(suburbsDF["suburb"][i]).lower() + str(int(suburbsDF["postcode"][i]))).replace(" ", "")
        }
        output.append(suburbInfo)
        

    return output

# output = WSM(university_, importanceScores)
# output