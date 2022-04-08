@app.get("/country/{country_name}")
async def getCountry(country_name, coords_only: bool = False):
    """
    ### Description:
        Get a country polygon given a country name.
    ### Params:
        country_name (str)  : A country name to search for
    ### Returns:
        dict / json
    ## Example:
    [http://127.0.0.1:8080/country/chad](http://127.0.0.1:8080/country/chad)
    ### Results:
    ```json
    {
        "type": "Feature",
        "id": "kk522dt9425.221",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
            [
                [
                [
                    23.98130579,
                    19.49612376
                ],
                [
                    23.98151249,
                    19.2638382
                ],
        ...
    }
    ```
    [http://127.0.0.1:8080/country/Niger?coords_only=True](http://127.0.0.1:8080/country/Niger?coords_only=True)

    ```json
    ### Results:
    [
      [
        [
        [
            23.98130579,
            19.49612376
        ],
        [
            23.98151249,
            19.2638382
        ],
        [
            23.9817192,
            19.03155263
        ],
        ...
    ]
    ```
    """
    # lowercase the country name then capitalize to fit the existing names.
    country_name = country_name.lower().title()

    # Go get the polygons
    polys = countryDB.getPolygons(country_name)

    largest = largestPoly(polys["geometry"]["coordinates"])

    if not polys:
        return {"Error": f"Country: {country_name} didn't exist!"}

    # Remove extra geodata info if coords_only is True
    if coords_only:
        return largest

    f = Feature(coords=largest, properties={"name": country_name})

    fc = FeatureCollection()
    fc.addFeature(feature=f)

    return fc


@app.get("/countryCenter/{country_name}")
async def countryCenter(country_name, raw: bool = False):
    """
    ### Description:
        Get a point that represents the spaital center of a countries polygon.
    ### Params:
        country_name (str)  : A country name to search for
    ### OptionalParams
        raw (bool)          : True = send coords only, no feature crap
    ### Returns:
        dict : json Feature collection
        list : center point (if raw = True)
    ## Examples:

    [http://127.0.0.1:8080/countryCenter/united%20kingdom](http://127.0.0.1:8080/countryCenter/united%20kingdom)

    ### Results:
    ```json
    {
        "type": "FeatureCollection",
        "features": [
            {
            "feature": {
                "type": "Feature",
                "geometry": {
                "type": "Point",
                "coordinates": [
                    -3.082751279583333,
                    54.005709779374996
                ]
                },
                "properties": {
                "name": "United Kingdom"
                }
            }
            }
        ]
    }
    ```

    [http://127.0.0.1:8080/countryCenter/united%20kingdom?raw=true](http://127.0.0.1:8080/countryCenter/united%20kingdom?raw=true)

    ### Results:
    ```json
    [
        -3.082751279583333,
        54.005709779374996
    ]
    ```
    """

    # lowercase the country name then capitalize to fit the existing names.
    country_name = country_name.lower().title()

    coll = FeatureCollection()
    centers = []
    country = countryDB.getPolygons(country_name)
    largest = largestPoly(country["geometry"]["coordinates"])

    print(largest)
    center = centroid(largest)

    if raw:
        return center

    feature = Feature(coords=center,
                      type="Point",
                      properties={"name": country["properties"]["name"]})
    centers.append(center)
    coll.addFeature(feature=feature)

    return coll.to_json()


@app.get("/country_lookup/{key}")
async def getCountryPartialMatch(key):
    """
    ### Description:
        Get country names that partially match the key passed in.
    ### Params:
        key (str)  : a substring compared with the beginning of every country name.
    ### Returns:
        list / json

    ## Example:
    [http://127.0.0.1:8080/country_lookup/ga](http://127.0.0.1:8080/country_lookup/ga)

    ### Results:
    ```json

    [
    "Gabon",
    "Gambia"
    ]
    """
    key = key.lower()
    partial = []
    names = countryDB.getNames()
    for name in names:
        low_name = name.lower()
        if low_name.startswith(key):
            partial.append(name)
    return partial


@app.get("/line_between/")
async def getLineBetween(start: str = None, end: str = None):
    """
    ### Description:
        Get a line feature that connects two country centroids
    ### Params:
        start (str) : country name
        end (str) : country name
    ### Returns:
        feature / coords
    ## Example:

    [http://localhost:8080/line_between/?start=finland&end=greenland](http://localhost:8080/line_between/?start=finland&end=greenland)

    ### Results:
    ```json
    {
        "type": "Feature",
        "geometry": {
            "type": "MultiLineString",
            "coordinates": [
            [
                [
                25.83077124897437,
                65.34954882461537
                ],
                [
                -40.8824912878788,
                74.1543870603788
                ]
            ]
            ]
        },
        "properties": {
            "from": "finland",
            "to": "greenland"
        }
    }
    ```
    """
    p1 = countryCentroid(start)
    p2 = countryCentroid(end)

    feature = Feature(
        coords=[[p1, p2]],
        type="LineString",
        properties={
            "from": start,
            "to": end
        },
    )

    return feature.to_json()


