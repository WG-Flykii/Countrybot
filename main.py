import discord
import requests
import re
import io
import asyncio
import math
import datetime
from datetime import datetime, timedelta, timezone
from discord import ui

CHANNEL_ID = 
OPENCAGE_API_KEY = ''


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

country_codes = {
    'ad': ['Andorra'],
    'ae': ['United Arab Emirates'],
    'af': ['Afghanistan'],
    'al': ['Albania'],
    'am': ['Armenia'],
    'ar': ['Argentina'],
    'at': ['Austria'],
    'au': ['Australia'],
    'be': ['Belgium'],
    'bg': ['Bulgaria'],
    'br': ['Brazil'],
    'ca': ['Canada'],
    'ch': ['Switzerland'],
    'cd': ['Democratic Republic of Congo', "drc"],
    'cl': ['Chile'],
    'cn': ['China'],
    'co': ['Colombia'],
    'cr': ['Costa Rica'],
    'cu': ['Cuba'],
    'cz': ['Czech Republic', 'czechia'],
    'de': ['Germany'],
    'dk': ['Denmark'],
    'do': ['Dominican Republic'],
    'dz': ['Algeria'],
    'ec': ['Ecuador'],
    'ee': ['Estonia'],
    'eg': ['Egypt'],
    'es': ['Spain'],
    'et': ['Ethiopia'],
    'fi': ['Finland'],
    'fr': ['France'],
    'ge': ['Georgia'],
    'gr': ['Greece'],
    'gt': ['Guatemala'],
    'hk': ['Hong Kong'],
    'hn': ['Honduras'],
    'hr': ['Croatia'],
    'hu': ['Hungary'],
    'id': ['Indonesia'],
    'ie': ['Ireland'],
    'il': ['Israel'],
    'in': ['India'],
    'iq': ['Iraq'],
    'ir': ['Iran'],
    'is': ['Iceland'],
    'it': ['Italy'],
    'jp': ['Japan'],
    'jo': ['Jordan'],
    'ke': ['Kenya'],
    'kg': ['Kyrgyzstan'],
    'kh': ['Cambodia'],
    'kr': ['South Korea'],
    'kw': ['Kuwait'],
    'kz': ['Kazakhstan'],
    'la': ['Laos'],
    'lb': ['Lebanon'],
    'lt': ['Lithuania'],
    'lu': ['Luxembourg'],
    'lv': ['Latvia'],
    'ly': ['Libya'],
    'ma': ['Morocco'],
    'md': ['Moldova'],
    'me': ['Montenegro'],
    'mg': ['Madagascar'],
    'mk': ['North Macedonia'],
    'mm': ['Myanmar'],
    'mn': ['Mongolia'],
    'mt': ['Malta'],
    'mu': ['Mauritius'],
    'mx': ['Mexico'],
    'my': ['Malaysia'],
    'mz': ['Mozambique'],
    'na': ['Namibia'],
    'ng': ['Nigeria'],
    'nl': ['Netherlands'],
    'no': ['Norway'],
    'np': ['Nepal'],
    'nz': ['New Zealand'],
    'om': ['Oman'],
    'pa': ['Panama'],
    'pe': ['Peru'],
    'ph': ['Philippines'],
    'pk': ['Pakistan'],
    'pl': ['Poland'],
    'pt': ['Portugal'],
    'py': ['Paraguay'],
    'qa': ['Qatar'],
    'ro': ['Romania'],
    'rs': ['Serbia'],
    'ru': ['Russia'],
    'sa': ['Saudi Arabia'],
    'sd': ['Sudan'],
    'se': ['Sweden'],
    'sg': ['Singapore'],
    'si': ['Slovenia'],
    'sk': ['Slovakia'],
    'sn': ['Senegal'],
    'sy': ['Syria'],
    'th': ['Thailand'],
    'tn': ['Tunisia'],
    'tr': ['Turkey'],
    'ua': ['Ukraine'],
    'ug': ['Uganda'],
    'uk': ['United Kingdom'],
    'us': ['United States', 'usa'],
    'uy': ['Uruguay'],
    'uz': ['Uzbekistan'],
    've': ['Venezuela'],
    'vn': ['Vietnam'],
    'ye': ['Yemen'],
    'za': ['South Africa'],
    'zw': ['Zimbabwe'],
}

