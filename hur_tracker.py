# -*- coding: utf-8 -*-
from StringIO import StringIO
import urllib2
import gzip
from pandas import Series, DataFrame
import numpy as np
from mpl_toolkits.basemap import Basemap
from collections import OrderedDict
from IPython.display import clear_output
from IPython.html import widgets 
from IPython.display import display
import matplotlib.pyplot as plt
import matplotlib.cm as cm
get_ipython().magic(u'matplotlib inline')

# Function to read text files
def readTextFile(url):
    request = urllib2.Request(url)

    # Adding user to header for NHC user logs
    request.add_header("User-agent", "Unidata Python Client Test")
    response = urllib2.urlopen(request)

    # Store data response in a string buffer.
    sio_buffer = StringIO(response.read())
    f = sio_buffer.getvalue()
    return f.splitlines()

# Function to open and read zipped files
def readGZFile(url):
    request = urllib2.Request(url)

    # Adding user to header for NHC user logs
    request.add_header("User-agent", "Unidata Python Client Test")
    response = urllib2.urlopen(request)

    # Store data response in a string buffer.
    sio_buffer = StringIO(response.read())

    # Read from the string buffer as if it were a physical file
    gzf = gzip.GzipFile(fileobj = sio_buffer)
    data = gzf.read()
    return data.splitlines()

# Class to sort ensemble members into ensembles
class SortModels:
    def __init__(self):
        # Reading in data from text file
        self.fileLines = readTextFile("ftp://ftp.nhc.noaa.gov/atcf/docs/nhc_techlist.dat")
        
        # Pulling necessary data from lines in file
        model, info = [],[]
        for line in self.fileLines[1:]:
            model.append(line[4:8].strip())
            info.append(line[68:].strip())

        #Combining data from file into a Pandas Dataframe dictionary.
        self.models = DataFrame({"Model":model, "Info":info})
        
    # Method to sort ensemble members into corresponding ensemble list    
    def shapeModelInfo(self):
        modelStuff = self.models
        
        # Ensemble lists
        gfsE,ecmwfE,gfdlE,hwrfE,nhcE,ukmetE,bamsE,shipsE,psuE,\
        cmcE,consenE,namE,coampsE,nogapsE,navgemE,jgsmE,esrlE,ncepE \
        = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        
        # FOR loop to seperate member by checking model information
        for line in range(len(modelStuff["Info"])):
            if (modelStuff["Info"][line].startswith("GFS")) & ("Mean" not in modelStuff["Info"][line]):
                gfsE.append(modelStuff["Model"][line])

            if ("SHIPS" in modelStuff["Info"][line]) & ("Mean" not in modelStuff["Info"][line]):    
                shipsE.append(modelStuff["Model"][line])

            if ("PSU" in modelStuff["Info"][line]) & ("Mean" not in modelStuff["Info"][line]):    
                psuE.append(modelStuff["Model"][line])

            if ("ESRL" in modelStuff["Info"][line]) & ("Mean" not in modelStuff["Info"][line]):     
                esrlE.append(modelStuff["Model"][line])

            if ("NCEP" in modelStuff["Info"][line]) & ("Mean" not in modelStuff["Info"][line]):    
                ncepE.append(modelStuff["Model"][line])

            if (modelStuff["Info"][line].startswith("Beta")) & ("Mean" not in modelStuff["Info"][line]):    
                bamsE.append(modelStuff["Model"][line])

            if (modelStuff["Info"][line].startswith("Japanese")) & ("Mean" not in modelStuff["Info"][line]):    
                jgsmE.append(modelStuff["Model"][line])

            if (modelStuff["Info"][line].startswith("NAM")) & ("Mean" not in modelStuff["Info"][line]):
                namE.append(modelStuff["Model"][line])

            if ("COAMPS" in modelStuff["Info"][line]) & ("Mean" not in modelStuff["Info"][line]):   
                coampsE.append(modelStuff["Model"][line])

            if (modelStuff["Info"][line].startswith("NOGAPS")) & ("Mean" not in modelStuff["Info"][line]):   
                nogapsE.append(modelStuff["Model"][line])

            if (modelStuff["Info"][line].startswith("NAVGEM")) & ("Mean" not in modelStuff["Info"][line]):    
                navgemE.append(modelStuff["Model"][line])

            if (modelStuff["Info"][line].startswith("Canadian")) & ("Mean" not in modelStuff["Info"][line]):
                cmcE.append(modelStuff["Model"][line])

            if (modelStuff["Info"][line].startswith("UKMET")) & ("Mean" not in modelStuff["Info"][line]):
                ukmetE.append(modelStuff["Model"][line]) 

            if (modelStuff["Info"][line].startswith("ECMWF")) & ("Mean" not in modelStuff["Info"][line]):
                ecmwfE.append(modelStuff["Model"][line])

            if ("GFDL" in modelStuff["Info"][line]) & ("Mean" not in modelStuff["Info"][line]):
                gfdlE.append(modelStuff["Model"][line])

            if ("Consensus" in modelStuff["Info"][line]) & ("Mean" not in modelStuff["Info"][line]):
                consenE.append(modelStuff["Model"][line])

            if ("HWRF" in modelStuff["Info"][line]) & ("Mean" not in modelStuff["Info"][line]):
                hwrfE.append(modelStuff["Model"][line])

            if (modelStuff["Info"][line].startswith("NHC")) & ("Mean" not in modelStuff["Info"][line]):
                nhcE.append(modelStuff["Model"][line])
        
        # Dictionary to store ensembles
        self.modelGroups = {"GFS":gfsE,"ECMWF":ecmwfE,"GFDL":gfdlE,"NHC":nhcE,"HWRF":hwrfE,
        "UKMET":ukmetE,"CMC":cmcE,"Consensus":consenE,"NAM":namE,"COAMPS":coampsE,
        "NOGAPS":nogapsE,"NAVGEM":navgemE,"BAMS":bamsE,"JGSM":jgsmE,"NCEP":ncepE,
        "SHIPS":shipsE,"PSU":psuE,"ESRL":esrlE}

        # Reversing the order of the previous dictionary to have the
        #  ensemble members be the dictionary keys
        self.modelToGroup = {}
        for group,models in self.modelGroups.items():
            for model in models:
                self.modelToGroup[model] = group

        return {"modelGroups":self.modelGroups, "modelToGroup":self.modelToGroup}

