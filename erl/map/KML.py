class KML:

    doubleSpace = "  "

    def __init__(self, fileName):
        self.fileName = fileName
        self.placemarkNumber = 1
        self.missionSatusNumber = 1
        self.objectIdNumber = 1
        #PLACEMARK FILE CREATION
        self.kmlPlacemarks = open(fileName + "-placemarks.kml", 'w')
        self.kmlPlacemarks.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
        self.kmlPlacemarks.write(self.doubleSpace + "<Folder>\n")
        self.kmlPlacemarks.write(2*self.doubleSpace + "<name>Placemarks</name>\n")
        self.kmlPlacemarks.write(2*self.doubleSpace + "<description>Path placemarks</description>\n")
        #MISSION FILE CREATION
        self.kmlMissionStatus = open(fileName + "-missionSatus.kml", 'w')
        self.kmlMissionStatus.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
        self.kmlMissionStatus.write(self.doubleSpace + "<Folder>\n")
        self.kmlMissionStatus.write(2*self.doubleSpace + "<name>Mission Status</name>\n")
        self.kmlMissionStatus.write(2*self.doubleSpace + "<description>Subtasks undertaken</description>\n")
        #OBJECT RECOGNITION CREATION 
        self.kmlObjectID = open(fileName + "-objectRecognition.kml", 'w')
        self.kmlObjectID.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
        self.kmlObjectID.write(self.doubleSpace + "<Folder>\n")
        self.kmlObjectID.write(2*self.doubleSpace + "<name>Object Recogniton</name>\n")
        self.kmlObjectID.write(2*self.doubleSpace + "<description>Infomartion about an object</description>\n")
    
    def __del__(self):
        #PLACEMARK 
        self.kmlPlacemarks.write(self.doubleSpace + "</Folder>\n")
        self.kmlPlacemarks.write("</kml>")
        #MISSION STATUS
        self.kmlMissionStatus.write(self.doubleSpace + "</Folder>\n")
        self.kmlMissionStatus.write("</kml>")
        #OBJECT RECOGNITION
        self.kmlObjectID.write(self.doubleSpace + "</Folder>\n")
        self.kmlObjectID.write("</kml>")

    def addNewPlacemark(self, timeStamp, headingDegrees, longitude, latitude, altitude):
        self.kmlPlacemarks.write(2*self.doubleSpace + "<Placemark>\n")
        self.kmlPlacemarks.write(3*self.doubleSpace + "<name>Placemark " + str(self.placemarkNumber) + "</name>\n")
        self.kmlPlacemarks.write(3*self.doubleSpace + "<description> Time: " + str(timeStamp) + " ,heading: " + str(headingDegrees) + "</description>\n")
        self.kmlPlacemarks.write(3*self.doubleSpace + "<Point>\n")
        self.kmlPlacemarks.write(4*self.doubleSpace + "<coordinates>" + str(longitude) + "," + str(latitude) + "," + str(altitude) + "</coordinates>\n")
        self.kmlPlacemarks.write(3*self.doubleSpace + "</Point>\n" + 2*self.doubleSpace + "</Placemark>\n")
        self.placemarkNumber += 1

    def addNewMissionStatus(self, subtaskUndertaken, keyDecisionMessage, timeStamp):
        self.kmlMissionStatus.write(2*self.doubleSpace + "<Placemark>\n")
        self.kmlMissionStatus.write(3*self.doubleSpace + "<name>Mission status " + str(self.missionSatusNumber) + "</name>\n")
        self.kmlMissionStatus.write(3*self.doubleSpace + "<description> Subtask: " + subtaskUndertaken + ", " + keyDecisionMessage + ", time: " + str(timeStamp) + "</description>\n")
        self.missionSatusNumber += 1

    def addNewObjectRecognition(self, objectID, longitude, latitude, altitude, targetImage = ""):
        self.kmlObjectID.write(2*self.doubleSpace + "<Placemark>\n")
        self.kmlObjectID.write(3*self.doubleSpace + "<name>Object " + str(self.objectIdNumber) + "</name>\n")
        self.kmlObjectID.write(3*self.doubleSpace + "<description> ID: " + str(objectID) + "</description>\n")
        self.kmlObjectID.write(3*self.doubleSpace + "<Point>\n")
        self.kmlObjectID.write(4*self.doubleSpace + "<coordinates>" + str(longitude) + "," + str(latitude) + "," + str(altitude) + "</coordinates>\n")
        self.kmlObjectID.write(3*self.doubleSpace + "</Point>\n" + 2*self.doubleSpace + "</Placemark>\n")
        self.objectIdNumber += 1
        