territory_codes = {
    "sl": ["Sierra Leone"],
    "sg": ["Singapore"],
    "sx": ["Sint Maarten"],
    "sk": ["Slovakia"],
    "si": ["Slovenia"],
    "sb": ["Solomon Islands"],
    "so": ["Somalia"],
    "gs": ["South Georgia and the South Sandwich Islands", "south georgia"],
    "ss": ["South Sudan"],
    "es": ["Spain"],
    "lk": ["Sri Lanka"],
    "sd": ["Sudan"],
    "sr": ["Suriname"],
    "sj": ["Svalbard and Jan Mayen", "svalbard"],
    "sz": ["Swaziland"],
    "se": ["Sweden"],
    "ch": ["Switzerland"],
    "sy": ["Syria"],
    "tw": ["Taiwan"],
    "tj": ["Tajikistan"],
    "tz": ["Tanzania"],
    "th": ["Thailand"],
    "tl": ["Timor Leste"],
    "tg": ["Togo"],
    "tk": ["Tokelau"],
    "to": ["Tonga"],
    "tt": ["Trinidad and Tobago"],
    "tn": ["Tunisia"],
    "tr": ["Turkey"],
    "tm": ["Turkmenistan"],
    "tc": ["Turks and Caicos Islands"],
    "tv": ["Tuvalu"],
    "ug": ["Uganda"],
    "ua": ["Ukraine"],
    "ae": ["United Arab Emirates"],
    "gb": ["United Kingdom"],
    "us": ["United States"],
    "um": ["United States Minor Outlying Islands"],
    "uy": ["Uruguay"],
    "uz": ["Uzbekistan"],
    "vu": ["Vanuatu"],
    "ve": ["Venezuela"],
    "vn": ["Vietnam"],
    "vg": ["Virgin Islands, British", "british virgin islands"],
    "vi": ["Virgin Islands, U.S.", "usvi", "us virgin islands"],
    "wf": ["Wallis and Futuna"],
    "eh": ["Western Sahara"],
    "ye": ["Yemen"],
    "zm": ["Zambia"],
    "zw": ["Zimbabwe"],
    "mc": ["Monaco"],
    "mn": ["Mongolia"],
    "me": ["Montenegro"],
    "ms": ["Montserrat"],
    "ma": ["Morocco"],
    "mz": ["Mozambique"],
    "na": ["Namibia"],
    "nr": ["Nauru"],
    "np": ["Nepal"],
    "nl": ["Netherlands"],
    "nc": ["New Caledonia"],
    "nz": ["New Zealand"],
    "ni": ["Nicaragua"],
    "ne": ["Niger"],
    "ng": ["Nigeria"],
    "nf": ["Norfolk Island"],
    "mp": ["Northern Mariana Islands", "nmi"],
    "pw": ["Palau"],
    "ps": ["Palestine", "Palestinian Territory"],
    "pg": ["Papua New Guinea", "png"],
    "py": ["Paraguay"],
    "pe": ["Peru"],
    "ph": ["Philippines"],
    "pn": ["Pitcairn"],
    "pl": ["Poland"],
    "pt": ["Portugal"],
    "pr": ["Puerto Rico"],
    "qa": ["Qatar"],
    "re": ["Reunion"],
    "ru": ["Russia"],
    "rw": ["Rwanda"],
    "bl": ["Saint Barthélemy"],
    "sh": ["Saint Helena, Ascension and Tristan da Cunha", "Saint helena"],
    "kn": ["Saint Kitts and Nevis"],
    "mf": ["Saint Martin"],
    "pm": ["Saint Pierre and Miquelon"],
    "vc": ["Saint Vincent and the Grenadines"],
    "sm": ["San Marino"],
    "st": ["Sao Tome and Principe", "sao tome"],
    "sa": ["Saudi Arabia"],
    "sn": ["Senegal"],
    "rs": ["Serbia"],
    "sc": ["Seychelles"],
    "gy": ["Guyana"],
    "ht": ["Haiti"],
    "hm": ["Heard Island and McDonald Islands", "Heard Island"],
    "va": ["Vatican City", "Vatican"],
    "hn": ["Honduras"],
    "hk": ["Hong Kong"],
    "hu": ["Hungary"],
    "is": ["Iceland"],
    "in": ["India"],
    "id": ["Indonesia"],
    "ir": ["Iran"],
    "iq": ["Iraq"],
    "ie": ["Ireland"],
    "im": ["Isle of Man"],
    "il": ["Israel"],
    "it": ["Italy"],
    "jm": ["Jamaica"],
    "jp": ["Japan"],
    "je": ["Jersey"],
    "jo": ["Jordan"],
    "kz": ["Kazakhstan"],
    "ke": ["Kenya"],
    "kg": ["Kyrgyzstan"],
    "kr": ["South Korea"],
    "kp": ["North Korea"],
    "kw": ["Kuwait"],
    "la": ["Laos"],
    "lv": ["Latvia"],
    "lb": ["Lebanon"],
    "ls": ["Lesotho"],
    "lr": ["Liberia"],
    "ly": ["Libya"],
    "li": ["Liechtenstein"],
    "lt": ["Lithuania"],
    "lu": ["Luxembourg"],
    "mo": ["Macao"],
    "mk": ["North Macedonia"],
    "mg": ["Madagascar"],
    "mw": ["Malawi"],
    "my": ["Malaysia"],
    "mv": ["Maldives"],
    "ml": ["Mali"],
    "mt": ["Malta"],
    "mh": ["Marshall Islands"],
    "mq": ["Martinique"],
    "mr": ["Mauritania"],
    "mu": ["Mauritius"],
    "yt": ["Mayotte"],
    "mx": ["Mexico"],
    "fm": ["Micronesia"],
    "md": ["Moldova, Republic of", "Moldova"],
    "cf": ["Central African Republic", "car", "CAR"],
    "td": ["Chad"],
    "cl": ["Chile"],
    "cn": ["China"],
    "cx": ["Christmas Island"],
    "cc": ["Cocos (Keeling) Islands", "cocos islands", "cocos", "coco"],
    "co": ["Colombia"],
    "km": ["Comoros"],
    "cg": ["Congo"],
    "cd": ["Democratic Republic of congo", "congo", "DRC", "drc"],
    "ck": ["Cook Islands"],
    "cr": ["Costa Rica"],
    "ci": ["Ivory Coast"],
    "hr": ["Croatia"],
    "cu": ["Cuba"],
    "cw": ["Curacao"],
    "cy": ["Cyprus"],
    "cz": ["Czech Republic", "czechia"],
    "dk": ["Denmark"],
    "dj": ["Djibouti"],
    "dm": ["Dominica"],
    "do": ["Dominican Republic"],
    "ec": ["Ecuador"],
    "eg": ["Egypt"],
    "sv": ["El Salvador"],
    "gq": ["Equatorial Guinea"],
    "er": ["Eritrea"],
    "ee": ["Estonia"],
    "et": ["Ethiopia"],
    "fk": ["Falkland Islands (Malvinas)", "Falkland", "Falkland islands", "islas Malvinas"],
    "fo": ["Faroe Islands", "fareo", "feroe"],
    "fj": ["Fiji"],
    "fi": ["Finland"],
    "fr": ["France"],
    "gf": ["French Guiana"],
    "pf": ["French Polynesia"],
    "tf": ["French Southern Territories", "taaf"],
    "ga": ["Gabon"],
    "gm": ["Gambia"],
    "ge": ["Georgia"],
    "de": ["Germany"],
    "gh": ["Ghana"],
    "gi": ["Gibraltar"],
    "gr": ["Greece"],
    "gl": ["Greenland"],
    "gd": ["Grenada"],
    "gp": ["Guadeloupe"],
    "gu": ["Guam"],
    "gt": ["Guatemala"],
    "gg": ["Guernsey"],
    "gn": ["Guinea"],
    "gw": ["Guinea Bissau"],
    "af": ["Afghanistan"],
    "ax": ["Aland Islands", "Aland"],
    "al": ["Albania"],
    "dz": ["Algeria"],
    "as": ["American Samoa"],
    "ad": ["Andorra"],
    "ao": ["Angola"],
    "ai": ["Anguilla"],
    "aq": ["Antarctica"],
    "ag": ["Antigua and Barbuda"],
    "ar": ["Argentina"],
    "am": ["Armenia"],
    "aw": ["Aruba"],
    "au": ["Australia"],
    "at": ["Austria"],
    "az": ["Azerbaijan"],
    "bs": ["Bahamas"],
    "bh": ["Bahrain"],
    "bd": ["Bangladesh"],
    "bb": ["Barbados"],
    "by": ["Belarus"],
    "be": ["Belgium"],
    "bz": ["Belize"],
    "bj": ["Benin"],
    "bm": ["Bermuda"],
    "bt": ["Bhutan"],
    "bo": ["Bolivia"],
    "bq": ["Bonaire, Sint Eustatius and Saba", "Bonaire"],
    "ba": ["Bosnia and Herzegovina", "bosnia"],
    "bw": ["Botswana"],
    "bv": ["Bouvet Island"],
    "br": ["Brazil"],
    "io": ["British Indian Ocean Territory"],
    "bn": ["Brunei Darussalam"],
    "bg": ["Bulgaria"],
    "bf": ["Burkina Faso"],
    "bi": ["Burundi"],
    "kh": ["Cambodia"],
    "cm": ["Cameroon"],
    "ca": ["Canada"],
    "cv": ["Cape Verde"],
    "ky": ["Cayman Islands", "cayman"]
}
import discord
import requests
import re
import io
import asyncio

