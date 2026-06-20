from pymongo import MongoClient
from config import mongo_uri

client = MongoClient(mongo_uri)

db = client['SOLIS_db']

collection = db["TDs"]

TDs = [
{
    "@context": [
      "https://www.w3.org/2019/wot/td.jsonld",
      {
        "@vocab": "https://www.w3.org/2019/wot/td#",
        "saref": "http://www.w3.org/ns/saref/",
        "schema": "http://schema.org/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
      }
    ],
    "@type": "Thing",
    "title": "Reverse Geocode",
    "description": "The TomTom Reverse Geocoding API gives users a tool to translate coordinates into human-understandable street addresses, street elements, or geography. Most often needed in tracking applications where you receive a GPS feed from the device or asset and want to know the address.",
    "securityDefinitions": {
      "apikey": {
        "@type": "SecurityScheme",
        "scheme": "apikey",
        "name": "key"
      }
    },
    "security": [
      {
        "apikey": []
      }
    ],
    "properties": {
      "position": {
        "@type": "Property",
        "title": "Position",
        "description": "Position of the result in the form of latitude,longitude coordinates. Position of the entry point.",
        "forms": [
          {
            "href": "https://api.tomtom.com/search/2/reverseGeocode/{position}.{ext}",
            "op": "readproperty",
            "htv:methodName": "GET"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "description": "Comma-separated string composed by lat,lon coordinates"
        },
        "readOnly": True
      },
      "address": {
        "@type": "Property",
        "title": "Address",
        "description": "The structured address for the result.",
        "forms": [
          {
            "href": "https://api.tomtom.com/search/2/reverseGeocode/{position}.{ext}",
            "op": "readproperty",
            "htv:methodName": "GET"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "object",
          "properties": {
            "buildingNumber": {
              "@type": "DataSchema",
              "type": "string",
              "description": "Deprecated. The building number on the street."
            },
            "streetNumber": {
              "@type": "DataSchema",
              "type": "string",
              "description": "The building number on the street."
            },
            "routeNumbers": {
              "@type": "DataSchema",
              "type": "array",
              "items": {
                "@type": "DataSchema",
                "type": "string"
              },
              "description": "The codes used to unambiguously identify the street."
            },
            "streetName": {
              "@type": "DataSchema",
              "type": "string",
              "description": "The street name."
            },
            "streetNameAndNumber": {
              "@type": "DataSchema",
              "type": "string",
              "description": "The street name and number."
            },
            "speedLimit": {
              "@type": "DataSchema",
              "type": "string",
              "description": "The speed limit for the street in the form (D)(D)D.DDUUU"
            },
            "countryCode": {
              "@type": "DataSchema",
              "type": "string",
              "description": "Country. Two-letter code."
            },
            "countrySubdivision": {
              "@type": "DataSchema",
              "type": "string",
              "description": "State or Province"
            },
            "countrySecondarySubdivision": {
              "@type": "DataSchema",
              "type": "string",
              "description": "County"
            },
            "municipality": {
              "@type": "DataSchema",
              "type": "string",
              "description": "City / Town"
            },
            "postalCode": {
              "@type": "DataSchema",
              "type": "string",
              "description": "Postal Code / Zip Code"
            },
            "neighbourhood": {
              "@type": "DataSchema",
              "type": "string",
              "description": "Neighbourhood"
            },
            "country": {
              "@type": "DataSchema",
              "type": "string",
              "description": "Country name"
            },
            "countryCodeISO3": {
              "@type": "DataSchema",
              "type": "string",
              "description": "ISO 3166-1 alpha-3 country code"
            },
            "freeformAddress": {
              "@type": "DataSchema",
              "type": "string",
              "description": "An address line formatted according to the formatting rules of a Result's country of origin"
            },
            "boundingBox": {
              "@type": "DataSchema",
              "type": "object",
              "properties": {
                "northEast": {
                  "@type": "DataSchema",
                  "type": "string",
                  "description": "North-east (top-left) latitude, longitude coordinate of the bounding box"
                },
                "southWest": {
                  "@type": "DataSchema",
                  "type": "string",
                  "description": "South-west (bottom-right) latitude, longitude coordinate of the bounding box"
                },
                "entity": {
                  "@type": "DataSchema",
                  "type": "string",
                  "description": "Entity type source of the bounding box. For reverse-geocoding this is always equal to 'position'."
                }
              }
            }
          }
        },
        "readOnly": True
      },
      "summary": {
        "@type": "Property",
        "title": "Summary",
        "description": "Summary information about the search that was performed.",
        "forms": [
          {
            "href": "https://api.tomtom.com/search/2/reverseGeocode/{position}.{ext}",
            "op": "readproperty",
            "htv:methodName": "GET"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "object",
          "properties": {
            "queryTime": {
              "@type": "DataSchema",
              "type": "integer",
              "description": "The time spent on resolving the query (in milliseconds)."
            },
            "numResults": {
              "@type": "DataSchema",
              "type": "integer",
              "description": "The number of results in the response. The current version of the API returns a maximum of 1 result."
            }
          }
        },
        "readOnly": True
      }
    },
    "actions": {
      "reverseGeocode": {
        "@type": "Action",
        "title": "Reverse Geocode",
        "description": "Translate coordinates into human-understandable street addresses, street elements, or geography.",
        "forms": [
          {
            "href": "https://api.tomtom.com/search/2/reverseGeocode/{position}.{ext}",
            "op": "invokeaction",
            "htv:methodName": "GET"
          }
        ],
        "input": {
          "@type": "DataSchema",
          "type": "object",
          "properties": {
            "baseURL": {
              "@type": "DataSchema",
              "type": "string",
              "description": "Base URL for the API. Values: api.tomtom.com, kr-api.tomtom.com"
            },
            "versionNumber": {
              "@type": "DataSchema",
              "type": "integer",
              "description": "API version number. Current value is 2.",
              "default": 2
            },
            "position": {
              "@type": "DataSchema",
              "type": "string",
              "description": "Comma-separated string composed by lat,lon coordinates"
            },
            "ext": {
              "@type": "DataSchema",
              "type": "string",
              "enum": [
                "json",
                "jsonp",
                "js",
                "xml"
              ],
              "description": "Response format. Values: json, jsonp, js, or xml"
            },
            "key": {
              "@type": "DataSchema",
              "type": "string",
              "description": "An API Key valid for the requested service"
            },
            "returnSpeedLimit": {
              "@type": "DataSchema",
              "type": "boolean",
              "description": "Enables the return of the posted speed limit (where available). Default value: False",
              "default": False
            },
            "heading": {
              "@type": "DataSchema",
              "type": "number",
              "minimum": -360,
              "maximum": 360,
              "description": "The directional heading of the vehicle in degrees. 0 is North, 90 is East. Precision can include up to one decimal place."
            },
            "radius": {
              "@type": "DataSchema",
              "type": "integer",
              "unit": "meters",
              "description": "The maximum distance in meters from the specified position for the reverseGeocode to consider. Default value: 10000 meters (10 km).",
              "default": 10000
            },
            "number": {
              "@type": "DataSchema",
              "type": "integer",
              "description": "Deprecated. If a house number is sent in along with the request, the response may include the side of the street."
            },
            "returnRoadClass": {
              "@type": "DataSchema",
              "type": "boolean",
              "description": "Enables the return of the roadClass array for reverseGeocodes at street level.",
              "default": False
            },
            "returnRoadUse": {
              "@type": "DataSchema",
              "type": "boolean",
              "description": "Enables the return of the roadUse array for reverseGeocodes at street level. Deprecated support will be removed.",
              "default": False
            },
            "entityType": {
              "@type": "DataSchema",
              "type": "string",
              "enum": [
                "PostalCodeArea"
              ],
              "description": "Type of entity to return. Can be used to get geometry."
            },
            "callback": {
              "@type": "DataSchema",
              "type": "string",
              "description": "Callback function name for JSONP responses"
            },
            "language": {
              "@type": "DataSchema",
              "type": "string",
              "description": "The language in which the reverse geocode result should be returned. Default value: NGT"
            },
            "allowFreeformNewline": {
              "@type": "DataSchema",
              "type": "boolean",
              "description": "The format of newlines in the formatted address. If True, the address will contain newlines. Otherwise, newlines will be converted to spaces.",
              "default": False
            },
            "returnMatchType": {
              "@type": "DataSchema",
              "type": "boolean",
              "description": "This includes information on the type of match the geocoder achieved in the response.",
              "default": False
            },
            "view": {
              "@type": "DataSchema",
              "type": "string",
              "enum": [
                "Unified",
                "AR",
                "IL",
                "IN",
                "MA",
                "PK",
                "RU",
                "TR",
                "CN"
              ],
              "description": "Geopolitical View. The context used to resolve the handling of disputed territories."
            },
            "mapcodes": {
              "@type": "DataSchema",
              "type": "string",
              "enum": [
                "Local",
                "International",
                "Alternative"
              ],
              "description": "Enables the return of mapcodes. Can also filter the response to only show selected mapcode types."
            },
            "filter": {
              "@type": "DataSchema",
              "type": "string",
              "enum": [
                "BackRoads"
              ],
              "description": "Excludes a certain group of inspected address-carrying elements in order to find the closest match to a requested point."
            }
          },
          "required": [
            "position",
            "key"
          ]
        }
      }
    },
    "events": {},
    "headers": {
      "Accept-Encoding": {
        "@type": "Header",
        "title": "Accept-Encoding",
        "description": "Enables response compression. Value: gzip"
      },
      "Tracking-ID": {
        "@type": "Header",
        "title": "Tracking-ID",
        "description": "Specifies an identifier for the request. It can be used to trace a call. The value must match the regular expression '^[a-zA-Z0-9-]{1,100}$'. For details check RFC 4122.",
        "pattern": "^[a-zA-Z0-9-]{1,100}$"
      }
    },
    "links": [
      {
        "@type": "Link",
        "href": "https://developer.tomtom.com/reverse-geocoding-api/documentation/reverse-geocode",
        "rel": "documentation"
      }
    ]
  },
  {
    "@context": {
      "@vocab": "https://www.w3.org/ns/wot#",
      "Thing": "http://schema.org/Thing",
      "Action": "http://schema.org/Action",
      "Property": "http://schema.org/Property",
      "SecurityScheme": "http://json-schema.org/draft-07/schema#",
      "htv": "http://www.w3.org/2011/http#",
      "saref": "http://www.w3.org/ns/saref/",
      "schema": "http://schema.org/"
    },
    "@type": "Thing",
    "name": "Geoapify Reverse Geocoding API",
    "description": "A powerful and easy-to-use Reverse Geocoding API that converts latitude/longitude coordinates to complete address information. Returns well-formed addresses with parts like city, postcode, street for the given coordinates.",
    "securitySchemes": {
      "apikey": {
        "@type": "SecurityScheme",
        "scheme": "apiKey",
        "in": "query",
        "name": "apiKey"
      }
    },
    "actions": [
      {
        "@type": "Action",
        "name": "reverseGeocode",
        "description": "Convert latitude/longitude coordinates to corresponding address information. Returns a GeoJSON FeatureCollection with complete address and its parts.",
        "forms": [
          {
            "href": "https://api.geoapify.com/v1/geocode/reverse",
            "op": "read",
            "contentType": "application/json",
            "htv:methodName": "GET"
          }
        ],
        "inputDataSchema": {
          "@type": "JsonSchema",
          "properties": {
            "lat": {
              "type": "number",
              "description": "Latitude coordinate"
            },
            "lon": {
              "type": "number",
              "description": "Longitude coordinate"
            },
            "apiKey": {
              "type": "string",
              "description": "API key for authentication"
            },
            "type": {
              "type": "string",
              "enum": [
                "country",
                "state",
                "city",
                "postcode",
                "street",
                "amenity"
              ],
              "description": "Location type to search"
            },
            "limit": {
              "type": "integer",
              "description": "Maximal number of results (default: 1)"
            },
            "lang": {
              "type": "string",
              "pattern": "^[A-Za-z]{2}$",
              "description": "Result language (2-character ISO 639-1 codes)"
            },
            "format": {
              "type": "string",
              "enum": [
                "json",
                "xml",
                "geojson"
              ],
              "default": "geojson",
              "description": "Response object type"
            }
          },
          "required": [
            "lat",
            "lon",
            "apiKey"
          ]
        },
        "outputDataSchema": {
          "@type": "JsonSchema",
          "properties": {
            "features": {
              "type": "array",
              "items": {
                "@type": "object",
                "properties": {
                  "properties": {
                    "@type": "object",
                    "properties": {
                      "formatted": {
                        "type": "string"
                      },
                      "amenity": {
                        "type": [
                          "string",
                          "null"
                        ]
                      },
                      "building": {
                        "type": [
                          "string",
                          "null"
                        ]
                      },
                      "street": {
                        "type": [
                          "string",
                          "null"
                        ]
                      },
                      "suburb": {
                        "type": [
                          "string",
                          "null"
                        ]
                      },
                      "district": {
                        "type": [
                          "string",
                          "null"
                        ]
                      },
                      "postcode": {
                        "type": [
                          "string",
                          "null"
                        ]
                      },
                      "city": {
                        "type": [
                          "string",
                          "null"
                        ]
                      },
                      "county": {
                        "type": [
                          "string",
                          "null"
                        ]
                      },
                      "state": {
                        "type": [
                          "string",
                          "null"
                        ]
                      },
                      "country": {
                        "type": [
                          "string",
                          "null"
                        ]
                      },
                      "full_match": {
                        "type": [
                          "boolean",
                          "null"
                        ]
                      },
                      "inner_part": {
                        "type": [
                          "string",
                          "null"
                        ]
                      },
                      "match_by_building": {
                        "type": [
                          "boolean",
                          "null"
                        ]
                      },
                      "match_by_street": {
                        "type": [
                          "boolean",
                          "null"
                        ]
                      },
                      "match_by_postcode": {
                        "type": [
                          "boolean",
                          "null"
                        ]
                      },
                      "match_by_city_or_disrict": {
                        "type": [
                          "boolean",
                          "null"
                        ]
                      },
                      "match_by_country_or_state": {
                        "type": [
                          "boolean",
                          "null"
                        ]
                      }
                    }
                  },
                  "geometry": {
                    "@type": "object",
                    "properties": {
                      "type": {
                        "type": "string"
                      },
                      "coordinates": {
                        "type": "array",
                        "items": {
                          "type": "number"
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    ],
    "properties": [
      {
        "@type": "Property",
        "name": "servicePurpose",
        "description": "Convert coordinates to address information for location-based services.",
        "schema": {
          "@type": "JsonSchema",
          "type": "string"
        }
      },
      {
        "@type": "Property",
        "name": "supportedLocationTypes",
        "description": "List of supported location types for geocoding.",
        "schema": {
          "@type": "JsonSchema",
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "country",
              "state",
              "city",
              "postcode",
              "street",
              "amenity"
            ]
          }
        }
      },
      {
        "@type": "Property",
        "name": "supportedLanguages",
        "description": "Supported languages for response (ISO 639-1 codes).",
        "schema": {
          "@type": "JsonSchema",
          "type": "string"
        }
      },
      {
        "@type": "Property",
        "name": "supportedFormats",
        "description": "Supported response formats.",
        "schema": {
          "@type": "JsonSchema",
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "json",
              "xml",
              "geojson"
            ]
          }
        }
      },
      {
        "@type": "Property",
        "name": "costModel",
        "description": "1 credit per request. 100 requests costs 100 credits.",
        "schema": {
          "@type": "JsonSchema",
          "type": "string"
        }
      },
      {
        "@type": "Property",
        "name": "geographicalCoverage",
        "description": "Global coverage with support for city, postcode, country, etc.",
        "schema": {
          "@type": "JsonSchema",
          "type": "string"
        }
      },
      {
        "@type": "Property",
        "name": "securityAndPrivacyAspects",
        "description": "API key authentication with optional IP address, HTTP referrer, origins, and CORS protection.",
        "schema": {
          "@type": "JsonSchema",
          "type": "string"
        }
      },
      {
        "@type": "Property",
        "name": "performanceCharacteristics",
        "description": "Different execution times and resource capacities required on servers.",
        "schema": {
          "@type": "JsonSchema",
          "type": "string"
        }
      },
      {
        "@type": "Property",
        "name": "languageAndLocalization",
        "description": "Support for multiple languages via ISO 639-1 language codes.",
        "schema": {
          "@type": "JsonSchema",
          "type": "string"
        }
      },
      {
        "@type": "Property",
        "name": "reliabilityAndAvailabilityCharacteristics",
        "description": "Returns result object with address fields. Some fields may be missing depending on location type.",
        "schema": {
          "@type": "JsonSchema",
          "type": "string"
        }
      }
    ]
  },{
    "@context": [
      "https://www.w3.org/ns/thing",
      "https://w3c.github.io/wot-thing-description-2.0/context.jsonld",
      "http://schema.org/",
      "http://saref.eu/saref#",
      "http://www.w3.org/2019/vocab/"
    ],
    "@type": "Thing",
    "title": "Nominatim Reverse Geocoding Service",
    "description": "Reverse geocoding service that generates an address from a coordinate given as latitude and longitude. Part of OpenStreetMap's Nominatim service for urban mobility, navigation, and location-based services.",
    "serviceDomain": "urban-mobility",
    "targetUser": [
      "commuters",
      "tourists",
      "businesses"
    ],
    "geographicalCoverage": {
      "@type": "GeoCoordinates",
      "description": "Global coverage with OSM data"
    },
    "operationalLimitations": [
      {
        "@type": "Constraint",
        "coordinateSystem": "WGS84 projection",
        "unitOfMeasurement": "decimal degrees"
      }
    ],
    "securityDefinitions": {
      "apikey": {
        "@type": "SecurityScheme",
        "scheme": "apikey",
        "in": "header",
        "name": "X-Api-Key"
      },
      "basic": {
        "@type": "SecurityScheme",
        "scheme": "basic"
      }
    },
    "security": [
      "apikey"
    ],
    "properties": [
      {
        "@type": "Property",
        "title": "Latitude",
        "description": "Latitude coordinate in WGS84 projection",
        "forms": [
          {
            "href": "https://nominatim.openstreetmap.org/reverse?lat={value}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "SchemaProperty",
          "type": "number",
          "minimum": -90,
          "maximum": 90,
          "unit": "degrees"
        },
        "readOnly": True
      },
      {
        "@type": "Property",
        "title": "Longitude",
        "description": "Longitude coordinate in WGS84 projection",
        "forms": [
          {
            "href": "https://nominatim.openstreetmap.org/reverse?lon={value}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "SchemaProperty",
          "type": "number",
          "minimum": -180,
          "maximum": 180,
          "unit": "degrees"
        },
        "readOnly": True
      },
      {
        "@type": "Property",
        "title": "Output Format",
        "description": "Preferred output format for results",
        "forms": [
          {
            "href": "https://nominatim.openstreetmap.org/reverse?format={value}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "SchemaProperty",
          "type": "string",
          "enum": [
            "xml",
            "json",
            "jsonv2",
            "geojson",
            "geocodejson"
          ]
        },
        "readOnly": True,
        "unitOfMeasurement": "language and localization"
      },
      {
        "@type": "Property",
        "title": "Address Breakdown Level",
        "description": "Include breakdown of address into elements when set to 1",
        "forms": [
          {
            "href": "https://nominatim.openstreetmap.org/reverse?addressdetails={value}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "SchemaProperty",
          "type": "integer",
          "minimum": 0,
          "maximum": 1
        },
        "readOnly": True
      },
      {
        "@type": "Property",
        "title": "Additional Information",
        "description": "Include additional information in result (e.g., wikipedia link, opening hours)",
        "forms": [
          {
            "href": "https://nominatim.openstreetmap.org/reverse?details={value}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "SchemaProperty",
          "type": "integer",
          "minimum": 0,
          "maximum": 1
        },
        "readOnly": True,
        "unitOfMeasurement": "reliability and availability characteristics"
      },
      {
        "@type": "Property",
        "title": "Name Details",
        "description": "Include full list of names for the result (language variants, older names, references)",
        "forms": [
          {
            "href": "https://nominatim.openstreetmap.org/reverse?namedetails={value}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "SchemaProperty",
          "type": "integer",
          "minimum": 0,
          "maximum": 1
        },
        "readOnly": True,
        "unitOfMeasurement": "reliability and availability characteristics"
      },
      {
        "@type": "Property",
        "title": "Result Type Restriction",
        "description": "Restrict results to specific type (address, poi, railway, natural, manmade)",
        "forms": [
          {
            "href": "https://nominatim.openstreetmap.org/reverse?resulttype={value}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "SchemaProperty",
          "type": "string",
          "enum": [
            "address",
            "poi",
            "railway",
            "natural",
            "manmade",
            "address,poi"
          ]
        },
        "readOnly": True
      },
      {
        "@type": "Property",
        "title": "Polygon Output Tolerance",
        "description": "Tolerance in degrees with which geometry may differ from original geometry",
        "forms": [
          {
            "href": "https://nominatim.openstreetmap.org/reverse?polygon_geojson={value}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "SchemaProperty",
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "readOnly": True,
        "unitOfMeasurement": "performance characteristics"
      },
      {
        "@type": "Property",
        "title": "Debug Information",
        "description": "Output assorted developer debug information (overrides machine readable format)",
        "forms": [
          {
            "href": "https://nominatim.openstreetmap.org/reverse?debug={value}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "SchemaProperty",
          "type": "integer",
          "minimum": 0,
          "maximum": 1
        },
        "readOnly": True,
        "unitOfMeasurement": "reliability and availability characteristics"
      }
    ],
    "actions": [
      {
        "@type": "Action",
        "title": "Reverse Geocode",
        "description": "Generates an address from a coordinate given as latitude and longitude. Returns exactly one result or an error when the coordinate is in an area with no OSM data coverage.",
        "forms": [
          {
            "href": "https://nominatim.openstreetmap.org/reverse",
            "op": "invokeaction",
            "htv": "methodName"
          }
        ],
        "inputSchema": {
          "@type": "SchemaProperty",
          "type": "object",
          "properties": {
            "lat": {
              "@type": "SchemaProperty",
              "type": "number",
              "minimum": -90,
              "maximum": 90,
              "unit": "degrees"
            },
            "lon": {
              "@type": "SchemaProperty",
              "type": "number",
              "minimum": -180,
              "maximum": 180,
              "unit": "degrees"
            },
            "format": {
              "@type": "SchemaProperty",
              "type": "string",
              "enum": [
                "xml",
                "json",
                "jsonv2",
                "geojson",
                "geocodejson"
              ]
            },
            "addressdetails": {
              "@type": "SchemaProperty",
              "type": "integer",
              "minimum": 0,
              "maximum": 1
            },
            "details": {
              "@type": "SchemaProperty",
              "type": "integer",
              "minimum": 0,
              "maximum": 1
            },
            "namedetails": {
              "@type": "SchemaProperty",
              "type": "integer",
              "minimum": 0,
              "maximum": 1
            },
            "resulttype": {
              "@type": "SchemaProperty",
              "type": "string",
              "enum": [
                "address",
                "poi",
                "railway",
                "natural",
                "manmade",
                "address,poi"
              ]
            },
            "polygon_geojson": {
              "@type": "SchemaProperty",
              "type": "number",
              "minimum": 0,
              "maximum": 1
            },
            "debug": {
              "@type": "SchemaProperty",
              "type": "integer",
              "minimum": 0,
              "maximum": 1
            }
          }
        },
        "outputSchema": {
          "@type": "SchemaProperty",
          "type": "object",
          "properties": {
            "place_id": {
              "@type": "SchemaProperty",
              "type": "string"
            },
            "licence": {
              "@type": "SchemaProperty",
              "type": "string"
            },
            "osm_type": {
              "@type": "SchemaProperty",
              "type": "string",
              "enum": [
                "node",
                "way",
                "relation"
              ]
            },
            "osm_id": {
              "@type": "SchemaProperty",
              "type": "integer"
            },
            "lat": {
              "@type": "SchemaProperty",
              "type": "string",
              "pattern": "^-?\\d+\\.\\d+$"
            },
            "lon": {
              "@type": "SchemaProperty",
              "type": "string",
              "pattern": "^-?\\d+\\.\\d+$"
            },
            "place_rank": {
              "@type": "SchemaProperty",
              "type": "integer"
            },
            "category": {
              "@type": "SchemaProperty",
              "type": "string"
            },
            "type": {
              "@type": "SchemaProperty",
              "type": "string"
            },
            "importance": {
              "@type": "SchemaProperty",
              "type": "number"
            },
            "addresstype": {
              "@type": "SchemaProperty",
              "type": "string"
            },
            "display_name": {
              "@type": "SchemaProperty",
              "type": "string"
            },
            "name": {
              "@type": "SchemaProperty",
              "type": "string"
            },
            "address": {
              "@type": "SchemaProperty",
              "type": "object",
              "properties": {
                "house_number": {
                  "@type": "SchemaProperty",
                  "type": "string"
                },
                "road": {
                  "@type": "SchemaProperty",
                  "type": "string"
                },
                "village": {
                  "@type": "SchemaProperty",
                  "type": "string"
                },
                "town": {
                  "@type": "SchemaProperty",
                  "type": "string"
                },
                "city": {
                  "@type": "SchemaProperty",
                  "type": "string"
                },
                "county": {
                  "@type": "SchemaProperty",
                  "type": "string"
                },
                "postcode": {
                  "@type": "SchemaProperty",
                  "type": "string"
                },
                "country": {
                  "@type": "SchemaProperty",
                  "type": "string"
                },
                "country_code": {
                  "@type": "SchemaProperty",
                  "type": "string"
                }
              }
            },
            "boundingbox": {
              "@type": "SchemaProperty",
              "type": "array",
              "items": {
                "@type": "SchemaProperty",
                "type": "number"
              }
            }
          }
        },
        "outputFormat": [
          {
            "@type": "MediaType",
            "mediaType": "application/json"
          },
          {
            "@type": "MediaType",
            "mediaType": "application/geo+json"
          },
          {
            "@type": "MediaType",
            "mediaType": "text/xml"
          }
        ]
      }
    ],
    "events": [],
    "links": [
      {
        "@type": "Link",
        "href": "https://nominatim.openstreetmap.org/reverse.php",
        "rel": "alternate"
      }
    ],
    "license": {
      "@type": "License",
      "name": "ODbL 1.0",
      "url": "https://www.openstreetmap.org/copyright"
    },
    "thirdPartyServices": [
      {
        "@type": "ThirdPartyService",
        "name": "OpenStreetMap Contributors",
        "description": "Data source for reverse geocoding"
      }
    ],
    "performanceCharacteristics": {
      "@type": "PerformanceCharacteristic",
      "tolerance": "Geometry may differ within specified tolerance in degrees",
      "unit": "degrees"
    },
    "reliabilityAndAvailabilityCharacteristics": {
      "@type": "ReliabilityCharacteristic",
      "errorCondition": "Returns error when coordinate is in area with no OSM data coverage",
      "coverageType": "OSM data coverage"
    },
    "languageAndLocalization": {
      "@type": "LanguageCharacteristic",
      "defaultBehavior": "local language (when Accept-Language header not sent)",
      "browserBehavior": "browser language (when Accept-Language header sent)"
    },
    "servicePurpose": "Reverse geocoding service that generates an address from a coordinate given as latitude and longitude",
    "transportCapability": "convert coordinates to addresses"
  },
{
    "@context": {
      "@vocab": "https://www.w3.org/2019/wot/td#",
      "xsd": "http://www.w3.org/2001/XMLSchema#",
      "sosa": "http://schema.org/SOSA",
      "saref": "http://www.w3.org/ns/saref/",
      "schema": "http://schema.org/"
    },
    "@type": "Thing",
    "title": "Open-Meteo Weather Service",
    "description": "Simple JSON APIs for weather forecasts, historical data, and environmental analysis with global coverage.",
    "securityDefinitions": {
      "apikey": {
        "scheme": "http://www.w3.org/2011/http#apikey",
        "in": "header",
        "name": "X-API-Key"
      }
    },
    "security": [],
    "properties": {
      "location": {
        "@type": "sosa:ObservationProperty",
        "title": "Location Coordinates",
        "description": "Geographical coordinates and elevation for the requested location.",
        "schema": {
          "@type": "object",
          "properties": {
            "latitude": {
              "@type": "xsd:double",
              "minInclusive": -90,
              "maxInclusive": 90,
              "unitCode": "http://codes.wmo.int/common/unit#degree_north"
            },
            "longitude": {
              "@type": "xsd:double",
              "minInclusive": -180,
              "maxInclusive": 180,
              "unitCode": "http://codes.wmo.int/common/unit#degree_east"
            },
            "elevation": {
              "@type": "xsd:decimal",
              "unitCode": "http://codes.wmo.int/common/unit#metre"
            },
            "timezone": {
              "@type": "xsd:string"
            },
            "utc_offset_seconds": {
              "@type": "xsd:integer"
            }
          }
        }
      },
      "weatherData": {
        "@type": "sosa:ObservationProperty",
        "title": "Weather Data",
        "description": "Hourly or daily weather variables depending on the API endpoint invoked.",
        "schema": {
          "@type": "object",
          "properties": {
            "hourly": {
              "@type": "object",
              "properties": {
                "time": {
                  "@type": "xsd:string",
                  "format": "date-time"
                },
                "temperature_2m": {
                  "@type": "xsd:double",
                  "unitCode": "http://codes.wmo.int/common/unit#celsius"
                },
                "wind_speed_10m": {
                  "@type": "xsd:double",
                  "unitCode": "http://codes.wmo.int/common/unit#metre_per_second"
                }
              }
            },
            "daily": {
              "@type": "object",
              "properties": {
                "time": {
                  "@type": "xsd:string",
                  "format": "date-time"
                },
                "temperature_2m_max": {
                  "@type": "xsd:double",
                  "unitCode": "http://codes.wmo.int/common/unit#celsius"
                }
              }
            },
            "generationtime_ms": {
              "@type": "xsd:decimal",
              "description": "API response time in milliseconds."
            }
          }
        }
      }
    },
    "actions": [
      {
        "@type": "Action",
        "name": "getForecast",
        "title": "Weather Forecast API",
        "description": "Provides weather forecasts for any location worldwide with up to 1 km resolution.",
        "forms": [
          {
            "href": "https://api.open-meteo.com/v1/forecast",
            "op": "invokeaction",
            "htv:methodName": "GET",
            "contentType": "application/json",
            "schema": {
              "@type": "object",
              "properties": {
                "latitude": {
                  "@type": "xsd:double",
                  "minInclusive": -90,
                  "maxInclusive": 90
                },
                "longitude": {
                  "@type": "xsd:double",
                  "minInclusive": -180,
                  "maxInclusive": 180
                }
              }
            }
          }
        ]
      },
      {
        "@type": "Action",
        "name": "getHistorical",
        "title": "Historical Weather API",
        "description": "Access past weather data from 1940 with hourly resolution for any location on earth.",
        "forms": [
          {
            "href": "https://api.open-meteo.com/v1/history",
            "op": "invokeaction",
            "htv:methodName": "GET"
          }
        ]
      },
      {
        "@type": "Action",
        "name": "getEnsemble",
        "title": "Ensemble Models API",
        "description": "Provides up to 35 days of weather forecasts in hourly resolution with specialized data like wind at 120-meter elevation.",
        "forms": [
          {
            "href": "https://api.open-meteo.com/v1/ensemble",
            "op": "invokeaction",
            "htv:methodName": "GET"
          }
        ]
      },
      {
        "@type": "Action",
        "name": "getClimate",
        "title": "Climate Change API",
        "description": "Delivers downscaled IPCC climate predictions tailored to a 10 km resolution, extending up to the year 2050.",
        "forms": [
          {
            "href": "https://api.open-meteo.com/v1/climate",
            "op": "invokeaction",
            "htv:methodName": "GET"
          }
        ]
      },
      {
        "@type": "Action",
        "name": "getMarine",
        "title": "Marine Weather API",
        "description": "Provides detailed ocean wave forecasts generated by both local and global models.",
        "forms": [
          {
            "href": "https://api.open-meteo.com/v1/marine",
            "op": "invokeaction",
            "htv:methodName": "GET"
          }
        ]
      },
      {
        "@type": "Action",
        "name": "getAirQuality",
        "title": "Air Quality API",
        "description": "Delivers air pollution forecasts encompassing particles, gases, and pollen.",
        "forms": [
          {
            "href": "https://api.open-meteo.com/v1/air-quality",
            "op": "invokeaction",
            "htv:methodName": "GET"
          }
        ]
      },
      {
        "@type": "Action",
        "name": "getFloods",
        "title": "Flood API",
        "description": "Access ensemble flood forecasts that estimate the volume of water discharged by rivers worldwide.",
        "forms": [
          {
            "href": "https://api.open-meteo.com/v1/flood",
            "op": "invokeaction",
            "htv:methodName": "GET"
          }
        ]
      },
      {
        "@type": "Action",
        "name": "getElevation",
        "title": "Elevation API",
        "description": "Resolve any set of coordinates to their corresponding elevation using a digital elevation model with up to 90 meters resolution.",
        "forms": [
          {
            "href": "https://api.open-meteo.com/v1/elevation",
            "op": "invokeaction",
            "htv:methodName": "GET"
          }
        ]
      },
      {
        "@type": "Action",
        "name": "getGeocoding",
        "title": "Geocoding API",
        "description": "Resolve city names to precise coordinates.",
        "forms": [
          {
            "href": "https://api.open-meteo.com/v1/geocoding",
            "op": "invokeaction",
            "htv:methodName": "GET"
          }
        ]
      },
      {
        "@type": "Action",
        "name": "getTimezone",
        "title": "Timezone API",
        "description": "Automatically resolve coordinates to their respective timezones.",
        "forms": [
          {
            "href": "https://api.open-meteo.com/v1/timezone",
            "op": "invokeaction",
            "htv:methodName": "GET"
          }
        ]
      }
    ],
    "links": [
      {
        "href": "https://open-meteo.com/en/features#available_apis",
        "type": "text/html",
        "title": "Features"
      },
      {
        "href": "https://open-meteo.com/en/docs",
        "type": "text/html",
        "title": "API Documentation"
      }
    ],
    "metadata": {
      "@type": "sosa:PhenomenonTime",
      "geographicalCoverage": {
        "@type": "schema:GeoCoordinates",
        "description": "Global coverage, Europe, North America."
      },
      "performanceCharacteristics": {
        "@type": "schema:Performance",
        "responseTime": {
          "@type": "xsd:decimal",
          "value": 10,
          "unitCode": "http://codes.wmo.int/common/unit#millisecond"
        }
      },
      "environmentalImpact": {
        "@type": "sosa:ObservationProperty",
        "description": "Specialised forecasts for solar radiation, wind, transpiration, soil moisture, waves, and air quality."
      }
    }
  }, 
  {
    "@context": [
      "https://www.w3.org/2022/wot/td/v1.1",
      {
        "@vocab": "https://www.w3.org/2022/wot/td/v1.1#",
        "securityDefinitions": {
          "oauth2": {
            "@type": "SecurityScheme",
            "scheme": "http",
            "description": "Mapbox Access Token authentication"
          }
        },
        "saref": "http://www.w3.org/ns/saref/",
        "schema": "http://schema.org/",
        "unit": "https://w3c.github.io/uom/"
      }
    ],
    "@type": "Thing",
    "title": "Mapbox Search Box API",
    "description": "The Mapbox Search Box API is the easiest way to add interactive location search to connected cars, micro-mobility services, delivery apps, and more. Supports interactive location search or stand-alone queries to search addresses, places, and points of interest.",
    "securityDefinitions": {
      "oauth2": {
        "@type": "SecurityScheme",
        "scheme": "http",
        "description": "Mapbox Access Token authentication required for all endpoints"
      }
    },
    "security": [
      "oauth2"
    ],
    "properties": {
      "query": {
        "@type": "Property",
        "title": "Search Query",
        "description": "The user's query string for text search operations",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "minLength": 1,
          "maxLength": 256,
          "description": "The user's query string. Limited to 256 characters."
        }
      },
      "access_token": {
        "@type": "Property",
        "title": "Access Token",
        "description": "Mapbox access token with default permissions",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string"
        }
      },
      "language": {
        "@type": "Property",
        "title": "Language Code",
        "description": "ISO language code to be returned. Default is English if not provided.",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "description": "Supported languages: Czech, Croatian, Danish, Dutch, English, Estonian, Finnish, French, German, Greek, Hungarian, Italian, Japanese, Lithuanian, Latvian, Polish, Portuguese, Romanian, Russian, Slovak, Slovenian, Spanish, Swedish, Turkish, Ukrainian"
        }
      },
      "limit": {
        "@type": "Property",
        "title": "Result Limit",
        "description": "The number of results to return",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "integer",
          "minimum": 1,
          "maximum": 256,
          "description": "Up to 10 for suggest/retrieve endpoints, up to 25 for category endpoint"
        }
      },
      "proximity": {
        "@type": "Property",
        "title": "Proximity Location",
        "description": "Bias the response to favor results closer to a specific location",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "description": "Either 'ip' to get results closest to user's IP location or two comma-separated coordinates in longitude,latitude order"
        }
      },
      "origin": {
        "@type": "Property",
        "title": "Origin Location",
        "description": "Location from which to calculate distance when ETA calculation is enabled",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "description": "Two comma-separated coordinates in longitude,latitude order"
        }
      },
      "bbox": {
        "@type": "Property",
        "title": "Bounding Box",
        "description": "Limit results to only those contained within the supplied bounding box",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "description": "Four numbers separated by commas: minimum longitude, minimum latitude, maximum longitude, maximum latitude. Cannot cross the 180th meridian."
        }
      },
      "country": {
        "@type": "Property",
        "title": "Country Codes",
        "description": "A comma-separated list of ISO 3166 alpha-2 country codes",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "description": "Supported geographies: United States, Canada, Europe"
        }
      },
      "types": {
        "@type": "Property",
        "title": "Feature Types",
        "description": "Limit results to one or more types of features",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "description": "Available types: country, region, postcode, district, place, city, locality, neighborhood, street, address, poi, category"
        }
      },
      "poi_category": {
        "@type": "Property",
        "title": "POI Category",
        "description": "Limit results to those that belong to one or more categories",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "description": "Comma-separated list of category names"
        }
      },
      "eta_type": {
        "@type": "Property",
        "title": "ETA Type",
        "description": "Enable Estimate Time Arrival calculation in the response",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "enum": [
            "navigation"
          ],
          "description": "The only allowed value is 'navigation'. Enabling ETA calculations will introduce additional latency and incur extra costs."
        }
      },
      "navigation_profile": {
        "@type": "Property",
        "title": "Navigation Profile",
        "description": "Routing profile to use when ETA calculation is enabled",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "enum": [
            "driving",
            "walking",
            "cycling"
          ],
          "description": "Available profiles: driving, walking, and cycling"
        }
      },
      "auto_complete": {
        "@type": "Property",
        "title": "Autocomplete Mode",
        "description": "Enable Autocomplete Mode by setting the value to True",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "enum": [
            "True"
          ],
          "description": "When enabled, search results will include partial and fuzzy matches. Suitable for autocomplete implementations."
        }
      },
      "session_token": {
        "@type": "Property",
        "title": "Session Token",
        "description": "Token used to group a series of requests together into one session for billing purposes",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/suggest",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "description": "Required for /suggest and /retrieve endpoints. Used for session-based pricing."
        }
      },
      "mapbox_id": {
        "@type": "Property",
        "title": "Mapbox ID",
        "description": "Identifier to retrieve a suggested feature",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/retrieve/{id}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string"
        }
      },
      "category_id": {
        "@type": "Property",
        "title": "Category ID",
        "description": "Canonical category ID for category search",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/category/{id}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "description": "Canonical category ID to use in a category search"
        }
      },
      "sar_type": {
        "@type": "Property",
        "title": "Search Along Route Type",
        "description": "Enable search-along-route requests",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/category/{id}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "enum": [
            "isochrone"
          ],
          "description": "The only allowed value is 'isochrone'"
        }
      },
      "route_geometry": {
        "@type": "Property",
        "title": "Route Geometry",
        "description": "Polyline encoded linestring describing the route for SAR requests",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/category/{id}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "enum": [
            "polyline",
            "polyline6"
          ],
          "description": "Options are polyline or polyline6. Default is polyline if not provided."
        }
      },
      "time_deviation": {
        "@type": "Property",
        "title": "Time Deviation",
        "description": "Maximum detour allowed in estimated minutes from the route when SAR is enabled",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/category/{id}",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "number",
          "description": "Maximum detour allowed in estimated minutes from the route"
        }
      },
      "poi_category_exclusions": {
        "@type": "Property",
        "title": "POI Category Exclusions",
        "description": "A comma-separated list of canonical category names that limits POI results to those not part of given categories",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "string",
          "description": "Comma-separated list of canonical category names"
        }
      },
      "list_items": {
        "@type": "Property",
        "title": "Category List Items",
        "description": "List of all available categories with their canonical ID and name",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/list/category",
            "op": "readproperty"
          }
        ],
        "schema": {
          "@type": "DataSchema",
          "type": "array",
          "items": {
            "@type": "DataSchema",
            "type": "object",
            "properties": {
              "canonical_id": {
                "@type": "DataSchema",
                "type": "string"
              },
              "icon": {
                "@type": "DataSchema",
                "type": "string"
              },
              "name": {
                "@type": "DataSchema",
                "type": "string"
              }
            }
          }
        }
      }
    },
    "actions": {
      "forward_search": {
        "@type": "Action",
        "title": "Text Search",
        "description": "Send one-off search requests and get relevant results with coordinates and metadata. Unlike Interactive Search, does not provide type-ahead suggestions.",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/forward",
            "op": "invokeaction"
          }
        ],
        "input": [
          {
            "@type": "DataSchema",
            "name": "q",
            "schema": {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            },
            "required": True
          },
          {
            "@type": "DataSchema",
            "name": "access_token",
            "schema": {
              "type": "string"
            },
            "required": True
          }
        ],
        "output": [
          {
            "@type": "DataSchema",
            "name": "FeatureCollection",
            "schema": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "FeatureCollection"
                  ]
                },
                "features": {
                  "type": "array",
                  "items": {
                    "@type": "DataSchema",
                    "type": "object",
                    "properties": {
                      "type": {
                        "type": "string",
                        "enum": [
                          "Feature"
                        ]
                      },
                      "geometry": {
                        "type": "object",
                        "properties": {
                          "coordinates": {
                            "type": "array",
                            "items": {
                              "type": "number"
                            }
                          },
                          "type": {
                            "type": "string",
                            "enum": [
                              "Point"
                            ]
                          }
                        }
                      },
                      "properties": {
                        "type": "object",
                        "properties": {
                          "name": {
                            "type": "string"
                          },
                          "name_preferred": {
                            "type": "string"
                          },
                          "mapbox_id": {
                            "type": "string"
                          },
                          "feature_type": {
                            "type": "string",
                            "enum": [
                              "poi",
                              "address"
                            ]
                          },
                          "address": {
                            "type": "string"
                          },
                          "full_address": {
                            "type": "string"
                          },
                          "place_formatted": {
                            "type": "string"
                          },
                          "context": {
                            "type": "object",
                            "properties": {
                              "country": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "country_code": {
                                    "type": "string"
                                  },
                                  "country_code_alpha_3": {
                                    "type": "string"
                                  }
                                }
                              },
                              "region": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "region_code": {
                                    "type": "string"
                                  },
                                  "region_code_full": {
                                    "type": "string"
                                  }
                                }
                              },
                              "postcode": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "district": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "place": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "locality": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "neighborhood": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "address": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "address_number": {
                                    "type": "string"
                                  },
                                  "street_name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "street": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              }
                            }
                          },
                          "coordinates": {
                            "type": "object",
                            "properties": {
                              "latitude": {
                                "type": "number"
                              },
                              "longitude": {
                                "type": "number"
                              },
                              "accuracy": {
                                "type": "string",
                                "enum": [
                                  "rooftop",
                                  "parcel",
                                  "point",
                                  "interpolated",
                                  "intersection",
                                  "approximate"
                                ]
                              },
                              "routable_points": {
                                "type": "array",
                                "items": {
                                  "type": "object",
                                  "properties": {
                                    "name": {
                                      "type": "string"
                                    },
                                    "latitude": {
                                      "type": "number"
                                    },
                                    "longitude": {
                                      "type": "number"
                                    }
                                  }
                                }
                              }
                            }
                          },
                          "language": {
                            "type": "string"
                          },
                          "maki": {
                            "type": "string"
                          },
                          "poi_category": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "poi_category_ids": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "brand": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "brand_id": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "external_ids": {
                            "type": "object"
                          },
                          "metadata": {
                            "type": "object"
                          },
                          "bbox": {
                            "type": "array",
                            "items": {
                              "type": "number"
                            }
                          }
                        }
                      }
                    }
                  }
                },
                "attribution": {
                  "type": "string"
                }
              }
            }
          }
        ]
      },
      "suggest_search": {
        "@type": "Action",
        "title": "Get Autocomplete Suggestions",
        "description": "Used in combination with /retrieve to create an interactive search experience for end users. Send user search queries to get suggested results.",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/suggest",
            "op": "invokeaction"
          }
        ],
        "input": [
          {
            "@type": "DataSchema",
            "name": "q",
            "schema": {
              "type": "string"
            },
            "required": True
          },
          {
            "@type": "DataSchema",
            "name": "access_token",
            "schema": {
              "type": "string"
            },
            "required": True
          }
        ],
        "output": [
          {
            "@type": "DataSchema",
            "name": "Suggestions",
            "schema": {
              "type": "object",
              "properties": {
                "suggestions": {
                  "type": "array",
                  "items": {
                    "@type": "DataSchema",
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string"
                      },
                      "mapbox_id": {
                        "type": "string"
                      },
                      "feature_type": {
                        "type": "string",
                        "enum": [
                          "poi"
                        ]
                      },
                      "address": {
                        "type": "string"
                      },
                      "full_address": {
                        "type": "string"
                      },
                      "place_formatted": {
                        "type": "string"
                      },
                      "context": {
                        "type": "object",
                        "properties": {
                          "country": {
                            "type": "object",
                            "properties": {
                              "name": {
                                "type": "string"
                              },
                              "country_code": {
                                "type": "string"
                              },
                              "country_code_alpha_3": {
                                "type": "string"
                              }
                            }
                          },
                          "region": {
                            "type": "object",
                            "properties": {
                              "name": {
                                "type": "string"
                              },
                              "region_code": {
                                "type": "string"
                              },
                              "region_code_full": {
                                "type": "string"
                              }
                            }
                          },
                          "postcode": {
                            "type": "object",
                            "properties": {
                              "name": {
                                "type": "string"
                              }
                            }
                          },
                          "place": {
                            "type": "object",
                            "properties": {
                              "name": {
                                "type": "string"
                              }
                            }
                          },
                          "neighborhood": {
                            "type": "object",
                            "properties": {
                              "name": {
                                "type": "string"
                              }
                            }
                          },
                          "street": {
                            "type": "object",
                            "properties": {
                              "name": {
                                "type": "string"
                              }
                            }
                          }
                        }
                      },
                      "language": {
                        "type": "string"
                      },
                      "maki": {
                        "type": "string",
                        "enum": [
                          "marker"
                        ]
                      },
                      "poi_category": {
                        "type": "array",
                        "items": {
                          "type": "string"
                        }
                      },
                      "poi_category_ids": {
                        "type": "array",
                        "items": {
                          "type": "string"
                        }
                      },
                      "external_ids": {
                        "type": "object"
                      },
                      "metadata": {
                        "type": "object"
                      }
                    }
                  }
                },
                "attribution": {
                  "type": "string"
                }
              }
            }
          }
        ]
      },
      "retrieve_feature": {
        "@type": "Action",
        "title": "Retrieve a Suggested Feature",
        "description": "Retrieve detailed information about a suggested feature using its mapbox_id.",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/retrieve/{id}",
            "op": "invokeaction"
          }
        ],
        "input": [
          {
            "@type": "DataSchema",
            "name": "mapbox_id",
            "schema": {
              "type": "string"
            },
            "required": True
          },
          {
            "@type": "DataSchema",
            "name": "access_token",
            "schema": {
              "type": "string"
            },
            "required": True
          }
        ],
        "output": [
          {
            "@type": "DataSchema",
            "name": "FeatureCollection",
            "schema": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "FeatureCollection"
                  ]
                },
                "features": {
                  "type": "array",
                  "items": {
                    "@type": "DataSchema",
                    "type": "object",
                    "properties": {
                      "type": {
                        "type": "string",
                        "enum": [
                          "Feature"
                        ]
                      },
                      "geometry": {
                        "type": "object",
                        "properties": {
                          "coordinates": {
                            "type": "array",
                            "items": {
                              "type": "number"
                            }
                          },
                          "type": {
                            "type": "string",
                            "enum": [
                              "Point"
                            ]
                          }
                        }
                      },
                      "properties": {
                        "type": "object",
                        "properties": {
                          "name": {
                            "type": "string"
                          },
                          "name_preferred": {
                            "type": "string"
                          },
                          "mapbox_id": {
                            "type": "string"
                          },
                          "feature_type": {
                            "type": "string",
                            "enum": [
                              "poi"
                            ]
                          },
                          "address": {
                            "type": "string"
                          },
                          "full_address": {
                            "type": "string"
                          },
                          "place_formatted": {
                            "type": "string"
                          },
                          "context": {
                            "type": "object",
                            "properties": {
                              "country": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "country_code": {
                                    "type": "string"
                                  },
                                  "country_code_alpha_3": {
                                    "type": "string"
                                  }
                                }
                              },
                              "region": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "region_code": {
                                    "type": "string"
                                  },
                                  "region_code_full": {
                                    "type": "string"
                                  }
                                }
                              },
                              "postcode": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "district": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "place": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "locality": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "neighborhood": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "address": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "address_number": {
                                    "type": "string"
                                  },
                                  "street_name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "street": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              }
                            }
                          },
                          "coordinates": {
                            "type": "object",
                            "properties": {
                              "latitude": {
                                "type": "number"
                              },
                              "longitude": {
                                "type": "number"
                              },
                              "accuracy": {
                                "type": "string",
                                "enum": [
                                  "rooftop",
                                  "parcel",
                                  "point",
                                  "interpolated",
                                  "intersection",
                                  "approximate"
                                ]
                              },
                              "routable_points": {
                                "type": "array",
                                "items": {
                                  "type": "object",
                                  "properties": {
                                    "name": {
                                      "type": "string"
                                    },
                                    "latitude": {
                                      "type": "number"
                                    },
                                    "longitude": {
                                      "type": "number"
                                    }
                                  }
                                }
                              }
                            }
                          },
                          "language": {
                            "type": "string"
                          },
                          "maki": {
                            "type": "string"
                          },
                          "poi_category": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "poi_category_ids": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "brand": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "brand_id": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "external_ids": {
                            "type": "object"
                          },
                          "metadata": {
                            "type": "object"
                          }
                        }
                      }
                    }
                  }
                },
                "attribution": {
                  "type": "string"
                }
              }
            }
          }
        ]
      },
      "category_search": {
        "@type": "Action",
        "title": "Retrieve POIs by Category",
        "description": "Browse entire categories of results, like coffee shops, hotels, and bookstores around a specific location or along a route.",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/category/{id}",
            "op": "invokeaction"
          }
        ],
        "input": [
          {
            "@type": "DataSchema",
            "name": "access_token",
            "schema": {
              "type": "string"
            },
            "required": True
          },
          {
            "@type": "DataSchema",
            "name": "category_id",
            "schema": {
              "type": "string"
            },
            "required": True
          }
        ],
        "output": [
          {
            "@type": "DataSchema",
            "name": "FeatureCollection",
            "schema": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "FeatureCollection"
                  ]
                },
                "features": {
                  "type": "array",
                  "items": {
                    "@type": "DataSchema",
                    "type": "object",
                    "properties": {
                      "type": {
                        "type": "string",
                        "enum": [
                          "Feature"
                        ]
                      },
                      "geometry": {
                        "type": "object",
                        "properties": {
                          "coordinates": {
                            "type": "array",
                            "items": {
                              "type": "number"
                            }
                          },
                          "type": {
                            "type": "string",
                            "enum": [
                              "Point"
                            ]
                          }
                        }
                      },
                      "properties": {
                        "type": "object",
                        "properties": {
                          "name": {
                            "type": "string"
                          },
                          "mapbox_id": {
                            "type": "string"
                          },
                          "feature_type": {
                            "type": "string",
                            "enum": [
                              "poi"
                            ]
                          },
                          "address": {
                            "type": "string"
                          },
                          "full_address": {
                            "type": "string"
                          },
                          "place_formatted": {
                            "type": "string"
                          },
                          "context": {
                            "type": "object",
                            "properties": {
                              "country": {
                                "type": "object",
                                "properties": {
                                  "name": {
                                    "type": "string"
                                  },
                                  "country_code": {
                                    "type": "string"
                                  },
                                  "country_code_alpha_3": {
                                    "type": "string"
                                  }
                                }
                              },
                              "region": {
                                "type": "object",
                                "properties": {
                                  "name": {
                                    "type": "string"
                                  },
                                  "region_code": {
                                    "type": "string"
                                  },
                                  "region_code_full": {
                                    "type": "string"
                                  }
                                }
                              },
                              "postcode": {
                                "type": "object",
                                "properties": {
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "street": {
                                "type": "object",
                                "properties": {
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              }
                            }
                          },
                          "coordinates": {
                            "type": "object",
                            "properties": {
                              "latitude": {
                                "type": "number"
                              },
                              "longitude": {
                                "type": "number"
                              },
                              "routable_points": {
                                "type": "array",
                                "items": {
                                  "type": "object",
                                  "properties": {
                                    "name": {
                                      "type": "string"
                                    },
                                    "latitude": {
                                      "type": "number"
                                    },
                                    "longitude": {
                                      "type": "number"
                                    }
                                  }
                                }
                              }
                            }
                          },
                          "maki": {
                            "type": "string",
                            "enum": [
                              "restaurant"
                            ]
                          },
                          "poi_category": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "poi_category_ids": {
                            "type": "array",
                            "items": {
                              "type": "string"
                            }
                          },
                          "external_ids": {
                            "type": "object"
                          },
                          "metadata": {
                            "type": "object"
                          }
                        }
                      }
                    }
                  }
                },
                "attribution": {
                  "type": "string"
                }
              }
            }
          }
        ]
      },
      "list_categories": {
        "@type": "Action",
        "title": "Get Category List",
        "description": "Return a list of all available categories with their canonical ID and name in the specified language.",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/list/category",
            "op": "invokeaction"
          }
        ],
        "input": [
          {
            "@type": "DataSchema",
            "name": "access_token",
            "schema": {
              "type": "string"
            },
            "required": True
          },
          {
            "@type": "DataSchema",
            "name": "language",
            "schema": {
              "type": "string"
            }
          }
        ],
        "output": [
          {
            "@type": "DataSchema",
            "name": "CategoryList",
            "schema": {
              "type": "object",
              "properties": {
                "listItems": {
                  "type": "array",
                  "items": {
                    "@type": "DataSchema",
                    "type": "object",
                    "properties": {
                      "canonical_id": {
                        "type": "string"
                      },
                      "icon": {
                        "type": "string"
                      },
                      "name": {
                        "type": "string"
                      },
                      "version": {
                        "type": "string"
                      },
                      "uuid": {
                        "type": "string"
                      }
                    }
                  }
                },
                "attribution": {
                  "type": "string"
                },
                "version": {
                  "type": "string"
                }
              }
            }
          }
        ]
      },
      "reverse_lookup": {
        "@type": "Action",
        "title": "Reverse Lookup",
        "description": "Perform a reverse geocode lookup to get address information from coordinates.",
        "forms": [
          {
            "href": "https://api.mapbox.com/search/searchbox/v1/reverse",
            "op": "invokeaction"
          }
        ],
        "input": [
          {
            "@type": "DataSchema",
            "name": "access_token",
            "schema": {
              "type": "string"
            },
            "required": True
          },
          {
            "@type": "DataSchema",
            "name": "longitude",
            "schema": {
              "type": "number"
            },
            "required": True
          },
          {
            "@type": "DataSchema",
            "name": "latitude",
            "schema": {
              "type": "number"
            },
            "required": True
          }
        ],
        "output": [
          {
            "@type": "DataSchema",
            "name": "FeatureCollection",
            "schema": {
              "type": "object",
              "properties": {
                "type": {
                  "type": "string",
                  "enum": [
                    "FeatureCollection"
                  ]
                },
                "features": {
                  "type": "array",
                  "items": {
                    "@type": "DataSchema",
                    "type": "object",
                    "properties": {
                      "type": {
                        "type": "string",
                        "enum": [
                          "Feature"
                        ]
                      },
                      "geometry": {
                        "type": "object",
                        "properties": {
                          "coordinates": {
                            "type": "array",
                            "items": {
                              "type": "number"
                            }
                          },
                          "type": {
                            "type": "string",
                            "enum": [
                              "Point"
                            ]
                          }
                        }
                      },
                      "properties": {
                        "type": "object",
                        "properties": {
                          "name": {
                            "type": "string"
                          },
                          "mapbox_id": {
                            "type": "string"
                          },
                          "feature_type": {
                            "type": "string",
                            "enum": [
                              "address"
                            ]
                          },
                          "address": {
                            "type": "string"
                          },
                          "full_address": {
                            "type": "string"
                          },
                          "place_formatted": {
                            "type": "string"
                          },
                          "context": {
                            "type": "object",
                            "properties": {
                              "country": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "country_code": {
                                    "type": "string"
                                  },
                                  "country_code_alpha_3": {
                                    "type": "string"
                                  }
                                }
                              },
                              "postcode": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "place": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "locality": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "address": {
                                "type": "object",
                                "properties": {
                                  "id": {
                                    "type": "string"
                                  },
                                  "name": {
                                    "type": "string"
                                  },
                                  "address_number": {
                                    "type": "string"
                                  },
                                  "street_name": {
                                    "type": "string"
                                  }
                                }
                              },
                              "street": {
                                "type": "object",
                                "properties": {
                                  "name": {
                                    "type": "string"
                                  }
                                }
                              }
                            }
                          },
                          "coordinates": {
                            "type": "object",
                            "properties": {
                              "latitude": {
                                "type": "number"
                              },
                              "longitude": {
                                "type": "number"
                              },
                              "accuracy": {
                                "type": "string",
                                "enum": [
                                  "rooftop",
                                  "parcel",
                                  "point",
                                  "interpolated",
                                  "intersection",
                                  "approximate"
                                ]
                              },
                              "routable_points": {
                                "type": "array",
                                "items": {
                                  "type": "object",
                                  "properties": {
                                    "name": {
                                      "type": "string"
                                    },
                                    "latitude": {
                                      "type": "number"
                                    },
                                    "longitude": {
                                      "type": "number"
                                    }
                                  }
                                }
                              }
                            }
                          },
                          "language": {
                            "type": "string"
                          },
                          "maki": {
                            "type": "string"
                          },
                          "external_ids": {
                            "type": "object"
                          },
                          "metadata": {
                            "type": "object"
                          }
                        }
                      }
                    }
                  }
                },
                "attribution": {
                  "type": "string"
                }
              }
            }
          }
        ]
      }
    },
    "events": {},
    "forms": [
      {
        "href": "https://api.mapbox.com/search/searchbox/v1/forward",
        "op": "readproperty",
        "htv:methodName": "GET"
      },
      {
        "href": "https://api.mapbox.com/search/searchbox/v1/suggest",
        "op": "readproperty",
        "htv:methodName": "GET"
      },
      {
        "href": "https://api.mapbox.com/search/searchbox/v1/retrieve/{id}",
        "op": "readproperty",
        "htv:methodName": "GET"
      },
      {
        "href": "https://api.mapbox.com/search/searchbox/v1/category/{id}",
        "op": "readproperty",
        "htv:methodName": "GET"
      },
      {
        "href": "https://api.mapbox.com/search/searchbox/v1/list/category",
        "op": "readproperty",
        "htv:methodName": "GET"
      },
      {
        "href": "https://api.mapbox.com/search/searchbox/v1/reverse",
        "op": "readproperty",
        "htv:methodName": "GET"
      }
    ],
    "geographicCoverage": [
      {
        "@type": "GeoCoordinates",
        "name": "United States",
        "description": "Full coverage of United States"
      },
      {
        "@type": "GeoCoordinates",
        "name": "Canada",
        "description": "Full coverage of Canada"
      },
      {
        "@type": "GeoCoordinates",
        "name": "Europe",
        "description": "Full coverage of Europe"
      }
    ],
    "usageStatistics": {
      "@type": "UsageStatistics",
      "billingModel": [
        {
          "@type": "BillingModel",
          "name": "Session-based pricing",
          "description": "For /suggest and /retrieve endpoints. Usage billed per search session."
        },
        {
          "@type": "BillingModel",
          "name": "Per-request pricing",
          "description": "For /category and /reverse endpoints. Each call incurs a separate charge."
        }
      ]
    },
    "securitySchemes": [
      {
        "@type": "SecurityScheme",
        "name": "oauth2",
        "scheme": "http",
        "description": "Mapbox Access Token authentication required for all endpoints"
      }
    ],
    "errors": [
      {
        "@type": "Error",
        "code": 401,
        "message": "Not authorized"
      },
      {
        "@type": "Error",
        "code": 400,
        "message": "Bad request"
      },
      {
        "@type": "Error",
        "code": 403,
        "message": "Forbidden"
      }
    ]
  }
]
result  = collection.insert_many(TDs)
