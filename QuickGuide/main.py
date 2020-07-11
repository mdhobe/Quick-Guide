from tkinter import *
from tkinter import ttk
import requests, json
import tkinter.messagebox
from geopy.geocoders import Nominatim

latitude, longitude = 0, 0
amenity = ('animal_boarding', 'animal_shelter', 'arts_centre', 'atm', 'baby_hatch', 'baking_oven', 'bank', 'bar', 'bbq', 'bench', 'bicycle_parking', 'bicycle_rental', 'bicycle_repair_station', 'biergarden', 'boat_rental', 'boat_sharing', 'bureau_de_change', 'bus_station', 'cafe', 'car_rental', 'car_sharing', 'car_wash', 'casino', 'charging_station', 'childcare', 'cinema', 'clinic', 'clock', 'college', 'community_centre', 'conference_centre', 'courthouse', 'crematorium', 'dentist', 'dive_centre', 'doctors', 'drinking_water', 'driving_school', 'embassy', 'fast_food', 'ferry_terminal', 'fire_station', 'food_court', 'fountain', 'fuel', 'gambling', 'give_box', 'grave_yard', 'grit_bin', 'hospital', 'hunting_stand', 'ice_cream', 'internet_cafe', 'kindergarten', 'kitchen', 'kneipp_water_cure', 'language_school', 'library', 'marketplace', 'monastery', 'motorcycle_parking', 'music_school', 'nightclub', 'nursing_home', 'parking', 'parking_entrance', 'parking_space', 'pharmacy', 'photo_booth', 'place_of_worship', 'planetarium', 'police', 'post_box', 'post_depot', 'post_office', 'prison', 'pub', 'public_bath', 'public_bookcase', 'ranger_station', 'recycling', 'refugee_site', 'restaurant', 'sanitary_dump_station', 'school', 'shelter', 'shower', 'social_centre', 'social_facility', 'studio', 'taxi', 'telephone', 'theatre', 'toilets', 'townhall', 'toy_library', 'university', 'vehicle_inspection', 'vending_machine', 'veterinary', 'waste_basket', 'waste_disposal', 'waste_transfer_station', 'water_point', 'watering_place')
color = ['blue', 'red', 'orange', 'green', 'black', 'purple', 'brown', 'tomato3', 'VioletRed4', 'magenta']
def get_nearest_location():
    global latitude, longitude
    res = requests.get('http://ipinfo.io/')
    data = res.json()
    region = data['region']
    city = data['city']
    loc = data['loc'].split(",")
    latitude = loc[0]
    longitude = loc[1]
    state_name.config(text="State : "+str(region))
    city_name.config(text="City : "+str(city))

def get_osm_data():
    if latitude == 0 and longitude == 0:
        tkinter.messagebox.showerror("Error Quick Guide", "First Click on\nGet Near City Location Button"
                                                          "\nto get City and Region Update")

    else:
        output = extract_raw_data_from_OSM(get_query())
        element = output['elements']
        listbox.delete(0, END)
        for ele in element:
            listbox.insert(END, ele)
            index = element.index(ele)
            listbox.itemconfig(index, {'fg': color[index % len(color)]})

def get_custom_osm_data():
    global latitude, longitude
    add = address.get()
    latitude, longitude = float(latitude_entry.get()), float(longitude_entry.get())
    if add != "":
        nom = Nominatim(user_agent="Project")
        n = nom.geocode(add)
        latitude, longitude = n.latitude, n.longitude
    if -90 <= float(latitude) and float(latitude) <= 90 and -180 <= float(longitude) and float(longitude) <= 180:
        output = extract_raw_data_from_OSM(get_custom_query())
        element = output['elements']
        listbox.delete(0, END)
        for ele in element:
            listbox.insert(END, ele)
            index = element.index(ele)
            listbox.itemconfig(index, {'fg': color[index % len(color)]})
    else:
        tkinter.messagebox.showerror("Error Quick Guide", "Latitude range (-90 to +90) & Longitude range (-180 to +180)")

def get_query():
    first = """[out:json][timeout:900];(node[amenity="""
    second = """](around:"""
    last = """););out body;>;out skel qt;"""
    q = str(scale_value.get()) + ',' + str(latitude) + ',' + str(longitude)
    built_query = first + str(drop.get()) + second + q + last
    return built_query

def get_custom_query():
    first = """[out:json][timeout:900];(node[amenity="""
    second = """](around:"""
    last = """););out body;>;out skel qt;"""
    q = str(scale_value_cutom.get()) + ',' + str(latitude) + ',' + str(longitude)
    built_query = first + str(drop_custom.get()) + second + q + last
    return built_query

def extract_raw_data_from_OSM(built_query):
    overpass_url = "http://overpass-api.de/api/interpreter"
    response = requests.get(overpass_url, params={'data': built_query})
    json_data = response.json()
    return json_data

def save_json():
    output = extract_raw_data_from_OSM(get_query())
    result = str(drop.get()) + "_" + str(latitude) + "_" + str(longitude) + "_" + str(int(scale_value.get())) + ".json"
    with open(result, "w") as outfile:
        json.dump(output, outfile)
    tkinter.messagebox.showinfo("Save Quick Guide", "Saved as\n"+result)