subdivision_data = {
    'argentina': {
        'buenos aires': {
            'answer': ['Buenos Aires', 'buenos aires']
        },
        'catamarca': {
            'answer': ['Catamarca', 'catamarca']
        },
        'chaco': {
            'answer': ['Chaco', 'chaco']
        },
        'chubut': {
            'answer': ['Chubut', 'chubut']
        },
        'cordoba': {
            'answer': ['Córdoba', 'Cordoba', 'córdoba', 'cordoba']
        },
        'corrientes': {
            'answer': ['Corrientes', 'corrientes']
        },
        'entre rios': {
            'answer': ['Entre Ríos', 'Entre Rios', 'entre ríos', 'entre rios']
        },
        'formosa': {
            'answer': ['Formosa', 'formosa']
        },
        'jujuy': {
            'answer': ['Jujuy', 'jujuy']
        },
        'la pampa': {
            'answer': ['La Pampa', 'la pampa']
        },
        'la rioja': {
            'answer': ['La Rioja', 'la rioja']
        },
        'mendoza': {
            'answer': ['Mendoza', 'mendoza']
        },
        'misiones': {
            'answer': ['Misiones', 'misiones']
        },
        'neuquen': {
            'answer': ['Neuquén', 'Neuquen', 'neuquén', 'neuquen']
        },
        'rio negro': {
            'answer': ['Río Negro', 'Rio Negro', 'río negro', 'rio negro']
        },
        'salta': {
            'answer': ['Salta', 'salta']
        },
        'san juan': {
            'answer': ['San Juan', 'san juan']
        },
        'san luis': {
            'answer': ['San Luis', 'san luis']
        },
        'santa cruz': {
            'answer': ['Santa Cruz', 'santa cruz']
        },
        'santa fe': {
            'answer': ['Santa Fe', 'santa fe']
        },
        'santiago del estero': {
            'answer': ['Santiago del Estero', 'santiago del estero']
        },
        'tierra del fuego': {
            'answer': ['Tierra del Fuego', 'tierra del fuego']
        },
        'tucuman': {
            'answer': ['Tucumán', 'Tucuman', 'tucumán', 'tucuman']
        }
    },
    'usa': {
        'alabama': {
            'answer': ['Alabama', 'alabama']
        },
        'alaska': {
            'answer': ['Alaska', 'alaska']
        },
        'arizona': {
            'answer': ['Arizona', 'arizona']
        },
        'arkansas': {
            'answer': ['Arkansas', 'arkansas']
        },
        'california': {
            'answer': ['California', 'california']
        },
        'colorado': {
            'answer': ['Colorado', 'colorado']
        },
        'connecticut': {
            'answer': ['Connecticut', 'connecticut']
        },
        'delaware': {
            'answer': ['Delaware', 'delaware']
        },
        'florida': {
            'answer': ['Florida', 'florida']
        },
        'georgia': {
            'answer': ['Georgia', 'georgia']
        },
        'hawaii': {
            'answer': ['Hawaii', 'hawaii']
        },
        'idaho': {
            'answer': ['Idaho', 'idaho']
        },
        'illinois': {
            'answer': ['Illinois', 'illinois']
        },
        'indiana': {
            'answer': ['Indiana', 'indiana']
        },
        'iowa': {
            'answer': ['Iowa', 'iowa']
        },
        'kansas': {
            'answer': ['Kansas', 'kansas']
        },
        'kentucky': {
            'answer': ['Kentucky', 'kentucky']
        },
        'louisiana': {
            'answer': ['Louisiana', 'louisiana']
        },
        'maine': {
            'answer': ['Maine', 'maine']
        },
        'maryland': {
            'answer': ['Maryland', 'maryland']
        },
        'massachusetts': {
            'answer': ['Massachusetts', 'massachusetts']
        },
        'michigan': {
            'answer': ['Michigan', 'michigan']
        },
        'minnesota': {
            'answer': ['Minnesota', 'minnesota']
        },
        'mississippi': {
            'answer': ['Mississippi', 'mississippi']
        },
        'missouri': {
            'answer': ['Missouri', 'missouri']
        },
        'montana': {
            'answer': ['Montana', 'montana']
        },
        'nebraska': {
            'answer': ['Nebraska', 'nebraska']
        },
        'nevada': {
            'answer': ['Nevada', 'nevada']
        },
        'new hampshire': {
            'answer': ['New Hampshire', 'new hampshire']
        },
        'new jersey': {
            'answer': ['New Jersey', 'new jersey']
        },
        'new mexico': {
            'answer': ['New Mexico', 'new mexico']
        },
        'new york': {
            'answer': ['New York', 'new york']
        },
        'north carolina': {
            'answer': ['North Carolina', 'north carolina']
        },
        'north dakota': {
            'answer': ['North Dakota', 'north dakota']
        },
        'ohio': {
            'answer': ['Ohio', 'ohio']
        },
        'oklahoma': {
            'answer': ['Oklahoma', 'oklahoma']
        },
        'oregon': {
            'answer': ['Oregon', 'oregon']
        },
        'pennsylvania': {
            'answer': ['Pennsylvania', 'pennsylvania']
        },
        'rhode island': {
            'answer': ['Rhode Island', 'rhode island']
        },
        'south carolina': {
            'answer': ['South Carolina', 'south carolina']
        },
        'south dakota': {
            'answer': ['South Dakota', 'south dakota']
        },
        'tennessee': {
            'answer': ['Tennessee', 'tennessee']
        },
        'texas': {
            'answer': ['Texas', 'texas']
        },
        'utah': {
            'answer': ['Utah', 'utah']
        },
        'vermont': {
            'answer': ['Vermont', 'vermont']
        },
        'virginia': {
            'answer': ['Virginia', 'virginia']
        },
        'washington': {
            'answer': ['Washington', 'washington']
        },
        'west virginia': {
            'answer': ['West Virginia', 'west virginia']
        },
        'wisconsin': {
            'answer': ['Wisconsin', 'wisconsin']
        },
        'wyoming': {
            'answer': ['Wyoming', 'wyoming']
        }
    },
    'canada': {
        'alberta': {
            'answer': ['Alberta', 'alberta']
        },
        'british columbia': {
            'answer': ['British Columbia', 'british columbia', 'bc', 'BC']
        },
        'manitoba': {
            'answer': ['Manitoba', 'manitoba']
        },
        'new brunswick': {
            'answer': ['New Brunswick', 'new brunswick']
        },
        'newfoundland and labrador': {
            'answer': ['Newfoundland and Labrador', 'newfoundland and labrador', 'NFL', 'nfl']
        },
        'nova scotia': {
            'answer': ['Nova Scotia', 'nova scotia']
        },
        'ontario': {
            'answer': ['Ontario', 'ontario']
        },
        'prince edward island': {
            'answer': ['Prince Edward Island', 'prince edward island']
        },
        'quebec': {
            'answer': ['Quebec', 'quebec']
        },
        'saskatchewan': {
            'answer': ['Saskatchewan', 'saskatchewan', 'sask']
        },
        'northwest territories': {
            'answer': ['Northwest Territories', 'northwest territories', 'nwt']
        },
        'nunavut': {
            'answer': ['Nunavut', 'nunavut']
        },
        'yukon': {
            'answer': ['Yukon', 'yukon']
        }
    },
    'brazil': {
        'acre': {
            'answer': ['Acre', 'acre']
        },
        'alagoas': {
            'answer': ['Alagoas', 'alagoas']
        },
        'amapa': {
            'answer': ['Amapá', 'amapa', 'Amapa', 'amapa']
        },
        'amazonas': {
            'answer': ['Amazonas', 'amazonas']
        },
        'bahia': {
            'answer': ['Bahia', 'bahia']
        },
        'ceara': {
            'answer': ['Ceará', 'ceara', 'Ceara', 'ceara']
        },
        'distrito federal': {
            'answer': ['Distrito Federal', 'distrito federal', 'brasilia']
        },
        'espirito santo': {
            'answer': ['Espírito Santo', 'espirito santo']
        },
        'goias': {
            'answer': ['Goiás', 'goias']
        },
        'maranhao': {
            'answer': ['Maranhão', 'maranhao']
        },
        'mato grosso': {
            'answer': ['Mato Grosso', 'mato grosso']
        },
        'mato grosso do sul': {
            'answer': ['Mato Grosso do Sul', 'mato grosso do sul', 'mgds']
        },
        'minas gerais': {
            'answer': ['Minas Gerais', 'minas gerais']
        },
        'parana': {
            'answer': ['Paraná', 'parana']
        },
        'paraiba': {
            'answer': ['Paraíba', 'paraiba']
        },
        'parana': {
            'answer': ['Paraná', 'parana']
        },
        'pernambuco': {
            'answer': ['Pernambuco', 'pernambuco']
        },
        'piaui': {
            'answer': ['Piauí', 'piaui']
        },
        'rio de janeiro': {
            'answer': ['Rio de Janeiro', 'rio de janeiro']
        },
        'rio grande do norte': {
            'answer': ['Rio Grande do Norte', 'rio grande do norte', 'rgdn']
        },
        'rio grande do sul': {
            'answer': ['Rio Grande do Sul', 'rio grande do sul', 'rgds']
        },
        'rondonia': {
            'answer': ['Rondônia', 'rondonia']
        },
        'roraima': {
            'answer': ['Roraima', 'roraima']
        },
        'santa catarina': {
            'answer': ['Santa Catarina', 'santa catarina']
        },
        'sao paulo': {
            'answer': ['São Paulo', 'sao paulo']
        },
        'sergipe': {
            'answer': ['Sergipe', 'sergipe']
        },
        'tocantins': {
            'answer': ['Tocantins', 'tocantins']
        }
    },
    'australia': {
        'new south wales': {
            'answer': ['New South Wales', 'new south wales', 'NSW', 'nsw']
        },
        'queensland': {
            'answer': ['Queensland', 'queensland', 'QLD', 'qld']
        },
        'victoria': {
            'answer': ['Victoria', 'victoria', 'VIC', 'vic']
        },
        'western australia': {
            'answer': ['Western Australia', 'western australia', 'WA', 'wa']
        },
        'south australia': {
            'answer': ['South Australia', 'south australia', 'SA', 'sa']
        },
        'tasmania': {
            'answer': ['Tasmania', 'tasmania', 'TAS', 'tas']
        },
        'australian capital territory': {
            'answer': ['Australian Capital Territory', 'australian capital territory', 'ACT', 'act', 'canberra']
        },
        'northern territory': {
            'answer': ['Northern Territory', 'northern territory', 'NT', 'nt']
        }
    },
    'mexico': {
        'aguascalientes': {
            'answer': ['Aguascalientes', 'aguascalientes']
        },
        'baja california': {
            'answer': ['Baja California', 'baja california', 'BC', 'bc', 'baja cali']
        },
        'baja california sur': {
            'answer': ['Baja California Sur', 'baja california sur', 'BCS', 'bcs', 'baja cali sur', 'baja california do sur', 'baja california de sur', 'baja california de sul', 'baja california do sul']
        },
        'campeche': {
            'answer': ['Campeche', 'campeche']
        },
        'chiapas': {
            'answer': ['Chiapas', 'chiapas']
        },
        'chihuahua': {
            'answer': ['Chihuahua', 'chihuahua']
        },
        'ciudad de mexico': {
            'answer': ['Ciudad de México', 'Ciudad de Mexico', 'ciudad de méxico', 'ciudad de mexico', 'CDMX', 'cdmx']
        },
        'coahuila': {
            'answer': ['Coahuila', 'coahuila']
        },
        'colima': {
            'answer': ['Colima', 'colima']
        },
        'durango': {
            'answer': ['Durango', 'durango']
        },
        'guanajuato': {
            'answer': ['Guanajuato', 'guanajuato']
        },
        'guerrero': {
            'answer': ['Guerrero', 'guerrero']
        },
        'hidalgo': {
            'answer': ['Hidalgo', 'hidalgo']
        },
        'jalisco': {
            'answer': ['Jalisco', 'jalisco']
        },
        'mexico': {
            'answer': ['México', 'mexico', 'estado de méxico', 'estado de mexico', 'mexico state']
        },
        'michoacan': {
            'answer': ['Michoacán', 'michoacan']
        },
        'morelos': {
            'answer': ['Morelos', 'morelos']
        },
        'nayarit': {
            'answer': ['Nayarit', 'nayarit']
        },
        'nuevo leon': {
            'answer': ['Nuevo León', 'nuevo león', 'nuevo leon']
        },
        'nuevo laredo': {
            'answer': ['Nuevo Laredo', 'nuevo laredo']
        },
        'oaxaca': {
            'answer': ['Oaxaca', 'oaxaca']
        },
        'puebla': {
            'answer': ['Puebla', 'puebla']
        },
        'queretaro': {
            'answer': ['Querétaro', 'queretaro']
        },
        'quintana roo': {
            'answer': ['Quintana Roo', 'quintana roo']
        },
        'san luis potosi': {
            'answer': ['San Luis Potosí', 'san luis potosi', 'slp']
        },
        'sinaloa': {
            'answer': ['Sinaloa', 'sinaloa']
        },
        'sonora': {
            'answer': ['Sonora', 'sonora']
        },
        'tabasco': {
            'answer': ['Tabasco', 'tabasco']
        },
        'tamaulipas': {
            'answer': ['Tamaulipas', 'tamaulipas']
        },
        'tlaxcala': {
            'answer': ['Tlaxcala', 'tlaxcala']
        },
        'veracruz': {
            'answer': ['Veracruz', 'veracruz']
        },
        'yucatan': {
            'answer': ['Yucatán', 'yucatan']
        },
        'zacatecas': {
            'answer': ['Zacatecas', 'zacatecas']
        }
    }

}

