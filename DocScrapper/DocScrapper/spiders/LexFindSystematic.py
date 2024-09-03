import scrapy
from scrapy import Request
from scrapy.http import JsonRequest
import requests
from datetime import datetime, timezone
from Connections.AzureDataLake import AzureStorageManager
from hashlib import sha256
from DocScrapper.items import PdfMetaData
 

mapper = {
    "": {
        "children": [
            1,
            75,
            112,
            127,
            175,
            200,
            234,
            286,
            366,
            413
        ]
    },
    "1": {
        "identifier": "1",
        "title": "Staat",
        "parent": None,
        "children": [
            2,
            27,
            53,
            60,
            65
        ],
        "tols": []
    },
    "2": {
        "identifier": "1.10",
        "title": "Grundlagen",
        "parent": 1,
        "children": [
            3,
            4,
            5,
            6,
            7,
            10,
            11,
            16,
            17,
            23,
            497,
            26
        ],
        "tols": []
    },
    "3": {
        "identifier": "1.10.10",
        "title": "Verfassung",
        "parent": 2,
        "children": [],
        "tols": []
    },
    "4": {
        "identifier": "1.10.20",
        "title": "Wappen",
        "parent": 2,
        "children": [],
        "tols": []
    },
    "5": {
        "identifier": "1.10.30",
        "title": "Zusammenarbeit mit dem Ausland",
        "parent": 2,
        "children": [
            504,
            505,
            511
        ],
        "tols": []
    },
    "504": {
        "identifier": "1.10.30.10",
        "title": "Internationale Organisationen",
        "parent": 5,
        "children": [],
        "tols": []
    },
    "505": {
        "identifier": "1.10.30.20",
        "title": "Diplomatische und konsularische Beziehungen",
        "parent": 5,
        "children": [],
        "tols": []
    },
    "511": {
        "identifier": "1.10.30.30",
        "title": "Regelung internationaler Streitigkeiten",
        "parent": 5,
        "children": [],
        "tols": []
    },
    "6": {
        "identifier": "1.10.40",
        "title": "Interkantonale Zusammenarbeit",
        "parent": 2,
        "children": [],
        "tols": []
    },
    "7": {
        "identifier": "1.10.50",
        "title": "Gebiet",
        "parent": 2,
        "children": [
            8,
            9
        ],
        "tols": []
    },
    "8": {
        "identifier": "1.10.50.10",
        "title": "Gebietseinteilung, Bezirke",
        "parent": 7,
        "children": [],
        "tols": []
    },
    "9": {
        "identifier": "1.10.50.20",
        "title": "Grenzen",
        "parent": 7,
        "children": [],
        "tols": []
    },
    "10": {
        "identifier": "1.10.60",
        "title": "Bürgerrecht",
        "parent": 2,
        "children": [],
        "tols": []
    },
    "11": {
        "identifier": "1.10.70",
        "title": "Niederlassung und Aufenthalt",
        "parent": 2,
        "children": [
            410,
            12
        ],
        "tols": []
    },
    "410": {
        "identifier": "1.10.70.10",
        "title": "Niederlassung und Aufenthalt Schweizer",
        "parent": 11,
        "children": [
            411
        ],
        "tols": []
    },
    "411": {
        "identifier": "1.10.70.10.10",
        "title": "Einwohnerkontrolle",
        "parent": 410,
        "children": [],
        "tols": []
    },
    "12": {
        "identifier": "1.10.70.20",
        "title": "Niederlassung und Aufenthalt Ausländer",
        "parent": 11,
        "children": [
            13,
            14,
            15
        ],
        "tols": []
    },
    "13": {
        "identifier": "1.10.70.20.10",
        "title": "Asylwesen",
        "parent": 12,
        "children": [],
        "tols": []
    },
    "14": {
        "identifier": "1.10.70.20.20",
        "title": "Zwangsmassnahmen",
        "parent": 12,
        "children": [],
        "tols": []
    },
    "15": {
        "identifier": "1.10.70.20.30",
        "title": "Integration",
        "parent": 12,
        "children": [],
        "tols": []
    },
    "16": {
        "identifier": "1.10.80",
        "title": "Ausweise",
        "parent": 2,
        "children": [],
        "tols": []
    },
    "17": {
        "identifier": "1.10.90",
        "title": "Grundrechte, Politische Rechte",
        "parent": 2,
        "children": [
            18,
            19
        ],
        "tols": []
    },
    "18": {
        "identifier": "1.10.90.10",
        "title": "Gleichstellung von Mann und Frau",
        "parent": 17,
        "children": [],
        "tols": []
    },
    "19": {
        "identifier": "1.10.90.20",
        "title": "Politische Rechte",
        "parent": 17,
        "children": [
            20,
            21,
            22
        ],
        "tols": []
    },
    "20": {
        "identifier": "1.10.90.20.10",
        "title": "Wahlen und Abstimmungen",
        "parent": 19,
        "children": [],
        "tols": []
    },
    "21": {
        "identifier": "1.10.90.20.20",
        "title": "Landsgemeinde",
        "parent": 19,
        "children": [],
        "tols": []
    },
    "22": {
        "identifier": "1.10.90.20.30",
        "title": "Ausstand, Unvereinbarkeit",
        "parent": 19,
        "children": [],
        "tols": []
    },
    "23": {
        "identifier": "1.10.100",
        "title": "Amtliche Veröffentlichungen",
        "parent": 2,
        "children": [
            24,
            25
        ],
        "tols": []
    },
    "24": {
        "identifier": "1.10.100.10",
        "title": "Gesetzessammlungen",
        "parent": 23,
        "children": [],
        "tols": []
    },
    "25": {
        "identifier": "1.10.100.20",
        "title": "Amtsblätter",
        "parent": 23,
        "children": [],
        "tols": []
    },
    "497": {
        "identifier": "1.10.110",
        "title": "Gesetzgebungsverfahren",
        "parent": 2,
        "children": [],
        "tols": []
    },
    "26": {
        "identifier": "1.10.120",
        "title": "Information der Öffentlichkeit",
        "parent": 2,
        "children": [],
        "tols": []
    },
    "27": {
        "identifier": "1.20",
        "title": "Behörden",
        "parent": 1,
        "children": [
            28,
            31,
            40,
            41,
            42,
            43,
            44,
            498
        ],
        "tols": []
    },
    "28": {
        "identifier": "1.20.10",
        "title": "Parlament",
        "parent": 27,
        "children": [
            29,
            30
        ],
        "tols": []
    },
    "29": {
        "identifier": "1.20.10.10",
        "title": "Wahl des Parlaments",
        "parent": 28,
        "children": [],
        "tols": []
    },
    "30": {
        "identifier": "1.20.10.20",
        "title": "Entschädigung der Parlamentarier",
        "parent": 28,
        "children": [],
        "tols": []
    },
    "31": {
        "identifier": "1.20.20",
        "title": "Regierung und Verwaltung",
        "parent": 27,
        "children": [
            32,
            33,
            481,
            36,
            412,
            438,
            39
        ],
        "tols": []
    },
    "32": {
        "identifier": "1.20.20.10",
        "title": "Organisation",
        "parent": 31,
        "children": [
            482
        ],
        "tols": []
    },
    "482": {
        "identifier": "1.20.20.10.10",
        "title": "Delegation",
        "parent": 32,
        "children": [],
        "tols": []
    },
    "33": {
        "identifier": "1.20.20.20",
        "title": "Regierung",
        "parent": 31,
        "children": [
            34,
            483,
            35,
            484
        ],
        "tols": []
    },
    "34": {
        "identifier": "1.20.20.20.10",
        "title": "Entschädigungen",
        "parent": 33,
        "children": [],
        "tols": []
    },
    "483": {
        "identifier": "1.20.20.20.20",
        "title": "Renten",
        "parent": 33,
        "children": [],
        "tols": []
    },
    "35": {
        "identifier": "1.20.20.20.30",
        "title": "Staatskanzlei",
        "parent": 33,
        "children": [],
        "tols": []
    },
    "484": {
        "identifier": "1.20.20.20.40",
        "title": "Regierungsstatthalter, Oberamtmann",
        "parent": 33,
        "children": [],
        "tols": []
    },
    "481": {
        "identifier": "1.20.20.30",
        "title": "Verwaltung",
        "parent": 31,
        "children": [
            488,
            489,
            490
        ],
        "tols": []
    },
    "488": {
        "identifier": "1.20.20.30.10",
        "title": "Departemente",
        "parent": 481,
        "children": [],
        "tols": []
    },
    "489": {
        "identifier": "1.20.20.30.20",
        "title": "Direktionen und Ämter",
        "parent": 481,
        "children": [],
        "tols": []
    },
    "490": {
        "identifier": "1.20.20.30.30",
        "title": "Kommissionen",
        "parent": 481,
        "children": [],
        "tols": []
    },
    "36": {
        "identifier": "1.20.20.40",
        "title": "Personalrecht",
        "parent": 31,
        "children": [
            37,
            480,
            439,
            38,
            419,
            469,
            476,
            477
        ],
        "tols": []
    },
    "37": {
        "identifier": "1.20.20.40.10",
        "title": "Anstellung",
        "parent": 36,
        "children": [],
        "tols": []
    },
    "480": {
        "identifier": "1.20.20.40.20",
        "title": "Eid",
        "parent": 36,
        "children": [],
        "tols": []
    },
    "439": {
        "identifier": "1.20.20.40.30",
        "title": "Arbeitszeit, Ferien, Urlaub",
        "parent": 36,
        "children": [],
        "tols": []
    },
    "38": {
        "identifier": "1.20.20.40.40",
        "title": "Löhne, Entschädigungen",
        "parent": 36,
        "children": [],
        "tols": []
    },
    "419": {
        "identifier": "1.20.20.40.50",
        "title": "Renten, Versicherungsansprüche",
        "parent": 36,
        "children": [],
        "tols": []
    },
    "469": {
        "identifier": "1.20.20.40.60",
        "title": "Ausbildung, Weiterbildung",
        "parent": 36,
        "children": [],
        "tols": []
    },
    "476": {
        "identifier": "1.20.20.40.70",
        "title": "Parkplätze",
        "parent": 36,
        "children": [],
        "tols": []
    },
    "477": {
        "identifier": "1.20.20.40.80",
        "title": "Personalausschüsse, paritätische Kommissionen",
        "parent": 36,
        "children": [],
        "tols": []
    },
    "412": {
        "identifier": "1.20.20.50",
        "title": "Verwaltungsverfahren, Verwaltungsrechtspflege",
        "parent": 31,
        "children": [],
        "tols": []
    },
    "438": {
        "identifier": "1.20.20.60",
        "title": "Verwaltungsgebühren",
        "parent": 31,
        "children": [],
        "tols": []
    },
    "39": {
        "identifier": "1.20.20.70",
        "title": "New Public Management",
        "parent": 31,
        "children": [],
        "tols": []
    },
    "40": {
        "identifier": "1.20.30",
        "title": "Ombudsperson",
        "parent": 27,
        "children": [],
        "tols": []
    },
    "41": {
        "identifier": "1.20.40",
        "title": "Staatshaftung",
        "parent": 27,
        "children": [],
        "tols": []
    },
    "42": {
        "identifier": "1.20.50",
        "title": "Datenschutz",
        "parent": 27,
        "children": [],
        "tols": []
    },
    "43": {
        "identifier": "1.20.60",
        "title": "Informatik",
        "parent": 27,
        "children": [
            535
        ],
        "tols": []
    },
    "535": {
        "identifier": "1.20.60.10",
        "title": "E-Government",
        "parent": 43,
        "children": [],
        "tols": []
    },
    "44": {
        "identifier": "1.20.70",
        "title": "Gerichtsorganisation",
        "parent": 27,
        "children": [
            45,
            478,
            467,
            468,
            52
        ],
        "tols": []
    },
    "45": {
        "identifier": "1.20.70.10",
        "title": "Gerichtsbehörden",
        "parent": 44,
        "children": [
            46,
            47,
            48,
            49,
            50,
            51
        ],
        "tols": []
    },
    "46": {
        "identifier": "1.20.70.10.10",
        "title": "Untersuchungs- und Anklagebehörden",
        "parent": 45,
        "children": [
            502,
            503
        ],
        "tols": []
    },
    "502": {
        "identifier": "1.20.70.10.10.10",
        "title": "Untersuchungsrichter",
        "parent": 46,
        "children": [],
        "tols": []
    },
    "503": {
        "identifier": "1.20.70.10.10.20",
        "title": "Staatsanwaltschaft",
        "parent": 46,
        "children": [],
        "tols": []
    },
    "47": {
        "identifier": "1.20.70.10.20",
        "title": "Obere Gerichte, Bundesgerichte",
        "parent": 45,
        "children": [],
        "tols": []
    },
    "48": {
        "identifier": "1.20.70.10.30",
        "title": "Verwaltungs-, Versicherungs- und Sozialversicherungsgericht",
        "parent": 45,
        "children": [],
        "tols": []
    },
    "49": {
        "identifier": "1.20.70.10.40",
        "title": "Bezirks-, Amts- und Friedensgericht",
        "parent": 45,
        "children": [],
        "tols": []
    },
    "50": {
        "identifier": "1.20.70.10.50",
        "title": "Arbeits- und Mietgericht",
        "parent": 45,
        "children": [],
        "tols": []
    },
    "51": {
        "identifier": "1.20.70.10.60",
        "title": "Kantonale Rekurskommissionen",
        "parent": 45,
        "children": [],
        "tols": []
    },
    "478": {
        "identifier": "1.20.70.20",
        "title": "Gerichtspersonal",
        "parent": 44,
        "children": [],
        "tols": []
    },
    "467": {
        "identifier": "1.20.70.30",
        "title": "Besoldung und Entschädigung der Richter",
        "parent": 44,
        "children": [],
        "tols": []
    },
    "468": {
        "identifier": "1.20.70.40",
        "title": "Renten und Versicherungsansprücher der Richter",
        "parent": 44,
        "children": [],
        "tols": []
    },
    "52": {
        "identifier": "1.20.70.50",
        "title": "Gerichtskosten, Gerichtsgebühren",
        "parent": 44,
        "children": [],
        "tols": []
    },
    "498": {
        "identifier": "1.20.80",
        "title": "Verfahrensfristen",
        "parent": 27,
        "children": [],
        "tols": []
    },
    "53": {
        "identifier": "1.30",
        "title": "Gemeinden",
        "parent": 1,
        "children": [
            54,
            55,
            56,
            57,
            58,
            59
        ],
        "tols": []
    },
    "54": {
        "identifier": "1.30.10",
        "title": "Gemeindefinanzen",
        "parent": 53,
        "children": [],
        "tols": []
    },
    "55": {
        "identifier": "1.30.20",
        "title": "Gemeindebeiträge",
        "parent": 53,
        "children": [],
        "tols": []
    },
    "56": {
        "identifier": "1.30.30",
        "title": "Gemeindesubventionen",
        "parent": 53,
        "children": [],
        "tols": []
    },
    "57": {
        "identifier": "1.30.40",
        "title": "Aufgabenteilung Kanton-Gemeinden",
        "parent": 53,
        "children": [],
        "tols": []
    },
    "58": {
        "identifier": "1.30.50",
        "title": "Gemeindefusionen",
        "parent": 53,
        "children": [],
        "tols": []
    },
    "59": {
        "identifier": "1.30.60",
        "title": "Bürgergemeinden, Allmend",
        "parent": 53,
        "children": [],
        "tols": []
    },
    "60": {
        "identifier": "1.40",
        "title": "Kirche und Staat",
        "parent": 1,
        "children": [
            61,
            62,
            63,
            64
        ],
        "tols": []
    },
    "61": {
        "identifier": "1.40.10",
        "title": "Römisch-Katholische Kirche",
        "parent": 60,
        "children": [],
        "tols": []
    },
    "62": {
        "identifier": "1.40.20",
        "title": "Christkatholische Kirche",
        "parent": 60,
        "children": [],
        "tols": []
    },
    "63": {
        "identifier": "1.40.30",
        "title": "Evangelisch-Reformierte Kirche",
        "parent": 60,
        "children": [],
        "tols": []
    },
    "64": {
        "identifier": "1.40.40",
        "title": "Andere Religionen",
        "parent": 60,
        "children": [],
        "tols": []
    },
    "65": {
        "identifier": "1.50",
        "title": "Juristische Berufe",
        "parent": 1,
        "children": [
            66,
            70
        ],
        "tols": []
    },
    "66": {
        "identifier": "1.50.10",
        "title": "Anwälte",
        "parent": 65,
        "children": [
            67,
            68,
            69
        ],
        "tols": []
    },
    "67": {
        "identifier": "1.50.10.10",
        "title": "Ausbildung",
        "parent": 66,
        "children": [],
        "tols": []
    },
    "68": {
        "identifier": "1.50.10.20",
        "title": "Honorare",
        "parent": 66,
        "children": [],
        "tols": []
    },
    "69": {
        "identifier": "1.50.10.30",
        "title": "Unentgeltliche Rechtspflege",
        "parent": 66,
        "children": [],
        "tols": []
    },
    "70": {
        "identifier": "1.50.20",
        "title": "Notare",
        "parent": 65,
        "children": [
            71,
            72,
            73,
            74
        ],
        "tols": []
    },
    "71": {
        "identifier": "1.50.20.10",
        "title": "Ausbildung",
        "parent": 70,
        "children": [],
        "tols": []
    },
    "72": {
        "identifier": "1.50.20.20",
        "title": "Gebühren, Tarife",
        "parent": 70,
        "children": [],
        "tols": []
    },
    "73": {
        "identifier": "1.50.20.30",
        "title": "Öffentliche Beurkundung",
        "parent": 70,
        "children": [],
        "tols": []
    },
    "74": {
        "identifier": "1.50.20.40",
        "title": "Rechtsagenten",
        "parent": 70,
        "children": [],
        "tols": []
    },
    "75": {
        "identifier": "2",
        "title": "Zivilrecht",
        "parent": None,
        "children": [
            76,
            88,
            103,
            104,
            105,
            109,
            111,
            416
        ],
        "tols": []
    },
    "76": {
        "identifier": "2.10",
        "title": "Einführungsgesetzgebung zum ZGB",
        "parent": 75,
        "children": [
            77,
            80,
            83,
            84
        ],
        "tols": []
    },
    "77": {
        "identifier": "2.10.10",
        "title": "Personenrecht, Zivilstand",
        "parent": 76,
        "children": [
            491,
            78
        ],
        "tols": []
    },
    "491": {
        "identifier": "2.10.10.10",
        "title": "Eingetragene Partnerschaft",
        "parent": 77,
        "children": [],
        "tols": []
    },
    "78": {
        "identifier": "2.10.10.20",
        "title": "Stiftungen, Stiftungsaufsicht",
        "parent": 77,
        "children": [
            79
        ],
        "tols": []
    },
    "79": {
        "identifier": "2.10.10.20.10",
        "title": "BVG-Stiftungen",
        "parent": 78,
        "children": [],
        "tols": []
    },
    "80": {
        "identifier": "2.10.20",
        "title": "Familienrecht",
        "parent": 76,
        "children": [
            81,
            440,
            82
        ],
        "tols": []
    },
    "81": {
        "identifier": "2.10.20.10",
        "title": "Vormundschaft",
        "parent": 80,
        "children": [],
        "tols": []
    },
    "440": {
        "identifier": "2.10.20.20",
        "title": "Pflegekinder, Adoption",
        "parent": 80,
        "children": [],
        "tols": []
    },
    "82": {
        "identifier": "2.10.20.30",
        "title": "Fürsorgerischer Freiheitsentzug",
        "parent": 80,
        "children": [],
        "tols": []
    },
    "83": {
        "identifier": "2.10.30",
        "title": "Erbrecht",
        "parent": 76,
        "children": [],
        "tols": []
    },
    "84": {
        "identifier": "2.10.40",
        "title": "Sachenrecht",
        "parent": 76,
        "children": [
            85,
            86,
            87
        ],
        "tols": []
    },
    "85": {
        "identifier": "2.10.40.10",
        "title": "Schätzung von Grundstücken",
        "parent": 84,
        "children": [],
        "tols": []
    },
    "86": {
        "identifier": "2.10.40.20",
        "title": "Erwerb von Grundstücke durch Personen im Ausland",
        "parent": 84,
        "children": [],
        "tols": []
    },
    "87": {
        "identifier": "2.10.40.30",
        "title": "Grundbuch und Grundbuchvermessung",
        "parent": 84,
        "children": [],
        "tols": []
    },
    "88": {
        "identifier": "2.20",
        "title": "Einführungsgesetzgebung OR",
        "parent": 75,
        "children": [
            89,
            101
        ],
        "tols": []
    },
    "89": {
        "identifier": "2.20.10",
        "title": "Vertragsverhältnisse",
        "parent": 88,
        "children": [
            90,
            91,
            93,
            94,
            100
        ],
        "tols": []
    },
    "90": {
        "identifier": "2.20.10.10",
        "title": "Versteigerungen",
        "parent": 89,
        "children": [],
        "tols": []
    },
    "91": {
        "identifier": "2.20.10.20",
        "title": "Miete und Pacht",
        "parent": 89,
        "children": [
            92
        ],
        "tols": []
    },
    "92": {
        "identifier": "2.20.10.20.10",
        "title": "Landwirtschaftliche Pacht",
        "parent": 91,
        "children": [],
        "tols": []
    },
    "93": {
        "identifier": "2.20.10.30",
        "title": "Leihe / Darlehen",
        "parent": 89,
        "children": [],
        "tols": []
    },
    "94": {
        "identifier": "2.20.10.40",
        "title": "Arbeitsvertragsrecht",
        "parent": 89,
        "children": [
            95,
            97
        ],
        "tols": []
    },
    "95": {
        "identifier": "2.20.10.40.10",
        "title": "Gesamtarbeitsverträge",
        "parent": 94,
        "children": [
            96
        ],
        "tols": []
    },
    "96": {
        "identifier": "2.20.10.40.10.10",
        "title": "Allgemeinverbindlichkeitserklärungen",
        "parent": 95,
        "children": [],
        "tols": []
    },
    "97": {
        "identifier": "2.20.10.40.20",
        "title": "Normalarbeitsverträge",
        "parent": 94,
        "children": [
            98,
            99
        ],
        "tols": []
    },
    "98": {
        "identifier": "2.20.10.40.20.10",
        "title": "Hausangestellte",
        "parent": 97,
        "children": [],
        "tols": []
    },
    "99": {
        "identifier": "2.20.10.40.20.30",
        "title": "Landwirtschaft",
        "parent": 97,
        "children": [],
        "tols": []
    },
    "100": {
        "identifier": "2.20.10.50",
        "title": "Ehe- und Partnerschaftsvermittlungen",
        "parent": 89,
        "children": [],
        "tols": []
    },
    "101": {
        "identifier": "2.20.20",
        "title": "Handelsrecht",
        "parent": 88,
        "children": [
            102
        ],
        "tols": []
    },
    "102": {
        "identifier": "2.20.20.10",
        "title": "Handelsregister",
        "parent": 101,
        "children": [],
        "tols": []
    },
    "103": {
        "identifier": "2.30",
        "title": "Geistiges Eigentum",
        "parent": 75,
        "children": [],
        "tols": []
    },
    "104": {
        "identifier": "2.40",
        "title": "Unlauterer Wettbewerb / Kartellrecht",
        "parent": 75,
        "children": [],
        "tols": []
    },
    "105": {
        "identifier": "2.50",
        "title": "Zivilrechtspflege",
        "parent": 75,
        "children": [
            106,
            107,
            108
        ],
        "tols": []
    },
    "106": {
        "identifier": "2.50.10",
        "title": "Kosten",
        "parent": 105,
        "children": [],
        "tols": []
    },
    "107": {
        "identifier": "2.50.20",
        "title": "Rechtshilfe",
        "parent": 105,
        "children": [],
        "tols": []
    },
    "108": {
        "identifier": "2.50.30",
        "title": "Vollstreckung",
        "parent": 105,
        "children": [],
        "tols": []
    },
    "109": {
        "identifier": "2.60",
        "title": "Schuldbetreibungs- und Konkursrecht",
        "parent": 75,
        "children": [
            110
        ],
        "tols": []
    },
    "110": {
        "identifier": "2.60.10",
        "title": "Organisation",
        "parent": 109,
        "children": [],
        "tols": []
    },
    "111": {
        "identifier": "2.70",
        "title": "Internationales Privatrecht",
        "parent": 75,
        "children": [],
        "tols": []
    },
    "416": {
        "identifier": "2.80",
        "title": "Schiedsgerichtsbarkeit",
        "parent": 75,
        "children": [],
        "tols": []
    },
    "112": {
        "identifier": "3",
        "title": "Strafrecht",
        "parent": None,
        "children": [
            113,
            115,
            474,
            121,
            118,
            122,
            124
        ],
        "tols": []
    },
    "113": {
        "identifier": "3.10",
        "title": "Einführungsgesetzgebung Strafgesetzbuch",
        "parent": 112,
        "children": [
            114,
            458
        ],
        "tols": []
    },
    "114": {
        "identifier": "3.10.10",
        "title": "Wirtschaftskriminalität, Geldwäscherei",
        "parent": 113,
        "children": [],
        "tols": []
    },
    "458": {
        "identifier": "3.10.20",
        "title": "Schwangerschaftsabbruch",
        "parent": 113,
        "children": [],
        "tols": []
    },
    "115": {
        "identifier": "3.20",
        "title": "Strafprozess",
        "parent": 112,
        "children": [
            528,
            119,
            492,
            493,
            117,
            116,
            120
        ],
        "tols": []
    },
    "528": {
        "identifier": "3.20.10",
        "title": "Strafprozessordnungen",
        "parent": 115,
        "children": [],
        "tols": []
    },
    "119": {
        "identifier": "3.20.20",
        "title": "Gerichtsmedizin",
        "parent": 115,
        "children": [],
        "tols": []
    },
    "492": {
        "identifier": "3.20.30",
        "title": "DNA-Profile",
        "parent": 115,
        "children": [],
        "tols": []
    },
    "493": {
        "identifier": "3.20.40",
        "title": "Verdeckte Ermittlung",
        "parent": 115,
        "children": [],
        "tols": []
    },
    "117": {
        "identifier": "3.20.50",
        "title": "Rechtshilfe",
        "parent": 115,
        "children": [],
        "tols": []
    },
    "116": {
        "identifier": "3.20.60",
        "title": "Kosten",
        "parent": 115,
        "children": [],
        "tols": []
    },
    "120": {
        "identifier": "3.20.70",
        "title": "Opferhilfe",
        "parent": 115,
        "children": [],
        "tols": []
    },
    "474": {
        "identifier": "3.30",
        "title": "Jugendstrafrecht und Jugendstrafprozessrecht",
        "parent": 112,
        "children": [],
        "tols": []
    },
    "121": {
        "identifier": "3.40",
        "title": "Militärstrafrecht",
        "parent": 112,
        "children": [],
        "tols": []
    },
    "118": {
        "identifier": "3.50",
        "title": "Ordnungsbussen",
        "parent": 112,
        "children": [],
        "tols": []
    },
    "122": {
        "identifier": "3.60",
        "title": "Strafregister",
        "parent": 112,
        "children": [
            123
        ],
        "tols": []
    },
    "123": {
        "identifier": "3.60.10",
        "title": "Leumundszeugnisse",
        "parent": 122,
        "children": [],
        "tols": []
    },
    "124": {
        "identifier": "3.70",
        "title": "Straf- und Massnahmenvollzug",
        "parent": 112,
        "children": [
            125,
            126
        ],
        "tols": []
    },
    "125": {
        "identifier": "3.70.10",
        "title": "Anstalten",
        "parent": 124,
        "children": [
            475
        ],
        "tols": []
    },
    "475": {
        "identifier": "3.70.10.10",
        "title": "Personal",
        "parent": 125,
        "children": [],
        "tols": []
    },
    "126": {
        "identifier": "3.70.20",
        "title": "Schutzaufsicht",
        "parent": 124,
        "children": [],
        "tols": []
    },
    "127": {
        "identifier": "4",
        "title": "Schulwesen, Wissenschaft, Dokumentation und Kultur",
        "parent": None,
        "children": [
            128,
            130,
            138,
            131,
            139,
            443,
            163,
            143,
            149,
            157,
            525,
            145,
            462,
            414,
            156,
            165,
            166,
            171
        ],
        "tols": []
    },
    "128": {
        "identifier": "4.10",
        "title": "Vorschule, Primarstufe, Sekundarstufe I",
        "parent": 127,
        "children": [
            360,
            129,
            514
        ],
        "tols": []
    },
    "360": {
        "identifier": "4.10.10",
        "title": "Krippen, Kinderhorte",
        "parent": 128,
        "children": [],
        "tols": []
    },
    "129": {
        "identifier": "4.10.20",
        "title": "Kindergarten",
        "parent": 128,
        "children": [],
        "tols": []
    },
    "514": {
        "identifier": "4.10.30",
        "title": "Volksschule, Primarschule, Sekundarschule I",
        "parent": 128,
        "children": [],
        "tols": []
    },
    "130": {
        "identifier": "4.20",
        "title": "Sekundarstufe II",
        "parent": 127,
        "children": [
            515,
            441,
            442
        ],
        "tols": []
    },
    "515": {
        "identifier": "4.20.10",
        "title": "Mittelschule",
        "parent": 130,
        "children": [],
        "tols": []
    },
    "441": {
        "identifier": "4.20.20",
        "title": "Fachmittelschulen, Diplommittelschulen",
        "parent": 130,
        "children": [],
        "tols": []
    },
    "442": {
        "identifier": "4.20.30",
        "title": "Handelsmittelschulen, Informatikmittelschulen",
        "parent": 130,
        "children": [],
        "tols": []
    },
    "138": {
        "identifier": "4.30",
        "title": "Sekundarstufe II (Berufliche Grundausbildung)",
        "parent": 127,
        "children": [
            154,
            516,
            153,
            517,
            518
        ],
        "tols": []
    },
    "154": {
        "identifier": "4.30.10",
        "title": "Berufsfachschulen",
        "parent": 138,
        "children": [
            155
        ],
        "tols": []
    },
    "155": {
        "identifier": "4.30.10.10",
        "title": "Hauswirtschaftliche Ausbildung",
        "parent": 154,
        "children": [],
        "tols": []
    },
    "516": {
        "identifier": "4.30.20",
        "title": "Berufsmaturitätsschulen",
        "parent": 138,
        "children": [],
        "tols": []
    },
    "153": {
        "identifier": "4.30.30",
        "title": "Berufsorientierung",
        "parent": 138,
        "children": [],
        "tols": []
    },
    "517": {
        "identifier": "4.30.40",
        "title": "Passerelle",
        "parent": 138,
        "children": [],
        "tols": []
    },
    "518": {
        "identifier": "4.30.50",
        "title": "Brückenangebote",
        "parent": 138,
        "children": [],
        "tols": []
    },
    "131": {
        "identifier": "4.40",
        "title": "Tertiärstufe: Universitäten",
        "parent": 127,
        "children": [
            132,
            133,
            134,
            135,
            136,
            137,
            499
        ],
        "tols": []
    },
    "132": {
        "identifier": "4.40.10",
        "title": "Rechtswissenschaftliche Fakultät",
        "parent": 131,
        "children": [],
        "tols": []
    },
    "133": {
        "identifier": "4.40.20",
        "title": "Theologische Fakultät",
        "parent": 131,
        "children": [],
        "tols": []
    },
    "134": {
        "identifier": "4.40.30",
        "title": "Wirtschaftsfakultät",
        "parent": 131,
        "children": [],
        "tols": []
    },
    "135": {
        "identifier": "4.40.40",
        "title": "Naturwissenschaftliche Fakultäten",
        "parent": 131,
        "children": [],
        "tols": []
    },
    "136": {
        "identifier": "4.40.50",
        "title": "Philosophische Fakultäten",
        "parent": 131,
        "children": [],
        "tols": []
    },
    "137": {
        "identifier": "4.40.60",
        "title": "Human- und Veterianärmedizinische Fakultät",
        "parent": 131,
        "children": [],
        "tols": []
    },
    "499": {
        "identifier": "4.40.70",
        "title": "Andere Studiengänge",
        "parent": 131,
        "children": [],
        "tols": []
    },
    "139": {
        "identifier": "4.50",
        "title": "Tertiärstufe: Fachhochschulen",
        "parent": 127,
        "children": [
            140,
            141,
            142,
            501,
            500
        ],
        "tols": []
    },
    "140": {
        "identifier": "4.50.10",
        "title": "Pädagogik",
        "parent": 139,
        "children": [],
        "tols": []
    },
    "141": {
        "identifier": "4.50.20",
        "title": "Soziales",
        "parent": 139,
        "children": [],
        "tols": []
    },
    "142": {
        "identifier": "4.50.30",
        "title": "Wirtschaft",
        "parent": 139,
        "children": [],
        "tols": []
    },
    "501": {
        "identifier": "4.50.40",
        "title": "Landwirtschaft",
        "parent": 139,
        "children": [],
        "tols": []
    },
    "500": {
        "identifier": "4.50.50",
        "title": "Andere Studiengänge",
        "parent": 139,
        "children": [],
        "tols": []
    },
    "443": {
        "identifier": "4.60",
        "title": "Tertiärstufe: Höhere Fachschulen",
        "parent": 127,
        "children": [],
        "tols": []
    },
    "163": {
        "identifier": "4.70",
        "title": "Weiterbildung (Quartärstufe)",
        "parent": 127,
        "children": [
            164,
            519
        ],
        "tols": []
    },
    "164": {
        "identifier": "4.70.10",
        "title": "Erwachsenenbildung",
        "parent": 163,
        "children": [],
        "tols": []
    },
    "519": {
        "identifier": "4.70.20",
        "title": "Weiterbildung Lehrpersonen",
        "parent": 163,
        "children": [],
        "tols": []
    },
    "143": {
        "identifier": "4.80",
        "title": "Sonderpädagogik",
        "parent": 127,
        "children": [
            144,
            510,
            431,
            507,
            444,
            520,
            521,
            522,
            523
        ],
        "tols": []
    },
    "144": {
        "identifier": "4.80.10",
        "title": "Sonderschulen",
        "parent": 143,
        "children": [],
        "tols": []
    },
    "510": {
        "identifier": "4.80.20",
        "title": "Hochbegabtenförderung",
        "parent": 143,
        "children": [],
        "tols": []
    },
    "431": {
        "identifier": "4.80.30",
        "title": "Kunst- und Sportschulen",
        "parent": 143,
        "children": [],
        "tols": []
    },
    "507": {
        "identifier": "4.80.40",
        "title": "Integration fremdsprachiger Schüler",
        "parent": 143,
        "children": [],
        "tols": []
    },
    "444": {
        "identifier": "4.80.50",
        "title": "Logopädie",
        "parent": 143,
        "children": [],
        "tols": []
    },
    "520": {
        "identifier": "4.80.60",
        "title": "Sonderklassen",
        "parent": 143,
        "children": [],
        "tols": []
    },
    "521": {
        "identifier": "4.80.70",
        "title": "Stütz- und Nachhilfeunterricht",
        "parent": 143,
        "children": [],
        "tols": []
    },
    "522": {
        "identifier": "4.80.80",
        "title": "Psychomotorik",
        "parent": 143,
        "children": [],
        "tols": []
    },
    "523": {
        "identifier": "4.80.90",
        "title": "Heilpädagogische Früherziehung",
        "parent": 143,
        "children": [],
        "tols": []
    },
    "149": {
        "identifier": "4.90",
        "title": "Lehrkörper",
        "parent": 127,
        "children": [
            150,
            151,
            152,
            415,
            479
        ],
        "tols": []
    },
    "150": {
        "identifier": "4.90.10",
        "title": "Anstellung",
        "parent": 149,
        "children": [],
        "tols": []
    },
    "151": {
        "identifier": "4.90.20",
        "title": "Löhne, Entschädigungen",
        "parent": 149,
        "children": [],
        "tols": []
    },
    "152": {
        "identifier": "4.90.30",
        "title": "Ausbildung",
        "parent": 149,
        "children": [],
        "tols": []
    },
    "415": {
        "identifier": "4.90.40",
        "title": "Personalvorsorge, Pensionskassen",
        "parent": 149,
        "children": [],
        "tols": []
    },
    "479": {
        "identifier": "4.90.50",
        "title": "Universitätspersonal",
        "parent": 149,
        "children": [],
        "tols": []
    },
    "157": {
        "identifier": "4.100",
        "title": "Ausbildungsbeiträge",
        "parent": 127,
        "children": [
            162,
            158,
            524
        ],
        "tols": []
    },
    "162": {
        "identifier": "4.100.10",
        "title": "Stipendien",
        "parent": 157,
        "children": [],
        "tols": []
    },
    "158": {
        "identifier": "4.100.20",
        "title": "Schulgelder",
        "parent": 157,
        "children": [],
        "tols": []
    },
    "524": {
        "identifier": "4.100.30",
        "title": "Schulgebühren",
        "parent": 157,
        "children": [],
        "tols": []
    },
    "525": {
        "identifier": "4.110",
        "title": "Familienergänzende Tagesstrukturen",
        "parent": 127,
        "children": [],
        "tols": []
    },
    "145": {
        "identifier": "4.120",
        "title": "Qualitätssicherung, Aufsicht, Leitung",
        "parent": 127,
        "children": [
            146,
            147,
            148,
            161,
            508,
            430,
            509,
            506,
            159,
            526,
            527,
            160
        ],
        "tols": []
    },
    "146": {
        "identifier": "4.120.10",
        "title": "Schulkoordination",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "147": {
        "identifier": "4.120.20",
        "title": "Schulgemeinden",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "148": {
        "identifier": "4.120.30",
        "title": "Schulaufsicht",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "161": {
        "identifier": "4.120.40",
        "title": "Lehrmittel",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "508": {
        "identifier": "4.120.50",
        "title": "Förderung von Informationstechnologien",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "430": {
        "identifier": "4.120.60",
        "title": "Schulbauten",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "509": {
        "identifier": "4.120.70",
        "title": "Schulbibliotheken",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "506": {
        "identifier": "4.120.80",
        "title": "Schulleitung",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "159": {
        "identifier": "4.120.90",
        "title": "Gesundheitspflege, schulpsychologische Dienste",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "526": {
        "identifier": "4.120.100",
        "title": "Schulbehörden",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "527": {
        "identifier": "4.120.110",
        "title": "Qualitätssicherung",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "160": {
        "identifier": "4.120.120",
        "title": "Schulversicherung",
        "parent": 145,
        "children": [],
        "tols": []
    },
    "462": {
        "identifier": "4.130",
        "title": "Privatschulen",
        "parent": 127,
        "children": [],
        "tols": []
    },
    "414": {
        "identifier": "4.140",
        "title": "Anerkennung von Diplomen",
        "parent": 127,
        "children": [],
        "tols": []
    },
    "156": {
        "identifier": "4.150",
        "title": "Schulsport",
        "parent": 127,
        "children": [],
        "tols": []
    },
    "165": {
        "identifier": "4.160",
        "title": "Wissenschaft, Forschung",
        "parent": 127,
        "children": [],
        "tols": []
    },
    "166": {
        "identifier": "4.170",
        "title": "Dokumentation",
        "parent": 127,
        "children": [
            167,
            168,
            169,
            170
        ],
        "tols": []
    },
    "167": {
        "identifier": "4.170.10",
        "title": "Statistik",
        "parent": 166,
        "children": [],
        "tols": []
    },
    "168": {
        "identifier": "4.170.20",
        "title": "Archive",
        "parent": 166,
        "children": [],
        "tols": []
    },
    "169": {
        "identifier": "4.170.30",
        "title": "Bibliotheken",
        "parent": 166,
        "children": [],
        "tols": []
    },
    "170": {
        "identifier": "4.170.40",
        "title": "Museen",
        "parent": 166,
        "children": [],
        "tols": []
    },
    "171": {
        "identifier": "4.180",
        "title": "Kunst, Kultur, Sport",
        "parent": 127,
        "children": [
            172,
            174,
            427
        ],
        "tols": []
    },
    "172": {
        "identifier": "4.180.10",
        "title": "Kunst",
        "parent": 171,
        "children": [
            173
        ],
        "tols": []
    },
    "173": {
        "identifier": "4.180.10.10",
        "title": "Film, Theater, Unterhaltung",
        "parent": 172,
        "children": [],
        "tols": []
    },
    "174": {
        "identifier": "4.180.20",
        "title": "Kulturförderung",
        "parent": 171,
        "children": [],
        "tols": []
    },
    "427": {
        "identifier": "4.180.30",
        "title": "Sport",
        "parent": 171,
        "children": [],
        "tols": []
    },
    "175": {
        "identifier": "5",
        "title": "Verteidigung, Bevölkerungsschutz, Polizeiwesen",
        "parent": None,
        "children": [
            176,
            181,
            193,
            436
        ],
        "tols": []
    },
    "176": {
        "identifier": "5.10",
        "title": "Verteidigung",
        "parent": 175,
        "children": [
            177,
            178,
            179,
            180
        ],
        "tols": []
    },
    "177": {
        "identifier": "5.10.10",
        "title": "Militärische Pflichten",
        "parent": 176,
        "children": [],
        "tols": []
    },
    "178": {
        "identifier": "5.10.20",
        "title": "Wehrpflichtersatz",
        "parent": 176,
        "children": [],
        "tols": []
    },
    "179": {
        "identifier": "5.10.30",
        "title": "Militärverwaltung",
        "parent": 176,
        "children": [],
        "tols": []
    },
    "180": {
        "identifier": "5.10.40",
        "title": "Waffenplätze, Zeughäuser",
        "parent": 176,
        "children": [],
        "tols": []
    },
    "181": {
        "identifier": "5.20",
        "title": "Bevölkerungsschutz",
        "parent": 175,
        "children": [
            182,
            186,
            187
        ],
        "tols": []
    },
    "182": {
        "identifier": "5.20.10",
        "title": "Zivilschutz",
        "parent": 181,
        "children": [
            183,
            184,
            185
        ],
        "tols": []
    },
    "183": {
        "identifier": "5.20.10.10",
        "title": "Finanzierung",
        "parent": 182,
        "children": [],
        "tols": []
    },
    "184": {
        "identifier": "5.20.10.20",
        "title": "Baubestimmungen Zivilschutz",
        "parent": 182,
        "children": [],
        "tols": []
    },
    "185": {
        "identifier": "5.20.10.30",
        "title": "Kulturgüterschutz im Kriegsfall",
        "parent": 182,
        "children": [],
        "tols": []
    },
    "186": {
        "identifier": "5.20.20",
        "title": "Landesversorgung",
        "parent": 181,
        "children": [],
        "tols": []
    },
    "187": {
        "identifier": "5.20.30",
        "title": "Feuerwehr / Elementarschäden",
        "parent": 181,
        "children": [
            188,
            189,
            190,
            191
        ],
        "tols": []
    },
    "188": {
        "identifier": "5.20.30.10",
        "title": "Feuerwehr",
        "parent": 187,
        "children": [],
        "tols": []
    },
    "189": {
        "identifier": "5.20.30.20",
        "title": "Brandschutz",
        "parent": 187,
        "children": [],
        "tols": []
    },
    "190": {
        "identifier": "5.20.30.30",
        "title": "Kaminfeger",
        "parent": 187,
        "children": [],
        "tols": []
    },
    "191": {
        "identifier": "5.20.30.40",
        "title": "Gebäudeversicherung",
        "parent": 187,
        "children": [
            192
        ],
        "tols": []
    },
    "192": {
        "identifier": "5.20.30.40.10",
        "title": "Elementarschadenversicherung",
        "parent": 191,
        "children": [],
        "tols": []
    },
    "193": {
        "identifier": "5.30",
        "title": "Innere Sicherheit",
        "parent": 175,
        "children": [
            194,
            197,
            198,
            199,
            435,
            449,
            496
        ],
        "tols": []
    },
    "194": {
        "identifier": "5.30.10",
        "title": "Polizei",
        "parent": 193,
        "children": [
            445,
            446,
            195,
            196,
            422,
            447
        ],
        "tols": []
    },
    "445": {
        "identifier": "5.30.10.10",
        "title": "Kantonspolizei",
        "parent": 194,
        "children": [],
        "tols": []
    },
    "446": {
        "identifier": "5.30.10.20",
        "title": "Gemeindepolizei",
        "parent": 194,
        "children": [],
        "tols": []
    },
    "195": {
        "identifier": "5.30.10.30",
        "title": "Personal",
        "parent": 194,
        "children": [],
        "tols": []
    },
    "196": {
        "identifier": "5.30.10.40",
        "title": "Gebühren",
        "parent": 194,
        "children": [],
        "tols": []
    },
    "422": {
        "identifier": "5.30.10.50",
        "title": "Polizeiliche Zusammenarbeit",
        "parent": 194,
        "children": [],
        "tols": []
    },
    "447": {
        "identifier": "5.30.10.60",
        "title": "Polizeitransporte",
        "parent": 194,
        "children": [],
        "tols": []
    },
    "197": {
        "identifier": "5.30.20",
        "title": "Öffentliche Ruhe und Ordnung",
        "parent": 193,
        "children": [
            448,
            451
        ],
        "tols": []
    },
    "448": {
        "identifier": "5.30.20.10",
        "title": "Hunde, gefährliche Tiere",
        "parent": 197,
        "children": [],
        "tols": []
    },
    "451": {
        "identifier": "5.30.20.20",
        "title": "Gemeingebrauch",
        "parent": 197,
        "children": [],
        "tols": []
    },
    "198": {
        "identifier": "5.30.30",
        "title": "Waffen und Munition",
        "parent": 193,
        "children": [],
        "tols": []
    },
    "199": {
        "identifier": "5.30.40",
        "title": "Sprengstoffe",
        "parent": 193,
        "children": [],
        "tols": []
    },
    "435": {
        "identifier": "5.30.50",
        "title": "Schiesstände",
        "parent": 193,
        "children": [],
        "tols": []
    },
    "449": {
        "identifier": "5.30.60",
        "title": "Sicherheitsunternehmen",
        "parent": 193,
        "children": [],
        "tols": []
    },
    "496": {
        "identifier": "5.30.70",
        "title": "Privatdetektive",
        "parent": 193,
        "children": [],
        "tols": []
    },
    "436": {
        "identifier": "5.40",
        "title": "Zölle",
        "parent": 175,
        "children": [
            530,
            534,
            531,
            532
        ],
        "tols": []
    },
    "530": {
        "identifier": "5.40.10",
        "title": "Grenzwacht",
        "parent": 436,
        "children": [],
        "tols": []
    },
    "534": {
        "identifier": "5.40.20",
        "title": "Grenzabfertigungsstellen",
        "parent": 436,
        "children": [],
        "tols": []
    },
    "531": {
        "identifier": "5.40.30",
        "title": "Warenverkehr",
        "parent": 436,
        "children": [
            533
        ],
        "tols": []
    },
    "533": {
        "identifier": "5.40.30.10",
        "title": "Landwirtschaftliche Erzeugnisse",
        "parent": 531,
        "children": [],
        "tols": []
    },
    "532": {
        "identifier": "5.40.40",
        "title": "Personenverkehr",
        "parent": 436,
        "children": [],
        "tols": []
    },
    "200": {
        "identifier": "6",
        "title": "Finanzen, Steuern, Monopole, Staatliche Unternehmen",
        "parent": None,
        "children": [
            201,
            207,
            223,
            232
        ],
        "tols": []
    },
    "201": {
        "identifier": "6.10",
        "title": "Finanzen",
        "parent": 200,
        "children": [
            202,
            203,
            204,
            205,
            206
        ],
        "tols": []
    },
    "202": {
        "identifier": "6.10.10",
        "title": "Budget und Rechnung",
        "parent": 201,
        "children": [],
        "tols": []
    },
    "203": {
        "identifier": "6.10.20",
        "title": "Finanzausgleich",
        "parent": 201,
        "children": [
            485
        ],
        "tols": []
    },
    "485": {
        "identifier": "6.10.20.10",
        "title": "Interkantonale Zusammenarbeit mit Lastenausgleich",
        "parent": 203,
        "children": [],
        "tols": []
    },
    "204": {
        "identifier": "6.10.30",
        "title": "Staatsbeiträge, Subventionen",
        "parent": 201,
        "children": [],
        "tols": []
    },
    "205": {
        "identifier": "6.10.40",
        "title": "Finanzkontrolle",
        "parent": 201,
        "children": [],
        "tols": []
    },
    "206": {
        "identifier": "6.10.50",
        "title": "Privatisierungen",
        "parent": 201,
        "children": [],
        "tols": []
    },
    "207": {
        "identifier": "6.20",
        "title": "Steuern",
        "parent": 200,
        "children": [
            208,
            215,
            216,
            217,
            424,
            432,
            218,
            219,
            433,
            220,
            221,
            222
        ],
        "tols": []
    },
    "208": {
        "identifier": "6.20.10",
        "title": "Einkommens- Vermögenssteuern / Gewinn- Kapitalsteuern",
        "parent": 207,
        "children": [
            209,
            210,
            211,
            471,
            212,
            213,
            214
        ],
        "tols": []
    },
    "209": {
        "identifier": "6.20.10.10",
        "title": "Bundessteuern",
        "parent": 208,
        "children": [],
        "tols": []
    },
    "210": {
        "identifier": "6.20.10.20",
        "title": "Staatssteuern",
        "parent": 208,
        "children": [],
        "tols": []
    },
    "211": {
        "identifier": "6.20.10.30",
        "title": "Gemeindesteuern",
        "parent": 208,
        "children": [],
        "tols": []
    },
    "471": {
        "identifier": "6.20.10.40",
        "title": "Pauschale Steueranrechnung",
        "parent": 208,
        "children": [],
        "tols": []
    },
    "212": {
        "identifier": "6.20.10.50",
        "title": "Kirchen- und Kultussteuern",
        "parent": 208,
        "children": [],
        "tols": []
    },
    "213": {
        "identifier": "6.20.10.60",
        "title": "Quellensteuern",
        "parent": 208,
        "children": [],
        "tols": []
    },
    "214": {
        "identifier": "6.20.10.70",
        "title": "Steuerfüsse",
        "parent": 208,
        "children": [],
        "tols": []
    },
    "215": {
        "identifier": "6.20.20",
        "title": "Handänderungssteuern",
        "parent": 207,
        "children": [],
        "tols": []
    },
    "216": {
        "identifier": "6.20.30",
        "title": "Liegenschaftssteuern",
        "parent": 207,
        "children": [],
        "tols": []
    },
    "217": {
        "identifier": "6.20.40",
        "title": "Erbschafts- und Schenkungssteuern",
        "parent": 207,
        "children": [],
        "tols": []
    },
    "424": {
        "identifier": "6.20.50",
        "title": "Stempelabgabe",
        "parent": 207,
        "children": [],
        "tols": []
    },
    "432": {
        "identifier": "6.20.60",
        "title": "Verrechnungssteuer",
        "parent": 207,
        "children": [],
        "tols": []
    },
    "218": {
        "identifier": "6.20.70",
        "title": "Hundesteuern",
        "parent": 207,
        "children": [],
        "tols": []
    },
    "219": {
        "identifier": "6.20.80",
        "title": "Vergnügungssteuern",
        "parent": 207,
        "children": [],
        "tols": []
    },
    "433": {
        "identifier": "6.20.90",
        "title": "Kurtaxen, Beherbergungstaxen",
        "parent": 207,
        "children": [],
        "tols": []
    },
    "220": {
        "identifier": "6.20.100",
        "title": "Steuerbefreiung und -erleichterungen",
        "parent": 207,
        "children": [],
        "tols": []
    },
    "221": {
        "identifier": "6.20.110",
        "title": "Ausschluss von Steuerabkommen",
        "parent": 207,
        "children": [],
        "tols": []
    },
    "222": {
        "identifier": "6.20.120",
        "title": "Doppelbesteuerung",
        "parent": 207,
        "children": [],
        "tols": []
    },
    "223": {
        "identifier": "6.30",
        "title": "Monopole, Staatliche Unternehmen",
        "parent": 200,
        "children": [
            224,
            225,
            226,
            450,
            227,
            229
        ],
        "tols": []
    },
    "224": {
        "identifier": "6.30.10",
        "title": "Alkohol",
        "parent": 223,
        "children": [],
        "tols": []
    },
    "225": {
        "identifier": "6.30.20",
        "title": "Bergwerk",
        "parent": 223,
        "children": [],
        "tols": []
    },
    "226": {
        "identifier": "6.30.30",
        "title": "Salzregal",
        "parent": 223,
        "children": [],
        "tols": []
    },
    "450": {
        "identifier": "6.30.40",
        "title": "Erdöl",
        "parent": 223,
        "children": [],
        "tols": []
    },
    "227": {
        "identifier": "6.30.50",
        "title": "Jagd",
        "parent": 223,
        "children": [
            228
        ],
        "tols": []
    },
    "228": {
        "identifier": "6.30.50.10",
        "title": "Jäger",
        "parent": 227,
        "children": [],
        "tols": []
    },
    "229": {
        "identifier": "6.30.60",
        "title": "Fischerei",
        "parent": 223,
        "children": [
            230,
            231
        ],
        "tols": []
    },
    "230": {
        "identifier": "6.30.60.10",
        "title": "Patente",
        "parent": 229,
        "children": [],
        "tols": []
    },
    "231": {
        "identifier": "6.30.60.20",
        "title": "Reviere",
        "parent": 229,
        "children": [],
        "tols": []
    },
    "232": {
        "identifier": "6.40",
        "title": "Staatliche Unternehmen",
        "parent": 200,
        "children": [
            233
        ],
        "tols": []
    },
    "233": {
        "identifier": "6.40.10",
        "title": "Kantonalbanken",
        "parent": 232,
        "children": [],
        "tols": []
    },
    "234": {
        "identifier": "7",
        "title": "Raumplanungs- und Baurecht, Enteignung, Öffentliche Werke, Energie, Verkehr, Umweltschutz, Naturschutz",
        "parent": None,
        "children": [
            235,
            242,
            243,
            252,
            256,
            272,
            281
        ],
        "tols": []
    },
    "235": {
        "identifier": "7.10",
        "title": "Raumplanungs- und Baurecht",
        "parent": 234,
        "children": [
            236,
            237,
            238,
            239,
            240,
            241,
            459
        ],
        "tols": []
    },
    "236": {
        "identifier": "7.10.10",
        "title": "Pläne",
        "parent": 235,
        "children": [],
        "tols": []
    },
    "237": {
        "identifier": "7.10.20",
        "title": "Zonen",
        "parent": 235,
        "children": [],
        "tols": []
    },
    "238": {
        "identifier": "7.10.30",
        "title": "Erschliessung",
        "parent": 235,
        "children": [],
        "tols": []
    },
    "239": {
        "identifier": "7.10.40",
        "title": "Landumlegung",
        "parent": 235,
        "children": [],
        "tols": []
    },
    "240": {
        "identifier": "7.10.50",
        "title": "Verfahren",
        "parent": 235,
        "children": [],
        "tols": []
    },
    "241": {
        "identifier": "7.10.60",
        "title": "Plakate und Werbung",
        "parent": 235,
        "children": [],
        "tols": []
    },
    "459": {
        "identifier": "7.10.70",
        "title": "Parkplätze",
        "parent": 235,
        "children": [],
        "tols": []
    },
    "242": {
        "identifier": "7.20",
        "title": "Enteignung",
        "parent": 234,
        "children": [],
        "tols": []
    },
    "243": {
        "identifier": "7.30",
        "title": "Öffentliche Werke",
        "parent": 234,
        "children": [
            244,
            245,
            248,
            251
        ],
        "tols": []
    },
    "244": {
        "identifier": "7.30.10",
        "title": "Staatliche Gebäude und Liegenschaften",
        "parent": 243,
        "children": [],
        "tols": []
    },
    "245": {
        "identifier": "7.30.20",
        "title": "Wasserbau",
        "parent": 243,
        "children": [
            246,
            247
        ],
        "tols": []
    },
    "246": {
        "identifier": "7.30.20.10",
        "title": "Gewässerkorrekturen / Hochwasserschutz",
        "parent": 245,
        "children": [],
        "tols": []
    },
    "247": {
        "identifier": "7.30.20.20",
        "title": "Gewässernutzung",
        "parent": 245,
        "children": [],
        "tols": []
    },
    "248": {
        "identifier": "7.30.30",
        "title": "Strassen",
        "parent": 243,
        "children": [
            249,
            250
        ],
        "tols": []
    },
    "249": {
        "identifier": "7.30.30.10",
        "title": "Nationalstrassen",
        "parent": 248,
        "children": [],
        "tols": []
    },
    "250": {
        "identifier": "7.30.30.20",
        "title": "Fuss- und Wanderwege",
        "parent": 248,
        "children": [],
        "tols": []
    },
    "251": {
        "identifier": "7.30.40",
        "title": "Submission",
        "parent": 243,
        "children": [],
        "tols": []
    },
    "252": {
        "identifier": "7.40",
        "title": "Energie",
        "parent": 234,
        "children": [
            253,
            254,
            255,
            417
        ],
        "tols": []
    },
    "253": {
        "identifier": "7.40.10",
        "title": "Energieversorgung",
        "parent": 252,
        "children": [],
        "tols": []
    },
    "254": {
        "identifier": "7.40.20",
        "title": "Wasserkraft",
        "parent": 252,
        "children": [],
        "tols": []
    },
    "255": {
        "identifier": "7.40.30",
        "title": "Kernenergie",
        "parent": 252,
        "children": [],
        "tols": []
    },
    "417": {
        "identifier": "7.40.40",
        "title": "Elektrizität",
        "parent": 252,
        "children": [],
        "tols": []
    },
    "256": {
        "identifier": "7.50",
        "title": "Verkehr",
        "parent": 234,
        "children": [
            257,
            261,
            264,
            265,
            266,
            269,
            437,
            512
        ],
        "tols": []
    },
    "257": {
        "identifier": "7.50.10",
        "title": "Öffentlicher Verkehr",
        "parent": 256,
        "children": [
            258,
            259,
            260
        ],
        "tols": []
    },
    "258": {
        "identifier": "7.50.10.10",
        "title": "Regionalverkehr",
        "parent": 257,
        "children": [],
        "tols": []
    },
    "259": {
        "identifier": "7.50.10.20",
        "title": "Eisenbahn",
        "parent": 257,
        "children": [],
        "tols": []
    },
    "260": {
        "identifier": "7.50.10.30",
        "title": "Busse und Trolleybusse",
        "parent": 257,
        "children": [],
        "tols": []
    },
    "261": {
        "identifier": "7.50.20",
        "title": "Strassenverkehr",
        "parent": 256,
        "children": [
            262,
            263,
            466,
            472
        ],
        "tols": []
    },
    "262": {
        "identifier": "7.50.20.10",
        "title": "Strassenverkehrssteuern und -abgaben",
        "parent": 261,
        "children": [],
        "tols": []
    },
    "263": {
        "identifier": "7.50.20.20",
        "title": "Strassenverkehrspolizei",
        "parent": 261,
        "children": [],
        "tols": []
    },
    "466": {
        "identifier": "7.50.20.30",
        "title": "Motorfahrzeugkontrolle",
        "parent": 261,
        "children": [],
        "tols": []
    },
    "472": {
        "identifier": "7.50.20.40",
        "title": "Personenbeförderung",
        "parent": 261,
        "children": [],
        "tols": []
    },
    "264": {
        "identifier": "7.50.30",
        "title": "Seilbahnen, Skilifte",
        "parent": 256,
        "children": [],
        "tols": []
    },
    "265": {
        "identifier": "7.50.40",
        "title": "Rohrleitungen",
        "parent": 256,
        "children": [],
        "tols": []
    },
    "266": {
        "identifier": "7.50.60",
        "title": "Schifffahrt",
        "parent": 256,
        "children": [
            267,
            268
        ],
        "tols": []
    },
    "267": {
        "identifier": "7.50.60.10",
        "title": "Schiffssteuern",
        "parent": 266,
        "children": [],
        "tols": []
    },
    "268": {
        "identifier": "7.50.60.20",
        "title": "Schifffahrtspolizei",
        "parent": 266,
        "children": [],
        "tols": []
    },
    "269": {
        "identifier": "7.50.70",
        "title": "Luftfahrt",
        "parent": 256,
        "children": [
            270,
            271
        ],
        "tols": []
    },
    "270": {
        "identifier": "7.50.70.10",
        "title": "Luftfahrzeuge",
        "parent": 269,
        "children": [],
        "tols": []
    },
    "271": {
        "identifier": "7.50.70.20",
        "title": "Flughäfen, Flugplätze",
        "parent": 269,
        "children": [],
        "tols": []
    },
    "437": {
        "identifier": "7.50.80",
        "title": "Post- und Fernmeldeverkehr",
        "parent": 256,
        "children": [],
        "tols": []
    },
    "512": {
        "identifier": "7.50.90",
        "title": "Weltraumrecht",
        "parent": 256,
        "children": [],
        "tols": []
    },
    "272": {
        "identifier": "7.60",
        "title": "Umweltschutz",
        "parent": 234,
        "children": [
            273,
            274,
            275,
            420,
            276,
            277,
            278,
            279,
            280
        ],
        "tols": []
    },
    "273": {
        "identifier": "7.60.10",
        "title": "Abfälle",
        "parent": 272,
        "children": [],
        "tols": []
    },
    "274": {
        "identifier": "7.60.20",
        "title": "Gewässerschutz",
        "parent": 272,
        "children": [],
        "tols": []
    },
    "275": {
        "identifier": "7.60.30",
        "title": "Lufthygiene",
        "parent": 272,
        "children": [
            495
        ],
        "tols": []
    },
    "495": {
        "identifier": "7.60.30.10",
        "title": "Feinstaub/Smog",
        "parent": 275,
        "children": [],
        "tols": []
    },
    "420": {
        "identifier": "7.60.40",
        "title": "Lärmschutz",
        "parent": 272,
        "children": [],
        "tols": []
    },
    "276": {
        "identifier": "7.60.50",
        "title": "Umweltverträglichkeitsprüfung",
        "parent": 272,
        "children": [],
        "tols": []
    },
    "277": {
        "identifier": "7.60.60",
        "title": "Strahlenschutz",
        "parent": 272,
        "children": [],
        "tols": []
    },
    "278": {
        "identifier": "7.60.70",
        "title": "Gifte, Chemikalien",
        "parent": 272,
        "children": [],
        "tols": []
    },
    "279": {
        "identifier": "7.60.80",
        "title": "Umweltgefährdende Stoffe",
        "parent": 272,
        "children": [],
        "tols": []
    },
    "280": {
        "identifier": "7.60.90",
        "title": "Schadenbekämpfung",
        "parent": 272,
        "children": [],
        "tols": []
    },
    "281": {
        "identifier": "7.70",
        "title": "Natur- und Heimatschutz",
        "parent": 234,
        "children": [
            282,
            283,
            284,
            473,
            285,
            452,
            421
        ],
        "tols": []
    },
    "282": {
        "identifier": "7.70.10",
        "title": "Landschaftsschutz",
        "parent": 281,
        "children": [],
        "tols": []
    },
    "283": {
        "identifier": "7.70.20",
        "title": "Tierschutz",
        "parent": 281,
        "children": [],
        "tols": []
    },
    "284": {
        "identifier": "7.70.30",
        "title": "Pflanzenschutz",
        "parent": 281,
        "children": [],
        "tols": []
    },
    "473": {
        "identifier": "7.70.40",
        "title": "Pilze",
        "parent": 281,
        "children": [],
        "tols": []
    },
    "285": {
        "identifier": "7.70.50",
        "title": "Naturschutz",
        "parent": 281,
        "children": [],
        "tols": []
    },
    "452": {
        "identifier": "7.70.60",
        "title": "Uferschutz",
        "parent": 281,
        "children": [],
        "tols": []
    },
    "421": {
        "identifier": "7.70.70",
        "title": "Denkmalschutz, Kulturgüterschutz",
        "parent": 281,
        "children": [],
        "tols": []
    },
    "286": {
        "identifier": "8",
        "title": "Gesundheitswesen, Arbeit, Sozialversicherungen, Wohnen, Sozialhilfe",
        "parent": None,
        "children": [
            287,
            323,
            333,
            353,
            356
        ],
        "tols": []
    },
    "287": {
        "identifier": "8.10",
        "title": "Gesundheitswesen",
        "parent": 286,
        "children": [
            454,
            288,
            291,
            302,
            303,
            304,
            305,
            306,
            307,
            308,
            311,
            312,
            314
        ],
        "tols": []
    },
    "454": {
        "identifier": "8.10.10",
        "title": "Ethik",
        "parent": 287,
        "children": [],
        "tols": []
    },
    "288": {
        "identifier": "8.10.20",
        "title": "Kranken- und Pflegeanstalten",
        "parent": 287,
        "children": [
            289,
            290,
            470
        ],
        "tols": []
    },
    "289": {
        "identifier": "8.10.20.10",
        "title": "Kantonsspitäler",
        "parent": 288,
        "children": [],
        "tols": []
    },
    "290": {
        "identifier": "8.10.20.20",
        "title": "Psychiatrische Kliniken",
        "parent": 288,
        "children": [],
        "tols": []
    },
    "470": {
        "identifier": "8.10.20.30",
        "title": "Patientenrechte",
        "parent": 288,
        "children": [],
        "tols": []
    },
    "291": {
        "identifier": "8.10.30",
        "title": "Medizinische Berufe",
        "parent": 287,
        "children": [
            292,
            293,
            294,
            295,
            296,
            297,
            298,
            299,
            300,
            301
        ],
        "tols": []
    },
    "292": {
        "identifier": "8.10.30.10",
        "title": "Ärzte",
        "parent": 291,
        "children": [],
        "tols": []
    },
    "293": {
        "identifier": "8.10.30.20",
        "title": "Zahnärzte",
        "parent": 291,
        "children": [],
        "tols": []
    },
    "294": {
        "identifier": "8.10.30.30",
        "title": "Krankenpflegepersonal",
        "parent": 291,
        "children": [],
        "tols": []
    },
    "295": {
        "identifier": "8.10.30.40",
        "title": "Hebammen",
        "parent": 291,
        "children": [],
        "tols": []
    },
    "296": {
        "identifier": "8.10.30.50",
        "title": "Chiropraktiker, Physiotherapeuten",
        "parent": 291,
        "children": [],
        "tols": []
    },
    "297": {
        "identifier": "8.10.30.60",
        "title": "Psychotherapeuten",
        "parent": 291,
        "children": [],
        "tols": []
    },
    "298": {
        "identifier": "8.10.30.70",
        "title": "Naturheilpraktiker",
        "parent": 291,
        "children": [],
        "tols": []
    },
    "299": {
        "identifier": "8.10.30.80",
        "title": "Fusspfleger",
        "parent": 291,
        "children": [],
        "tols": []
    },
    "300": {
        "identifier": "8.10.30.90",
        "title": "Apotheker",
        "parent": 291,
        "children": [],
        "tols": []
    },
    "301": {
        "identifier": "8.10.30.100",
        "title": "Tierärzte",
        "parent": 291,
        "children": [],
        "tols": []
    },
    "302": {
        "identifier": "8.10.40",
        "title": "Medizinische Labors",
        "parent": 287,
        "children": [],
        "tols": []
    },
    "303": {
        "identifier": "8.10.50",
        "title": "Psychiatrische Dienste",
        "parent": 287,
        "children": [],
        "tols": []
    },
    "304": {
        "identifier": "8.10.60",
        "title": "Spitalexterne Krankenpflege",
        "parent": 287,
        "children": [],
        "tols": []
    },
    "305": {
        "identifier": "8.10.70",
        "title": "Heil- und Betäubungsmittel",
        "parent": 287,
        "children": [],
        "tols": []
    },
    "306": {
        "identifier": "8.10.80",
        "title": "Apotheken und Drogerien",
        "parent": 287,
        "children": [],
        "tols": []
    },
    "307": {
        "identifier": "8.10.90",
        "title": "Rettungsdienst",
        "parent": 287,
        "children": [],
        "tols": []
    },
    "308": {
        "identifier": "8.10.100",
        "title": "Krankheitsbekämpfung",
        "parent": 287,
        "children": [
            309,
            310
        ],
        "tols": []
    },
    "309": {
        "identifier": "8.10.100.10",
        "title": "Epidemien, Pandemien",
        "parent": 308,
        "children": [],
        "tols": []
    },
    "310": {
        "identifier": "8.10.100.20",
        "title": "Tuberkulose",
        "parent": 308,
        "children": [],
        "tols": []
    },
    "311": {
        "identifier": "8.10.110",
        "title": "Unfallbekämpfung",
        "parent": 287,
        "children": [],
        "tols": []
    },
    "312": {
        "identifier": "8.10.120",
        "title": "Suchtprävention",
        "parent": 287,
        "children": [
            313,
            463
        ],
        "tols": []
    },
    "313": {
        "identifier": "8.10.120.10",
        "title": "Alkoholismus",
        "parent": 312,
        "children": [],
        "tols": []
    },
    "463": {
        "identifier": "8.10.120.20",
        "title": "Rauchverbote",
        "parent": 312,
        "children": [],
        "tols": []
    },
    "314": {
        "identifier": "8.10.130",
        "title": "Hygiene",
        "parent": 287,
        "children": [
            315,
            453,
            320,
            321,
            322
        ],
        "tols": []
    },
    "315": {
        "identifier": "8.10.130.10",
        "title": "Lebensmittel und Gebrauchsgegenstände",
        "parent": 314,
        "children": [
            316,
            317,
            319
        ],
        "tols": []
    },
    "316": {
        "identifier": "8.10.130.10.10",
        "title": "Lebensmittelaufsicht",
        "parent": 315,
        "children": [],
        "tols": []
    },
    "317": {
        "identifier": "8.10.130.10.20",
        "title": "Fleischhygiene",
        "parent": 315,
        "children": [
            318
        ],
        "tols": []
    },
    "318": {
        "identifier": "8.10.130.10.20.10",
        "title": "Schlachthöfe",
        "parent": 317,
        "children": [],
        "tols": []
    },
    "319": {
        "identifier": "8.10.130.10.30",
        "title": "Pilze",
        "parent": 315,
        "children": [],
        "tols": []
    },
    "453": {
        "identifier": "8.10.130.20",
        "title": "Wasserversorgung",
        "parent": 314,
        "children": [],
        "tols": []
    },
    "320": {
        "identifier": "8.10.130.30",
        "title": "Badeanstalten",
        "parent": 314,
        "children": [],
        "tols": []
    },
    "321": {
        "identifier": "8.10.130.40",
        "title": "Bestattungswesen, Friedhöfe",
        "parent": 314,
        "children": [],
        "tols": []
    },
    "322": {
        "identifier": "8.10.130.50",
        "title": "Tierkörperentsorgung",
        "parent": 314,
        "children": [],
        "tols": []
    },
    "323": {
        "identifier": "8.20",
        "title": "Arbeitsrecht",
        "parent": 286,
        "children": [
            324,
            328,
            332,
            429
        ],
        "tols": []
    },
    "324": {
        "identifier": "8.20.10",
        "title": "Arbeitnehmer",
        "parent": 323,
        "children": [
            455,
            325,
            326,
            327
        ],
        "tols": []
    },
    "455": {
        "identifier": "8.20.10.10",
        "title": "Sicherheit",
        "parent": 324,
        "children": [],
        "tols": []
    },
    "325": {
        "identifier": "8.20.10.20",
        "title": "Arbeitszeit",
        "parent": 324,
        "children": [],
        "tols": []
    },
    "326": {
        "identifier": "8.20.10.30",
        "title": "Sonn- und Feiertage",
        "parent": 324,
        "children": [],
        "tols": []
    },
    "327": {
        "identifier": "8.20.10.40",
        "title": "Mobbing, Sexuelle Belästigung",
        "parent": 324,
        "children": [],
        "tols": []
    },
    "328": {
        "identifier": "8.20.20",
        "title": "Arbeitsmarkt",
        "parent": 323,
        "children": [
            329,
            330,
            331,
            456,
            529
        ],
        "tols": []
    },
    "329": {
        "identifier": "8.20.20.10",
        "title": "Arbeitsbeschaffung, steuerbegünstigte Arbeitsbeschaffungsreserven",
        "parent": 328,
        "children": [],
        "tols": []
    },
    "330": {
        "identifier": "8.20.20.20",
        "title": "Entsendung von Arbeitnehmern",
        "parent": 328,
        "children": [],
        "tols": []
    },
    "331": {
        "identifier": "8.20.20.30",
        "title": "Personenfreizügigkeit",
        "parent": 328,
        "children": [],
        "tols": []
    },
    "456": {
        "identifier": "8.20.20.40",
        "title": "Arbeitsvermittlung und Personalverleih",
        "parent": 328,
        "children": [],
        "tols": []
    },
    "529": {
        "identifier": "8.20.20.50",
        "title": "Schwarzarbeit",
        "parent": 328,
        "children": [],
        "tols": []
    },
    "332": {
        "identifier": "8.20.30",
        "title": "Einigungsämter",
        "parent": 323,
        "children": [],
        "tols": []
    },
    "429": {
        "identifier": "8.20.40",
        "title": "Heimarbeit",
        "parent": 323,
        "children": [],
        "tols": []
    },
    "333": {
        "identifier": "8.30",
        "title": "Sozialversicherungsrecht",
        "parent": 286,
        "children": [
            334,
            335,
            336,
            337,
            338,
            339,
            345,
            346,
            347,
            348,
            351,
            352
        ],
        "tols": []
    },
    "334": {
        "identifier": "8.30.10",
        "title": "Ausgleichskassen",
        "parent": 333,
        "children": [],
        "tols": []
    },
    "335": {
        "identifier": "8.30.20",
        "title": "ATSG",
        "parent": 333,
        "children": [],
        "tols": []
    },
    "336": {
        "identifier": "8.30.30",
        "title": "AHV / IV",
        "parent": 333,
        "children": [],
        "tols": []
    },
    "337": {
        "identifier": "8.30.40",
        "title": "Ergänzungsleistungen",
        "parent": 333,
        "children": [],
        "tols": []
    },
    "338": {
        "identifier": "8.30.50",
        "title": "BVG",
        "parent": 333,
        "children": [],
        "tols": []
    },
    "339": {
        "identifier": "8.30.60",
        "title": "KVG",
        "parent": 333,
        "children": [
            340,
            343,
            344,
            457
        ],
        "tols": []
    },
    "340": {
        "identifier": "8.30.60.10",
        "title": "Tarife",
        "parent": 339,
        "children": [
            341,
            342
        ],
        "tols": []
    },
    "341": {
        "identifier": "8.30.60.10.10",
        "title": "TARMED",
        "parent": 340,
        "children": [],
        "tols": []
    },
    "342": {
        "identifier": "8.30.60.10.20",
        "title": "Vereinbarungen",
        "parent": 340,
        "children": [],
        "tols": []
    },
    "343": {
        "identifier": "8.30.60.20",
        "title": "Prämienverbilligungen",
        "parent": 339,
        "children": [],
        "tols": []
    },
    "344": {
        "identifier": "8.30.60.30",
        "title": "Spitallisten",
        "parent": 339,
        "children": [],
        "tols": []
    },
    "457": {
        "identifier": "8.30.60.40",
        "title": "Einschränkung der Zulassung von Leistungserbringern",
        "parent": 339,
        "children": [],
        "tols": []
    },
    "345": {
        "identifier": "8.30.70",
        "title": "UVG",
        "parent": 333,
        "children": [],
        "tols": []
    },
    "346": {
        "identifier": "8.30.80",
        "title": "Militärversicherung",
        "parent": 333,
        "children": [],
        "tols": []
    },
    "347": {
        "identifier": "8.30.90",
        "title": "Erwerbsersatz",
        "parent": 333,
        "children": [],
        "tols": []
    },
    "348": {
        "identifier": "8.30.100",
        "title": "Familienzulagen",
        "parent": 333,
        "children": [
            349,
            350
        ],
        "tols": []
    },
    "349": {
        "identifier": "8.30.100.10",
        "title": "Landwirtschaftliche Arbeitnehmer",
        "parent": 348,
        "children": [],
        "tols": []
    },
    "350": {
        "identifier": "8.30.100.20",
        "title": "Arbeitnehmer und Selbständige",
        "parent": 348,
        "children": [],
        "tols": []
    },
    "351": {
        "identifier": "8.30.110",
        "title": "Arbeitslosenversicherung",
        "parent": 333,
        "children": [],
        "tols": []
    },
    "352": {
        "identifier": "8.30.120",
        "title": "Mutterschaftsversicherung, Mutterschaftsbeiträge",
        "parent": 333,
        "children": [],
        "tols": []
    },
    "353": {
        "identifier": "8.40",
        "title": "Wohnverhältnisse",
        "parent": 286,
        "children": [
            354,
            355
        ],
        "tols": []
    },
    "354": {
        "identifier": "8.40.10",
        "title": "Eigentums- und Wohnungsbauförderung",
        "parent": 353,
        "children": [],
        "tols": []
    },
    "355": {
        "identifier": "8.40.20",
        "title": "Wohnverhältnisse in Berggebieten",
        "parent": 353,
        "children": [],
        "tols": []
    },
    "356": {
        "identifier": "8.70",
        "title": "Fürsorge",
        "parent": 286,
        "children": [
            418,
            425,
            357,
            361,
            363,
            364,
            365,
            426,
            465
        ],
        "tols": []
    },
    "418": {
        "identifier": "8.70.10",
        "title": "Sozialhilfe",
        "parent": 356,
        "children": [],
        "tols": []
    },
    "425": {
        "identifier": "8.70.20",
        "title": "Jugendschutz, Jugendhilfe",
        "parent": 356,
        "children": [],
        "tols": []
    },
    "357": {
        "identifier": "8.70.30",
        "title": "Heime",
        "parent": 356,
        "children": [
            358,
            359
        ],
        "tols": []
    },
    "358": {
        "identifier": "8.70.30.10",
        "title": "Alters- und Pflegeheime",
        "parent": 357,
        "children": [],
        "tols": []
    },
    "359": {
        "identifier": "8.70.30.20",
        "title": "Kinder- und Jugendheime",
        "parent": 357,
        "children": [],
        "tols": []
    },
    "361": {
        "identifier": "8.70.50",
        "title": "Menschen mit Behinderungen",
        "parent": 356,
        "children": [
            362
        ],
        "tols": []
    },
    "362": {
        "identifier": "8.70.50.10",
        "title": "Eingliederungsstätten, Werkstätte",
        "parent": 361,
        "children": [],
        "tols": []
    },
    "363": {
        "identifier": "8.70.60",
        "title": "Spenden und gemeinnützige Sammlungen",
        "parent": 356,
        "children": [],
        "tols": []
    },
    "364": {
        "identifier": "8.70.70",
        "title": "Alimentenbevorschussung",
        "parent": 356,
        "children": [],
        "tols": []
    },
    "365": {
        "identifier": "8.70.80",
        "title": "Schwangerschaftsberatung",
        "parent": 356,
        "children": [],
        "tols": []
    },
    "426": {
        "identifier": "8.70.90",
        "title": "Familien- und Eheberatung",
        "parent": 356,
        "children": [],
        "tols": []
    },
    "465": {
        "identifier": "8.70.100",
        "title": "Familienpolitik, Familienförderung",
        "parent": 356,
        "children": [],
        "tols": []
    },
    "366": {
        "identifier": "9",
        "title": "Wirtschaft",
        "parent": None,
        "children": [
            434,
            367,
            386,
            389,
            392,
            390
        ],
        "tols": []
    },
    "434": {
        "identifier": "9.10",
        "title": "Wirtschaftsförderung",
        "parent": 366,
        "children": [],
        "tols": []
    },
    "367": {
        "identifier": "9.20",
        "title": "Landwirtschaft",
        "parent": 366,
        "children": [
            368,
            369,
            370,
            371,
            372,
            373,
            374,
            376,
            379,
            381,
            382,
            383,
            384,
            385
        ],
        "tols": []
    },
    "368": {
        "identifier": "9.20.10",
        "title": "Förderungsmassnahmen",
        "parent": 367,
        "children": [],
        "tols": []
    },
    "369": {
        "identifier": "9.20.20",
        "title": "Biologische Landwirtschaft",
        "parent": 367,
        "children": [],
        "tols": []
    },
    "370": {
        "identifier": "9.20.30",
        "title": "Bäuerliches Bodenrecht",
        "parent": 367,
        "children": [],
        "tols": []
    },
    "371": {
        "identifier": "9.20.40",
        "title": "Berggebiete",
        "parent": 367,
        "children": [],
        "tols": []
    },
    "372": {
        "identifier": "9.20.50",
        "title": "Meliorationen",
        "parent": 367,
        "children": [],
        "tols": []
    },
    "373": {
        "identifier": "9.20.60",
        "title": "Landwirtschaftlicher Kredit",
        "parent": 367,
        "children": [],
        "tols": []
    },
    "374": {
        "identifier": "9.20.70",
        "title": "Landwirtschaftliches Bildungswesen",
        "parent": 367,
        "children": [
            375
        ],
        "tols": []
    },
    "375": {
        "identifier": "9.20.70.10",
        "title": "Landwirtschaftliche Schule",
        "parent": 374,
        "children": [],
        "tols": []
    },
    "376": {
        "identifier": "9.20.80",
        "title": "Pflanzenbau",
        "parent": 367,
        "children": [
            377,
            378
        ],
        "tols": []
    },
    "377": {
        "identifier": "9.20.80.10",
        "title": "Rebbau",
        "parent": 376,
        "children": [],
        "tols": []
    },
    "378": {
        "identifier": "9.20.80.20",
        "title": "Schädlingsbekämpfung",
        "parent": 376,
        "children": [],
        "tols": []
    },
    "379": {
        "identifier": "9.20.90",
        "title": "Tierwirtschaftliche Produktion",
        "parent": 367,
        "children": [
            380,
            460
        ],
        "tols": []
    },
    "380": {
        "identifier": "9.20.90.10",
        "title": "Rindvieh und Kleinvieh",
        "parent": 379,
        "children": [],
        "tols": []
    },
    "460": {
        "identifier": "9.20.90.20",
        "title": "Viehhandel",
        "parent": 379,
        "children": [],
        "tols": []
    },
    "381": {
        "identifier": "9.20.100",
        "title": "Milch",
        "parent": 367,
        "children": [],
        "tols": []
    },
    "382": {
        "identifier": "9.20.110",
        "title": "Imkerei",
        "parent": 367,
        "children": [],
        "tols": []
    },
    "383": {
        "identifier": "9.20.120",
        "title": "Tierseuchen",
        "parent": 367,
        "children": [],
        "tols": []
    },
    "384": {
        "identifier": "9.20.130",
        "title": "Alpfahrt",
        "parent": 367,
        "children": [],
        "tols": []
    },
    "385": {
        "identifier": "9.20.140",
        "title": "Viehversicherungen",
        "parent": 367,
        "children": [],
        "tols": []
    },
    "386": {
        "identifier": "9.30",
        "title": "Forstwirtschaft",
        "parent": 366,
        "children": [
            387,
            388,
            461
        ],
        "tols": []
    },
    "387": {
        "identifier": "9.30.10",
        "title": "Schutzmassnahmen",
        "parent": 386,
        "children": [],
        "tols": []
    },
    "388": {
        "identifier": "9.30.20",
        "title": "Forstpersonal",
        "parent": 386,
        "children": [],
        "tols": []
    },
    "461": {
        "identifier": "9.30.30",
        "title": "Bildungswesen",
        "parent": 386,
        "children": [],
        "tols": []
    },
    "389": {
        "identifier": "9.40",
        "title": "Wirtschaftliche Entwicklung in Berggebieten",
        "parent": 366,
        "children": [],
        "tols": []
    },
    "392": {
        "identifier": "9.50",
        "title": "Gewerbe",
        "parent": 366,
        "children": [
            393
        ],
        "tols": []
    },
    "393": {
        "identifier": "9.50.10",
        "title": "Dienstleistungen",
        "parent": 392,
        "children": [
            394,
            395,
            396,
            423,
            398,
            399,
            464,
            401,
            428
        ],
        "tols": []
    },
    "394": {
        "identifier": "9.50.10.10",
        "title": "Berufsausübungsbewilligungen",
        "parent": 393,
        "children": [],
        "tols": []
    },
    "395": {
        "identifier": "9.50.10.20",
        "title": "Tourismus",
        "parent": 393,
        "children": [],
        "tols": []
    },
    "396": {
        "identifier": "9.50.10.30",
        "title": "Gastwirtschaft",
        "parent": 393,
        "children": [
            397
        ],
        "tols": []
    },
    "397": {
        "identifier": "9.50.10.30.10",
        "title": "Camping",
        "parent": 396,
        "children": [],
        "tols": []
    },
    "423": {
        "identifier": "9.50.10.40",
        "title": "Taxigewerbe",
        "parent": 393,
        "children": [],
        "tols": []
    },
    "398": {
        "identifier": "9.50.10.50",
        "title": "Kino-, Theater- und Unterhaltungsgewerbe",
        "parent": 393,
        "children": [],
        "tols": []
    },
    "399": {
        "identifier": "9.50.10.60",
        "title": "Glücksspiel und Lotterien",
        "parent": 393,
        "children": [
            400,
            487,
            486
        ],
        "tols": []
    },
    "400": {
        "identifier": "9.50.10.60.10",
        "title": "Lotteriefonds",
        "parent": 399,
        "children": [],
        "tols": []
    },
    "487": {
        "identifier": "9.50.10.60.20",
        "title": "Sport-Toto",
        "parent": 399,
        "children": [],
        "tols": []
    },
    "486": {
        "identifier": "9.50.10.60.30",
        "title": "Spielbanken",
        "parent": 399,
        "children": [],
        "tols": []
    },
    "464": {
        "identifier": "9.50.10.70",
        "title": "Prostitution",
        "parent": 393,
        "children": [],
        "tols": []
    },
    "401": {
        "identifier": "9.50.10.80",
        "title": "Kreditinstitutionen / Versicherungen",
        "parent": 393,
        "children": [
            402
        ],
        "tols": []
    },
    "402": {
        "identifier": "9.50.10.80.10",
        "title": "Banken, Börsen",
        "parent": 401,
        "children": [],
        "tols": []
    },
    "428": {
        "identifier": "9.50.10.90",
        "title": "Konsumkredit",
        "parent": 393,
        "children": [],
        "tols": []
    },
    "390": {
        "identifier": "9.60",
        "title": "Handel",
        "parent": 366,
        "children": [
            403,
            404,
            405,
            494,
            406,
            407,
            391,
            408,
            409,
            513
        ],
        "tols": []
    },
    "403": {
        "identifier": "9.60.10",
        "title": "Ladenöffnungszeiten",
        "parent": 390,
        "children": [],
        "tols": []
    },
    "404": {
        "identifier": "9.60.20",
        "title": "Messwesen, Zahlungsverkehr",
        "parent": 390,
        "children": [],
        "tols": []
    },
    "405": {
        "identifier": "9.60.30",
        "title": "Preisüberwachung",
        "parent": 390,
        "children": [],
        "tols": []
    },
    "494": {
        "identifier": "9.60.40",
        "title": "Konsumentenschutz",
        "parent": 390,
        "children": [],
        "tols": []
    },
    "406": {
        "identifier": "9.60.50",
        "title": "Binnenmarkt, Handelshemmnisse",
        "parent": 390,
        "children": [],
        "tols": []
    },
    "407": {
        "identifier": "9.60.60",
        "title": "Reisendengewerbe",
        "parent": 390,
        "children": [],
        "tols": []
    },
    "391": {
        "identifier": "9.60.70",
        "title": "Messen, Märkte",
        "parent": 390,
        "children": [],
        "tols": []
    },
    "408": {
        "identifier": "9.60.80",
        "title": "Warenautomaten",
        "parent": 390,
        "children": [],
        "tols": []
    },
    "409": {
        "identifier": "9.60.90",
        "title": "Aussenhandel",
        "parent": 390,
        "children": [],
        "tols": []
    },
    "513": {
        "identifier": "9.60.100",
        "title": "Entwicklung und Zusammenarbeit",
        "parent": 390,
        "children": [],
        "tols": []
    },
    "413": {
        "identifier": "10",
        "title": "Publikationen ohne Text",
        "parent": None,
        "children": [],
        "tols": []
    }
}

params = {
    "active_only": "false",
    "category_filter[]": "1",
    "category_filter[]": "2",
    "category_filter[]": "3",
    "category_filter[]": "4",
    "category_filter[]": "5",
    "category_filter[]": "6",
    "category_filter[]": "7",
    "category_filter[]": "8",
    "category_filter[]": "9",
    "entity_filter[]": "1",
    "entity_filter[]": "10",
    "entity_filter[]": "11",
    "entity_filter[]": "12",
    "entity_filter[]": "13",
    "entity_filter[]": "14",
    "entity_filter[]": "15",
    "entity_filter[]": "16",
    "entity_filter[]": "17",
    "entity_filter[]": "18",
    "entity_filter[]": "19",
    "entity_filter[]": "2",
    "entity_filter[]": "20",
    "entity_filter[]": "21",
    "entity_filter[]": "22",
    "entity_filter[]": "23",
    "entity_filter[]": "24",
    "entity_filter[]": "25",
    "entity_filter[]": "26",
    "entity_filter[]": "27",
    "entity_filter[]": "28",
    "entity_filter[]": "3",
    "entity_filter[]": "4",
    "entity_filter[]": "5",
    "entity_filter[]": "6",
    "entity_filter[]": "7",
    "entity_filter[]": "8",
    "entity_filter[]": "9",
    'tols_for_systematics[]': '',
}

cookies = {
    '__Host-lexfind_be': '2a8cf6ae9326c56ca814ff70d8a62ad2',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
}


pdf_headers = {
    'content-transfer-encoding': 'binary',
    'content-type' : 'application/pdf'

}

BASE_URL = "https://www.lexfind.ch/api/fe/de/global/systematics?active_only=false&category_filter%5B%5D=1&category_filter%5B%5D=2&category_filter%5B%5D=3&category_filter%5B%5D=4&category_filter%5B%5D=5&category_filter%5B%5D=6&category_filter%5B%5D=7&category_filter%5B%5D=8&category_filter%5B%5D=9&entity_filter%5B%5D=1&entity_filter%5B%5D=10&entity_filter%5B%5D=11&entity_filter%5B%5D=12&entity_filter%5B%5D=13&entity_filter%5B%5D=14&entity_filter%5B%5D=15&entity_filter%5B%5D=16&entity_filter%5B%5D=17&entity_filter%5B%5D=18&entity_filter%5B%5D=19&entity_filter%5B%5D=2&entity_filter%5B%5D=20&entity_filter%5B%5D=21&entity_filter%5B%5D=22&entity_filter%5B%5D=23&entity_filter%5B%5D=24&entity_filter%5B%5D=25&entity_filter%5B%5D=26&entity_filter%5B%5D=27&entity_filter%5B%5D=28&entity_filter%5B%5D=3&entity_filter%5B%5D=4&entity_filter%5B%5D=5&entity_filter%5B%5D=6&entity_filter%5B%5D=7&entity_filter%5B%5D=8&entity_filter%5B%5D=9&tols_for_systematics%5B%5D={tols_id}"

LANGUAGES = ['de', 'it', 'fr']

class LexfindsystematicSpider(scrapy.Spider):
    name = "LexFindSystematic"
    allowed_domains = ["www.lexfind.ch"]

    def __init__(self):


        self.blob_storage_manager = AzureStorageManager()


        super(LexfindsystematicSpider, self).__init__()

    def update_params(self, tols_id):
        params_updated = params.copy()
        params_updated.update(tols_id)
        return params_updated

    def start_requests(self):
        # print(mapper.keys())
        for key in mapper.keys() :
             
            yield JsonRequest(
                url = BASE_URL.format(tols_id=key),
              
                headers=headers,
                callback=self.parse_page,
                cb_kwargs={
                    "tols_id": key
                },
                method="GET"
            )


    def parse_page(self, response, tols_id):
 
        response = response.json()[tols_id]
        tols = response['tols']

        for tols_item in tols:
            # print(tols_item)
            for language in LANGUAGES:
                page_pdf_url = f"https://www.lexfind.ch/fe/de/tol/{tols_item['id']}/{language}"
                version_url = f"https://www.lexfind.ch/api/fe/de/texts-of-law/{tols_id}/with-version-groups"
                meta_data = {
                        "id": tols_item['id'],
                        "title" : tols_item['title'],
                        "systematic_number" : tols_item['systematic_number'],
                        "language" : language,
                        "page_pdf_url" : page_pdf_url,
                        "version_url" : version_url
                        }
                yield Request(
                    version_url,
                    callback=self.parse,
                    cb_kwargs={
                    "tols_id" : tols_id,
                    "meta_data": meta_data
                } 
                )

    def parse(self, response, tols_id, meta_data) -> PdfMetaData:
        item =PdfMetaData()
        version_meta_data = response.json()['families'][0][0][0]
        meta_data['version_initial_date'] = version_meta_data['version_active_since']
        meta_data['version_last_update'] = version_meta_data['version_active_since']
         
        latest_pdf_sys_id = version_meta_data['id']
        pdf_download_url = f"https://www.lexfind.ch/tolv/{latest_pdf_sys_id}/{meta_data['language']}"
        meta_data['pdf_download_url'] = pdf_download_url

        pdf_binary = requests.get(pdf_download_url, headers= pdf_headers).content
        meta_data['pdf_content_hash'] = sha256(pdf_binary).hexdigest()

        _, month, year = meta_data['version_last_update'].split('.')

        blob_storage_relative_path = f"{meta_data['language']}/{year}/{month}/{meta_data['pdf_content_hash']}.pdf"
        meta_data['blob_relative_path'] = blob_storage_relative_path
        self.blob_storage_manager.upload_data(pdf_binary, blob_storage_relative_path)
        meta_data['ts_inserted'] = datetime.now(timezone.utc)

        item =PdfMetaData()
        item.update(meta_data)
        yield item
 
