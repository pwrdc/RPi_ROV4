class KML(object):

    space = " "

    def __init__(self, fileName):
        self.fileName = fileName
        self.placemarkNumber = 1
        self.missionSatusNumber = 1
        self.objectIdNumber = 1
        #PLACEMARK FILE CREATION
        self.kmlPlacemarks = open(fileName + "-placemarks.kml", 'w')
        self.kmlPlacemarks.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
        self.kmlPlacemarks.write(2*self.space + "<Folder>\n")
        self.kmlPlacemarks.write(4*self.space + "<name>Placemarks</name>\n")
        self.kmlPlacemarks.write(4*self.space + "<description>Path placemarks</description>\n")
        #MISSION FILE CREATION
        self.kmlMissionStatus = open(fileName + "-missionSatus.kml", 'w')
        self.kmlMissionStatus.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
        self.kmlMissionStatus.write(2*self.space + "<Folder>\n")
        self.kmlMissionStatus.write(4*self.space + "<name>Mission Status</name>\n")
        self.kmlMissionStatus.write(4*self.space + "<description>Subtasks undertaken</description>\n")
        #OBJECT RECOGNITION CREATION 
        self.kmlObjectID = open(fileName + "-objectRecognition.kml", 'w')
        self.kmlObjectID.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
        self.kmlObjectID.write(2*self.space + "<Folder>\n")
        self.kmlObjectID.write(4*self.space + "<name>Object Recogniton</name>\n")
        self.kmlObjectID.write(4*self.space + "<description>Infomartion about an object</description>\n")
    
    def __del__(self):
        #PLACEMARK
        self.kmlPlacemarks.write(2*self.space + "</Folder>\n")
        self.kmlPlacemarks.write("</kml>")
        #MISSION STATUS
        self.kmlMissionStatus.write(2*self.space + "</Folder>\n")
        self.kmlMissionStatus.write("</kml>")
        #OBJECT RECOGNITION
        self.kmlObjectID.write(2*self.space + "</Folder>\n")
        self.kmlObjectID.write("</kml>")

    def addNewPlacemark(self, timeStamp, headingDegrees, longitude, latitude, altitude):
        self.kmlPlacemarks.write(4*self.space + "<Placemark>\n")
        self.kmlPlacemarks.write(6*self.space + "<name>Placemark " + str(self.placemarkNumber) + "</name>\n")
        self.kmlPlacemarks.write(6*self.space + "<description> Time: " + str(timeStamp) + " ,heading: " + str(headingDegrees) + "</description>\n")
        self.kmlPlacemarks.write(6*self.space + "<Point>\n")
        self.kmlPlacemarks.write(8*self.space + "<coordinates>" + str(longitude) + "," + str(latitude) + "," + str(altitude) + "</coordinates>\n")
        self.kmlPlacemarks.write(6*self.space + "</Point>\n" + 4*self.space + "</Placemark>\n")
        self.placemarkNumber += 1

    def addNewMissionStatus(self, subtaskUndertaken, keyDecisionMessage, timeStamp):
        self.kmlMissionStatus.write(4*self.space + "<Placemark>\n")
        self.kmlMissionStatus.write(6*self.space + "<name>Mission status " + str(self.missionSatusNumber) + "</name>\n")
        self.kmlMissionStatus.write(6*self.space + "<description> Subtask: " + subtaskUndertaken + ", " + keyDecisionMessage + ", time: " + str(timeStamp) + "</description>\n")
        self.missionSatusNumber += 1

    def addNewObjectRecognition(self, objectID, longitude, latitude, altitude, targetImage = ""):
        self.kmlObjectID.write(4*self.space + "<Placemark>\n")
        self.kmlObjectID.write(6*self.space + "<name>Object " + str(self.objectIdNumber) + "</name>\n")
        self.kmlObjectID.write(6*self.space + "<description> ID: " + str(objectID) + "</description>\n")
        self.kmlObjectID.write(6*self.space + "<Point>\n")
        self.kmlObjectID.write(8*self.space + "<coordinates>" + str(longitude) + "," + str(latitude) + "," + str(altitude) + "</coordinates>\n")
        self.kmlObjectID.write(6*self.space + "</Point>\n" + 4*self.space + "</Placemark>\n")
        self.objectIdNumber += 1

if __name__== "__main__":
     kmlfile = KML("file")
     kmlfile.addNewPlacemark("1944-06-06T06:00:00", 78.5, -122.0822035425683, 37.42228990140251, 0)
     kmlfile.addNewPlacemark("1944-06-06T06:00:01", 78.5, -123.0822035425683, 38.42228990140251, 0)
     kmlfile.addNewObjectRecognition("Body", -118.0822035425683, 40.42228990140251, 0)
        