emoji = "<:thinking:1277698843932364960>"
current_country = None
game_in_progress = False
subdivision_mode = False
guessed_countries = []
guessed_subdivisions = []
current_image_data = None
lat, lon = None, None
current_subdivision = None

def extract_coords_from_link(link):
    match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', link)
    if match:
        lat = match.group(1)
        lon = match.group(2)
        return lat, lon
    return None, None

# API OpenCageData
def get_country_from_coords(lat, lon):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={OPENCAGE_API_KEY}'
    response = requests.get(url).json()
    
    if response['results']:
        components = response['results'][0]['components']
        country = components.get('country')

        for code, names in territory_codes.items():
            if any(name in components.values() for name in names):
                return names[0]  # Premier nom du pays

        return country

    return None

def check_subdivision_answer(country, user_answer):
    if country in subdivision_data:
        for subdivision, data in subdivision_data[country].items():
            possible_answers = data['answer']
            if user_answer.lower() in [answer.lower() for answer in possible_answers]:
                return subdivision
    return None


@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
async def on_message(message):
    global current_country, game_in_progress, subdivision_mode, current_subdivision, guessed_subdivisions, lat, lon

    if message.author == client.user:
        return

    if client.user in message.mentions:
        await message.channel.send("Don't ping unless urgent!")

    if message.content.lower() == '!stopbot':
        if message.author.guild_permissions.administrator:
            if game_in_progress:
                google_maps_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}"
                
                correct_subdivision = None
                
                if current_country and current_country.lower() in subdivision_data:
                    for user_answer in guessed_subdivisions:
                        correct_subdivision = check_subdivision_answer(current_country.lower(), user_answer)
                        if correct_subdivision:
                            break
                

                if correct_subdivision is None:
                    correct_subdivision = current_subdivision if current_subdivision else "None"
                    
                await message.channel.send(f"Stopped. The correct subdivision answer was: **[{correct_subdivision}]({google_maps_url})**")
                
                current_country = None
                game_in_progress = False
                subdivision_mode = False
                current_subdivision = None
                guessed_subdivisions.clear()
            else:
                await message.channel.send("There is no game in progress.")
        else:
            await message.channel.send("You don't have permission to stop the game.")   

    # DM
    if isinstance(message.channel, discord.DMChannel):
        if game_in_progress:
            await message.channel.send("A challenge is already in progress. Please wait for the current challenge to end first.")
            return
        
        if message.attachments and "www.google.com" in message.content:
            image_url = message.attachments[0].url
            response = requests.get(image_url)
            current_image_data = io.BytesIO(response.content)
            
            lat, lon = extract_coords_from_link(message.content)
            
            if lat and lon:
                current_country = get_country_from_coords(lat, lon)

                channel = client.get_channel(CHANNEL_ID)
                
                if channel:
                    current_image_data.seek(0)
                    embed = discord.Embed(
                        title=f"{message.author.name} challenged you!",
                        description="Find out which country/territory this photo comes from!",
                        color=discord.Color.blue()
                    )
                    embed.set_image(url="attachment://image.png")
                    await channel.send(embed=embed, file=discord.File(fp=current_image_data, filename='image.png'))

                    if current_country:
                        await channel.send("Guess the country/territory with a command like `!france`.")
                        game_in_progress = True
                        guessed_countries.clear()
                        subdivision_mode = False
                        await asyncio.sleep(2)
                        await channel.send(f"Wait a second, is this coverage official {emoji}?")
                    else:
                        await channel.send("I couldn't identify the country. Ping Flykii if you need help")
                    
                    await message.channel.send("It's good :ok_hand:")
            else:
                await message.channel.send("I couldn't extract the coordinates from the Google Maps link. Ping Flykii if you need help")
        else:
            await message.channel.send("Please send a valid Google Maps link with an image attachment. Ping Flykii if you need help")
        return

    if message.channel.id == CHANNEL_ID and game_in_progress:
        if message.content.lower().startswith('!'):
            command = message.content[1:].lower()
            
            if command == "screen" or command == "screenshot":
                if current_image_data:
                    current_image_data.seek(0)
                    embed = discord.Embed(
                        title="Challenge Image",
                        description="Here's the current image.",
                        color=discord.Color.blue()
                    )
                    embed.set_image(url="attachment://image.png")
                    await message.channel.send(embed=embed, file=discord.File(fp=current_image_data, filename='image.png'))
                else:
                    await message.channel.send("No challenge image available.")
                return

            elif command == "guessed":
                if guessed_countries:
                    guessed_list = "\n".join(guessed_countries)
                    await message.channel.send(f"Countries guessed so far:\n{guessed_list}")
                else:
                    await message.channel.send("No countries have been guessed yet.")
                return

            guess = command.lower()

            if not subdivision_mode:
                if guess == current_country.lower() or any(guess == code for code, names in {**country_codes, **territory_codes}.items() if current_country in names):
                    await message.add_reaction('🏆')
                    await message.channel.send(f"Congratulations! The correct country is **{current_country}**!")
                    
                    google_maps_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}"
                    await message.channel.send(f"[View the location on Google Street View]({google_maps_url})")

                    # SUBDIV MOOOOOOOOOOD
                    if current_country.lower() in ['united states', 'canada', 'brazil', 'australia', 'mexico', 'argentina']:
                        subdivision_mode = True
                        current_subdivision = None
                        guessed_subdivisions.clear()
                        embed = discord.Embed(
                            title="Now, guess the subdivision (state/province) for this country!",
                            description=f"What is the name of this subdivision in **{current_country}**?",
                            color=discord.Color.yellow()
                        )
                        await message.channel.send(embed=embed)
                    else:
                        current_country = None
                        game_in_progress = False

                else:
                    if guess not in guessed_countries:
                        guessed_countries.append(guess)
                        await message.add_reaction('❌')
                    else:
                        await message.add_reaction('🔄')

            else:
                correct_subdivision = check_subdivision_answer(current_country.lower(), guess)
                if correct_subdivision:
                    await message.add_reaction('🏆')
                    await message.channel.send(f"Congratulations! The correct subdivision was **{correct_subdivision}** 🐐 !")

                    current_country = None
                    game_in_progress = False
                    subdivision_mode = False
                else:
                    if guess not in guessed_subdivisions:
                        guessed_subdivisions.append(guess)
                        await message.add_reaction('❌') 
                    else:
                        await message.add_reaction('🔄')               


