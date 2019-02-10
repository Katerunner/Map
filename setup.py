try:
    import folium
    from geopy.geocoders import Nominatim
    from tqdm import tqdm
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    from geopy.extra.rate_limiter import RateLimiter
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    import random
except:
    print('\nOhh, seems like you dont have all libraries (modules).\n\nRequired libraries (modules):\n- TQDM (pip install tqdm)\n- Folium (pip install folium)\n- Geopy (pip install geopy)\n')
    exit()


def create_map():

    """
    Creates map with several tile layers
    """

    global map

    map = folium.Map(tiles ='mapbox bright', attr = 'Thank you')

    folium.TileLayer('Mapbox Bright', attr = 'Thank you', name = "Mapbox Bright").add_to(map)
    folium.TileLayer('Mapbox Control Room', attr = 'Thank you', name = "Mapbox Control Room").add_to(map)
    folium.TileLayer('stamenterrain', attr = 'Thank you', name = "Stamen Terrain").add_to(map)
    folium.TileLayer('stamentoner', attr = 'Thank you', name = "Stamen Toner").add_to(map)
    folium.TileLayer('stamenwatercolor', attr = 'Thank you', name = "Stamen Water Color").add_to(map)
    folium.TileLayer('cartodbpositron', attr = 'Thank you', name = "Cartodbpositron").add_to(map)
    folium.TileLayer('cartodbdark_matter', attr = 'Thank you', name = "Cartodbdark Matter").add_to(map)



def add_groups():
    """
    Adds 3 feature groups to the map
    """

    global map, eua, ame, asi, eua_lim, ame_lim, asi_lim

    eua = folium.FeatureGroup(name="Europe, Africa and West Asia")
    eua_lim = (-30, 60)
    ame = folium.FeatureGroup(name="North and South America")
    ame_lim = (-180, -30)
    asi = folium.FeatureGroup(name="Asia, Australia and Oceania")
    asi_lim = (60, 180)

    map.add_child(eua)
    map.add_child(ame)
    map.add_child(asi)



def add_countries(con_file):
    """
    Adds countries' borders and colors them by population,
    Adds countries' names markers
    """


    global map, world

    world = folium.GeoJson(name = "Countries", data=open('world.json', 'r',
    encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor':'green'
    if x['properties']['POP2005'] < 10000000
    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
    else 'red'})


    q = open(con_file, 'r')

    c_data = q.readlines()

    for i in c_data[1:]:
        temp = i.strip().split('\t')
        try:
            world.add_child(folium.CircleMarker(location=[float(temp[1]), float(temp[2])],
                    radius=10,
                    popup=temp[-1] + " " + temp[0],
                    fill_color='yellow',
                    color=None,
                    fill_opacity=0.2))
        except:
            pass

    map.add_child(world)




def wel_input():
    """
    Welcomes and asks for state, year. Also creates title
    """


    global state, inyear, title

    print("\nWelcome! This is a program in which you can create a HTML file with map and location of films in a year you choose.")
    print("After you type the year the program will create a HTML file with name 'Film_Location_Year_1920_Map.html' when 1920 is chosen year.")
    print("\nNow, print working mode,\nStatic - HTML file will be created after program completes its work (It is a little bit faster).\nDynamic - Program will add locations dynamicly so you can use your brawser to open html file in procces and see current result. (F5 to refresh in browser)")
    state = input("Mode: (s - static, d - dynamic): ")
    while True:
        if state != 's' and state != 'd':
            print("Try again:")
            state = input("Mode: (s - static, d - dynamic): ")
        else:
            break
    print("You will see all progress on the console screen.\nIt will take a time.\n")

    inyear = input("Type a year: ")

    while True:
        try:
            if int(inyear) >= 0 and int(inyear) <= 3000:
                break
            else:
                inyear = input("Try type a year again: ")
        except:
            inyear = input("Try type a year again: ")

    inyear = int(inyear)

    title = "Film_Location_Year_" + str(inyear) + "_Map.html"

    print("\nloading...")



def search_year(film_file):
    """
    Creates dict with films for certain year
    """

    global setik, dikt, loc, year, film

    setik = set()
    dikt = {}

    f = open(film_file, 'r')

    file =  f.readlines()[14:]

    print("\nProgram is searching films with" , inyear, "year:\n")

    for i in tqdm(file):
        try:
            film = i.strip().split('\t')[0]
            loc = i.strip().split('\t')[-1]
            if loc.endswith(")"):
                loc = i.strip().split('\t')[-2]
            loc = ", ".join(loc.split(", ")[-3:])
            year = int(film[film.index("(")+1:film.index(")")])
            if year == inyear:
                dikt[film] = loc
        except:
            pass



def add_markers():
    """
    Adds film location markers to the map
    """

    print("\nProgram is putting film locations on the map.\nFilms completed:\n")

    for i in tqdm(dikt):
        try:
            location = geolocator.geocode(dikt[i])

            if (location.latitude, location.longitude) in setik:
                pass
            else:
                setik.add((location.latitude, location.longitude))
                if location.longitude >= eua_lim[0] and location.longitude <= eua_lim[1]:
                    eua.add_child(folium.Marker(location=[location.latitude, location.longitude],
                    popup=i,
                    icon=folium.Icon(color = 'green')))
                elif location.longitude >= ame_lim[0] and location.longitude <= ame_lim[1]:
                    ame.add_child(folium.Marker(location=[location.latitude, location.longitude],
                    popup=i,
                    icon=folium.Icon(color = 'blue')))
                else:
                    asi.add_child(folium.Marker(location=[location.latitude, location.longitude],
                    popup=i,
                    icon=folium.Icon(color = 'red')))
                if state == 'd':
                    tmp = random.randrange(1,4)
                    if tmp == 3:
                        map.save(title)
        except:
            pass



def ending():
    """
    Adds layer control, saves and goodbye
    """
    map.add_child(folium.LayerControl())
    map.save(title)
    print("\nYeah! We made it to the end!\nGood luck ;)\n")



if __name__ == "__main__":
    create_map()
    add_groups()
    add_countries('countries.txt')
    wel_input()
    search_year('locations.list')
    add_markers()
    ending()