@app.get("/property/{country}")
async def getProperty(country, key: str = None, allKeys: bool = False):
    """
    ### Description:
        Get a property from a country or all of them.
    ### Params:
        country (str)  : name of the country
        key (str) : the key value in the properties dictionary
        allKeys (bool) : return all the property keys
    ### Returns:
        bearingious : string, object, list, etc.
    ## Examples:

    [http://127.0.0.1:8080/property/france?key=bbox](http://127.0.0.1:8080/property/france?key=bbox)

    #### Response:
    ```
    [
        -54.5247542,
        2.05338919,
        9.56001631,
        51.14850617
    ]
    ```

    [http://127.0.0.1:8080/property/united%20kingdom?allKeys=false](http://127.0.0.1:8080/property/united%20kingdom?allKeys=false)

    #### Response:
    ```
    {
        "scalerank": 1,
        "featurecla": "Admin-0 country",
        "labelrank": 2,
        "sovereignt": "United Kingdom",
        "sov_a3": "GB1",
        "adm0_dif": 1,
        "level": 2,
        "type": "Country",
        "admin": "United Kingdom",
        "adm0_a3": "GBR",
        "geou_dif": 0,
        "geounit": "United Kingdom",
        "gu_a3": "GBR",
        "su_dif": 0,
        "subunit": "United Kingdom",
        "su_a3": "GBR",
        ...
    }
    ```
    """

    # lowercase the country name then capitalize to fit the existing names.
    country = country.lower().title()
    data = countryDB.getProperties(country)

    if key:
        return data[key]

    if allKeys:
        return list(data.keys())

    return data


@app.get("/bbox/{country}")
async def getBbox(country, raw: bool = False):
    """
    ### Description:
        Get a polygon formattexd bbox from a country's properties.
    ### Params:
        country (str)  : name of the country
        raw (bool) : return the raw bounding box (extremes W,S,E,N) and not a polygon
    ### Returns:
        list/Feature : either raw list of extreme points, or a feature with a polygon bbox
    ## Examples:
    [http://127.0.0.1:8080/bbox/united%20kingdom?raw=false](http://127.0.0.1:8080/bbox/united%20kingdom?raw=false)
    #### Response:
    ```
        {
        "feature": {
                "type": "Feature",
                "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                                [
                                        [
                                                -7.57216793,
                                                49.9599999
                                        ],
                                        [
                                                1.6815308,
                                                49.9599999
                                        ],
                                        [
                                                1.6815308,
                                                58.63500011
                                        ],
                                        [
                                                -7.57216793,
                                                58.63500011
                                        ],
                                        [
                                                -7.57216793,
                                                49.9599999
                                        ]
                                ]
                        ]
                },
                "properties": {
                        "country": "United Kingdom"
                }
        }
    }
    ```
    [http://127.0.0.1:8080/bbox/ireland?raw=true](http://127.0.0.1:8080/bbox/ireland?raw=true)

    ### Response:
    ```
    [
        -9.97708574,
        51.66930126,
        -6.0329854,
        55.13162222
    ]
    ```
    """
    country = country.lower().title()
    bbox = countryDB.getBbox(country)

    if raw:
        return bbox

    west, south, east, north = tuple(bbox)

    poly = [[west, south], [east, south], [east, north], [west, north],
            [west, south]]

    feature = Feature(coords=[poly], properties={"country": country}).to_json()
    print(feature)
    return feature


@app.get("/bboxCenter/{country}")
async def getbboxCenter(country, raw: bool = False):
    """
    ### Description:
        Get a center point from a country's bbox.
    ### Params:
        country (str)  : name of the country
        raw (bool) : return the raw point and not a feature
    ### Returns:
        point/Feature : either center point [x,y], or a feature with the point in it
    ## Examples:
    [http://127.0.0.1:8080/centerPoint/united%20kingdom?raw=false](http://127.0.0.1:8080/centerPoint/united%20kingdom?raw=false)
    #### Response:
    ```
    {
    "feature":{
        "type":"Feature",
        "geometry":{
            "type":"Point",
            "coordinates":[
                -8.00503557,
                53.40046174
            ]
        },
        "properties":{
            "country":"Ireland"
        }
    }
    }
    ```
    [http://127.0.0.1:8080/centerPoint/ireland?raw=true](http://127.0.0.1:8080/centerPoint/ireland?raw=true)

    ### Response:
    ```
    [
        -8.00503557,
        53.40046174
    ]
    ```
    """
    country = country.lower().title()
    bbox = countryDB.getBbox(country)

    west, south, east, north = tuple(bbox)

    center = [(west + east) / 2.0, (north + south) / 2.0]

    if raw:
        return center

    feature = Feature(coords=center, properties={"country": country}).to_json()
    print(feature)
    return feature