# Class to get storm names and file name
class StormNameData:     
    def __init__(self):
        self.fileLines = readTextFile("http://ftp.nhc.noaa.gov/atcf/index/storm_list.txt")
        
    # Method to pull necessary data from lines in file
    def splitStormInfo(self):
        name, cycloneNum, year, stormType, basin, filename = [],[],[],[],[],[]
        for line in self.fileLines[1:]:
            fields = line.split(",")
            name.append(fields[0].strip())
            basin.append(fields[1].strip())
            cycloneNum.append(fields[7].strip())
            year.append(fields[8].strip())
            stormType.append(fields[9].strip())
            filename.append(fields[-1].strip().lower())
    
        # Combining data from file into a Pandas Dataframe dictionary.
        self.storms = DataFrame({"Name":name, "Basin":basin, "CycloneNum":np.array(cycloneNum), "Year":np.array(year),                      "StormType":stormType, "Filename":filename})
        return self.storms

# Class to select desired storm
class StormSelector:
    def __init__(self):
        self.stormStuff = StormNameData().splitStormInfo()
        years = sorted(self.stormStuff.groupby(["Year"]).groups.keys())
        
        # Slider to select year for file
        self.menuYears = widgets.IntSliderWidget(min=1851, max=2014, step=1, value=2014, description = "Year")
        self.menuNames = widgets.DropdownWidget()
        self.menuNames.on_trait_change(self._createUrl, 'value')

        # Button to create dropdown menu of storms for the selected year
        self.buttonName = widgets.ButtonWidget(description="Get Storm Names")#, value = menuYears.value)
        self.buttonName.on_click(self._updateNames)
        
        # Button to call the plotting class and other necessary classes
        self.plottingButton = widgets.ButtonWidget(description = "Plot Selected Storm", disabled = True)
        
        # Container widget to hold storm selection widgets
        self.stormSelector = widgets.ContainerWidget(children = [self.menuYears, self.buttonName, 
                                                            self.menuNames, self.plottingButton], visible = True)
        
        # Container widget to hold both storm selectign widgets and plotting button
        self.form = widgets.ContainerWidget()
        self.form.children = [self.stormSelector]
        display(self.form)

   # Method to display storms for the specified year in the dropdown menu widget   
    def _updateNames(self, *args):
        p1 = self.stormStuff[self.stormStuff.Year == str(self.menuYears.value)]
        self.p2 = p1.groupby(["Name"])
        names = sorted(self.p2.groups.keys())
        if names:
            self.menuNames.values = OrderedDict(zip(names, names))
        else:
            self.menuNames.values.clear()
    
    # Method to test if files exist for the selected storm
    def test_url(self,url):
        request = urllib2.Request(url)
        request.get_method = lambda : 'HEAD'
        try:
            response = urllib2.urlopen(request)
            return True
        except:
            return False
    
    # Method to create urls for selected storm
    def _createUrl(self, *args):
        pullName = self.stormStuff.loc[self.p2.groups[self.menuNames.value]]
        full = pullName.Filename.values[0]
        
        # Creates different path for 2014 storms
        if self.menuYears.value == 2014:
            url = "http://ftp.nhc.noaa.gov/atcf/aid_public/a%8s.dat.gz" % (full)
            urlb = "http://ftp.nhc.noaa.gov/atcf/btk/b%8s.dat" % (full)
        else:
            url = "http://ftp.nhc.noaa.gov/atcf/archive/%4s/a%8s.dat.gz" % (self.menuYears.value,full)
            urlb = "http://ftp.nhc.noaa.gov/atcf/archive/%4s/b%8s.dat.gz" % (self.menuYears.value,full)

        self.urls = {"Forecast":url, "Best":urlb}
        self.aExists = self.test_url(url)
        self.bExists = self.test_url(urlb)
        
        clear_output()
        
        # Creating message for intances in which the url test passes or fails
        if self.aExists and self.bExists:
            message = 'Selected data for: {}'.format(self.menuNames.value)
            self.plottingButton.disabled = False
            self.plottingButton.on_click(toPlottingFunction)
        else:
            self.stormSelector.visible = True
            self.plottingButton.disabled = True
            message = 'No data found for: '
            if (not self.aExists) and (not self.bExists):
                message = message + "forecast tracks and best track"
            elif not self.aExists:
                message = message + "forecast tracks"
            else:
                message = message + "best track"           
                
        print message
        