#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE
#               5K CHALLENGE


image_channel_id = 1273947708356431933 # staff-cmds
guess_channel_id = 1298705606995214417   # daily-5k-challenge : 1298705606995214417  ---- bot tests : 1229957623671951361
ping_role_id = 1299390525568323646       # community manager : 1273709328259485868 ---- daily challenge ping : 1299390525568323646
winner_role_id = 1299303928554328124


original_lat = None
original_lon = None
challenge_active = False
last_guess_times = {}

class GuessModal(ui.Modal, title="Submit your guess"):
    def __init__(self):
        super().__init__()
        self.guess = ui.TextInput(
            label="Enter your guess",
            placeholder="/w PlonkIt !g latitude, longitude",
            required=True,
            style=discord.TextStyle.short
        )
        self.add_item(self.guess)

    async def on_submit(self, interaction: discord.Interaction):
        global last_guess_times

        guess_match = re.fullmatch(r"/w PlonkIt !g (-?\d+\.\d+), (-?\d+\.\d+)", self.guess.value.strip())
        if not guess_match:
            await interaction.response.send_message("Invalid format! Please use: `/w PlonkIt !g latitude, longitude`", ephemeral=True)
            return

        guess_lat = float(guess_match.group(1))
        guess_lon = float(guess_match.group(2))
        distance = haversine(original_lat, original_lon, guess_lat, guess_lon)
        formatted_distance = format_distance(distance)
        user_id = interaction.user.id
        now = datetime.now(timezone.utc)

        if user_id in last_guess_times and (now - last_guess_times[user_id]) < timedelta(minutes=3):
            remaining_time = 3 - (now - last_guess_times[user_id]).total_seconds() // 60
            await interaction.response.send_message(f"Sorry {interaction.user.mention}, you can only make a guess once every 3 minutes. Please wait {int(remaining_time)} minutes.", ephemeral=True)
            return
        last_guess_times[user_id] = now
        await interaction.response.send_message("Your guess has been submitted!", ephemeral=True)

        if distance <= 200:
            google_maps_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={original_lat},{original_lon}&heading=0&pitch=0"
            winner_role = discord.utils.get(interaction.guild.roles, id=winner_role_id)
            
            # Retirer le rôle de gagnant précédent
            async for member in interaction.guild.fetch_members():
                if winner_role in member.roles:
                    await member.remove_roles(winner_role)
        
            # Ajouter le rôle au gagnant actuel
            await interaction.user.add_roles(winner_role)

            # Embedding pour la victoire
            embed = discord.Embed(
                title="🎉 5k Achieved!",
                description=f"{interaction.user.mention}, you were {formatted_distance} away!",
                color=discord.Color.green()
            )
            embed.add_field(name="Exact Location", value=f"[Click here to view on Streetview]({google_maps_url})")
            embed.set_footer(text="Great job!")
            
            await interaction.channel.send(embed=embed)
            
            # Stop le challenge
            global challenge_active
            challenge_active = False  # Marquer le challenge comme terminé

            # Annonce du gagnant
            current_date = datetime.now().strftime("%d/%m/%Y")
            winner_channel = interaction.guild.get_channel(1305096064046600263)
            await winner_channel.send(f"5k daily challenge winner of {current_date} is {interaction.user.mention}")
            print(f'5k daily challenge winner of {current_date} is {interaction.user.mention}')

            
            
        else:
            embed = discord.Embed(
                title="🚶 Keep Guessing!",
                description=f"{interaction.user.mention}, you are {format_distance_range(distance)} away.",
                color=discord.Color.orange()
            )
            await interaction.channel.send(embed=embed)

