from KML import KML

kmlfile = KML("file")
kmlfile.addNewPlacemark("1944-06-06T06:00:00", 78.5, -122.0822035425683, 37.42228990140251, 0)
kmlfile.addNewPlacemark("1944-06-06T06:00:01", 78.5, -123.0822035425683, 38.42228990140251, 0)
kmlfile.addNewObjectRecognition("Body", -118.0822035425683, 40.42228990140251, 0)