# Class to gather data from storm files
class HandleStormData:
    def __init__(self, ss): 
        # Creating dictionary that will be filled with data from forecast files and best track files
        self.dataDict = {}
        for key in ss.urls.keys():
            if (ss.urls[key].endswith(".dat")):
                self.lines = readTextFile(ss.urls[key])
            else:
                self.lines = readGZFile(ss.urls[key])
            lat = []
            lon = []
            basin, cycloneNum, warnDT, model = [],[],[],[]
            for line in self.lines:
                fields = line.split(",")
                #Joins together lattitude and longitude strings without directional letters.
                #Includes type conversion in order to divide by 10 to get the correct coordinate.
                latSingle = int(fields[6][:-1])/10.0
                lonSingle = -(int(fields[7][:-1])/10.0)
                lat.append(latSingle)
                lon.append(lonSingle)
                basin.append(fields[0])
                cycloneNum.append(fields[1].strip())
                warnDT.append(fields[2].strip())
                model.append(fields[4].strip())

            #Combining data from file into a Pandas Dataframe dictionary.
            self.dataDict[key] = DataFrame({"Basin":basin, "CycloneNum":np.array(cycloneNum), 
                                            "WarnDT":np.array(warnDT), "Model":model, 
                                            "Lat":np.array(lat), "Lon":np.array(lon), "Group":''})
    
    # Method to fill in Group column with corresponding ensemble name        
    def sortGroup(self):
        modelInfo = SortModels().shapeModelInfo()
        ensembleMembers = modelInfo["modelToGroup"]
        data = self.dataDict["Forecast"]
        for k in range(len(data["Model"])):
            if data["Model"][k] in ensembleMembers:
                data["Group"][k] = ensembleMembers[data["Model"][k]]
            else:
                data["Group"][k] = data["Model"][k]

        self.dataDict["Forecast"] = data
        return self.dataDict