class GuessButton(ui.Button):
    def __init__(self):
        super().__init__(
            label="Guess Here",
            style=discord.ButtonStyle.primary,
            custom_id="guess_button"
        )

    async def callback(self, interaction: discord.Interaction):
        if challenge_active:
            user_id = interaction.user.id
            now = datetime.now(timezone.utc)
            if user_id in last_guess_times and (now - last_guess_times[user_id]) < timedelta(minutes=3):
                remaining_time = 3 - (now - last_guess_times[user_id]).total_seconds() // 60
                await interaction.response.send_message(f"Sorry {interaction.user.mention}, you can only make a guess once every 3 minutes. Please wait {int(remaining_time)} minutes.", ephemeral=True)
                return
            await interaction.response.send_modal(GuessModal())
        else:
            await interaction.response.send_message("There is no active challenge right now!", ephemeral=True)

class GuessView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GuessButton())

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_m = R * c
    return round(distance_m)

def format_distance_range(distance_m):
    if distance_m >= 50000:  # Si distance >= 50 km
        distance_km = distance_m / 1000
        rounded_km = int(round(distance_km + 5, -1))  # Arrondi à la dizaine supérieure
        return f"{rounded_km} Km"
    elif distance_m >= 1000:  # Si 1 km <= distance < 50 km
        distance_km = distance_m / 1000
        lower_bound = int(distance_km // 1)
        upper_bound = lower_bound + 1
        return f"between {lower_bound} and {upper_bound} Km"
    else:  # Si distance < 1 km
        lower_bound = int(distance_m // 100) * 100
        upper_bound = lower_bound + 100
        return f"between {lower_bound} and {upper_bound} meters"

def format_distance(distance_m):
    if distance_m >= 50000:  # Si distance >= 50 km
        distance_km = distance_m / 1000
        distance_miles = distance_km * 0.621371
        rounded_km = int(round(distance_km + 5, -1))  # Arrondi à la dizaine supérieure
        rounded_miles = int(round(distance_miles + 5, -1))  # Arrondi à la dizaine supérieure
        return f"{rounded_km} Km ({rounded_miles} Miles)"
    elif distance_m >= 1000:  # Si 1 km <= distance < 50 km
        distance_km = distance_m / 1000
        distance_miles = distance_km * 0.621371
        return f"{int(round(distance_km))} Km ({int(round(distance_miles))} Miles)"
    else:  # Si distance < 1 km
        distance_feet = distance_m * 3.28084
        return f"{int(round(distance_m))} m ({int(round(distance_feet))} feet)"





def format_distance(distance_m):
    if distance_m >= 1000:
        distance_km = distance_m / 1000
        distance_miles = distance_km * 0.621371
        return f"{round(distance_km)} Km ({round(distance_miles)} Miles)"
    else:
        distance_feet = distance_m * 3.28084
        return f"{round(distance_m)} m ({round(distance_feet)} feet)"




async def background_task_resend_button(channel):
    while challenge_active:
        await asyncio.sleep(600)
        if not challenge_active:
            break
        await channel.send("Make a guess using the button below!", view=GuessView())


async def send_challenge_message(guess_channel):
    global image_url, challenge_active
    if image_url:
        await guess_channel.send(image_url)
    challenge_active = True
    embed = discord.Embed(
        title="New 5K Challenge!",
        description="Guess the location using [the ChatGuessr Map](https://chatguessr.com/map/PlonkIt).\n\n"
        "⚠️ **Note:** Reverse image search tools are **not allowed** to ensure fair play. Check the pinned message for more informations.\n"
        "Make a guess using the button below!",
        color=discord.Color.blue()
    )
    await guess_channel.send(embed=embed, view=GuessView())

    asyncio.create_task(background_task_resend_button(guess_channel))
    

async def send_ping_reminder(challenge_channel):
    role_ping = f"<@&{ping_role_id}>"
    await challenge_channel.send(f"{role_ping} Daily Challenge in 2 minutes!")

async def send_reminder_and_challenge(start_time):
    global challenge_active

    now = datetime.now(timezone.utc)
    challenge_channel = client.get_channel(guess_channel_id)
    reminder_time = start_time - timedelta(minutes=2)

    await asyncio.sleep((reminder_time - now).total_seconds())
    await send_ping_reminder(challenge_channel)

    await asyncio.sleep((start_time - reminder_time).total_seconds())
    await send_challenge_message(challenge_channel)

@client.event
async def on_ready():
    print(f"Bot is ready as {client.user}")

@client.event
async def on_message(message):
    global original_lat, original_lon, image_url, challenge_active, last_guess_times

    if message.author == client.user:
        return

    if message.channel.id == image_channel_id:
        match = re.search(r"/w PlonkIt !g (-?\d+\.\d+), (-?\d+\.\d+)", message.content)
        if match and message.attachments:
            original_lat = float(match.group(1))
            original_lon = float(match.group(2))
            image_url = message.attachments[0].url

            now = datetime.now(timezone.utc)
            start_time = now.replace(hour=18, minute=0, second=0, microsecond=0) # utc (faut rajouter +1 si on veux heure de paris)
            if now >= start_time:
                start_time += timedelta(days=1)
            start_time_paris = start_time + timedelta(hours=1)
            formatted_start_time = start_time_paris.strftime("%d/%m/%Y %H:%M:%S")
            await message.channel.send(f"✅ Challenge is set up and will start today {formatted_start_time} (Paris time).")
            challenge_active = True
            last_guess_times.clear()
            await send_reminder_and_challenge(start_time)

    elif message.channel.id == guess_channel_id:
        if challenge_active and not message.author.bot:
            user_id = message.author.id
            now = datetime.now(timezone.utc)

            if user_id in last_guess_times:
                time_since_last_guess = now - last_guess_times[user_id]
                if time_since_last_guess < timedelta(minutes=3):
                    await message.delete()
                    remaining_time = 3 - time_since_last_guess.total_seconds() // 60
                    await message.channel.send(
                        f"{message.author.mention}, you can only make a guess once every 3 minutes. Please wait {int(remaining_time)} minutes.",
                        delete_after=10
                    )
                    return


client.run('') #bot-token
