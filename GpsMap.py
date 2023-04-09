import time
import osmnx as ox
import matplotlib
matplotlib.use('TkAgg')
import geopandas as gpd
import folium
from folium.plugins import draw
import taxicab as tc
import matplotlib.pyplot as plt
import webbrowser
class Map:
    def __init__(self, location="London", settings=None):
        self.location = location
        self.settings = settings
        self.zoom = 10
        self.visible = False
        self.map=None
        self.graph=None




            
    def startMapNavigation(self):
        print("Map navigation started.")
    
    def setMapLocation(self, location):
        self.location = location
    
    def setMapZoom(self, zoom):
        self.zoom = zoom
    
    def setMapSettings(self, settings):
        self.settings = settings
    
    
    def shortRoute(self,G):
        

        # impute edge (driving) speeds and calculate edge traversal times
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)

        # convert string address into geographical coordinates
        def geocode_address(address, crs=4326):
            geocode = gpd.tools.geocode(address, provider='nominatim', 
                        user_agent="drive time demo").to_crs(crs)
            return (geocode.iloc[0].geometry.y, geocode.iloc[0].geometry.x)

        # get origin and destination coordinates
        origin_point = geocode_address("Whimbrel Place, Woronora Heights, NSW")
        destination_point = geocode_address("Prince Edward Park, Woronora, NSW")
        

        # get closes graph nodes to origin and destination
        orig_node = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0])
        destination_node = ox.distance.nearest_nodes(G, 
            destination_point[1], destination_point[0])

        # find shortest path based on travel time
        route = ox.shortest_path(G, orig_node, destination_node, weight='travel_time')
        

        fig, ax = ox.plot_graph_route(G, route, node_size=0, figsize=(40,40))


        edge_lengths = ox.utils_graph.get_route_edge_attributes(G, route, 'length') 
        total_route_length = sum(edge_lengths)
        print("Total route length in km:", total_route_length/1000)

        edge_travel_time = ox.utils_graph.get_route_edge_attributes(
            G, route, 'travel_time') 
        route_travel_time = sum(edge_travel_time)
        print("Travel time in minutes:", route_travel_time/60)


    def getOsmIDFromAddress(self,location):
        G=ox.graph_from_address(location,network_type="drive", simplify=True)
        #nodes,streets=ox.graph_to_gdfs(G)
        
        nodeList=list(G.edges(data=True))
        print("okay")
        id=nodeList[0]
        #nodeList[0]
        # for node in nodeList:
        #   print("Third node:{0}".format(node[2]["name"]))
        return id
    def getLatLonFromAddress(self,location):
        G=ox.graph_from_address(location,network_type="drive", simplify=True)
        nodes,streets=ox.graph_to_gdfs(G)
        l=list(nodes["geometry"])[0]
        lon=l.x
        lat=l.y
        return (lat,lon)


    def findShortestRoute(self, latlon1,latlon2):
        # print("finding shortest route between two nodes of osm")
        # nodes,streets=ox.graph_to_gdfs(self.graph)
        # lat=nodes[osmid]
        # lon=nodes[osmid]

        # lat2=self.graph.nodes[osmid2]
        # lon2=self.graph.nodes[osmid2]

        
        onode = ox.nearest_nodes(self.graph, latlon1[1],latlon1[0])
        
        dnode = ox.nearest_nodes(self.graph, latlon2[1],latlon2[0])
        route = ox.shortest_path(self.graph, onode, dnode, 'travel_time')
        route_map = ox.plot_route_folium(self.graph, route)
        route_map.save('test.html')
        
        print("Lat:{0} Lon:{1}".format(latlon1[1],latlon1[0]))
        print("2 Lat:{0} Lon:{1}".format(latlon2[1],latlon2[0]))

        print("onodes:{0} dnode:{1}".format(onode,dnode))
     
        
        # G = ox.graph_from_point((latlon1[1], latlon1[0]), dist=6000, network_type='drive')
        # G=self.graph
        # G = ox.speed.add_edge_speeds(G)
        # G = ox.speed.add_edge_travel_times(G)

        # orig = (latlon1[1], latlon1[0])
        # dest = (latlon2[1], latlon2[0])

       

        # route = tc.distance.shortest_path(G, orig, dest)

        # fig, ax = tc.plot.plot_graph_route(G, route, node_size=30, show=False, close=False, figsize=(10,10))
        # padding = 0.001
        # ax.scatter(orig[1], orig[0], c='lime', s=200, label='orig', marker='x')
        # ax.scatter(dest[1], dest[0], c='red', s=200, label='dest', marker='x')
        # ax.set_ylim([min([orig[0], dest[0]])-padding, max([orig[0], dest[0]])+padding])
        # ax.set_xlim([min([orig[1], dest[1]])-padding, max([orig[1], dest[1]])+padding])
        # plt.show()




        

    def getGpsLocationFromAddress(self,address):
        G=ox.graph_from_address(address,network_type="drive", simplify=True)
        nodes,streets=ox.graph_to_gdfs(G)
        l=list(nodes["geometry"])[0]
        lon=l.x
        lat=l.y
        p=[lat,lon]
        print("P:{0}".format(p))
        G = ox.graph_from_point(p, dist=100, network_type='drive')
        self.graph=G
        print("***Printing Nodes***")
        nodeList=list(G.edges(data=True))
        infoList=[]
        for node in nodeList:
         if "geometry" in node[2].keys():
          infoList.append(node[2])
          print("Third node:{0}".format(node[2]["name"]))
        print("***Printing Nodes Ended***")
        




        H = G.copy()
        H1 = G.copy()
        #H.remove_edges_from(G.edges - set(map(lambda x: tuple(x)+(0,),max_response_edges)))
        m = ox.folium.plot_graph_folium(H,tiles='openstreetmap',popup_attribute='name',opacity = 1,color = 'red',weight= 10)
        #H1.remove_edges_from(set(map(lambda x: tuple(x)+(0,),max_response_edges)))
        m = ox.folium.plot_graph_folium(H1, graph_map = m,tiles='openstreetmap',popup_attribute='name',opacity = 1,color = 'blue',weight= 10)
        m.save('test2.html')
        webbrowser.open("test2.html", new=2)
        
        #ox.plot_graph(G)
        
        
        
        #print("GNode:{0}".format(G.nodes(data=True)[0]))
        
        return infoList
        #return list["x"][0],list["y"][0]


    def showMap(self):
        print("ok")
        

    def showMapbbak(self,location=None):
        #m = folium.Map(location=[45.5236, -122.6750])
        #m.show_in_browser()
        # self.getNearLocations()
        #G=self.getNearLocations()
        import osmnx as ox
        import osmnx as ox
        point=(51.502777,-0.151250)
        G = ox.graph_from_point(point, dist=1000, network_type='drive')
        #ox.plot_graph(G)
        #ox.plot_graph(G)
        
        nodes,streets=ox.graph_to_gdfs(G)
        path = ox.shortest_path(G, G.nodes()[0], G.nodes()[1])
        out=nodes.loc[path]
        print("Nodes:{0} lat:{1}".format(out.out.lat))



        streetsOrig=streets
        streets = streets[streets.geom_type == 'Polygon'][:1000]
        print("Streets head:{0}".format(streets.head()))

        
        location=[51.502777,-0.151250]
        #G=ox.graph_from_point(point,dist=500,network_type="drive", simplify=True)
        m = folium.Map(point, zoom_start=10)
        
        
        # tags = {'building':True}
        # building = ox.geometries_from_point(point,dist=50,tags=tags)
        # print ("Head:{0}".format(building.head()))
        # buildings = building[building.geom_type == 'Polygon'][:1000]
        
        
        
        #route=self.getNearLocations()
        print("Streets:{0}".format(streets[:1000]))

        folium.GeoJson(streets[:1000]).add_to(m)
        
        folium.CircleMarker(location=location).add_to(m)
        print("columns:{0}".format(streetsOrig))
        folium.PolyLine(streetsOrig[:1000]).add_to(m)
        print("All done, program ended")
        
        m.show_in_browser()
        data = get_pos(m['last_clicked']['lat'],m['last_clicked']['lng'])
        #m.save('cafes.html')

    def getNearLocations(self,point=(51.502777,-0.151250)):
        self.visible = True        
        #point=(51.502777,-0.151250)
        G = ox.graph_from_point(point, dist=600, network_type='drive')
        #G = ox.graph_from_place('Sutherland Shire Council', network_type='all') 
        #ox.plot_graph(G)
        print("Finding nearest nodes")
        #station_st_node_id = ox.distance.nearest_nodes(G, [51.502777],[-0.151250])[0]
        station_st_node_id = ox.distance.nearest_nodes(G, [151.014898], [-34.06714])[0]
        

        G.nodes.get(station_st_node_id)
        # --> {'street_count': 3, 'x': 151.0149055, 'y': -34.0671669}

        # find its neighbouring nodes
        list(G.neighbors(station_st_node_id))
        # --> [1839271812, 668727077]

        import json

        # show edge attributes
        for edge in G.out_edges(station_st_node_id, data=True):
            print("\n=== Edge ====")
            print("Source and target node ID:", edge[:2])
            edge_attributes = edge[2]
            # remove geometry object from output
            edge_attributes_wo_geometry = {i:edge_attributes[i] for i in edge_attributes if i!='geometry'}
            print("Edge attributes:", json.dumps(edge_attributes_wo_geometry, indent=4))


            #how long it would take to reach there
            # impute edge (driving) speeds and calculate edge traversal times
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)
        return G
        #self.shortRoute(G)
       
        
    
    def hideMap(self):
        self.visible = False
        print("Map is now hidden.")