# Class to create and mange storm plots
class Plotting:
    def __init__(self, hsd):
        # Creating necessary dictionaries for data
        plt.close('all')
        self.modelList = []
        self.artistDict = {}
        self.multiArtistDict = {}
        self.multiTrackDict = {}
        self.container = None

        # Assigning data from position keys to appropriate tracks
        sortedModels = SortModels()
        self.membersToEnsemble = sortedModels.shapeModelInfo()["modelGroups"]
        self.best = hsd.sortGroup()["Best"]
        self.forecast = hsd.sortGroup()["Forecast"]
        
        # Command to set up widgets and actions
        self.userControls()
        
        # Creates figure and sets the axes for animation.
        self.fig = plt.figure(figsize=(8,8))
        self.ax = self.fig.add_subplot(111, autoscale_on=False)
        self.ax.grid()
        # Creating map for appropriate basin
        self.map = self.createMap(self.forecast["Basin"][0], ax=self.ax)
        # Commands to set up plot and to plot initial tracks for NHC model
        self.plotDetails()
        self.setModel("NHC")
        
        
    
    # Method create widgets and set up widget events
    def userControls(self):
        # Button to select new storm from StormSelector
        self.selectStorm = widgets.ButtonWidget(description = "Select New Storm", visible = True)
        self.selectStorm.on_click(selectNewStorm)
        
        # Model selection widgets and controls to change model
        self.modelSelection = widgets.DropdownWidget(values = self.forecast.groupby(["Group"]).groups.keys(), value = "NHC")        
        self.modelSelection.on_trait_change(self.onChangeModel, 'value')
        # Slider widget to move plots through time
        self.frameNumber = widgets.IntSliderWidget(min=0, max=1, value = 0, step=1, description = "Time")

        # Button widgets to advance and retract time frames
        add = widgets.ButtonWidget(description = "+")
        subtract = widgets.ButtonWidget(description = "-")
        add.on_click(self.advanceFrame)
        subtract.on_click(self.subtractFrame)
        
        # Checkbox to add multiple tracks to plot
        clearAll = widgets.ButtonWidget(description = "Clear Plot")
        clearAll.on_click(self.clearPlot)
        self.check = widgets.CheckboxWidget(description = "Add multiple tracks:", value = False)
        # Widgets to tracks to plot
        self.newTrackMenu = widgets.DropdownWidget(values = self.forecast.groupby(["Group"]).groups.keys())
        self.addTrackButton = widgets.ButtonWidget(description = "Add New Track")
        self.plotMultiTrackButton = widgets.ButtonWidget(description = "Plot New Tracks")
        # Container that holds multiple track widgets
        self.addNewTrack = widgets.ContainerWidget(visible=False, children = [self.newTrackMenu, self.addTrackButton, 
                                                                            self.plotMultiTrackButton, clearAll])
        # Adding actions to control frameNumber slider widget
        self.addTrackButton.on_click(self.addingNewTrack)
        self.plotMultiTrackButton.on_click(self.plottingTracks)
        self.check.on_trait_change(self.addTracks, 'value')
        
        if self.container is None:
            # Container that holds all widgets
            self.container = widgets.ContainerWidget(children = [self.selectStorm, self.frameNumber, add, subtract,
                                                                self.modelSelection, self.check, self.addNewTrack])
            display(self.container)
    
        self.container.visible = True
    
    # Method to clear multi track dictionaries    
    def clearPlot(self,b):
        for line in self.multiArtistDict.values():
            line.remove()
        self.multiArtistDict.clear()
        self.multiTrackDict.clear()
        self.modelList = []
    
    # Method to make visible the widgets to add tracks to plot
    def addTracks(self, name, value):
        self.clearPlot(0)
        if value:
            self.modelSelection.disabled = True
            self.addNewTrack.visible = True
        else:
            self.modelSelection.disabled = False
            self.addNewTrack.visible = False
    
    # Method to advance frame number by one
    def advanceFrame(self, b):
        if self.addNewTrack.visible is True:
            if self.frameNumber.value < len(self.allTimes)-1:
                self.frameNumber.value += 1
        else:
            if self.frameNumber.value < len(self.time)-1:
                self.frameNumber.value += 1
        
    # Method to retract frame by one
    def subtractFrame(self, b):
        if self.addNewTrack.visible is True:
            if self.frameNumber.value > 0:
                self.frameNumber.value -= 1
        else:
            if self.frameNumber.value > 0:
                self.frameNumber.value -= 1        
     
    # Method to add events to frameNumber slider   
    def updateUI(self):
        # Adjust frameNumber length to correspond to the forecast times for the selected model
        if self.addNewTrack.visible is True:
            self.frameNumber.max = len(self.allTimes) - 1
            self.init_multi()            
        else:
            self.frameNumber.max = len(self.time) - 1
            self.init_trackPlot()
        
        # Adding appropriate action for the frameNumber slider     
        self.frameNumber.on_trait_change(self.update_trackPlot, 'value', remove=self.addNewTrack.visible)        
        self.frameNumber.on_trait_change(self.update_multi, 'value', remove=not self.addNewTrack.visible)
    
    # Re-drawing map for display        
    def refreshDisplay(self):
        self.fig.canvas.draw()
        clear_output(wait=True)
        display(self.fig)
    
    # Method called to re-assimilate data and frameNumber slider for newly selected model    
    def setModel(self, newModel):
        self.manageData(newModel)
        self.updateUI()
    
    # Method called when new model is selected
    def onChangeModel(self, traitName, newModel):
        self.frameNumber.value = 0
        self.setModel(newModel)
        self.refreshDisplay()
    
    # Method called when models are selected for multiple track plot    
    def addingNewTrack(self, b):
        self.modelList.append(self.newTrackMenu.value)
    
    # Method to create multiple track dictionaries           
    def plottingTracks(self, b):
        self.updateModelTitle()
        self.frameNumber.value = 0
        self.refreshDisplay()
        # Setting up color cycle for multiple tracks
        colormap = plt.cm.gist_rainbow
        color_cycle = ([colormap(i) for i in np.linspace(0, 0.9, len(self.modelList))])
        self.alltimes = []
        # FOR look to create data for tracks and to set color for track
        for i in range(len(self.modelList)):
            self.trackColor = color_cycle[i]
            self.manageData(self.modelList[i])
            self.alltimes += self.time
        
        # Creating an array of times from all selected tracks    
        self.allTimes = sorted(list(set(self.alltimes)))
        self.updateUI()
    
    # Method to display title(s) selected    
    def updateModelTitle(self):            
        if self.addNewTrack.visible is True:
            self.modelTitle.set_text("Plotting Models: %s" % '\n'.join(self.modelList))
        else:
            self.modelTitle.set_text("Plotting Model: %s" % self.modelChosen)
    
    # Method to set up data dictionariers for selected model
    def manageData(self,  model = None):
        self.modelChosen = model
        self.updateModelTitle()
        
        # Reset dictionary of lines -- also need to remove from plot
        for line in self.artistDict.values():
            line.remove()
        self.artistDict.clear()

        # Selecting data for a specific model, Model. Grouping by warning data and time
        forecast2 = self.forecast[self.forecast.Group == self.modelChosen]
        self.timesInGroup = forecast2.groupby(["WarnDT"])
        modelsInGroup = forecast2.groupby(["Model"])
        
        # MasterDict order: {"WarnDT":{"model":[lonlats]} }
        self.masterDict = {}
        for x in sorted(self.timesInGroup.groups):
            self.masterDict[x] = {}

        self.time = []
        for times in sorted(self.timesInGroup.groups):
            self.time.append(times)
            warningTimes = forecast2.loc[self.timesInGroup.groups[times]]
            warndtModels = warningTimes.groupby(["Model"])
            for model in sorted(warndtModels.groups):
                # Eliminating erroneous lattitude and longitude data
                modelPlot = forecast2.loc[warndtModels.groups[model]]
                modelPlot = modelPlot[modelPlot.Lon != 0]
                self.masterDict[times][model] = self.map(modelPlot["Lon"].values, modelPlot["Lat"].values)

        # Filling in dictionaries for multi track plot use
        for line in modelsInGroup.groups:
            if self.addNewTrack.visible is True:
                self.multiTrackDict[line] = self.masterDict
                self.multiArtistDict[line], = self.map.plot([], [], linewidth=2.0, color = self.trackColor, zorder=5)
            else:
                self.artistDict[line], = self.map.plot([], [], linewidth=2.0, zorder=5)        
    
    # Method to create plotting titles, text, and best track line
    def plotDetails(self):
        stormStuff = StormNameData().splitStormInfo()
        self.stormName = stormStuff[(stormStuff.Year == self.forecast["WarnDT"][0][:4]) & 
                                    (stormStuff.Basin == self.forecast["Basin"][0]) &                            
                                    (stormStuff.CycloneNum == self.forecast["CycloneNum"][0])]
        titlestring ="Storm Name: %s   Storm Number: %-4s Year: %-6s" % \
                    (self.stormName.Name.values[0], self.forecast["CycloneNum"].values[0],
                    self.forecast["WarnDT"][0][:4])
                    
        self.ax.set_title(titlestring, fontsize=13)
        
        self.modelTitle = self.ax.text(1.35, 1.05, "", horizontalalignment='right', verticalalignment = "top",
                                       transform=self.ax.transAxes, fontsize = 13)
        self.lineb, = self.map.plot([],[], linewidth=2.5, linestyle = '--', color='b', zorder=4)
        self.lonlatsbest = self.map(self.best["Lon"].values, self.best["Lat"].values)    
        self.time_template = 'Date/Time of Warning: %s'
        self.time_text = self.ax.text(0.03, 0.05, '', backgroundcolor='white', transform=self.ax.transAxes,
                                      color='red', fontsize=15.0)
    
    # Method to create map for storm specific basin           
    def createMap(self, basinName, ax=None):
        if ax is None:
            ax = plt.gca()

        mapParam = {"EP":[-10.0,60.0,-150.0,-80.0], "CP":[-10.0,60.0,-180.0,-130.0],
                    "AL":[-5.0,60.0,-110.0,-5.0], "SL":[10.0,-40.0,-100.0,-10.0],            
                    "WP":[-10.0,60.0,110.0,-170], "IO":[-10.0,30.0,30.0,110.0],            
                    "SH":[-50.0,10.0,30.0,150.0]}
                    
        # Create polar stereographic Basemap instance.
        self.bm = Basemap(projection='mill',
                    llcrnrlat= mapParam[basinName][0],urcrnrlat= mapParam[basinName][1],                    
                    llcrnrlon= mapParam[basinName][2],urcrnrlon= mapParam[basinName][3],                    
                    rsphere=6371200.,resolution='c', ax=ax)
                    
        # Draw coastlines and fills in colors.
        self.bm.drawcoastlines()
        self.bm.fillcontinents(color = 'tan',lake_color='aqua')
        self.bm.drawmapboundary(fill_color='aqua')
        # Draw parallels.
        parallels = np.arange(0.,90,10.)
        self.bm.drawparallels(parallels,labels=[1,0,0,0],fontsize=8)
        # Draw meridians
        meridians = np.arange(180.,360.,10.)
        self.bm.drawmeridians(meridians,labels=[0,0,0,1],fontsize=8)
        return self.bm
        
    # Functions to initialize and animate single model track plots
    def init_trackPlot(self):
        self.lineb.set_data(self.lonlatsbest)
        self.time_text.set_text('')
        for line in self.artistDict:
            self.artistDict[line].set_data([], [])
    
    def update_trackPlot(self, value, Time):
        self.time_text.set_text(self.time_template % self.time[Time])
        for line in self.artistDict.keys():
            framedata = self.masterDict[sorted(self.timesInGroup.groups.keys())[Time]]
            if line in framedata:
                self.artistDict[line].set_data(framedata[line])
            else:
                self.artistDict[line].set_data([],[])
    
        self.refreshDisplay()
    
    # Functions to initialize and animate multiple model track plots    
    def init_multi(self):
        self.lineb.set_data(self.lonlatsbest)
        self.time_text.set_text('')
        for line in self.multiArtistDict:
            self.multiArtistDict[line].set_data([], [])

    def update_multi(self, value, time):
        self.time_text.set_text(self.time_template % self.allTimes[time])
        for model in self.multiTrackDict.keys():
            if self.allTimes[time] in self.multiTrackDict[model].keys():
                for ensembleMember in self.multiTrackDict[model][self.allTimes[time]].keys():
                    framedata = self.multiTrackDict[model][self.allTimes[time]]
                    if ensembleMember in framedata:
                        self.multiArtistDict[ensembleMember].set_data(framedata[ensembleMember])
                    else:
                        self.multiArtistDict[ensembleMember].set_data([],[])
            else:
                self.multiArtistDict[model].set_data([],[])
                
        self.refreshDisplay()

# Command to run storm selector widgets
ss = StormSelector()

# Function to re-select strom from storm selector widgets
def selectNewStorm(b):
    tt.container.visible = False
    ss.stormSelector.visible = True

# Funtion to hide storm selector widgets and to run plotting class
def toPlottingFunction(b):
    ss.stormSelector.visible = False
    global tt 
    tt = Plotting(HandleStormData(ss))
    