@app.get("/centroidRelations/")
async def centroidRelations(start: str, end: str):
    """
    ### Description:
        Get the distance between 2 polygon centroids. This is meant for you to improve on!
        Also get the bearing between the two centroids.
    ### Params:
        start (str)  : name of country
        end (str) : name of country
    ### Returns:
        dict: {"distance":float, "bearing":float}
            distance in miles
            bearing between the two
        Line: A line feature between the two

    ## Examples:

    [http://localhost:8080/centroidRelations/?start=france&end=greece](http://localhost:8080/centroidRelations/?start=france&end=greece)

    ### Results
    ```json
    {
    "distance": 1114.8495334378304,
    "bearing": 109.29581652664211,
    "line": {
        "feature": {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
            [
                3.245872756458333,
                47.023721337291676
            ],
            [
                23.223037302790694,
                39.80152575325582
            ]
            ]
        },
        "properties": {
            "from": "france",
            "to": "greece"
        }
        }
    }
    }
    ```
    """
    lon1, lat1 = countryCentroid(start)
    lon2, lat2 = countryCentroid(end)

    feature = Feature(
        coords=[[lon1, lat1], [lon2, lat2]],
        type="LineString",
        properties={
            "from": start,
            "to": end
        },
    )

    print(lon1, lat1)
    print(lon2, lat2)

    # lon1, lat1, lon2, lat2,
    distance = haversineDistance(lon1, lat1, lon2, lat2)
    bearing = compass_bearing((lat1, lon1), (lat2, lon2))

    feature = feature.to_json()

    return {
        "distance": distance,
        "bearing": bearing,
        "line": feature,
    }


@app.get("/borderRelations/")
async def borderRelations(start: str, end: str):
    """
    ### Description:
        Get the distance between 2 polygons in a brute force fashion. This is meant for you to improve on!
    ### Params:
        start (str)  : name of country
        end (str) : name of country
    ### Returns:
        dict: {"closest":dict, "touching":list}
            closest =  the closest two points (if distance > 0)
            OR
            list of the points that are touching

    ## Examples:

    [http://127.0.0.1:8080/borderRelations/?start=germany&end=austria](http://127.0.0.1:8080/borderRelations/?start=germany&end=austria)

    ### Response:

    ```json
    {
    "closest": {
        "points": [],
        "distance": 0
    },
    "touching": [
        [
        13.59594567,
        48.87717194
        ],
        [
        13.24335737,
        48.41611481
        ],

        12.14135746,
        47.7030834
        ],
        [
        11.42641402,
        47.52376618
        ],
        ...
    ]
    }
    ```
    """
    poly1 = countryPoly(start)
    poly2 = countryPoly(end)

    min = 999999
    closest = {}
    touching = []

    for p1 in poly1:
        lon1, lat1 = p1
        for p2 in poly2:
            lon2, lat2 = p2
            d = haversineDistance(lon1, lat1, lon2, lat2)
            if d == 0:
                touching.append(p2)
            if d < min:
                min = d
                closest = {"points": [p1, p2], "distance": d}

    if len(touching) > 0:
        closest = {"points": [], "distance": 0}
    return {"closest": closest, "touching": touching}


@app.get("/lengthLine/{country}")
async def lengthLine(country):
    """
    ### Description:
        Get a line between the furthest two points within one country polygon.
    ### Params:
        country (str)  : name of country
    ### Returns:
        feature: line between furthest two points in a countries polygon

    ## Examples:

    [http://localhost:8080/lengthLine/germany](http://localhost:8080/lengthLine/germany)

    ### Response:

    ```json
    {
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": [
        [
            12.93262699,
            47.46764558
        ],
        [
            8.52622928,
            54.96274364
        ]
        ]
    },
    "properties": {
        "country": "germany",
        "distance": 551.2008987920657
    }
    }

    ```
    """
    poly = countryPoly(country)

    max = -999999

    for p1 in poly:
        lon1, lat1 = p1
        for p2 in poly:
            lon2, lat2 = p2
            d = haversineDistance(lon1, lat1, lon2, lat2)
            if d == 0:
                continue
            if d > max:
                max = d
                maxp1 = p1
                maxp2 = p2
                maxd = d

    feature = Feature(
        coords=[maxp1, maxp2],
        type="LineString",
        properties={
            "country": country,
            "distance": maxd
        },
    )

    return feature.to_json()


@app.get("/cardinal/{degrees}")
async def cardinal(degrees):
    """
    This method works returns the cardinal direction given a bearing in decimal degrees.
    Params:
        degrees (float) : decimal degrees
    Returns:
        cardinal direction (string) : N, NNE ..... NW, NNW

    ## Examples:

    [http://localhost:8080/cardinal/76](http://localhost:8080/cardinal/76)

    ### Response:

        ```json
        {
            "direction": "ENE",
            "image": "ENE.png",
            "img_tag": "<img src='./images/ENE.png'>"
        }
        ```
    """
    dirs = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    degrees = int(float(degrees))
    ix = int((degrees + 11.25) / 22.5)
    d = dirs[ix % 16]

    return {
        "direction": d,
        "image": str(d) + ".png",
        "img_tag": f"<img src='./images/{d}.png'>",
    }