def save_txt():
    output = extract_raw_data_from_OSM(get_query())
    result = str(drop.get()) + "_" + str(latitude) + "_" + str(longitude) + "_" + str(int(scale_value.get())) + ".txt"
    with open(result, "w") as outfile:
        json.dump(output, outfile)
    tkinter.messagebox.showinfo("Save Quick Guide", "Saved as\n"+result)

def show_query():
    query.delete(0, END)
    query.insert(END, get_query())
    tkinter.messagebox.showinfo("Show Map Quick Guide", "Copy and Paste the query in below box and paste in Overpass turo")

# Driver code
if __name__ == "__main__" :
    root = Tk()
    root.geometry("1000x700")
    root.resizable(False, False)
    root.title("Quick Guide")

    headlabel = Label(root, text='Welcome to Quick India Guide')
    headlabel.place(x=400, y=10)

    top_frame = LabelFrame(root, text="Use nearest city location", height=130, width=1000)
    top_frame.pack(padx=10, pady=10)

    get_location = Button(top_frame, text="Get Near City Location", command=get_nearest_location, width=35)
    get_location.place(x=50, y=10)

    state_name = Label(top_frame, text='State : State_name')
    state_name.place(x=380, y=13)

    city_name = Label(top_frame, text='City : City_name')
    city_name.place(x=680, y=13)

    scale_value = DoubleVar()
    scale = Scale(top_frame, variable=scale_value, from_=1, to=40000, orient=HORIZONTAL, label="Radius (meters)")
    scale.set(2000)
    scale.place(x=380, y=40)

    get_osm_details_custom = Button(top_frame, text="Search", command=get_osm_data, width=35)
    get_osm_details_custom.place(x=680, y=60)

    click_amenity = StringVar()
    drop = ttk.Combobox(top_frame, textvariable=click_amenity, width=38)
    drop.place(x=50, y=60)
    drop['values'] = amenity
    drop.current(49)

    middle_frame = LabelFrame(root, text="Custom city location", height=180, width=1000)
    middle_frame.pack(padx=10, pady=10)

    address_name = Label(middle_frame, text='Place Address : ')
    address_name.place(x=10, y=10)

    address = Entry(middle_frame, width=100)
    address.place(x=100, y=10)

    eg_address_name = Label(middle_frame, text='(*example: Taj Mahal Agra Uttar Pradesh India)', fg="red")
    eg_address_name.place(x=720, y=10)

    or_extra = Label(middle_frame, text='-------------------------------------------------------------------------------------------- OR --------------------------------------------------------------------------------------------')
    or_extra.place(x=10, y=30)

    latitude_label = Label(middle_frame, text='Latitude : ')
    latitude_label.place(x=10, y=55)

    latitude_entry = Entry(middle_frame, width=35)
    latitude_entry.insert(END, '0')
    latitude_entry.place(x=70, y=55)

    longitude_label = Label(middle_frame, text='Longitude : ')
    longitude_label.place(x=320, y=55)

    longitude_entry = Entry(middle_frame, width=35)
    longitude_entry.insert(END, '0')
    longitude_entry.place(x=390, y=55)

    coordinates_comment = Label(middle_frame, text="Latitude range (-90 to +90) & Longitude range (-180 to +180)", fg="red")
    coordinates_comment.place(x=642, y=55)

    click_amenity_custom = StringVar()
    drop_custom = ttk.Combobox(middle_frame, textvariable=click_amenity_custom, width=42)
    drop_custom.place(x=10, y=110)
    drop_custom['values'] = amenity
    drop_custom.current(49)

    scale_value_cutom = DoubleVar()
    scale_custom = Scale(middle_frame, variable=scale_value_cutom, from_=1, to=40000, orient=HORIZONTAL, label="Radius (meters)")
    scale_custom.set(2000)
    scale_custom.place(x=380, y=90)

    get_osm_details = Button(middle_frame, text="Search", command=get_custom_osm_data, width=35)
    get_osm_details.place(x=680, y=110)

    save_frame = LabelFrame(root, text="Save", height=85, width=1000)
    save_frame.pack(padx=10, pady=10)

    json_button = Button(save_frame, text="Save as .json file", width=40, command=save_json)
    json_button.place(x=10, y=0)

    txt_button = Button(save_frame, text="Save as .txt file", width=40, command=save_txt)
    txt_button.place(x=340, y=0)

    map_button = Button(save_frame, text="Show in Overpass turbo for map", width=40, command=show_query)
    map_button.place(x=670, y=0)

    query = Entry(save_frame, width=158, fg='blue')
    query.insert(END, 'Query for Overpass Turbo')
    query.place(x=10, y=40)

    result_frame = LabelFrame(root, text="Result", height=200, width=1000)
    result_frame.pack(padx=10, pady=10)

    yscrollbar = Scrollbar(result_frame)
    yscrollbar.pack(side=RIGHT, fill=Y)
    xscrollbar = Scrollbar(result_frame, orient='horizontal')
    xscrollbar.pack(side=BOTTOM, fill=X)

    listbox = Listbox(result_frame, yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set, height=300, width=1000)
    listbox.pack(side=LEFT, fill=BOTH)

    yscrollbar.config(command=listbox.yview)
    xscrollbar.config(command=listbox.xview)

    root.mainloop()