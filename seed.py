import asyncio
import json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.config import settings
from app.database import build_engine

engine = build_engine(settings.database_url)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

HIRAGANA = [
    {
        "kana": "あ",
        "romaji": "a",
        "grp": "vowel"
    },
    {
        "kana": "い",
        "romaji": "i",
        "grp": "vowel"
    },
    {
        "kana": "う",
        "romaji": "u",
        "grp": "vowel"
    },
    {
        "kana": "え",
        "romaji": "e",
        "grp": "vowel"
    },
    {
        "kana": "お",
        "romaji": "o",
        "grp": "vowel"
    },
    {
        "kana": "か",
        "romaji": "ka",
        "grp": "k"
    },
    {
        "kana": "き",
        "romaji": "ki",
        "grp": "k"
    },
    {
        "kana": "く",
        "romaji": "ku",
        "grp": "k"
    },
    {
        "kana": "け",
        "romaji": "ke",
        "grp": "k"
    },
    {
        "kana": "こ",
        "romaji": "ko",
        "grp": "k"
    },
    {
        "kana": "さ",
        "romaji": "sa",
        "grp": "s"
    },
    {
        "kana": "し",
        "romaji": "shi",
        "grp": "s"
    },
    {
        "kana": "す",
        "romaji": "su",
        "grp": "s"
    },
    {
        "kana": "せ",
        "romaji": "se",
        "grp": "s"
    },
    {
        "kana": "そ",
        "romaji": "so",
        "grp": "s"
    },
    {
        "kana": "た",
        "romaji": "ta",
        "grp": "t"
    },
    {
        "kana": "ち",
        "romaji": "chi",
        "grp": "t"
    },
    {
        "kana": "つ",
        "romaji": "tsu",
        "grp": "t"
    },
    {
        "kana": "て",
        "romaji": "te",
        "grp": "t"
    },
    {
        "kana": "と",
        "romaji": "to",
        "grp": "t"
    },
    {
        "kana": "な",
        "romaji": "na",
        "grp": "n"
    },
    {
        "kana": "に",
        "romaji": "ni",
        "grp": "n"
    },
    {
        "kana": "ぬ",
        "romaji": "nu",
        "grp": "n"
    },
    {
        "kana": "ね",
        "romaji": "ne",
        "grp": "n"
    },
    {
        "kana": "の",
        "romaji": "no",
        "grp": "n"
    },
    {
        "kana": "は",
        "romaji": "ha",
        "grp": "h"
    },
    {
        "kana": "ひ",
        "romaji": "hi",
        "grp": "h"
    },
    {
        "kana": "ふ",
        "romaji": "fu",
        "grp": "h"
    },
    {
        "kana": "へ",
        "romaji": "he",
        "grp": "h"
    },
    {
        "kana": "ほ",
        "romaji": "ho",
        "grp": "h"
    },
    {
        "kana": "ま",
        "romaji": "ma",
        "grp": "m"
    },
    {
        "kana": "み",
        "romaji": "mi",
        "grp": "m"
    },
    {
        "kana": "む",
        "romaji": "mu",
        "grp": "m"
    },
    {
        "kana": "め",
        "romaji": "me",
        "grp": "m"
    },
    {
        "kana": "も",
        "romaji": "mo",
        "grp": "m"
    },
    {
        "kana": "や",
        "romaji": "ya",
        "grp": "y"
    },
    {
        "kana": "ゆ",
        "romaji": "yu",
        "grp": "y"
    },
    {
        "kana": "よ",
        "romaji": "yo",
        "grp": "y"
    },
    {
        "kana": "ら",
        "romaji": "ra",
        "grp": "r"
    },
    {
        "kana": "り",
        "romaji": "ri",
        "grp": "r"
    },
    {
        "kana": "る",
        "romaji": "ru",
        "grp": "r"
    },
    {
        "kana": "れ",
        "romaji": "re",
        "grp": "r"
    },
    {
        "kana": "ろ",
        "romaji": "ro",
        "grp": "r"
    },
    {
        "kana": "わ",
        "romaji": "wa",
        "grp": "w"
    },
    {
        "kana": "を",
        "romaji": "wo",
        "grp": "w"
    },
    {
        "kana": "ん",
        "romaji": "n",
        "grp": "special"
    },
    {
        "kana": "が",
        "romaji": "ga",
        "grp": "g"
    },
    {
        "kana": "ぎ",
        "romaji": "gi",
        "grp": "g"
    },
    {
        "kana": "ぐ",
        "romaji": "gu",
        "grp": "g"
    },
    {
        "kana": "げ",
        "romaji": "ge",
        "grp": "g"
    },
    {
        "kana": "ご",
        "romaji": "go",
        "grp": "g"
    },
    {
        "kana": "ざ",
        "romaji": "za",
        "grp": "z"
    },
    {
        "kana": "じ",
        "romaji": "ji",
        "grp": "z"
    },
    {
        "kana": "ず",
        "romaji": "zu",
        "grp": "z"
    },
    {
        "kana": "ぜ",
        "romaji": "ze",
        "grp": "z"
    },
    {
        "kana": "ぞ",
        "romaji": "zo",
        "grp": "z"
    },
    {
        "kana": "だ",
        "romaji": "da",
        "grp": "d"
    },
    {
        "kana": "ぢ",
        "romaji": "di",
        "grp": "d"
    },
    {
        "kana": "づ",
        "romaji": "du",
        "grp": "d"
    },
    {
        "kana": "で",
        "romaji": "de",
        "grp": "d"
    },
    {
        "kana": "ど",
        "romaji": "do",
        "grp": "d"
    },
    {
        "kana": "ば",
        "romaji": "ba",
        "grp": "b"
    },
    {
        "kana": "び",
        "romaji": "bi",
        "grp": "b"
    },
    {
        "kana": "ぶ",
        "romaji": "bu",
        "grp": "b"
    },
    {
        "kana": "べ",
        "romaji": "be",
        "grp": "b"
    },
    {
        "kana": "ぼ",
        "romaji": "bo",
        "grp": "b"
    },
    {
        "kana": "ぱ",
        "romaji": "pa",
        "grp": "p"
    },
    {
        "kana": "ぴ",
        "romaji": "pi",
        "grp": "p"
    },
    {
        "kana": "ぷ",
        "romaji": "pu",
        "grp": "p"
    },
    {
        "kana": "ぺ",
        "romaji": "pe",
        "grp": "p"
    },
    {
        "kana": "ぽ",
        "romaji": "po",
        "grp": "p"
    }
]

KATAKANA = [
    {
        "kana": "ア",
        "romaji": "a",
        "grp": "vowel"
    },
    {
        "kana": "イ",
        "romaji": "i",
        "grp": "vowel"
    },
    {
        "kana": "ウ",
        "romaji": "u",
        "grp": "vowel"
    },
    {
        "kana": "エ",
        "romaji": "e",
        "grp": "vowel"
    },
    {
        "kana": "オ",
        "romaji": "o",
        "grp": "vowel"
    },
    {
        "kana": "カ",
        "romaji": "ka",
        "grp": "k"
    },
    {
        "kana": "キ",
        "romaji": "ki",
        "grp": "k"
    },
    {
        "kana": "ク",
        "romaji": "ku",
        "grp": "k"
    },
    {
        "kana": "ケ",
        "romaji": "ke",
        "grp": "k"
    },
    {
        "kana": "コ",
        "romaji": "ko",
        "grp": "k"
    },
    {
        "kana": "サ",
        "romaji": "sa",
        "grp": "s"
    },
    {
        "kana": "シ",
        "romaji": "shi",
        "grp": "s"
    },
    {
        "kana": "ス",
        "romaji": "su",
        "grp": "s"
    },
    {
        "kana": "セ",
        "romaji": "se",
        "grp": "s"
    },
    {
        "kana": "ソ",
        "romaji": "so",
        "grp": "s"
    },
    {
        "kana": "タ",
        "romaji": "ta",
        "grp": "t"
    },
    {
        "kana": "チ",
        "romaji": "chi",
        "grp": "t"
    },
    {
        "kana": "ツ",
        "romaji": "tsu",
        "grp": "t"
    },
    {
        "kana": "テ",
        "romaji": "te",
        "grp": "t"
    },
    {
        "kana": "ト",
        "romaji": "to",
        "grp": "t"
    },
    {
        "kana": "ナ",
        "romaji": "na",
        "grp": "n"
    },
    {
        "kana": "ニ",
        "romaji": "ni",
        "grp": "n"
    },
    {
        "kana": "ヌ",
        "romaji": "nu",
        "grp": "n"
    },
    {
        "kana": "ネ",
        "romaji": "ne",
        "grp": "n"
    },
    {
        "kana": "ノ",
        "romaji": "no",
        "grp": "n"
    },
    {
        "kana": "ハ",
        "romaji": "ha",
        "grp": "h"
    },
    {
        "kana": "ヒ",
        "romaji": "hi",
        "grp": "h"
    },
    {
        "kana": "フ",
        "romaji": "fu",
        "grp": "h"
    },
    {
        "kana": "ヘ",
        "romaji": "he",
        "grp": "h"
    },
    {
        "kana": "ホ",
        "romaji": "ho",
        "grp": "h"
    },
    {
        "kana": "マ",
        "romaji": "ma",
        "grp": "m"
    },
    {
        "kana": "ミ",
        "romaji": "mi",
        "grp": "m"
    },
    {
        "kana": "ム",
        "romaji": "mu",
        "grp": "m"
    },
    {
        "kana": "メ",
        "romaji": "me",
        "grp": "m"
    },
    {
        "kana": "モ",
        "romaji": "mo",
        "grp": "m"
    },
    {
        "kana": "ヤ",
        "romaji": "ya",
        "grp": "y"
    },
    {
        "kana": "ユ",
        "romaji": "yu",
        "grp": "y"
    },
    {
        "kana": "ヨ",
        "romaji": "yo",
        "grp": "y"
    },
    {
        "kana": "ラ",
        "romaji": "ra",
        "grp": "r"
    },
    {
        "kana": "リ",
        "romaji": "ri",
        "grp": "r"
    },
    {
        "kana": "ル",
        "romaji": "ru",
        "grp": "r"
    },
    {
        "kana": "レ",
        "romaji": "re",
        "grp": "r"
    },
    {
        "kana": "ロ",
        "romaji": "ro",
        "grp": "r"
    },
    {
        "kana": "ワ",
        "romaji": "wa",
        "grp": "w"
    },
    {
        "kana": "ヲ",
        "romaji": "wo",
        "grp": "w"
    },
    {
        "kana": "ン",
        "romaji": "n",
        "grp": "special"
    },
    {
        "kana": "ガ",
        "romaji": "ga",
        "grp": "g"
    },
    {
        "kana": "ギ",
        "romaji": "gi",
        "grp": "g"
    },
    {
        "kana": "グ",
        "romaji": "gu",
        "grp": "g"
    },
    {
        "kana": "ゲ",
        "romaji": "ge",
        "grp": "g"
    },
    {
        "kana": "ゴ",
        "romaji": "go",
        "grp": "g"
    },
    {
        "kana": "ザ",
        "romaji": "za",
        "grp": "z"
    },
    {
        "kana": "ジ",
        "romaji": "ji",
        "grp": "z"
    },
    {
        "kana": "ズ",
        "romaji": "zu",
        "grp": "z"
    },
    {
        "kana": "ゼ",
        "romaji": "ze",
        "grp": "z"
    },
    {
        "kana": "ゾ",
        "romaji": "zo",
        "grp": "z"
    },
    {
        "kana": "ダ",
        "romaji": "da",
        "grp": "d"
    },
    {
        "kana": "ヂ",
        "romaji": "di",
        "grp": "d"
    },
    {
        "kana": "ヅ",
        "romaji": "du",
        "grp": "d"
    },
    {
        "kana": "デ",
        "romaji": "de",
        "grp": "d"
    },
    {
        "kana": "ド",
        "romaji": "do",
        "grp": "d"
    },
    {
        "kana": "バ",
        "romaji": "ba",
        "grp": "b"
    },
    {
        "kana": "ビ",
        "romaji": "bi",
        "grp": "b"
    },
    {
        "kana": "ブ",
        "romaji": "bu",
        "grp": "b"
    },
    {
        "kana": "ベ",
        "romaji": "be",
        "grp": "b"
    },
    {
        "kana": "ボ",
        "romaji": "bo",
        "grp": "b"
    },
    {
        "kana": "パ",
        "romaji": "pa",
        "grp": "p"
    },
    {
        "kana": "ピ",
        "romaji": "pi",
        "grp": "p"
    },
    {
        "kana": "プ",
        "romaji": "pu",
        "grp": "p"
    },
    {
        "kana": "ペ",
        "romaji": "pe",
        "grp": "p"
    },
    {
        "kana": "ポ",
        "romaji": "po",
        "grp": "p"
    }
]

KANJI = [
    {
        "kanji": "一",
        "meaning": [
            "one"
        ],
        "onyomi": [
            "イチ",
            "イツ"
        ],
        "kunyomi": [
            "ひと.つ"
        ],
        "jlpt": "N5",
        "stroke_count": 1,
        "examples": [
            {
                "word": "一つ",
                "reading": "ひとつ",
                "meaning": "one thing"
            },
            {
                "word": "一月",
                "reading": "いちがつ",
                "meaning": "January"
            },
            {
                "word": "一番",
                "reading": "いちばん",
                "meaning": "number one; most"
            }
        ]
    },
    {
        "kanji": "二",
        "meaning": [
            "two"
        ],
        "onyomi": [
            "ニ"
        ],
        "kunyomi": [
            "ふた.つ"
        ],
        "jlpt": "N5",
        "stroke_count": 2,
        "examples": [
            {
                "word": "二つ",
                "reading": "ふたつ",
                "meaning": "two things"
            },
            {
                "word": "二月",
                "reading": "にがつ",
                "meaning": "February"
            },
            {
                "word": "二人",
                "reading": "ふたり",
                "meaning": "two people"
            }
        ]
    },
    {
        "kanji": "三",
        "meaning": [
            "three"
        ],
        "onyomi": [
            "サン"
        ],
        "kunyomi": [
            "みっ.つ"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "三つ",
                "reading": "みっつ",
                "meaning": "three things"
            },
            {
                "word": "三月",
                "reading": "さんがつ",
                "meaning": "March"
            },
            {
                "word": "三人",
                "reading": "さんにん",
                "meaning": "three people"
            }
        ]
    },
    {
        "kanji": "四",
        "meaning": [
            "four"
        ],
        "onyomi": [
            "シ"
        ],
        "kunyomi": [
            "よ.つ",
            "よん"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "四つ",
                "reading": "よっつ",
                "meaning": "four things"
            },
            {
                "word": "四月",
                "reading": "しがつ",
                "meaning": "April"
            },
            {
                "word": "四人",
                "reading": "よにん",
                "meaning": "four people"
            }
        ]
    },
    {
        "kanji": "五",
        "meaning": [
            "five"
        ],
        "onyomi": [
            "ゴ"
        ],
        "kunyomi": [
            "いつ.つ"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "五つ",
                "reading": "いつつ",
                "meaning": "five things"
            },
            {
                "word": "五月",
                "reading": "ごがつ",
                "meaning": "May"
            },
            {
                "word": "五分",
                "reading": "ごふん",
                "meaning": "five minutes"
            }
        ]
    },
    {
        "kanji": "六",
        "meaning": [
            "six"
        ],
        "onyomi": [
            "ロク"
        ],
        "kunyomi": [
            "むっ.つ"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "六つ",
                "reading": "むっつ",
                "meaning": "six things"
            },
            {
                "word": "六月",
                "reading": "ろくがつ",
                "meaning": "June"
            },
            {
                "word": "六時",
                "reading": "ろくじ",
                "meaning": "six o'clock"
            }
        ]
    },
    {
        "kanji": "七",
        "meaning": [
            "seven"
        ],
        "onyomi": [
            "シチ"
        ],
        "kunyomi": [
            "なな.つ"
        ],
        "jlpt": "N5",
        "stroke_count": 2,
        "examples": [
            {
                "word": "七つ",
                "reading": "ななつ",
                "meaning": "seven things"
            },
            {
                "word": "七月",
                "reading": "しちがつ",
                "meaning": "July"
            },
            {
                "word": "七日",
                "reading": "なのか",
                "meaning": "7th day; seven days"
            }
        ]
    },
    {
        "kanji": "八",
        "meaning": [
            "eight"
        ],
        "onyomi": [
            "ハチ"
        ],
        "kunyomi": [
            "やっ.つ"
        ],
        "jlpt": "N5",
        "stroke_count": 2,
        "examples": [
            {
                "word": "八つ",
                "reading": "やっつ",
                "meaning": "eight things"
            },
            {
                "word": "八月",
                "reading": "はちがつ",
                "meaning": "August"
            },
            {
                "word": "八百屋",
                "reading": "やおや",
                "meaning": "greengrocer"
            }
        ]
    },
    {
        "kanji": "九",
        "meaning": [
            "nine"
        ],
        "onyomi": [
            "キュウ",
            "ク"
        ],
        "kunyomi": [
            "ここの.つ"
        ],
        "jlpt": "N5",
        "stroke_count": 2,
        "examples": [
            {
                "word": "九つ",
                "reading": "ここのつ",
                "meaning": "nine things"
            },
            {
                "word": "九月",
                "reading": "くがつ",
                "meaning": "September"
            },
            {
                "word": "九時",
                "reading": "くじ",
                "meaning": "nine o'clock"
            }
        ]
    },
    {
        "kanji": "十",
        "meaning": [
            "ten"
        ],
        "onyomi": [
            "ジュウ",
            "ジッ"
        ],
        "kunyomi": [
            "とお",
            "と"
        ],
        "jlpt": "N5",
        "stroke_count": 2,
        "examples": [
            {
                "word": "十月",
                "reading": "じゅうがつ",
                "meaning": "October"
            },
            {
                "word": "二十歳",
                "reading": "はたち",
                "meaning": "20 years old"
            },
            {
                "word": "十分",
                "reading": "じゅっぷん",
                "meaning": "ten minutes"
            }
        ]
    },
    {
        "kanji": "百",
        "meaning": [
            "hundred"
        ],
        "onyomi": [
            "ヒャク"
        ],
        "kunyomi": [],
        "jlpt": "N5",
        "stroke_count": 6,
        "examples": [
            {
                "word": "百円",
                "reading": "ひゃくえん",
                "meaning": "100 yen"
            },
            {
                "word": "三百",
                "reading": "さんびゃく",
                "meaning": "three hundred"
            },
            {
                "word": "何百",
                "reading": "なんびゃく",
                "meaning": "how many hundreds"
            }
        ]
    },
    {
        "kanji": "千",
        "meaning": [
            "thousand"
        ],
        "onyomi": [
            "セン"
        ],
        "kunyomi": [
            "ち"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "千円",
                "reading": "せんえん",
                "meaning": "1000 yen"
            },
            {
                "word": "三千",
                "reading": "さんぜん",
                "meaning": "three thousand"
            },
            {
                "word": "千葉",
                "reading": "ちば",
                "meaning": "Chiba (place name)"
            }
        ]
    },
    {
        "kanji": "万",
        "meaning": [
            "ten thousand"
        ],
        "onyomi": [
            "マン",
            "バン"
        ],
        "kunyomi": [],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "一万円",
                "reading": "いちまんえん",
                "meaning": "10,000 yen"
            },
            {
                "word": "万年筆",
                "reading": "まんねんひつ",
                "meaning": "fountain pen"
            },
            {
                "word": "万国",
                "reading": "ばんこく",
                "meaning": "all nations"
            }
        ]
    },
    {
        "kanji": "円",
        "meaning": [
            "yen; circle"
        ],
        "onyomi": [
            "エン"
        ],
        "kunyomi": [
            "まる.い"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "五百円",
                "reading": "ごひゃくえん",
                "meaning": "500 yen"
            },
            {
                "word": "円い",
                "reading": "まるい",
                "meaning": "round; circular"
            },
            {
                "word": "円安",
                "reading": "えんやす",
                "meaning": "weak yen"
            }
        ]
    },
    {
        "kanji": "何",
        "meaning": [
            "what; how many"
        ],
        "onyomi": [
            "カ"
        ],
        "kunyomi": [
            "なに",
            "なん"
        ],
        "jlpt": "N5",
        "stroke_count": 7,
        "examples": [
            {
                "word": "何時",
                "reading": "なんじ",
                "meaning": "what time"
            },
            {
                "word": "何人",
                "reading": "なんにん",
                "meaning": "how many people"
            },
            {
                "word": "何月",
                "reading": "なんがつ",
                "meaning": "what month"
            }
        ]
    },
    {
        "kanji": "年",
        "meaning": [
            "year"
        ],
        "onyomi": [
            "ネン"
        ],
        "kunyomi": [
            "とし"
        ],
        "jlpt": "N5",
        "stroke_count": 6,
        "examples": [
            {
                "word": "今年",
                "reading": "ことし",
                "meaning": "this year"
            },
            {
                "word": "来年",
                "reading": "らいねん",
                "meaning": "next year"
            },
            {
                "word": "毎年",
                "reading": "まいとし",
                "meaning": "every year"
            }
        ]
    },
    {
        "kanji": "月",
        "meaning": [
            "moon; month"
        ],
        "onyomi": [
            "ゲツ",
            "ガツ"
        ],
        "kunyomi": [
            "つき"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "月曜日",
                "reading": "げつようび",
                "meaning": "Monday"
            },
            {
                "word": "今月",
                "reading": "こんげつ",
                "meaning": "this month"
            },
            {
                "word": "月見",
                "reading": "つきみ",
                "meaning": "moon viewing"
            }
        ]
    },
    {
        "kanji": "日",
        "meaning": [
            "sun; day"
        ],
        "onyomi": [
            "ニチ",
            "ジツ"
        ],
        "kunyomi": [
            "ひ",
            "か"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "日曜日",
                "reading": "にちようび",
                "meaning": "Sunday"
            },
            {
                "word": "毎日",
                "reading": "まいにち",
                "meaning": "every day"
            },
            {
                "word": "誕生日",
                "reading": "たんじょうび",
                "meaning": "birthday"
            }
        ]
    },
    {
        "kanji": "時",
        "meaning": [
            "time; o'clock"
        ],
        "onyomi": [
            "ジ"
        ],
        "kunyomi": [
            "とき"
        ],
        "jlpt": "N5",
        "stroke_count": 10,
        "examples": [
            {
                "word": "何時",
                "reading": "なんじ",
                "meaning": "what time"
            },
            {
                "word": "時間",
                "reading": "じかん",
                "meaning": "time; hours"
            },
            {
                "word": "時々",
                "reading": "ときどき",
                "meaning": "sometimes"
            }
        ]
    },
    {
        "kanji": "分",
        "meaning": [
            "minute; part"
        ],
        "onyomi": [
            "フン",
            "ブン"
        ],
        "kunyomi": [
            "わ.かる",
            "わ.ける"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "五分",
                "reading": "ごふん",
                "meaning": "five minutes"
            },
            {
                "word": "自分",
                "reading": "じぶん",
                "meaning": "oneself"
            },
            {
                "word": "十分",
                "reading": "じゅうぶん",
                "meaning": "enough; sufficient"
            }
        ]
    },
    {
        "kanji": "半",
        "meaning": [
            "half"
        ],
        "onyomi": [
            "ハン"
        ],
        "kunyomi": [
            "なか.ば"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "三時半",
                "reading": "さんじはん",
                "meaning": "half past three"
            },
            {
                "word": "半分",
                "reading": "はんぶん",
                "meaning": "half"
            },
            {
                "word": "前半",
                "reading": "ぜんはん",
                "meaning": "first half"
            }
        ]
    },
    {
        "kanji": "週",
        "meaning": [
            "week"
        ],
        "onyomi": [
            "シュウ"
        ],
        "kunyomi": [],
        "jlpt": "N5",
        "stroke_count": 11,
        "examples": [
            {
                "word": "今週",
                "reading": "こんしゅう",
                "meaning": "this week"
            },
            {
                "word": "来週",
                "reading": "らいしゅう",
                "meaning": "next week"
            },
            {
                "word": "毎週",
                "reading": "まいしゅう",
                "meaning": "every week"
            }
        ]
    },
    {
        "kanji": "今",
        "meaning": [
            "now; present"
        ],
        "onyomi": [
            "コン",
            "キン"
        ],
        "kunyomi": [
            "いま"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "今日",
                "reading": "きょう",
                "meaning": "today"
            },
            {
                "word": "今年",
                "reading": "ことし",
                "meaning": "this year"
            },
            {
                "word": "今朝",
                "reading": "けさ",
                "meaning": "this morning"
            }
        ]
    },
    {
        "kanji": "毎",
        "meaning": [
            "every; each"
        ],
        "onyomi": [
            "マイ"
        ],
        "kunyomi": [],
        "jlpt": "N5",
        "stroke_count": 6,
        "examples": [
            {
                "word": "毎日",
                "reading": "まいにち",
                "meaning": "every day"
            },
            {
                "word": "毎週",
                "reading": "まいしゅう",
                "meaning": "every week"
            },
            {
                "word": "毎朝",
                "reading": "まいあさ",
                "meaning": "every morning"
            }
        ]
    },
    {
        "kanji": "前",
        "meaning": [
            "before; front"
        ],
        "onyomi": [
            "ゼン"
        ],
        "kunyomi": [
            "まえ"
        ],
        "jlpt": "N5",
        "stroke_count": 9,
        "examples": [
            {
                "word": "午前",
                "reading": "ごぜん",
                "meaning": "AM; morning"
            },
            {
                "word": "名前",
                "reading": "なまえ",
                "meaning": "name"
            },
            {
                "word": "前日",
                "reading": "ぜんじつ",
                "meaning": "the day before"
            }
        ]
    },
    {
        "kanji": "後",
        "meaning": [
            "after; behind"
        ],
        "onyomi": [
            "ゴ",
            "コウ"
        ],
        "kunyomi": [
            "あと",
            "のち",
            "うし.ろ"
        ],
        "jlpt": "N5",
        "stroke_count": 9,
        "examples": [
            {
                "word": "午後",
                "reading": "ごご",
                "meaning": "PM; afternoon"
            },
            {
                "word": "後ろ",
                "reading": "うしろ",
                "meaning": "behind; back"
            },
            {
                "word": "最後",
                "reading": "さいご",
                "meaning": "last; final"
            }
        ]
    },
    {
        "kanji": "朝",
        "meaning": [
            "morning"
        ],
        "onyomi": [
            "チョウ"
        ],
        "kunyomi": [
            "あさ"
        ],
        "jlpt": "N5",
        "stroke_count": 12,
        "examples": [
            {
                "word": "今朝",
                "reading": "けさ",
                "meaning": "this morning"
            },
            {
                "word": "毎朝",
                "reading": "まいあさ",
                "meaning": "every morning"
            },
            {
                "word": "朝食",
                "reading": "ちょうしょく",
                "meaning": "breakfast"
            }
        ]
    },
    {
        "kanji": "夜",
        "meaning": [
            "night; evening"
        ],
        "onyomi": [
            "ヤ"
        ],
        "kunyomi": [
            "よる",
            "よ"
        ],
        "jlpt": "N5",
        "stroke_count": 8,
        "examples": [
            {
                "word": "今夜",
                "reading": "こんや",
                "meaning": "tonight"
            },
            {
                "word": "夜中",
                "reading": "よなか",
                "meaning": "midnight"
            },
            {
                "word": "昨夜",
                "reading": "さくや",
                "meaning": "last night"
            }
        ]
    },
    {
        "kanji": "人",
        "meaning": [
            "person; people"
        ],
        "onyomi": [
            "ジン",
            "ニン"
        ],
        "kunyomi": [
            "ひと"
        ],
        "jlpt": "N5",
        "stroke_count": 2,
        "examples": [
            {
                "word": "日本人",
                "reading": "にほんじん",
                "meaning": "Japanese person"
            },
            {
                "word": "一人",
                "reading": "ひとり",
                "meaning": "one person; alone"
            },
            {
                "word": "大人",
                "reading": "おとな",
                "meaning": "adult"
            }
        ]
    },
    {
        "kanji": "父",
        "meaning": [
            "father"
        ],
        "onyomi": [
            "フ"
        ],
        "kunyomi": [
            "ちち"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "父",
                "reading": "ちち",
                "meaning": "(my) father"
            },
            {
                "word": "父親",
                "reading": "ちちおや",
                "meaning": "father"
            },
            {
                "word": "祖父",
                "reading": "そふ",
                "meaning": "(my) grandfather"
            }
        ]
    },
    {
        "kanji": "母",
        "meaning": [
            "mother"
        ],
        "onyomi": [
            "ボ"
        ],
        "kunyomi": [
            "はは"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "母",
                "reading": "はは",
                "meaning": "(my) mother"
            },
            {
                "word": "母親",
                "reading": "ははおや",
                "meaning": "mother"
            },
            {
                "word": "祖母",
                "reading": "そぼ",
                "meaning": "(my) grandmother"
            }
        ]
    },
    {
        "kanji": "男",
        "meaning": [
            "male; man"
        ],
        "onyomi": [
            "ダン",
            "ナン"
        ],
        "kunyomi": [
            "おとこ"
        ],
        "jlpt": "N5",
        "stroke_count": 7,
        "examples": [
            {
                "word": "男の子",
                "reading": "おとこのこ",
                "meaning": "boy"
            },
            {
                "word": "男性",
                "reading": "だんせい",
                "meaning": "male; man"
            },
            {
                "word": "長男",
                "reading": "ちょうなん",
                "meaning": "eldest son"
            }
        ]
    },
    {
        "kanji": "女",
        "meaning": [
            "female; woman"
        ],
        "onyomi": [
            "ジョ",
            "ニョ"
        ],
        "kunyomi": [
            "おんな",
            "め"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "女の子",
                "reading": "おんなのこ",
                "meaning": "girl"
            },
            {
                "word": "女性",
                "reading": "じょせい",
                "meaning": "female; woman"
            },
            {
                "word": "少女",
                "reading": "しょうじょ",
                "meaning": "young girl"
            }
        ]
    },
    {
        "kanji": "子",
        "meaning": [
            "child"
        ],
        "onyomi": [
            "シ",
            "ス"
        ],
        "kunyomi": [
            "こ"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "子供",
                "reading": "こども",
                "meaning": "child"
            },
            {
                "word": "女の子",
                "reading": "おんなのこ",
                "meaning": "girl"
            },
            {
                "word": "双子",
                "reading": "ふたご",
                "meaning": "twins"
            }
        ]
    },
    {
        "kanji": "先",
        "meaning": [
            "ahead; previous; tip"
        ],
        "onyomi": [
            "セン"
        ],
        "kunyomi": [
            "さき",
            "ま.ず"
        ],
        "jlpt": "N5",
        "stroke_count": 6,
        "examples": [
            {
                "word": "先生",
                "reading": "せんせい",
                "meaning": "teacher"
            },
            {
                "word": "先週",
                "reading": "せんしゅう",
                "meaning": "last week"
            },
            {
                "word": "先に",
                "reading": "さきに",
                "meaning": "ahead; first"
            }
        ]
    },
    {
        "kanji": "生",
        "meaning": [
            "life; birth; raw"
        ],
        "onyomi": [
            "セイ",
            "ショウ"
        ],
        "kunyomi": [
            "い.きる",
            "う.まれる",
            "なま"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "学生",
                "reading": "がくせい",
                "meaning": "student"
            },
            {
                "word": "先生",
                "reading": "せんせい",
                "meaning": "teacher"
            },
            {
                "word": "生まれる",
                "reading": "うまれる",
                "meaning": "to be born"
            }
        ]
    },
    {
        "kanji": "友",
        "meaning": [
            "friend"
        ],
        "onyomi": [
            "ユウ"
        ],
        "kunyomi": [
            "とも"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "友達",
                "reading": "ともだち",
                "meaning": "friend"
            },
            {
                "word": "友人",
                "reading": "ゆうじん",
                "meaning": "friend (formal)"
            },
            {
                "word": "友好",
                "reading": "ゆうこう",
                "meaning": "friendship; amity"
            }
        ]
    },
    {
        "kanji": "手",
        "meaning": [
            "hand"
        ],
        "onyomi": [
            "シュ"
        ],
        "kunyomi": [
            "て"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "右手",
                "reading": "みぎて",
                "meaning": "right hand"
            },
            {
                "word": "手紙",
                "reading": "てがみ",
                "meaning": "letter (mail)"
            },
            {
                "word": "手伝う",
                "reading": "てつだう",
                "meaning": "to help"
            }
        ]
    },
    {
        "kanji": "目",
        "meaning": [
            "eye"
        ],
        "onyomi": [
            "モク",
            "ボク"
        ],
        "kunyomi": [
            "め"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "目玉",
                "reading": "めだま",
                "meaning": "eyeball"
            },
            {
                "word": "一目",
                "reading": "ひとめ",
                "meaning": "at a glance"
            },
            {
                "word": "目的",
                "reading": "もくてき",
                "meaning": "purpose; goal"
            }
        ]
    },
    {
        "kanji": "口",
        "meaning": [
            "mouth"
        ],
        "onyomi": [
            "コウ",
            "ク"
        ],
        "kunyomi": [
            "くち"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "入り口",
                "reading": "いりぐち",
                "meaning": "entrance"
            },
            {
                "word": "出口",
                "reading": "でぐち",
                "meaning": "exit"
            },
            {
                "word": "口紅",
                "reading": "くちべに",
                "meaning": "lipstick"
            }
        ]
    },
    {
        "kanji": "耳",
        "meaning": [
            "ear"
        ],
        "onyomi": [
            "ジ"
        ],
        "kunyomi": [
            "みみ"
        ],
        "jlpt": "N5",
        "stroke_count": 6,
        "examples": [
            {
                "word": "耳鳴り",
                "reading": "みみなり",
                "meaning": "ringing in the ears"
            },
            {
                "word": "耳元",
                "reading": "みみもと",
                "meaning": "close to one's ear"
            },
            {
                "word": "耳鼻科",
                "reading": "じびか",
                "meaning": "ENT clinic"
            }
        ]
    },
    {
        "kanji": "足",
        "meaning": [
            "foot; leg; enough"
        ],
        "onyomi": [
            "ソク"
        ],
        "kunyomi": [
            "あし",
            "た.りる"
        ],
        "jlpt": "N5",
        "stroke_count": 7,
        "examples": [
            {
                "word": "足りる",
                "reading": "たりる",
                "meaning": "to be enough"
            },
            {
                "word": "手足",
                "reading": "てあし",
                "meaning": "hands and feet; limbs"
            },
            {
                "word": "足音",
                "reading": "あしおと",
                "meaning": "sound of footsteps"
            }
        ]
    },
    {
        "kanji": "体",
        "meaning": [
            "body"
        ],
        "onyomi": [
            "タイ",
            "テイ"
        ],
        "kunyomi": [
            "からだ"
        ],
        "jlpt": "N5",
        "stroke_count": 7,
        "examples": [
            {
                "word": "体重",
                "reading": "たいじゅう",
                "meaning": "body weight"
            },
            {
                "word": "体育",
                "reading": "たいいく",
                "meaning": "physical education"
            },
            {
                "word": "体温",
                "reading": "たいおん",
                "meaning": "body temperature"
            }
        ]
    },
    {
        "kanji": "心",
        "meaning": [
            "heart; mind"
        ],
        "onyomi": [
            "シン"
        ],
        "kunyomi": [
            "こころ"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "心配",
                "reading": "しんぱい",
                "meaning": "worry; concern"
            },
            {
                "word": "安心",
                "reading": "あんしん",
                "meaning": "peace of mind"
            },
            {
                "word": "心臓",
                "reading": "しんぞう",
                "meaning": "heart (organ)"
            }
        ]
    },
    {
        "kanji": "山",
        "meaning": [
            "mountain"
        ],
        "onyomi": [
            "サン",
            "ザン"
        ],
        "kunyomi": [
            "やま"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "富士山",
                "reading": "ふじさん",
                "meaning": "Mt. Fuji"
            },
            {
                "word": "山登り",
                "reading": "やまのぼり",
                "meaning": "mountain climbing"
            },
            {
                "word": "火山",
                "reading": "かざん",
                "meaning": "volcano"
            }
        ]
    },
    {
        "kanji": "川",
        "meaning": [
            "river"
        ],
        "onyomi": [
            "セン"
        ],
        "kunyomi": [
            "かわ"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "川原",
                "reading": "かわら",
                "meaning": "riverbed"
            },
            {
                "word": "小川",
                "reading": "おがわ",
                "meaning": "stream; brook"
            },
            {
                "word": "川沿い",
                "reading": "かわぞい",
                "meaning": "along the river"
            }
        ]
    },
    {
        "kanji": "海",
        "meaning": [
            "sea; ocean"
        ],
        "onyomi": [
            "カイ"
        ],
        "kunyomi": [
            "うみ"
        ],
        "jlpt": "N5",
        "stroke_count": 9,
        "examples": [
            {
                "word": "海外",
                "reading": "かいがい",
                "meaning": "overseas; abroad"
            },
            {
                "word": "海水",
                "reading": "かいすい",
                "meaning": "seawater"
            },
            {
                "word": "日本海",
                "reading": "にほんかい",
                "meaning": "Sea of Japan"
            }
        ]
    },
    {
        "kanji": "空",
        "meaning": [
            "sky; empty"
        ],
        "onyomi": [
            "クウ"
        ],
        "kunyomi": [
            "そら",
            "あ.く",
            "から"
        ],
        "jlpt": "N5",
        "stroke_count": 8,
        "examples": [
            {
                "word": "空港",
                "reading": "くうこう",
                "meaning": "airport"
            },
            {
                "word": "青空",
                "reading": "あおぞら",
                "meaning": "blue sky"
            },
            {
                "word": "空気",
                "reading": "くうき",
                "meaning": "air; atmosphere"
            }
        ]
    },
    {
        "kanji": "雨",
        "meaning": [
            "rain"
        ],
        "onyomi": [
            "ウ"
        ],
        "kunyomi": [
            "あめ",
            "あま"
        ],
        "jlpt": "N5",
        "stroke_count": 8,
        "examples": [
            {
                "word": "雨天",
                "reading": "うてん",
                "meaning": "rainy weather"
            },
            {
                "word": "大雨",
                "reading": "おおあめ",
                "meaning": "heavy rain"
            },
            {
                "word": "梅雨",
                "reading": "つゆ",
                "meaning": "rainy season"
            }
        ]
    },
    {
        "kanji": "木",
        "meaning": [
            "tree; wood"
        ],
        "onyomi": [
            "モク",
            "ボク"
        ],
        "kunyomi": [
            "き",
            "こ"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "木曜日",
                "reading": "もくようび",
                "meaning": "Thursday"
            },
            {
                "word": "木材",
                "reading": "もくざい",
                "meaning": "lumber; timber"
            },
            {
                "word": "木の葉",
                "reading": "このは",
                "meaning": "leaf of a tree"
            }
        ]
    },
    {
        "kanji": "花",
        "meaning": [
            "flower"
        ],
        "onyomi": [
            "カ"
        ],
        "kunyomi": [
            "はな"
        ],
        "jlpt": "N5",
        "stroke_count": 7,
        "examples": [
            {
                "word": "花見",
                "reading": "はなみ",
                "meaning": "cherry blossom viewing"
            },
            {
                "word": "花火",
                "reading": "はなび",
                "meaning": "fireworks"
            },
            {
                "word": "生花",
                "reading": "せいか",
                "meaning": "fresh flowers; ikebana"
            }
        ]
    },
    {
        "kanji": "水",
        "meaning": [
            "water"
        ],
        "onyomi": [
            "スイ"
        ],
        "kunyomi": [
            "みず"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "水曜日",
                "reading": "すいようび",
                "meaning": "Wednesday"
            },
            {
                "word": "水道",
                "reading": "すいどう",
                "meaning": "tap water; water supply"
            },
            {
                "word": "水泳",
                "reading": "すいえい",
                "meaning": "swimming"
            }
        ]
    },
    {
        "kanji": "火",
        "meaning": [
            "fire"
        ],
        "onyomi": [
            "カ"
        ],
        "kunyomi": [
            "ひ",
            "ほ"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "火曜日",
                "reading": "かようび",
                "meaning": "Tuesday"
            },
            {
                "word": "火事",
                "reading": "かじ",
                "meaning": "fire; conflagration"
            },
            {
                "word": "花火",
                "reading": "はなび",
                "meaning": "fireworks"
            }
        ]
    },
    {
        "kanji": "土",
        "meaning": [
            "earth; soil"
        ],
        "onyomi": [
            "ド",
            "ト"
        ],
        "kunyomi": [
            "つち"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "土曜日",
                "reading": "どようび",
                "meaning": "Saturday"
            },
            {
                "word": "土地",
                "reading": "とち",
                "meaning": "land; plot"
            },
            {
                "word": "土台",
                "reading": "どだい",
                "meaning": "foundation; base"
            }
        ]
    },
    {
        "kanji": "石",
        "meaning": [
            "stone; rock"
        ],
        "onyomi": [
            "セキ",
            "シャク"
        ],
        "kunyomi": [
            "いし"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "石けん",
                "reading": "せっけん",
                "meaning": "soap"
            },
            {
                "word": "宝石",
                "reading": "ほうせき",
                "meaning": "gem; jewel"
            },
            {
                "word": "石油",
                "reading": "せきゆ",
                "meaning": "petroleum; oil"
            }
        ]
    },
    {
        "kanji": "国",
        "meaning": [
            "country; nation"
        ],
        "onyomi": [
            "コク"
        ],
        "kunyomi": [
            "くに"
        ],
        "jlpt": "N5",
        "stroke_count": 8,
        "examples": [
            {
                "word": "外国",
                "reading": "がいこく",
                "meaning": "foreign country"
            },
            {
                "word": "国際",
                "reading": "こくさい",
                "meaning": "international"
            },
            {
                "word": "中国",
                "reading": "ちゅうごく",
                "meaning": "China"
            }
        ]
    },
    {
        "kanji": "学",
        "meaning": [
            "study; learn"
        ],
        "onyomi": [
            "ガク"
        ],
        "kunyomi": [
            "まな.ぶ"
        ],
        "jlpt": "N5",
        "stroke_count": 8,
        "examples": [
            {
                "word": "学校",
                "reading": "がっこう",
                "meaning": "school"
            },
            {
                "word": "大学",
                "reading": "だいがく",
                "meaning": "university"
            },
            {
                "word": "学生",
                "reading": "がくせい",
                "meaning": "student"
            }
        ]
    },
    {
        "kanji": "校",
        "meaning": [
            "school"
        ],
        "onyomi": [
            "コウ"
        ],
        "kunyomi": [],
        "jlpt": "N5",
        "stroke_count": 10,
        "examples": [
            {
                "word": "学校",
                "reading": "がっこう",
                "meaning": "school"
            },
            {
                "word": "高校",
                "reading": "こうこう",
                "meaning": "high school"
            },
            {
                "word": "校長",
                "reading": "こうちょう",
                "meaning": "school principal"
            }
        ]
    },
    {
        "kanji": "会",
        "meaning": [
            "meeting; society"
        ],
        "onyomi": [
            "カイ",
            "エ"
        ],
        "kunyomi": [
            "あ.う",
            "あつ.まる"
        ],
        "jlpt": "N5",
        "stroke_count": 6,
        "examples": [
            {
                "word": "会社",
                "reading": "かいしゃ",
                "meaning": "company"
            },
            {
                "word": "会議",
                "reading": "かいぎ",
                "meaning": "meeting"
            },
            {
                "word": "社会",
                "reading": "しゃかい",
                "meaning": "society"
            }
        ]
    },
    {
        "kanji": "社",
        "meaning": [
            "company; shrine"
        ],
        "onyomi": [
            "シャ"
        ],
        "kunyomi": [
            "やしろ"
        ],
        "jlpt": "N5",
        "stroke_count": 7,
        "examples": [
            {
                "word": "会社",
                "reading": "かいしゃ",
                "meaning": "company"
            },
            {
                "word": "社長",
                "reading": "しゃちょう",
                "meaning": "company president"
            },
            {
                "word": "神社",
                "reading": "じんじゃ",
                "meaning": "Shinto shrine"
            }
        ]
    },
    {
        "kanji": "店",
        "meaning": [
            "shop; store"
        ],
        "onyomi": [
            "テン"
        ],
        "kunyomi": [
            "みせ"
        ],
        "jlpt": "N5",
        "stroke_count": 8,
        "examples": [
            {
                "word": "喫茶店",
                "reading": "きっさてん",
                "meaning": "café"
            },
            {
                "word": "本屋",
                "reading": "ほんや",
                "meaning": "bookstore"
            },
            {
                "word": "店員",
                "reading": "てんいん",
                "meaning": "shop clerk"
            }
        ]
    },
    {
        "kanji": "車",
        "meaning": [
            "car; vehicle; wheel"
        ],
        "onyomi": [
            "シャ"
        ],
        "kunyomi": [
            "くるま"
        ],
        "jlpt": "N5",
        "stroke_count": 7,
        "examples": [
            {
                "word": "電車",
                "reading": "でんしゃ",
                "meaning": "train"
            },
            {
                "word": "自転車",
                "reading": "じてんしゃ",
                "meaning": "bicycle"
            },
            {
                "word": "自動車",
                "reading": "じどうしゃ",
                "meaning": "automobile"
            }
        ]
    },
    {
        "kanji": "電",
        "meaning": [
            "electricity; lightning"
        ],
        "onyomi": [
            "デン"
        ],
        "kunyomi": [],
        "jlpt": "N5",
        "stroke_count": 13,
        "examples": [
            {
                "word": "電車",
                "reading": "でんしゃ",
                "meaning": "train"
            },
            {
                "word": "電話",
                "reading": "でんわ",
                "meaning": "telephone"
            },
            {
                "word": "電気",
                "reading": "でんき",
                "meaning": "electricity; light"
            }
        ]
    },
    {
        "kanji": "駅",
        "meaning": [
            "station"
        ],
        "onyomi": [
            "エキ"
        ],
        "kunyomi": [],
        "jlpt": "N5",
        "stroke_count": 14,
        "examples": [
            {
                "word": "駅員",
                "reading": "えきいん",
                "meaning": "station staff"
            },
            {
                "word": "近くの駅",
                "reading": "ちかくのえき",
                "meaning": "nearby station"
            },
            {
                "word": "終点駅",
                "reading": "しゅうてんえき",
                "meaning": "terminal station"
            }
        ]
    },
    {
        "kanji": "東",
        "meaning": [
            "east"
        ],
        "onyomi": [
            "トウ"
        ],
        "kunyomi": [
            "ひがし"
        ],
        "jlpt": "N5",
        "stroke_count": 8,
        "examples": [
            {
                "word": "東京",
                "reading": "とうきょう",
                "meaning": "Tokyo"
            },
            {
                "word": "東口",
                "reading": "ひがしぐち",
                "meaning": "east exit"
            },
            {
                "word": "中東",
                "reading": "ちゅうとう",
                "meaning": "Middle East"
            }
        ]
    },
    {
        "kanji": "西",
        "meaning": [
            "west"
        ],
        "onyomi": [
            "セイ",
            "サイ"
        ],
        "kunyomi": [
            "にし"
        ],
        "jlpt": "N5",
        "stroke_count": 6,
        "examples": [
            {
                "word": "西口",
                "reading": "にしぐち",
                "meaning": "west exit"
            },
            {
                "word": "関西",
                "reading": "かんさい",
                "meaning": "Kansai region"
            },
            {
                "word": "西洋",
                "reading": "せいよう",
                "meaning": "the West; Western"
            }
        ]
    },
    {
        "kanji": "南",
        "meaning": [
            "south"
        ],
        "onyomi": [
            "ナン"
        ],
        "kunyomi": [
            "みなみ"
        ],
        "jlpt": "N5",
        "stroke_count": 9,
        "examples": [
            {
                "word": "南口",
                "reading": "みなみぐち",
                "meaning": "south exit"
            },
            {
                "word": "南米",
                "reading": "なんべい",
                "meaning": "South America"
            },
            {
                "word": "南極",
                "reading": "なんきょく",
                "meaning": "South Pole; Antarctica"
            }
        ]
    },
    {
        "kanji": "北",
        "meaning": [
            "north"
        ],
        "onyomi": [
            "ホク"
        ],
        "kunyomi": [
            "きた"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "北口",
                "reading": "きたぐち",
                "meaning": "north exit"
            },
            {
                "word": "北海道",
                "reading": "ほっかいどう",
                "meaning": "Hokkaido"
            },
            {
                "word": "北極",
                "reading": "ほっきょく",
                "meaning": "North Pole; Arctic"
            }
        ]
    },
    {
        "kanji": "上",
        "meaning": [
            "up; above; top"
        ],
        "onyomi": [
            "ジョウ",
            "ショウ"
        ],
        "kunyomi": [
            "うえ",
            "あ.がる",
            "のぼ.る"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "上手",
                "reading": "じょうず",
                "meaning": "skillful; good at"
            },
            {
                "word": "以上",
                "reading": "いじょう",
                "meaning": "more than; and above"
            },
            {
                "word": "上る",
                "reading": "のぼる",
                "meaning": "to climb; to go up"
            }
        ]
    },
    {
        "kanji": "下",
        "meaning": [
            "below; under; descent"
        ],
        "onyomi": [
            "カ",
            "ゲ"
        ],
        "kunyomi": [
            "した",
            "さ.がる",
            "くだ.る"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "以下",
                "reading": "いか",
                "meaning": "less than; below"
            },
            {
                "word": "地下",
                "reading": "ちか",
                "meaning": "underground; subway"
            },
            {
                "word": "下手",
                "reading": "へた",
                "meaning": "unskillful; poor at"
            }
        ]
    },
    {
        "kanji": "中",
        "meaning": [
            "middle; inside; during"
        ],
        "onyomi": [
            "チュウ"
        ],
        "kunyomi": [
            "なか"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "中学校",
                "reading": "ちゅうがっこう",
                "meaning": "junior high school"
            },
            {
                "word": "中心",
                "reading": "ちゅうしん",
                "meaning": "center; core"
            },
            {
                "word": "途中",
                "reading": "とちゅう",
                "meaning": "on the way; midway"
            }
        ]
    },
    {
        "kanji": "外",
        "meaning": [
            "outside; foreign"
        ],
        "onyomi": [
            "ガイ",
            "ゲ"
        ],
        "kunyomi": [
            "そと",
            "はず.れる"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "外国",
                "reading": "がいこく",
                "meaning": "foreign country"
            },
            {
                "word": "海外",
                "reading": "かいがい",
                "meaning": "overseas"
            },
            {
                "word": "外出",
                "reading": "がいしゅつ",
                "meaning": "going out"
            }
        ]
    },
    {
        "kanji": "右",
        "meaning": [
            "right (direction)"
        ],
        "onyomi": [
            "ウ",
            "ユウ"
        ],
        "kunyomi": [
            "みぎ"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "右手",
                "reading": "みぎて",
                "meaning": "right hand"
            },
            {
                "word": "左右",
                "reading": "さゆう",
                "meaning": "left and right"
            },
            {
                "word": "右折",
                "reading": "うせつ",
                "meaning": "right turn"
            }
        ]
    },
    {
        "kanji": "左",
        "meaning": [
            "left (direction)"
        ],
        "onyomi": [
            "サ"
        ],
        "kunyomi": [
            "ひだり"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "左手",
                "reading": "ひだりて",
                "meaning": "left hand"
            },
            {
                "word": "左右",
                "reading": "さゆう",
                "meaning": "left and right"
            },
            {
                "word": "左折",
                "reading": "させつ",
                "meaning": "left turn"
            }
        ]
    },
    {
        "kanji": "家",
        "meaning": [
            "house; home; family"
        ],
        "onyomi": [
            "カ",
            "ケ"
        ],
        "kunyomi": [
            "いえ",
            "うち"
        ],
        "jlpt": "N5",
        "stroke_count": 10,
        "examples": [
            {
                "word": "家族",
                "reading": "かぞく",
                "meaning": "family"
            },
            {
                "word": "家庭",
                "reading": "かてい",
                "meaning": "home; household"
            },
            {
                "word": "国家",
                "reading": "こっか",
                "meaning": "nation; state"
            }
        ]
    },
    {
        "kanji": "食",
        "meaning": [
            "eat; food"
        ],
        "onyomi": [
            "ショク",
            "ジキ"
        ],
        "kunyomi": [
            "た.べる",
            "く.う"
        ],
        "jlpt": "N5",
        "stroke_count": 9,
        "examples": [
            {
                "word": "食事",
                "reading": "しょくじ",
                "meaning": "meal"
            },
            {
                "word": "食べ物",
                "reading": "たべもの",
                "meaning": "food"
            },
            {
                "word": "食堂",
                "reading": "しょくどう",
                "meaning": "dining hall; cafeteria"
            }
        ]
    },
    {
        "kanji": "飲",
        "meaning": [
            "drink"
        ],
        "onyomi": [
            "イン"
        ],
        "kunyomi": [
            "の.む"
        ],
        "jlpt": "N5",
        "stroke_count": 12,
        "examples": [
            {
                "word": "飲み物",
                "reading": "のみもの",
                "meaning": "drink; beverage"
            },
            {
                "word": "飲食",
                "reading": "いんしょく",
                "meaning": "eating and drinking"
            },
            {
                "word": "飲み会",
                "reading": "のみかい",
                "meaning": "drinking party"
            }
        ]
    },
    {
        "kanji": "本",
        "meaning": [
            "book; origin; true"
        ],
        "onyomi": [
            "ホン"
        ],
        "kunyomi": [
            "もと"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "日本",
                "reading": "にほん",
                "meaning": "Japan"
            },
            {
                "word": "本屋",
                "reading": "ほんや",
                "meaning": "bookstore"
            },
            {
                "word": "本当に",
                "reading": "ほんとうに",
                "meaning": "really; truly"
            }
        ]
    },
    {
        "kanji": "語",
        "meaning": [
            "language; word; speak"
        ],
        "onyomi": [
            "ゴ"
        ],
        "kunyomi": [
            "かた.る",
            "かた.らう"
        ],
        "jlpt": "N5",
        "stroke_count": 14,
        "examples": [
            {
                "word": "日本語",
                "reading": "にほんご",
                "meaning": "Japanese language"
            },
            {
                "word": "英語",
                "reading": "えいご",
                "meaning": "English language"
            },
            {
                "word": "物語",
                "reading": "ものがたり",
                "meaning": "story; tale"
            }
        ]
    },
    {
        "kanji": "読",
        "meaning": [
            "read"
        ],
        "onyomi": [
            "ドク",
            "トク"
        ],
        "kunyomi": [
            "よ.む"
        ],
        "jlpt": "N5",
        "stroke_count": 14,
        "examples": [
            {
                "word": "読書",
                "reading": "どくしょ",
                "meaning": "reading (books)"
            },
            {
                "word": "音読",
                "reading": "おんどく",
                "meaning": "reading aloud"
            },
            {
                "word": "読み方",
                "reading": "よみかた",
                "meaning": "way of reading; pronunciation"
            }
        ]
    },
    {
        "kanji": "書",
        "meaning": [
            "write"
        ],
        "onyomi": [
            "ショ"
        ],
        "kunyomi": [
            "か.く"
        ],
        "jlpt": "N5",
        "stroke_count": 10,
        "examples": [
            {
                "word": "書類",
                "reading": "しょるい",
                "meaning": "documents; paperwork"
            },
            {
                "word": "図書館",
                "reading": "としょかん",
                "meaning": "library"
            },
            {
                "word": "書道",
                "reading": "しょどう",
                "meaning": "calligraphy"
            }
        ]
    },
    {
        "kanji": "聞",
        "meaning": [
            "hear; ask; listen"
        ],
        "onyomi": [
            "ブン",
            "モン"
        ],
        "kunyomi": [
            "き.く",
            "き.こえる"
        ],
        "jlpt": "N5",
        "stroke_count": 14,
        "examples": [
            {
                "word": "新聞",
                "reading": "しんぶん",
                "meaning": "newspaper"
            },
            {
                "word": "聞こえる",
                "reading": "きこえる",
                "meaning": "can be heard"
            },
            {
                "word": "見聞き",
                "reading": "みきき",
                "meaning": "seeing and hearing"
            }
        ]
    },
    {
        "kanji": "話",
        "meaning": [
            "talk; story"
        ],
        "onyomi": [
            "ワ"
        ],
        "kunyomi": [
            "はな.す",
            "はなし"
        ],
        "jlpt": "N5",
        "stroke_count": 13,
        "examples": [
            {
                "word": "電話",
                "reading": "でんわ",
                "meaning": "telephone"
            },
            {
                "word": "会話",
                "reading": "かいわ",
                "meaning": "conversation"
            },
            {
                "word": "話し合い",
                "reading": "はなしあい",
                "meaning": "discussion"
            }
        ]
    },
    {
        "kanji": "見",
        "meaning": [
            "see; look; watch"
        ],
        "onyomi": [
            "ケン"
        ],
        "kunyomi": [
            "み.る",
            "み.える"
        ],
        "jlpt": "N5",
        "stroke_count": 7,
        "examples": [
            {
                "word": "花見",
                "reading": "はなみ",
                "meaning": "cherry blossom viewing"
            },
            {
                "word": "見物",
                "reading": "けんぶつ",
                "meaning": "sightseeing"
            },
            {
                "word": "見える",
                "reading": "みえる",
                "meaning": "can be seen; to appear"
            }
        ]
    },
    {
        "kanji": "行",
        "meaning": [
            "go; conduct"
        ],
        "onyomi": [
            "コウ",
            "ギョウ"
        ],
        "kunyomi": [
            "い.く",
            "おこな.う"
        ],
        "jlpt": "N5",
        "stroke_count": 6,
        "examples": [
            {
                "word": "旅行",
                "reading": "りょこう",
                "meaning": "travel; trip"
            },
            {
                "word": "銀行",
                "reading": "ぎんこう",
                "meaning": "bank"
            },
            {
                "word": "行動",
                "reading": "こうどう",
                "meaning": "action; behavior"
            }
        ]
    },
    {
        "kanji": "来",
        "meaning": [
            "come"
        ],
        "onyomi": [
            "ライ"
        ],
        "kunyomi": [
            "く.る",
            "き.たる"
        ],
        "jlpt": "N5",
        "stroke_count": 7,
        "examples": [
            {
                "word": "来年",
                "reading": "らいねん",
                "meaning": "next year"
            },
            {
                "word": "来週",
                "reading": "らいしゅう",
                "meaning": "next week"
            },
            {
                "word": "出来る",
                "reading": "できる",
                "meaning": "can do; to be completed"
            }
        ]
    },
    {
        "kanji": "入",
        "meaning": [
            "enter"
        ],
        "onyomi": [
            "ニュウ"
        ],
        "kunyomi": [
            "はい.る",
            "い.れる"
        ],
        "jlpt": "N5",
        "stroke_count": 2,
        "examples": [
            {
                "word": "入口",
                "reading": "いりぐち",
                "meaning": "entrance"
            },
            {
                "word": "入学",
                "reading": "にゅうがく",
                "meaning": "school enrollment"
            },
            {
                "word": "輸入",
                "reading": "ゆにゅう",
                "meaning": "import"
            }
        ]
    },
    {
        "kanji": "出",
        "meaning": [
            "exit; appear; take out"
        ],
        "onyomi": [
            "シュツ",
            "スイ"
        ],
        "kunyomi": [
            "で.る",
            "だ.す"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "出口",
                "reading": "でぐち",
                "meaning": "exit"
            },
            {
                "word": "出発",
                "reading": "しゅっぱつ",
                "meaning": "departure"
            },
            {
                "word": "輸出",
                "reading": "ゆしゅつ",
                "meaning": "export"
            }
        ]
    },
    {
        "kanji": "休",
        "meaning": [
            "rest; day off"
        ],
        "onyomi": [
            "キュウ"
        ],
        "kunyomi": [
            "やす.む",
            "やす.み"
        ],
        "jlpt": "N5",
        "stroke_count": 6,
        "examples": [
            {
                "word": "休日",
                "reading": "きゅうじつ",
                "meaning": "holiday; day off"
            },
            {
                "word": "夏休み",
                "reading": "なつやすみ",
                "meaning": "summer vacation"
            },
            {
                "word": "休憩",
                "reading": "きゅうけい",
                "meaning": "break; rest"
            }
        ]
    },
    {
        "kanji": "立",
        "meaning": [
            "stand; establish"
        ],
        "onyomi": [
            "リツ",
            "リュウ"
        ],
        "kunyomi": [
            "た.つ",
            "た.てる"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "立つ",
                "reading": "たつ",
                "meaning": "to stand up"
            },
            {
                "word": "役立つ",
                "reading": "やくだつ",
                "meaning": "to be useful"
            },
            {
                "word": "独立",
                "reading": "どくりつ",
                "meaning": "independence"
            }
        ]
    },
    {
        "kanji": "起",
        "meaning": [
            "wake up; rise; occur"
        ],
        "onyomi": [
            "キ"
        ],
        "kunyomi": [
            "お.きる",
            "お.こる",
            "お.こす"
        ],
        "jlpt": "N5",
        "stroke_count": 10,
        "examples": [
            {
                "word": "起きる",
                "reading": "おきる",
                "meaning": "to wake up; to get up"
            },
            {
                "word": "起こる",
                "reading": "おこる",
                "meaning": "to occur; to happen"
            },
            {
                "word": "早起き",
                "reading": "はやおき",
                "meaning": "getting up early"
            }
        ]
    },
    {
        "kanji": "帰",
        "meaning": [
            "return; go home"
        ],
        "onyomi": [
            "キ"
        ],
        "kunyomi": [
            "かえ.る",
            "かえ.す"
        ],
        "jlpt": "N5",
        "stroke_count": 10,
        "examples": [
            {
                "word": "帰国",
                "reading": "きこく",
                "meaning": "returning to one's country"
            },
            {
                "word": "帰宅",
                "reading": "きたく",
                "meaning": "returning home"
            },
            {
                "word": "日帰り",
                "reading": "ひがえり",
                "meaning": "day trip"
            }
        ]
    },
    {
        "kanji": "言",
        "meaning": [
            "say; speak"
        ],
        "onyomi": [
            "ゲン",
            "ゴン"
        ],
        "kunyomi": [
            "い.う",
            "こと"
        ],
        "jlpt": "N5",
        "stroke_count": 7,
        "examples": [
            {
                "word": "言葉",
                "reading": "ことば",
                "meaning": "word; language"
            },
            {
                "word": "言語",
                "reading": "げんご",
                "meaning": "language"
            },
            {
                "word": "一言",
                "reading": "ひとこと",
                "meaning": "a word; brief comment"
            }
        ]
    },
    {
        "kanji": "思",
        "meaning": [
            "think; feel"
        ],
        "onyomi": [
            "シ"
        ],
        "kunyomi": [
            "おも.う"
        ],
        "jlpt": "N5",
        "stroke_count": 9,
        "examples": [
            {
                "word": "思い出",
                "reading": "おもいで",
                "meaning": "memory; recollection"
            },
            {
                "word": "思想",
                "reading": "しそう",
                "meaning": "thought; ideology"
            },
            {
                "word": "不思議",
                "reading": "ふしぎ",
                "meaning": "mysterious; strange"
            }
        ]
    },
    {
        "kanji": "知",
        "meaning": [
            "know"
        ],
        "onyomi": [
            "チ"
        ],
        "kunyomi": [
            "し.る",
            "し.らせる"
        ],
        "jlpt": "N5",
        "stroke_count": 8,
        "examples": [
            {
                "word": "知識",
                "reading": "ちしき",
                "meaning": "knowledge"
            },
            {
                "word": "知人",
                "reading": "ちじん",
                "meaning": "acquaintance"
            },
            {
                "word": "通知",
                "reading": "つうち",
                "meaning": "notification"
            }
        ]
    },
    {
        "kanji": "買",
        "meaning": [
            "buy"
        ],
        "onyomi": [
            "バイ"
        ],
        "kunyomi": [
            "か.う"
        ],
        "jlpt": "N5",
        "stroke_count": 12,
        "examples": [
            {
                "word": "買い物",
                "reading": "かいもの",
                "meaning": "shopping"
            },
            {
                "word": "購買",
                "reading": "こうばい",
                "meaning": "purchase; buying"
            },
            {
                "word": "売り買い",
                "reading": "うりかい",
                "meaning": "buying and selling"
            }
        ]
    },
    {
        "kanji": "大",
        "meaning": [
            "big; large; great"
        ],
        "onyomi": [
            "ダイ",
            "タイ"
        ],
        "kunyomi": [
            "おお.きい",
            "おお"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "大学",
                "reading": "だいがく",
                "meaning": "university"
            },
            {
                "word": "大切",
                "reading": "たいせつ",
                "meaning": "important"
            },
            {
                "word": "大丈夫",
                "reading": "だいじょうぶ",
                "meaning": "OK; all right"
            }
        ]
    },
    {
        "kanji": "小",
        "meaning": [
            "small; little"
        ],
        "onyomi": [
            "ショウ"
        ],
        "kunyomi": [
            "ちい.さい",
            "こ",
            "お"
        ],
        "jlpt": "N5",
        "stroke_count": 3,
        "examples": [
            {
                "word": "小学校",
                "reading": "しょうがっこう",
                "meaning": "elementary school"
            },
            {
                "word": "小説",
                "reading": "しょうせつ",
                "meaning": "novel"
            },
            {
                "word": "小さい",
                "reading": "ちいさい",
                "meaning": "small"
            }
        ]
    },
    {
        "kanji": "高",
        "meaning": [
            "tall; high; expensive"
        ],
        "onyomi": [
            "コウ"
        ],
        "kunyomi": [
            "たか.い",
            "たか"
        ],
        "jlpt": "N5",
        "stroke_count": 10,
        "examples": [
            {
                "word": "高校",
                "reading": "こうこう",
                "meaning": "high school"
            },
            {
                "word": "高速",
                "reading": "こうそく",
                "meaning": "high speed; expressway"
            },
            {
                "word": "最高",
                "reading": "さいこう",
                "meaning": "the best; maximum"
            }
        ]
    },
    {
        "kanji": "長",
        "meaning": [
            "long; leader; chief"
        ],
        "onyomi": [
            "チョウ"
        ],
        "kunyomi": [
            "なが.い"
        ],
        "jlpt": "N5",
        "stroke_count": 8,
        "examples": [
            {
                "word": "校長",
                "reading": "こうちょう",
                "meaning": "school principal"
            },
            {
                "word": "長所",
                "reading": "ちょうしょ",
                "meaning": "strong point; merit"
            },
            {
                "word": "社長",
                "reading": "しゃちょう",
                "meaning": "company president"
            }
        ]
    },
    {
        "kanji": "多",
        "meaning": [
            "many; much"
        ],
        "onyomi": [
            "タ"
        ],
        "kunyomi": [
            "おお.い"
        ],
        "jlpt": "N5",
        "stroke_count": 6,
        "examples": [
            {
                "word": "多数",
                "reading": "たすう",
                "meaning": "large number; majority"
            },
            {
                "word": "多分",
                "reading": "たぶん",
                "meaning": "probably; perhaps"
            },
            {
                "word": "多くの",
                "reading": "おおくの",
                "meaning": "many; most of"
            }
        ]
    },
    {
        "kanji": "少",
        "meaning": [
            "few; little; young"
        ],
        "onyomi": [
            "ショウ"
        ],
        "kunyomi": [
            "すく.ない",
            "すこ.し"
        ],
        "jlpt": "N5",
        "stroke_count": 4,
        "examples": [
            {
                "word": "少し",
                "reading": "すこし",
                "meaning": "a little; a few"
            },
            {
                "word": "少年",
                "reading": "しょうねん",
                "meaning": "boy; youth"
            },
            {
                "word": "少女",
                "reading": "しょうじょ",
                "meaning": "girl; young woman"
            }
        ]
    },
    {
        "kanji": "新",
        "meaning": [
            "new"
        ],
        "onyomi": [
            "シン"
        ],
        "kunyomi": [
            "あたら.しい",
            "にい"
        ],
        "jlpt": "N5",
        "stroke_count": 13,
        "examples": [
            {
                "word": "新聞",
                "reading": "しんぶん",
                "meaning": "newspaper"
            },
            {
                "word": "新幹線",
                "reading": "しんかんせん",
                "meaning": "bullet train"
            },
            {
                "word": "最新",
                "reading": "さいしん",
                "meaning": "latest; newest"
            }
        ]
    },
    {
        "kanji": "古",
        "meaning": [
            "old; used"
        ],
        "onyomi": [
            "コ"
        ],
        "kunyomi": [
            "ふる.い"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "古い",
                "reading": "ふるい",
                "meaning": "old"
            },
            {
                "word": "古典",
                "reading": "こてん",
                "meaning": "classic; classical"
            },
            {
                "word": "中古",
                "reading": "ちゅうこ",
                "meaning": "used; secondhand"
            }
        ]
    },
    {
        "kanji": "白",
        "meaning": [
            "white"
        ],
        "onyomi": [
            "ハク",
            "ビャク"
        ],
        "kunyomi": [
            "しろ",
            "しら"
        ],
        "jlpt": "N5",
        "stroke_count": 5,
        "examples": [
            {
                "word": "白い",
                "reading": "しろい",
                "meaning": "white"
            },
            {
                "word": "白紙",
                "reading": "はくし",
                "meaning": "blank paper"
            },
            {
                "word": "明白",
                "reading": "めいはく",
                "meaning": "obvious; clear"
            }
        ]
    },
    {
        "kanji": "黒",
        "meaning": [
            "black"
        ],
        "onyomi": [
            "コク"
        ],
        "kunyomi": [
            "くろ",
            "くろ.い"
        ],
        "jlpt": "N5",
        "stroke_count": 11,
        "examples": [
            {
                "word": "黒い",
                "reading": "くろい",
                "meaning": "black"
            },
            {
                "word": "黒板",
                "reading": "こくばん",
                "meaning": "blackboard"
            },
            {
                "word": "黒字",
                "reading": "くろじ",
                "meaning": "profit; in the black"
            }
        ]
    },
    {
        "kanji": "赤",
        "meaning": [
            "red"
        ],
        "onyomi": [
            "セキ",
            "シャク"
        ],
        "kunyomi": [
            "あか",
            "あか.い"
        ],
        "jlpt": "N5",
        "stroke_count": 7,
        "examples": [
            {
                "word": "赤い",
                "reading": "あかい",
                "meaning": "red"
            },
            {
                "word": "赤ちゃん",
                "reading": "あかちゃん",
                "meaning": "baby"
            },
            {
                "word": "赤字",
                "reading": "あかじ",
                "meaning": "deficit; in the red"
            }
        ]
    },
    {
        "kanji": "青",
        "meaning": [
            "blue; green"
        ],
        "onyomi": [
            "セイ",
            "ショウ"
        ],
        "kunyomi": [
            "あお",
            "あお.い"
        ],
        "jlpt": "N5",
        "stroke_count": 8,
        "examples": [
            {
                "word": "青い",
                "reading": "あおい",
                "meaning": "blue; unripe; inexperienced"
            },
            {
                "word": "青空",
                "reading": "あおぞら",
                "meaning": "blue sky"
            },
            {
                "word": "青年",
                "reading": "せいねん",
                "meaning": "young person; youth"
            }
        ]
    },
    {
        "kanji": "朝",
        "meaning": [
            "morning"
        ],
        "onyomi": [
            "チョウ"
        ],
        "kunyomi": [
            "あさ"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "今朝",
                "reading": "けさ",
                "meaning": "this morning"
            },
            {
                "word": "毎朝",
                "reading": "まいあさ",
                "meaning": "every morning"
            },
            {
                "word": "朝食",
                "reading": "ちょうしょく",
                "meaning": "breakfast"
            }
        ]
    },
    {
        "kanji": "昼",
        "meaning": [
            "daytime; noon"
        ],
        "onyomi": [
            "チュウ"
        ],
        "kunyomi": [
            "ひる"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "昼ご飯",
                "reading": "ひるごはん",
                "meaning": "lunch"
            },
            {
                "word": "昼間",
                "reading": "ひるま",
                "meaning": "daytime"
            },
            {
                "word": "昼休み",
                "reading": "ひるやすみ",
                "meaning": "lunch break"
            }
        ]
    },
    {
        "kanji": "夕",
        "meaning": [
            "evening; dusk"
        ],
        "onyomi": [
            "セキ"
        ],
        "kunyomi": [
            "ゆう"
        ],
        "jlpt": "N4",
        "stroke_count": 3,
        "examples": [
            {
                "word": "夕方",
                "reading": "ゆうがた",
                "meaning": "evening; late afternoon"
            },
            {
                "word": "夕食",
                "reading": "ゆうしょく",
                "meaning": "dinner; supper"
            },
            {
                "word": "夕暮れ",
                "reading": "ゆうぐれ",
                "meaning": "dusk; twilight"
            }
        ]
    },
    {
        "kanji": "昨",
        "meaning": [
            "yesterday; previous"
        ],
        "onyomi": [
            "サク"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "昨日",
                "reading": "きのう",
                "meaning": "yesterday"
            },
            {
                "word": "昨年",
                "reading": "さくねん",
                "meaning": "last year"
            },
            {
                "word": "昨夜",
                "reading": "さくや",
                "meaning": "last night"
            }
        ]
    },
    {
        "kanji": "去",
        "meaning": [
            "past; leave"
        ],
        "onyomi": [
            "キョ",
            "コ"
        ],
        "kunyomi": [
            "さ.る"
        ],
        "jlpt": "N4",
        "stroke_count": 5,
        "examples": [
            {
                "word": "去年",
                "reading": "きょねん",
                "meaning": "last year"
            },
            {
                "word": "過去",
                "reading": "かこ",
                "meaning": "the past"
            },
            {
                "word": "去る",
                "reading": "さる",
                "meaning": "to leave; to depart"
            }
        ]
    },
    {
        "kanji": "近",
        "meaning": [
            "near; close"
        ],
        "onyomi": [
            "キン"
        ],
        "kunyomi": [
            "ちか.い"
        ],
        "jlpt": "N4",
        "stroke_count": 7,
        "examples": [
            {
                "word": "近所",
                "reading": "きんじょ",
                "meaning": "neighborhood"
            },
            {
                "word": "近代",
                "reading": "きんだい",
                "meaning": "modern times"
            },
            {
                "word": "最近",
                "reading": "さいきん",
                "meaning": "recently"
            }
        ]
    },
    {
        "kanji": "遠",
        "meaning": [
            "far; distant"
        ],
        "onyomi": [
            "エン"
        ],
        "kunyomi": [
            "とお.い"
        ],
        "jlpt": "N4",
        "stroke_count": 13,
        "examples": [
            {
                "word": "遠足",
                "reading": "えんそく",
                "meaning": "field trip; excursion"
            },
            {
                "word": "遠方",
                "reading": "えんぽう",
                "meaning": "distant place"
            },
            {
                "word": "遠慮",
                "reading": "えんりょ",
                "meaning": "hesitation; restraint"
            }
        ]
    },
    {
        "kanji": "間",
        "meaning": [
            "between; interval; space"
        ],
        "onyomi": [
            "カン",
            "ケン"
        ],
        "kunyomi": [
            "あいだ",
            "ま"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "時間",
                "reading": "じかん",
                "meaning": "time; hours"
            },
            {
                "word": "人間",
                "reading": "にんげん",
                "meaning": "human being"
            },
            {
                "word": "週間",
                "reading": "しゅうかん",
                "meaning": "week(s) duration"
            }
        ]
    },
    {
        "kanji": "代",
        "meaning": [
            "generation; era; substitute"
        ],
        "onyomi": [
            "ダイ",
            "タイ"
        ],
        "kunyomi": [
            "か.わる",
            "しろ",
            "よ"
        ],
        "jlpt": "N4",
        "stroke_count": 5,
        "examples": [
            {
                "word": "時代",
                "reading": "じだい",
                "meaning": "era; period"
            },
            {
                "word": "代わり",
                "reading": "かわり",
                "meaning": "substitute; instead"
            },
            {
                "word": "年代",
                "reading": "ねんだい",
                "meaning": "age; era; decade"
            }
        ]
    },
    {
        "kanji": "春",
        "meaning": [
            "spring"
        ],
        "onyomi": [
            "シュン"
        ],
        "kunyomi": [
            "はる"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "春休み",
                "reading": "はるやすみ",
                "meaning": "spring vacation"
            },
            {
                "word": "青春",
                "reading": "せいしゅん",
                "meaning": "youth; springtime of life"
            },
            {
                "word": "立春",
                "reading": "りっしゅん",
                "meaning": "first day of spring"
            }
        ]
    },
    {
        "kanji": "夏",
        "meaning": [
            "summer"
        ],
        "onyomi": [
            "カ",
            "ゲ"
        ],
        "kunyomi": [
            "なつ"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "夏休み",
                "reading": "なつやすみ",
                "meaning": "summer vacation"
            },
            {
                "word": "真夏",
                "reading": "まなつ",
                "meaning": "midsummer"
            },
            {
                "word": "夏至",
                "reading": "げし",
                "meaning": "summer solstice"
            }
        ]
    },
    {
        "kanji": "秋",
        "meaning": [
            "autumn; fall"
        ],
        "onyomi": [
            "シュウ"
        ],
        "kunyomi": [
            "あき"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "秋分",
                "reading": "しゅうぶん",
                "meaning": "autumnal equinox"
            },
            {
                "word": "初秋",
                "reading": "しょしゅう",
                "meaning": "early autumn"
            },
            {
                "word": "秋空",
                "reading": "あきぞら",
                "meaning": "autumn sky"
            }
        ]
    },
    {
        "kanji": "冬",
        "meaning": [
            "winter"
        ],
        "onyomi": [
            "トウ"
        ],
        "kunyomi": [
            "ふゆ"
        ],
        "jlpt": "N4",
        "stroke_count": 5,
        "examples": [
            {
                "word": "冬休み",
                "reading": "ふゆやすみ",
                "meaning": "winter vacation"
            },
            {
                "word": "真冬",
                "reading": "まふゆ",
                "meaning": "midwinter"
            },
            {
                "word": "冬至",
                "reading": "とうじ",
                "meaning": "winter solstice"
            }
        ]
    },
    {
        "kanji": "週",
        "meaning": [
            "week"
        ],
        "onyomi": [
            "シュウ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "今週",
                "reading": "こんしゅう",
                "meaning": "this week"
            },
            {
                "word": "週末",
                "reading": "しゅうまつ",
                "meaning": "weekend"
            },
            {
                "word": "毎週",
                "reading": "まいしゅう",
                "meaning": "every week"
            }
        ]
    },
    {
        "kanji": "親",
        "meaning": [
            "parent; intimate; kind"
        ],
        "onyomi": [
            "シン"
        ],
        "kunyomi": [
            "おや",
            "した.しい"
        ],
        "jlpt": "N4",
        "stroke_count": 16,
        "examples": [
            {
                "word": "親切",
                "reading": "しんせつ",
                "meaning": "kindness"
            },
            {
                "word": "両親",
                "reading": "りょうしん",
                "meaning": "both parents"
            },
            {
                "word": "親友",
                "reading": "しんゆう",
                "meaning": "close friend"
            }
        ]
    },
    {
        "kanji": "兄",
        "meaning": [
            "older brother"
        ],
        "onyomi": [
            "ケイ",
            "キョウ"
        ],
        "kunyomi": [
            "あに"
        ],
        "jlpt": "N4",
        "stroke_count": 5,
        "examples": [
            {
                "word": "兄弟",
                "reading": "きょうだい",
                "meaning": "siblings; brothers"
            },
            {
                "word": "お兄さん",
                "reading": "おにいさん",
                "meaning": "older brother (polite)"
            },
            {
                "word": "義兄",
                "reading": "ぎけい",
                "meaning": "brother-in-law"
            }
        ]
    },
    {
        "kanji": "姉",
        "meaning": [
            "older sister"
        ],
        "onyomi": [
            "シ"
        ],
        "kunyomi": [
            "あね"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "姉妹",
                "reading": "しまい",
                "meaning": "sisters"
            },
            {
                "word": "お姉さん",
                "reading": "おねえさん",
                "meaning": "older sister (polite)"
            },
            {
                "word": "義姉",
                "reading": "ぎし",
                "meaning": "sister-in-law"
            }
        ]
    },
    {
        "kanji": "弟",
        "meaning": [
            "younger brother"
        ],
        "onyomi": [
            "テイ",
            "ダイ",
            "デ"
        ],
        "kunyomi": [
            "おとうと"
        ],
        "jlpt": "N4",
        "stroke_count": 7,
        "examples": [
            {
                "word": "弟子",
                "reading": "でし",
                "meaning": "disciple; pupil"
            },
            {
                "word": "兄弟",
                "reading": "きょうだい",
                "meaning": "siblings"
            },
            {
                "word": "義弟",
                "reading": "ぎてい",
                "meaning": "brother-in-law (younger)"
            }
        ]
    },
    {
        "kanji": "妹",
        "meaning": [
            "younger sister"
        ],
        "onyomi": [
            "マイ"
        ],
        "kunyomi": [
            "いもうと"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "姉妹",
                "reading": "しまい",
                "meaning": "sisters"
            },
            {
                "word": "妹さん",
                "reading": "いもうとさん",
                "meaning": "younger sister (polite)"
            },
            {
                "word": "義妹",
                "reading": "ぎまい",
                "meaning": "sister-in-law (younger)"
            }
        ]
    },
    {
        "kanji": "夫",
        "meaning": [
            "husband; man"
        ],
        "onyomi": [
            "フ",
            "フウ"
        ],
        "kunyomi": [
            "おっと",
            "おとこ"
        ],
        "jlpt": "N4",
        "stroke_count": 4,
        "examples": [
            {
                "word": "夫婦",
                "reading": "ふうふ",
                "meaning": "married couple; husband and wife"
            },
            {
                "word": "夫人",
                "reading": "ふじん",
                "meaning": "wife; Mrs."
            },
            {
                "word": "工夫",
                "reading": "くふう",
                "meaning": "ingenuity; contrivance"
            }
        ]
    },
    {
        "kanji": "妻",
        "meaning": [
            "wife"
        ],
        "onyomi": [
            "サイ"
        ],
        "kunyomi": [
            "つま"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "夫婦",
                "reading": "ふうふ",
                "meaning": "married couple"
            },
            {
                "word": "妻子",
                "reading": "さいし",
                "meaning": "wife and children"
            },
            {
                "word": "後妻",
                "reading": "のちぞい",
                "meaning": "second wife"
            }
        ]
    },
    {
        "kanji": "者",
        "meaning": [
            "person; one who"
        ],
        "onyomi": [
            "シャ"
        ],
        "kunyomi": [
            "もの"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "医者",
                "reading": "いしゃ",
                "meaning": "doctor"
            },
            {
                "word": "記者",
                "reading": "きしゃ",
                "meaning": "journalist"
            },
            {
                "word": "若者",
                "reading": "わかもの",
                "meaning": "young person"
            }
        ]
    },
    {
        "kanji": "員",
        "meaning": [
            "member; staff"
        ],
        "onyomi": [
            "イン"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "会社員",
                "reading": "かいしゃいん",
                "meaning": "company employee"
            },
            {
                "word": "店員",
                "reading": "てんいん",
                "meaning": "shop clerk"
            },
            {
                "word": "全員",
                "reading": "ぜんいん",
                "meaning": "all members; everyone"
            }
        ]
    },
    {
        "kanji": "長",
        "meaning": [
            "chief; long; leader"
        ],
        "onyomi": [
            "チョウ"
        ],
        "kunyomi": [
            "なが.い"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "部長",
                "reading": "ぶちょう",
                "meaning": "department manager"
            },
            {
                "word": "課長",
                "reading": "かちょう",
                "meaning": "section chief"
            },
            {
                "word": "成長",
                "reading": "せいちょう",
                "meaning": "growth; development"
            }
        ]
    },
    {
        "kanji": "客",
        "meaning": [
            "guest; customer"
        ],
        "onyomi": [
            "キャク",
            "カク"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "お客さん",
                "reading": "おきゃくさん",
                "meaning": "customer; guest"
            },
            {
                "word": "観客",
                "reading": "かんきゃく",
                "meaning": "audience; spectators"
            },
            {
                "word": "旅客",
                "reading": "りょかく",
                "meaning": "passenger; traveler"
            }
        ]
    },
    {
        "kanji": "族",
        "meaning": [
            "family; clan; tribe"
        ],
        "onyomi": [
            "ゾク"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "家族",
                "reading": "かぞく",
                "meaning": "family"
            },
            {
                "word": "民族",
                "reading": "みんぞく",
                "meaning": "ethnic group; people"
            },
            {
                "word": "水族館",
                "reading": "すいぞくかん",
                "meaning": "aquarium"
            }
        ]
    },
    {
        "kanji": "部",
        "meaning": [
            "part; department; club"
        ],
        "onyomi": [
            "ブ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "部屋",
                "reading": "へや",
                "meaning": "room"
            },
            {
                "word": "全部",
                "reading": "ぜんぶ",
                "meaning": "all; everything"
            },
            {
                "word": "部活",
                "reading": "ぶかつ",
                "meaning": "club activities"
            }
        ]
    },
    {
        "kanji": "係",
        "meaning": [
            "person in charge; relate to"
        ],
        "onyomi": [
            "ケイ"
        ],
        "kunyomi": [
            "かか.る",
            "かかり"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "係員",
                "reading": "かかりいん",
                "meaning": "person in charge; attendant"
            },
            {
                "word": "関係",
                "reading": "かんけい",
                "meaning": "relationship; connection"
            },
            {
                "word": "係わる",
                "reading": "かかわる",
                "meaning": "to be involved with"
            }
        ]
    },
    {
        "kanji": "様",
        "meaning": [
            "manner; Mr./Mrs./Ms."
        ],
        "onyomi": [
            "ヨウ"
        ],
        "kunyomi": [
            "さま"
        ],
        "jlpt": "N4",
        "stroke_count": 14,
        "examples": [
            {
                "word": "様子",
                "reading": "ようす",
                "meaning": "state; condition; appearance"
            },
            {
                "word": "皆様",
                "reading": "みなさま",
                "meaning": "everyone (very polite)"
            },
            {
                "word": "お客様",
                "reading": "おきゃくさま",
                "meaning": "valued customer (very polite)"
            }
        ]
    },
    {
        "kanji": "首",
        "meaning": [
            "neck; head; dismiss"
        ],
        "onyomi": [
            "シュ"
        ],
        "kunyomi": [
            "くび"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "首相",
                "reading": "しゅしょう",
                "meaning": "prime minister"
            },
            {
                "word": "首都",
                "reading": "しゅと",
                "meaning": "capital city"
            },
            {
                "word": "手首",
                "reading": "てくび",
                "meaning": "wrist"
            }
        ]
    },
    {
        "kanji": "肩",
        "meaning": [
            "shoulder"
        ],
        "onyomi": [
            "ケン"
        ],
        "kunyomi": [
            "かた"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "肩書き",
                "reading": "かたがき",
                "meaning": "title; one's position"
            },
            {
                "word": "肩こり",
                "reading": "かたこり",
                "meaning": "stiff shoulders"
            },
            {
                "word": "双肩",
                "reading": "そうけん",
                "meaning": "both shoulders"
            }
        ]
    },
    {
        "kanji": "胸",
        "meaning": [
            "chest; breast; heart"
        ],
        "onyomi": [
            "キョウ"
        ],
        "kunyomi": [
            "むね",
            "むな"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "胸中",
                "reading": "きょうちゅう",
                "meaning": "in one's heart; one's thoughts"
            },
            {
                "word": "胸焼け",
                "reading": "むねやけ",
                "meaning": "heartburn"
            },
            {
                "word": "胸騒ぎ",
                "reading": "むなさわぎ",
                "meaning": "premonition; foreboding"
            }
        ]
    },
    {
        "kanji": "指",
        "meaning": [
            "finger; point to"
        ],
        "onyomi": [
            "シ"
        ],
        "kunyomi": [
            "ゆび",
            "さ.す"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "指輪",
                "reading": "ゆびわ",
                "meaning": "ring (jewelry)"
            },
            {
                "word": "指定",
                "reading": "してい",
                "meaning": "designation; specification"
            },
            {
                "word": "指導",
                "reading": "しどう",
                "meaning": "guidance; leadership"
            }
        ]
    },
    {
        "kanji": "血",
        "meaning": [
            "blood"
        ],
        "onyomi": [
            "ケツ"
        ],
        "kunyomi": [
            "ち"
        ],
        "jlpt": "N4",
        "stroke_count": 6,
        "examples": [
            {
                "word": "血液",
                "reading": "けつえき",
                "meaning": "blood"
            },
            {
                "word": "献血",
                "reading": "けんけつ",
                "meaning": "blood donation"
            },
            {
                "word": "血圧",
                "reading": "けつあつ",
                "meaning": "blood pressure"
            }
        ]
    },
    {
        "kanji": "病",
        "meaning": [
            "illness; disease"
        ],
        "onyomi": [
            "ビョウ",
            "ヘイ"
        ],
        "kunyomi": [
            "やまい",
            "や.む"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "病院",
                "reading": "びょういん",
                "meaning": "hospital"
            },
            {
                "word": "病気",
                "reading": "びょうき",
                "meaning": "illness; sickness"
            },
            {
                "word": "看病",
                "reading": "かんびょう",
                "meaning": "nursing; caring for the sick"
            }
        ]
    },
    {
        "kanji": "院",
        "meaning": [
            "institution; temple"
        ],
        "onyomi": [
            "イン"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "病院",
                "reading": "びょういん",
                "meaning": "hospital"
            },
            {
                "word": "入院",
                "reading": "にゅういん",
                "meaning": "hospitalization"
            },
            {
                "word": "美容院",
                "reading": "びよういん",
                "meaning": "beauty salon"
            }
        ]
    },
    {
        "kanji": "医",
        "meaning": [
            "medicine; doctor"
        ],
        "onyomi": [
            "イ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 7,
        "examples": [
            {
                "word": "医者",
                "reading": "いしゃ",
                "meaning": "doctor"
            },
            {
                "word": "医学",
                "reading": "いがく",
                "meaning": "medical science"
            },
            {
                "word": "医院",
                "reading": "いいん",
                "meaning": "clinic; doctor's office"
            }
        ]
    },
    {
        "kanji": "薬",
        "meaning": [
            "medicine; drug"
        ],
        "onyomi": [
            "ヤク"
        ],
        "kunyomi": [
            "くすり"
        ],
        "jlpt": "N4",
        "stroke_count": 16,
        "examples": [
            {
                "word": "薬局",
                "reading": "やっきょく",
                "meaning": "pharmacy"
            },
            {
                "word": "薬剤師",
                "reading": "やくざいし",
                "meaning": "pharmacist"
            },
            {
                "word": "農薬",
                "reading": "のうやく",
                "meaning": "pesticide; agricultural chemical"
            }
        ]
    },
    {
        "kanji": "痛",
        "meaning": [
            "pain; ache"
        ],
        "onyomi": [
            "ツウ"
        ],
        "kunyomi": [
            "いた.い",
            "いた.む"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "頭痛",
                "reading": "ずつう",
                "meaning": "headache"
            },
            {
                "word": "腹痛",
                "reading": "ふくつう",
                "meaning": "stomachache"
            },
            {
                "word": "痛み",
                "reading": "いたみ",
                "meaning": "pain; ache"
            }
        ]
    },
    {
        "kanji": "熱",
        "meaning": [
            "heat; fever; enthusiasm"
        ],
        "onyomi": [
            "ネツ"
        ],
        "kunyomi": [
            "あつ.い"
        ],
        "jlpt": "N4",
        "stroke_count": 15,
        "examples": [
            {
                "word": "発熱",
                "reading": "はつねつ",
                "meaning": "fever; developing a temperature"
            },
            {
                "word": "熱心",
                "reading": "ねっしん",
                "meaning": "enthusiasm; eagerness"
            },
            {
                "word": "熱帯",
                "reading": "ねったい",
                "meaning": "tropics"
            }
        ]
    },
    {
        "kanji": "健",
        "meaning": [
            "healthy; strong"
        ],
        "onyomi": [
            "ケン"
        ],
        "kunyomi": [
            "すこ.やか"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "健康",
                "reading": "けんこう",
                "meaning": "health"
            },
            {
                "word": "健全",
                "reading": "けんぜん",
                "meaning": "healthy; sound"
            },
            {
                "word": "保健",
                "reading": "ほけん",
                "meaning": "health care; hygiene"
            }
        ]
    },
    {
        "kanji": "康",
        "meaning": [
            "peace; health"
        ],
        "onyomi": [
            "コウ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "健康",
                "reading": "けんこう",
                "meaning": "health"
            },
            {
                "word": "健康的",
                "reading": "けんこうてき",
                "meaning": "healthy"
            },
            {
                "word": "健康保険",
                "reading": "けんこうほけん",
                "meaning": "health insurance"
            }
        ]
    },
    {
        "kanji": "森",
        "meaning": [
            "forest"
        ],
        "onyomi": [
            "シン"
        ],
        "kunyomi": [
            "もり"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "森林",
                "reading": "しんりん",
                "meaning": "forest; woods"
            },
            {
                "word": "森閑",
                "reading": "しんかん",
                "meaning": "perfectly quiet"
            },
            {
                "word": "深森",
                "reading": "しんもり",
                "meaning": "deep forest"
            }
        ]
    },
    {
        "kanji": "林",
        "meaning": [
            "grove; woods"
        ],
        "onyomi": [
            "リン"
        ],
        "kunyomi": [
            "はやし"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "森林",
                "reading": "しんりん",
                "meaning": "forest"
            },
            {
                "word": "林業",
                "reading": "りんぎょう",
                "meaning": "forestry"
            },
            {
                "word": "竹林",
                "reading": "ちくりん",
                "meaning": "bamboo grove"
            }
        ]
    },
    {
        "kanji": "島",
        "meaning": [
            "island"
        ],
        "onyomi": [
            "トウ"
        ],
        "kunyomi": [
            "しま"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "半島",
                "reading": "はんとう",
                "meaning": "peninsula"
            },
            {
                "word": "島国",
                "reading": "しまぐに",
                "meaning": "island nation"
            },
            {
                "word": "無人島",
                "reading": "むじんとう",
                "meaning": "uninhabited island"
            }
        ]
    },
    {
        "kanji": "岩",
        "meaning": [
            "rock; cliff"
        ],
        "onyomi": [
            "ガン"
        ],
        "kunyomi": [
            "いわ"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "岩石",
                "reading": "がんせき",
                "meaning": "rock; stone"
            },
            {
                "word": "火岩",
                "reading": "かがん",
                "meaning": "igneous rock"
            },
            {
                "word": "岩場",
                "reading": "いわば",
                "meaning": "rocky place"
            }
        ]
    },
    {
        "kanji": "草",
        "meaning": [
            "grass; plants"
        ],
        "onyomi": [
            "ソウ"
        ],
        "kunyomi": [
            "くさ"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "草原",
                "reading": "そうげん",
                "meaning": "grassland; plain"
            },
            {
                "word": "雑草",
                "reading": "ざっそう",
                "meaning": "weeds"
            },
            {
                "word": "草花",
                "reading": "くさばな",
                "meaning": "flowers and plants"
            }
        ]
    },
    {
        "kanji": "葉",
        "meaning": [
            "leaf; blade"
        ],
        "onyomi": [
            "ヨウ"
        ],
        "kunyomi": [
            "は"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "落ち葉",
                "reading": "おちば",
                "meaning": "fallen leaves"
            },
            {
                "word": "言葉",
                "reading": "ことば",
                "meaning": "words; language"
            },
            {
                "word": "紅葉",
                "reading": "こうよう",
                "meaning": "autumn leaves; maple"
            }
        ]
    },
    {
        "kanji": "根",
        "meaning": [
            "root; base"
        ],
        "onyomi": [
            "コン"
        ],
        "kunyomi": [
            "ね"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "根本",
                "reading": "こんぽん",
                "meaning": "root; basis; fundamental"
            },
            {
                "word": "屋根",
                "reading": "やね",
                "meaning": "roof"
            },
            {
                "word": "根拠",
                "reading": "こんきょ",
                "meaning": "basis; ground; foundation"
            }
        ]
    },
    {
        "kanji": "枝",
        "meaning": [
            "branch; twig"
        ],
        "onyomi": [
            "シ"
        ],
        "kunyomi": [
            "えだ"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "枝豆",
                "reading": "えだまめ",
                "meaning": "edamame; green soybeans"
            },
            {
                "word": "木枝",
                "reading": "きえだ",
                "meaning": "branch of a tree"
            },
            {
                "word": "枝分かれ",
                "reading": "えだわかれ",
                "meaning": "branching; ramification"
            }
        ]
    },
    {
        "kanji": "鳥",
        "meaning": [
            "bird"
        ],
        "onyomi": [
            "チョウ"
        ],
        "kunyomi": [
            "とり"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "小鳥",
                "reading": "ことり",
                "meaning": "small bird"
            },
            {
                "word": "野鳥",
                "reading": "やちょう",
                "meaning": "wild bird"
            },
            {
                "word": "渡り鳥",
                "reading": "わたりどり",
                "meaning": "migratory bird"
            }
        ]
    },
    {
        "kanji": "馬",
        "meaning": [
            "horse"
        ],
        "onyomi": [
            "バ"
        ],
        "kunyomi": [
            "うま"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "馬車",
                "reading": "ばしゃ",
                "meaning": "horse-drawn carriage"
            },
            {
                "word": "乗馬",
                "reading": "じょうば",
                "meaning": "horse riding"
            },
            {
                "word": "競馬",
                "reading": "けいば",
                "meaning": "horse racing"
            }
        ]
    },
    {
        "kanji": "牛",
        "meaning": [
            "cow; cattle"
        ],
        "onyomi": [
            "ギュウ"
        ],
        "kunyomi": [
            "うし"
        ],
        "jlpt": "N4",
        "stroke_count": 4,
        "examples": [
            {
                "word": "牛乳",
                "reading": "ぎゅうにゅう",
                "meaning": "milk"
            },
            {
                "word": "牛肉",
                "reading": "ぎゅうにく",
                "meaning": "beef"
            },
            {
                "word": "乳牛",
                "reading": "にゅうぎゅう",
                "meaning": "dairy cow"
            }
        ]
    },
    {
        "kanji": "虫",
        "meaning": [
            "insect; bug"
        ],
        "onyomi": [
            "チュウ"
        ],
        "kunyomi": [
            "むし"
        ],
        "jlpt": "N4",
        "stroke_count": 6,
        "examples": [
            {
                "word": "害虫",
                "reading": "がいちゅう",
                "meaning": "harmful insect; pest"
            },
            {
                "word": "昆虫",
                "reading": "こんちゅう",
                "meaning": "insect"
            },
            {
                "word": "虫歯",
                "reading": "むしば",
                "meaning": "cavity; decayed tooth"
            }
        ]
    },
    {
        "kanji": "地",
        "meaning": [
            "ground; earth; area"
        ],
        "onyomi": [
            "チ",
            "ジ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 6,
        "examples": [
            {
                "word": "地図",
                "reading": "ちず",
                "meaning": "map"
            },
            {
                "word": "地下鉄",
                "reading": "ちかてつ",
                "meaning": "subway"
            },
            {
                "word": "土地",
                "reading": "とち",
                "meaning": "land; plot"
            }
        ]
    },
    {
        "kanji": "界",
        "meaning": [
            "world; boundary"
        ],
        "onyomi": [
            "カイ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "世界",
                "reading": "せかい",
                "meaning": "world"
            },
            {
                "word": "限界",
                "reading": "げんかい",
                "meaning": "limit; boundary"
            },
            {
                "word": "業界",
                "reading": "ぎょうかい",
                "meaning": "industry; business world"
            }
        ]
    },
    {
        "kanji": "風",
        "meaning": [
            "wind; style"
        ],
        "onyomi": [
            "フウ",
            "フ"
        ],
        "kunyomi": [
            "かぜ",
            "かざ"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "台風",
                "reading": "たいふう",
                "meaning": "typhoon"
            },
            {
                "word": "風景",
                "reading": "ふうけい",
                "meaning": "scenery; landscape"
            },
            {
                "word": "風邪",
                "reading": "かぜ",
                "meaning": "cold (illness)"
            }
        ]
    },
    {
        "kanji": "雲",
        "meaning": [
            "cloud"
        ],
        "onyomi": [
            "ウン"
        ],
        "kunyomi": [
            "くも"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "雲海",
                "reading": "うんかい",
                "meaning": "sea of clouds"
            },
            {
                "word": "積乱雲",
                "reading": "せきらんうん",
                "meaning": "cumulonimbus cloud"
            },
            {
                "word": "入道雲",
                "reading": "にゅうどうぐも",
                "meaning": "thunderhead cloud"
            }
        ]
    },
    {
        "kanji": "星",
        "meaning": [
            "star"
        ],
        "onyomi": [
            "セイ",
            "ショウ"
        ],
        "kunyomi": [
            "ほし"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "星座",
                "reading": "せいざ",
                "meaning": "constellation"
            },
            {
                "word": "火星",
                "reading": "かせい",
                "meaning": "Mars"
            },
            {
                "word": "流れ星",
                "reading": "ながれぼし",
                "meaning": "shooting star"
            }
        ]
    },
    {
        "kanji": "味",
        "meaning": [
            "taste; flavor"
        ],
        "onyomi": [
            "ミ"
        ],
        "kunyomi": [
            "あじ",
            "あじ.わう"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "味噌",
                "reading": "みそ",
                "meaning": "miso"
            },
            {
                "word": "趣味",
                "reading": "しゅみ",
                "meaning": "hobby; taste"
            },
            {
                "word": "調味料",
                "reading": "ちょうみりょう",
                "meaning": "seasoning; condiment"
            }
        ]
    },
    {
        "kanji": "料",
        "meaning": [
            "fee; material; cuisine"
        ],
        "onyomi": [
            "リョウ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "料理",
                "reading": "りょうり",
                "meaning": "cooking; dish"
            },
            {
                "word": "料金",
                "reading": "りょうきん",
                "meaning": "fee; charge"
            },
            {
                "word": "材料",
                "reading": "ざいりょう",
                "meaning": "ingredients; materials"
            }
        ]
    },
    {
        "kanji": "飯",
        "meaning": [
            "cooked rice; meal"
        ],
        "onyomi": [
            "ハン"
        ],
        "kunyomi": [
            "めし"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "ご飯",
                "reading": "ごはん",
                "meaning": "rice; meal"
            },
            {
                "word": "朝飯",
                "reading": "あさめし",
                "meaning": "breakfast (informal)"
            },
            {
                "word": "炊飯器",
                "reading": "すいはんき",
                "meaning": "rice cooker"
            }
        ]
    },
    {
        "kanji": "茶",
        "meaning": [
            "tea"
        ],
        "onyomi": [
            "チャ",
            "サ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "お茶",
                "reading": "おちゃ",
                "meaning": "tea"
            },
            {
                "word": "喫茶店",
                "reading": "きっさてん",
                "meaning": "café"
            },
            {
                "word": "茶道",
                "reading": "さどう",
                "meaning": "tea ceremony"
            }
        ]
    },
    {
        "kanji": "酒",
        "meaning": [
            "alcohol; sake"
        ],
        "onyomi": [
            "シュ"
        ],
        "kunyomi": [
            "さけ",
            "さか"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "日本酒",
                "reading": "にほんしゅ",
                "meaning": "Japanese sake"
            },
            {
                "word": "居酒屋",
                "reading": "いざかや",
                "meaning": "izakaya; Japanese pub"
            },
            {
                "word": "禁酒",
                "reading": "きんしゅ",
                "meaning": "abstinence from alcohol"
            }
        ]
    },
    {
        "kanji": "肉",
        "meaning": [
            "meat; flesh"
        ],
        "onyomi": [
            "ニク"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 6,
        "examples": [
            {
                "word": "牛肉",
                "reading": "ぎゅうにく",
                "meaning": "beef"
            },
            {
                "word": "豚肉",
                "reading": "ぶたにく",
                "meaning": "pork"
            },
            {
                "word": "肉体",
                "reading": "にくたい",
                "meaning": "body; the flesh"
            }
        ]
    },
    {
        "kanji": "魚",
        "meaning": [
            "fish"
        ],
        "onyomi": [
            "ギョ"
        ],
        "kunyomi": [
            "さかな",
            "うお"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "金魚",
                "reading": "きんぎょ",
                "meaning": "goldfish"
            },
            {
                "word": "魚市場",
                "reading": "さかなしじょう",
                "meaning": "fish market"
            },
            {
                "word": "魚介類",
                "reading": "ぎょかいるい",
                "meaning": "seafood"
            }
        ]
    },
    {
        "kanji": "野",
        "meaning": [
            "field; wild"
        ],
        "onyomi": [
            "ヤ"
        ],
        "kunyomi": [
            "の"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "野菜",
                "reading": "やさい",
                "meaning": "vegetables"
            },
            {
                "word": "野球",
                "reading": "やきゅう",
                "meaning": "baseball"
            },
            {
                "word": "野原",
                "reading": "のはら",
                "meaning": "field; plain"
            }
        ]
    },
    {
        "kanji": "菜",
        "meaning": [
            "vegetable; greens"
        ],
        "onyomi": [
            "サイ"
        ],
        "kunyomi": [
            "な"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "野菜",
                "reading": "やさい",
                "meaning": "vegetables"
            },
            {
                "word": "菜食",
                "reading": "さいしょく",
                "meaning": "vegetarian diet"
            },
            {
                "word": "菜の花",
                "reading": "なのはな",
                "meaning": "rapeseed flower"
            }
        ]
    },
    {
        "kanji": "米",
        "meaning": [
            "rice (uncooked); USA"
        ],
        "onyomi": [
            "ベイ",
            "マイ"
        ],
        "kunyomi": [
            "こめ"
        ],
        "jlpt": "N4",
        "stroke_count": 6,
        "examples": [
            {
                "word": "お米",
                "reading": "おこめ",
                "meaning": "rice (uncooked)"
            },
            {
                "word": "日米",
                "reading": "にちべい",
                "meaning": "Japan-America"
            },
            {
                "word": "米国",
                "reading": "べいこく",
                "meaning": "United States"
            }
        ]
    },
    {
        "kanji": "豆",
        "meaning": [
            "bean; legume"
        ],
        "onyomi": [
            "トウ",
            "ズ"
        ],
        "kunyomi": [
            "まめ"
        ],
        "jlpt": "N4",
        "stroke_count": 7,
        "examples": [
            {
                "word": "豆腐",
                "reading": "とうふ",
                "meaning": "tofu"
            },
            {
                "word": "大豆",
                "reading": "だいず",
                "meaning": "soybean"
            },
            {
                "word": "枝豆",
                "reading": "えだまめ",
                "meaning": "edamame"
            }
        ]
    },
    {
        "kanji": "皿",
        "meaning": [
            "plate; dish; counter for dishes"
        ],
        "onyomi": [
            "サン"
        ],
        "kunyomi": [
            "さら"
        ],
        "jlpt": "N4",
        "stroke_count": 5,
        "examples": [
            {
                "word": "大皿",
                "reading": "おおざら",
                "meaning": "large plate; platter"
            },
            {
                "word": "小皿",
                "reading": "こざら",
                "meaning": "small plate; saucer"
            },
            {
                "word": "灰皿",
                "reading": "はいざら",
                "meaning": "ashtray"
            }
        ]
    },
    {
        "kanji": "室",
        "meaning": [
            "room; chamber"
        ],
        "onyomi": [
            "シツ"
        ],
        "kunyomi": [
            "むろ"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "教室",
                "reading": "きょうしつ",
                "meaning": "classroom"
            },
            {
                "word": "温室",
                "reading": "おんしつ",
                "meaning": "greenhouse"
            },
            {
                "word": "和室",
                "reading": "わしつ",
                "meaning": "Japanese-style room"
            }
        ]
    },
    {
        "kanji": "堂",
        "meaning": [
            "hall; temple; magnificent"
        ],
        "onyomi": [
            "ドウ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "食堂",
                "reading": "しょくどう",
                "meaning": "dining hall; cafeteria"
            },
            {
                "word": "講堂",
                "reading": "こうどう",
                "meaning": "auditorium"
            },
            {
                "word": "国会議事堂",
                "reading": "こっかいぎじどう",
                "meaning": "National Diet Building"
            }
        ]
    },
    {
        "kanji": "館",
        "meaning": [
            "building; hall"
        ],
        "onyomi": [
            "カン"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 16,
        "examples": [
            {
                "word": "図書館",
                "reading": "としょかん",
                "meaning": "library"
            },
            {
                "word": "博物館",
                "reading": "はくぶつかん",
                "meaning": "museum"
            },
            {
                "word": "旅館",
                "reading": "りょかん",
                "meaning": "Japanese inn"
            }
        ]
    },
    {
        "kanji": "場",
        "meaning": [
            "place; venue; occasion"
        ],
        "onyomi": [
            "ジョウ"
        ],
        "kunyomi": [
            "ば"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "場所",
                "reading": "ばしょ",
                "meaning": "place; location"
            },
            {
                "word": "工場",
                "reading": "こうじょう",
                "meaning": "factory"
            },
            {
                "word": "駐車場",
                "reading": "ちゅうしゃじょう",
                "meaning": "parking lot"
            }
        ]
    },
    {
        "kanji": "橋",
        "meaning": [
            "bridge"
        ],
        "onyomi": [
            "キョウ"
        ],
        "kunyomi": [
            "はし"
        ],
        "jlpt": "N4",
        "stroke_count": 16,
        "examples": [
            {
                "word": "鉄橋",
                "reading": "てっきょう",
                "meaning": "iron bridge; railroad bridge"
            },
            {
                "word": "歩道橋",
                "reading": "ほどうきょう",
                "meaning": "pedestrian bridge"
            },
            {
                "word": "橋渡し",
                "reading": "はしわたし",
                "meaning": "mediation; bridge-building"
            }
        ]
    },
    {
        "kanji": "道",
        "meaning": [
            "road; way; path"
        ],
        "onyomi": [
            "ドウ",
            "トウ"
        ],
        "kunyomi": [
            "みち"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "北海道",
                "reading": "ほっかいどう",
                "meaning": "Hokkaido"
            },
            {
                "word": "道路",
                "reading": "どうろ",
                "meaning": "road; highway"
            },
            {
                "word": "道具",
                "reading": "どうぐ",
                "meaning": "tool; instrument"
            }
        ]
    },
    {
        "kanji": "角",
        "meaning": [
            "corner; angle; horn"
        ],
        "onyomi": [
            "カク"
        ],
        "kunyomi": [
            "かど",
            "つの"
        ],
        "jlpt": "N4",
        "stroke_count": 7,
        "examples": [
            {
                "word": "角を曲がる",
                "reading": "かどをまがる",
                "meaning": "to turn the corner"
            },
            {
                "word": "三角",
                "reading": "さんかく",
                "meaning": "triangle"
            },
            {
                "word": "四角",
                "reading": "しかく",
                "meaning": "square; rectangle"
            }
        ]
    },
    {
        "kanji": "工",
        "meaning": [
            "work; construction; industry"
        ],
        "onyomi": [
            "コウ",
            "ク"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 3,
        "examples": [
            {
                "word": "工場",
                "reading": "こうじょう",
                "meaning": "factory"
            },
            {
                "word": "工業",
                "reading": "こうぎょう",
                "meaning": "industry; manufacturing"
            },
            {
                "word": "工事",
                "reading": "こうじ",
                "meaning": "construction; engineering works"
            }
        ]
    },
    {
        "kanji": "農",
        "meaning": [
            "agriculture; farming"
        ],
        "onyomi": [
            "ノウ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 13,
        "examples": [
            {
                "word": "農業",
                "reading": "のうぎょう",
                "meaning": "agriculture; farming"
            },
            {
                "word": "農家",
                "reading": "のうか",
                "meaning": "farm household; farmer"
            },
            {
                "word": "農産物",
                "reading": "のうさんぶつ",
                "meaning": "agricultural produce"
            }
        ]
    },
    {
        "kanji": "産",
        "meaning": [
            "produce; give birth; assets"
        ],
        "onyomi": [
            "サン"
        ],
        "kunyomi": [
            "う.む",
            "う.まれる"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "産業",
                "reading": "さんぎょう",
                "meaning": "industry"
            },
            {
                "word": "生産",
                "reading": "せいさん",
                "meaning": "production; manufacturing"
            },
            {
                "word": "土産",
                "reading": "みやげ",
                "meaning": "souvenir; gift"
            }
        ]
    },
    {
        "kanji": "業",
        "meaning": [
            "business; industry; karma"
        ],
        "onyomi": [
            "ギョウ",
            "ゴウ"
        ],
        "kunyomi": [
            "わざ"
        ],
        "jlpt": "N4",
        "stroke_count": 13,
        "examples": [
            {
                "word": "卒業",
                "reading": "そつぎょう",
                "meaning": "graduation"
            },
            {
                "word": "授業",
                "reading": "じゅぎょう",
                "meaning": "class; lesson"
            },
            {
                "word": "職業",
                "reading": "しょくぎょう",
                "meaning": "occupation; profession"
            }
        ]
    },
    {
        "kanji": "都",
        "meaning": [
            "capital; metropolis"
        ],
        "onyomi": [
            "ト",
            "ツ"
        ],
        "kunyomi": [
            "みやこ"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "東京都",
                "reading": "とうきょうと",
                "meaning": "Tokyo Metropolis"
            },
            {
                "word": "首都",
                "reading": "しゅと",
                "meaning": "capital city"
            },
            {
                "word": "都市",
                "reading": "とし",
                "meaning": "city; urban area"
            }
        ]
    },
    {
        "kanji": "市",
        "meaning": [
            "city; market"
        ],
        "onyomi": [
            "シ"
        ],
        "kunyomi": [
            "いち"
        ],
        "jlpt": "N4",
        "stroke_count": 5,
        "examples": [
            {
                "word": "市場",
                "reading": "いちば",
                "meaning": "market; marketplace"
            },
            {
                "word": "市民",
                "reading": "しみん",
                "meaning": "citizen"
            },
            {
                "word": "都市",
                "reading": "とし",
                "meaning": "city; urban area"
            }
        ]
    },
    {
        "kanji": "村",
        "meaning": [
            "village"
        ],
        "onyomi": [
            "ソン"
        ],
        "kunyomi": [
            "むら"
        ],
        "jlpt": "N4",
        "stroke_count": 7,
        "examples": [
            {
                "word": "農村",
                "reading": "のうそん",
                "meaning": "farming village; rural area"
            },
            {
                "word": "村人",
                "reading": "むらびと",
                "meaning": "villager"
            },
            {
                "word": "市町村",
                "reading": "しちょうそん",
                "meaning": "municipalities"
            }
        ]
    },
    {
        "kanji": "町",
        "meaning": [
            "town; neighborhood"
        ],
        "onyomi": [
            "チョウ"
        ],
        "kunyomi": [
            "まち"
        ],
        "jlpt": "N4",
        "stroke_count": 7,
        "examples": [
            {
                "word": "町中",
                "reading": "まちなか",
                "meaning": "downtown; in the middle of town"
            },
            {
                "word": "町内",
                "reading": "ちょうない",
                "meaning": "neighborhood; town district"
            },
            {
                "word": "下町",
                "reading": "したまち",
                "meaning": "shitamachi; low city"
            }
        ]
    },
    {
        "kanji": "乗",
        "meaning": [
            "ride; board; multiply"
        ],
        "onyomi": [
            "ジョウ"
        ],
        "kunyomi": [
            "の.る",
            "の.せる"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "乗り換え",
                "reading": "のりかえ",
                "meaning": "transfer; change"
            },
            {
                "word": "乗り場",
                "reading": "のりば",
                "meaning": "boarding area; stop"
            },
            {
                "word": "乗客",
                "reading": "じょうきゃく",
                "meaning": "passenger"
            }
        ]
    },
    {
        "kanji": "降",
        "meaning": [
            "descend; get off; rain"
        ],
        "onyomi": [
            "コウ"
        ],
        "kunyomi": [
            "お.りる",
            "ふ.る"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "降りる",
                "reading": "おりる",
                "meaning": "to get off; to descend"
            },
            {
                "word": "降水量",
                "reading": "こうすいりょう",
                "meaning": "precipitation"
            },
            {
                "word": "以降",
                "reading": "いこう",
                "meaning": "since then; on and after"
            }
        ]
    },
    {
        "kanji": "着",
        "meaning": [
            "arrive; wear; attach"
        ],
        "onyomi": [
            "チャク"
        ],
        "kunyomi": [
            "き.る",
            "つ.く",
            "き.せる"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "到着",
                "reading": "とうちゃく",
                "meaning": "arrival"
            },
            {
                "word": "着物",
                "reading": "きもの",
                "meaning": "kimono"
            },
            {
                "word": "着替え",
                "reading": "きがえ",
                "meaning": "change of clothes"
            }
        ]
    },
    {
        "kanji": "発",
        "meaning": [
            "depart; emit; start"
        ],
        "onyomi": [
            "ハツ",
            "ホツ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "出発",
                "reading": "しゅっぱつ",
                "meaning": "departure"
            },
            {
                "word": "発表",
                "reading": "はっぴょう",
                "meaning": "announcement; presentation"
            },
            {
                "word": "発展",
                "reading": "はってん",
                "meaning": "development; growth"
            }
        ]
    },
    {
        "kanji": "通",
        "meaning": [
            "pass through; commute; street"
        ],
        "onyomi": [
            "ツウ",
            "ツ"
        ],
        "kunyomi": [
            "とお.る",
            "かよ.う"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "交通",
                "reading": "こうつう",
                "meaning": "traffic; transportation"
            },
            {
                "word": "通勤",
                "reading": "つうきん",
                "meaning": "commuting to work"
            },
            {
                "word": "通り",
                "reading": "とおり",
                "meaning": "street; avenue"
            }
        ]
    },
    {
        "kanji": "運",
        "meaning": [
            "carry; luck; fate"
        ],
        "onyomi": [
            "ウン"
        ],
        "kunyomi": [
            "はこ.ぶ"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "運転",
                "reading": "うんてん",
                "meaning": "driving; operation"
            },
            {
                "word": "運動",
                "reading": "うんどう",
                "meaning": "exercise; movement"
            },
            {
                "word": "運命",
                "reading": "うんめい",
                "meaning": "fate; destiny"
            }
        ]
    },
    {
        "kanji": "転",
        "meaning": [
            "roll; turn; change"
        ],
        "onyomi": [
            "テン"
        ],
        "kunyomi": [
            "ころ.ぶ",
            "ころ.がる"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "自転車",
                "reading": "じてんしゃ",
                "meaning": "bicycle"
            },
            {
                "word": "運転",
                "reading": "うんてん",
                "meaning": "driving"
            },
            {
                "word": "転居",
                "reading": "てんきょ",
                "meaning": "change of address; moving"
            }
        ]
    },
    {
        "kanji": "急",
        "meaning": [
            "sudden; hurry; steep"
        ],
        "onyomi": [
            "キュウ"
        ],
        "kunyomi": [
            "いそ.ぐ"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "急行",
                "reading": "きゅうこう",
                "meaning": "express (train)"
            },
            {
                "word": "急ぐ",
                "reading": "いそぐ",
                "meaning": "to hurry"
            },
            {
                "word": "緊急",
                "reading": "きんきゅう",
                "meaning": "emergency; urgent"
            }
        ]
    },
    {
        "kanji": "特",
        "meaning": [
            "special; particular"
        ],
        "onyomi": [
            "トク"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "特急",
                "reading": "とっきゅう",
                "meaning": "limited express"
            },
            {
                "word": "特別",
                "reading": "とくべつ",
                "meaning": "special"
            },
            {
                "word": "特に",
                "reading": "とくに",
                "meaning": "especially; particularly"
            }
        ]
    },
    {
        "kanji": "図",
        "meaning": [
            "diagram; map; plan"
        ],
        "onyomi": [
            "ズ",
            "ト"
        ],
        "kunyomi": [
            "はか.る"
        ],
        "jlpt": "N4",
        "stroke_count": 7,
        "examples": [
            {
                "word": "地図",
                "reading": "ちず",
                "meaning": "map"
            },
            {
                "word": "図書館",
                "reading": "としょかん",
                "meaning": "library"
            },
            {
                "word": "図形",
                "reading": "ずけい",
                "meaning": "figure; shape"
            }
        ]
    },
    {
        "kanji": "港",
        "meaning": [
            "harbor; port"
        ],
        "onyomi": [
            "コウ"
        ],
        "kunyomi": [
            "みなと"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "空港",
                "reading": "くうこう",
                "meaning": "airport"
            },
            {
                "word": "港町",
                "reading": "みなとまち",
                "meaning": "port town"
            },
            {
                "word": "出港",
                "reading": "しゅっこう",
                "meaning": "departure from port"
            }
        ]
    },
    {
        "kanji": "旅",
        "meaning": [
            "travel; journey"
        ],
        "onyomi": [
            "リョ"
        ],
        "kunyomi": [
            "たび"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "旅行",
                "reading": "りょこう",
                "meaning": "travel; trip"
            },
            {
                "word": "旅館",
                "reading": "りょかん",
                "meaning": "Japanese inn"
            },
            {
                "word": "旅費",
                "reading": "りょひ",
                "meaning": "travel expenses"
            }
        ]
    },
    {
        "kanji": "研",
        "meaning": [
            "polish; study; research"
        ],
        "onyomi": [
            "ケン"
        ],
        "kunyomi": [
            "と.ぐ"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "研究",
                "reading": "けんきゅう",
                "meaning": "research; study"
            },
            {
                "word": "研修",
                "reading": "けんしゅう",
                "meaning": "training; study program"
            },
            {
                "word": "研磨",
                "reading": "けんま",
                "meaning": "polishing; grinding"
            }
        ]
    },
    {
        "kanji": "究",
        "meaning": [
            "research; investigate"
        ],
        "onyomi": [
            "キュウ"
        ],
        "kunyomi": [
            "きわ.める"
        ],
        "jlpt": "N4",
        "stroke_count": 7,
        "examples": [
            {
                "word": "研究",
                "reading": "けんきゅう",
                "meaning": "research"
            },
            {
                "word": "究極",
                "reading": "きゅうきょく",
                "meaning": "ultimate; final"
            },
            {
                "word": "追究",
                "reading": "ついきゅう",
                "meaning": "investigation; inquiry"
            }
        ]
    },
    {
        "kanji": "発",
        "meaning": [
            "depart; emit; announce"
        ],
        "onyomi": [
            "ハツ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "発表",
                "reading": "はっぴょう",
                "meaning": "presentation; announcement"
            },
            {
                "word": "発達",
                "reading": "はったつ",
                "meaning": "development; growth"
            },
            {
                "word": "出発",
                "reading": "しゅっぱつ",
                "meaning": "departure"
            }
        ]
    },
    {
        "kanji": "試",
        "meaning": [
            "try; test; attempt"
        ],
        "onyomi": [
            "シ"
        ],
        "kunyomi": [
            "こころ.みる",
            "ため.す"
        ],
        "jlpt": "N4",
        "stroke_count": 13,
        "examples": [
            {
                "word": "試験",
                "reading": "しけん",
                "meaning": "exam; test"
            },
            {
                "word": "試合",
                "reading": "しあい",
                "meaning": "match; game; contest"
            },
            {
                "word": "試着",
                "reading": "しちゃく",
                "meaning": "trying on clothes"
            }
        ]
    },
    {
        "kanji": "験",
        "meaning": [
            "effect; result; exam"
        ],
        "onyomi": [
            "ケン",
            "ゲン"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 18,
        "examples": [
            {
                "word": "試験",
                "reading": "しけん",
                "meaning": "exam; test"
            },
            {
                "word": "経験",
                "reading": "けいけん",
                "meaning": "experience"
            },
            {
                "word": "実験",
                "reading": "じっけん",
                "meaning": "experiment"
            }
        ]
    },
    {
        "kanji": "文",
        "meaning": [
            "sentence; literature; pattern"
        ],
        "onyomi": [
            "ブン",
            "モン"
        ],
        "kunyomi": [
            "ふみ"
        ],
        "jlpt": "N4",
        "stroke_count": 4,
        "examples": [
            {
                "word": "文法",
                "reading": "ぶんぽう",
                "meaning": "grammar"
            },
            {
                "word": "文化",
                "reading": "ぶんか",
                "meaning": "culture"
            },
            {
                "word": "作文",
                "reading": "さくぶん",
                "meaning": "composition; essay"
            }
        ]
    },
    {
        "kanji": "法",
        "meaning": [
            "law; method; way"
        ],
        "onyomi": [
            "ホウ",
            "ハッ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "文法",
                "reading": "ぶんぽう",
                "meaning": "grammar"
            },
            {
                "word": "方法",
                "reading": "ほうほう",
                "meaning": "method; way"
            },
            {
                "word": "法律",
                "reading": "ほうりつ",
                "meaning": "law"
            }
        ]
    },
    {
        "kanji": "習",
        "meaning": [
            "learn; practice; habit"
        ],
        "onyomi": [
            "シュウ"
        ],
        "kunyomi": [
            "なら.う"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "習慣",
                "reading": "しゅうかん",
                "meaning": "habit; custom"
            },
            {
                "word": "予習",
                "reading": "よしゅう",
                "meaning": "preparation; previewing"
            },
            {
                "word": "復習",
                "reading": "ふくしゅう",
                "meaning": "review; revision"
            }
        ]
    },
    {
        "kanji": "練",
        "meaning": [
            "practice; knead; train"
        ],
        "onyomi": [
            "レン"
        ],
        "kunyomi": [
            "ね.る"
        ],
        "jlpt": "N4",
        "stroke_count": 14,
        "examples": [
            {
                "word": "練習",
                "reading": "れんしゅう",
                "meaning": "practice"
            },
            {
                "word": "訓練",
                "reading": "くんれん",
                "meaning": "training; drill"
            },
            {
                "word": "熟練",
                "reading": "じゅくれん",
                "meaning": "skill; mastery"
            }
        ]
    },
    {
        "kanji": "教",
        "meaning": [
            "teach; religion"
        ],
        "onyomi": [
            "キョウ"
        ],
        "kunyomi": [
            "おし.える",
            "おそ.わる"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "教育",
                "reading": "きょういく",
                "meaning": "education"
            },
            {
                "word": "教師",
                "reading": "きょうし",
                "meaning": "teacher"
            },
            {
                "word": "宗教",
                "reading": "しゅうきょう",
                "meaning": "religion"
            }
        ]
    },
    {
        "kanji": "授",
        "meaning": [
            "teach; grant; award"
        ],
        "onyomi": [
            "ジュ"
        ],
        "kunyomi": [
            "さず.ける"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "授業",
                "reading": "じゅぎょう",
                "meaning": "class; lesson"
            },
            {
                "word": "教授",
                "reading": "きょうじゅ",
                "meaning": "professor"
            },
            {
                "word": "授与",
                "reading": "じゅよ",
                "meaning": "presentation; conferring"
            }
        ]
    },
    {
        "kanji": "卒",
        "meaning": [
            "graduate; soldier; die"
        ],
        "onyomi": [
            "ソツ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "卒業",
                "reading": "そつぎょう",
                "meaning": "graduation"
            },
            {
                "word": "卒業生",
                "reading": "そつぎょうせい",
                "meaning": "graduate; alumnus"
            },
            {
                "word": "卒論",
                "reading": "そつろん",
                "meaning": "graduation thesis"
            }
        ]
    },
    {
        "kanji": "科",
        "meaning": [
            "department; subject; branch"
        ],
        "onyomi": [
            "カ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "科学",
                "reading": "かがく",
                "meaning": "science"
            },
            {
                "word": "外科",
                "reading": "げか",
                "meaning": "surgery; surgical department"
            },
            {
                "word": "教科書",
                "reading": "きょうかしょ",
                "meaning": "textbook"
            }
        ]
    },
    {
        "kanji": "専",
        "meaning": [
            "specialize; concentrate"
        ],
        "onyomi": [
            "セン"
        ],
        "kunyomi": [
            "もっぱ.ら"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "専門",
                "reading": "せんもん",
                "meaning": "specialty; major field"
            },
            {
                "word": "専攻",
                "reading": "せんこう",
                "meaning": "major; specialization"
            },
            {
                "word": "専用",
                "reading": "せんよう",
                "meaning": "exclusive use; dedicated"
            }
        ]
    },
    {
        "kanji": "始",
        "meaning": [
            "begin; start"
        ],
        "onyomi": [
            "シ"
        ],
        "kunyomi": [
            "はじ.める",
            "はじ.まる"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "開始",
                "reading": "かいし",
                "meaning": "start; commencement"
            },
            {
                "word": "始業",
                "reading": "しぎょう",
                "meaning": "start of work/school"
            },
            {
                "word": "始末",
                "reading": "しまつ",
                "meaning": "management; disposal"
            }
        ]
    },
    {
        "kanji": "終",
        "meaning": [
            "end; finish"
        ],
        "onyomi": [
            "シュウ"
        ],
        "kunyomi": [
            "お.わる",
            "お.える"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "終了",
                "reading": "しゅうりょう",
                "meaning": "end; completion"
            },
            {
                "word": "最終",
                "reading": "さいしゅう",
                "meaning": "last; final"
            },
            {
                "word": "終点",
                "reading": "しゅうてん",
                "meaning": "terminal; last stop"
            }
        ]
    },
    {
        "kanji": "決",
        "meaning": [
            "decide; determine"
        ],
        "onyomi": [
            "ケツ"
        ],
        "kunyomi": [
            "き.める",
            "き.まる"
        ],
        "jlpt": "N4",
        "stroke_count": 7,
        "examples": [
            {
                "word": "決定",
                "reading": "けってい",
                "meaning": "decision; determination"
            },
            {
                "word": "解決",
                "reading": "かいけつ",
                "meaning": "resolution; solution"
            },
            {
                "word": "決勝",
                "reading": "けっしょう",
                "meaning": "final; decisive match"
            }
        ]
    },
    {
        "kanji": "変",
        "meaning": [
            "change; strange"
        ],
        "onyomi": [
            "ヘン"
        ],
        "kunyomi": [
            "か.わる",
            "か.える"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "変化",
                "reading": "へんか",
                "meaning": "change; variation"
            },
            {
                "word": "大変",
                "reading": "たいへん",
                "meaning": "terrible; very"
            },
            {
                "word": "変わる",
                "reading": "かわる",
                "meaning": "to change; to be different"
            }
        ]
    },
    {
        "kanji": "増",
        "meaning": [
            "increase; more"
        ],
        "onyomi": [
            "ゾウ"
        ],
        "kunyomi": [
            "ふ.える",
            "ふ.やす"
        ],
        "jlpt": "N4",
        "stroke_count": 14,
        "examples": [
            {
                "word": "増加",
                "reading": "ぞうか",
                "meaning": "increase"
            },
            {
                "word": "増える",
                "reading": "ふえる",
                "meaning": "to increase"
            },
            {
                "word": "増税",
                "reading": "ぞうぜい",
                "meaning": "tax increase"
            }
        ]
    },
    {
        "kanji": "減",
        "meaning": [
            "decrease; less"
        ],
        "onyomi": [
            "ゲン"
        ],
        "kunyomi": [
            "へ.る",
            "へ.らす"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "削減",
                "reading": "さくげん",
                "meaning": "reduction; curtailment"
            },
            {
                "word": "減少",
                "reading": "げんしょう",
                "meaning": "decrease; reduction"
            },
            {
                "word": "節減",
                "reading": "せつげん",
                "meaning": "economizing; saving"
            }
        ]
    },
    {
        "kanji": "集",
        "meaning": [
            "gather; collect"
        ],
        "onyomi": [
            "シュウ"
        ],
        "kunyomi": [
            "あつ.まる",
            "あつ.める"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "集中",
                "reading": "しゅうちゅう",
                "meaning": "concentration; focus"
            },
            {
                "word": "収集",
                "reading": "しゅうしゅう",
                "meaning": "collection; gathering"
            },
            {
                "word": "編集",
                "reading": "へんしゅう",
                "meaning": "editing; compilation"
            }
        ]
    },
    {
        "kanji": "別",
        "meaning": [
            "separate; different; special"
        ],
        "onyomi": [
            "ベツ"
        ],
        "kunyomi": [
            "わか.れる"
        ],
        "jlpt": "N4",
        "stroke_count": 7,
        "examples": [
            {
                "word": "特別",
                "reading": "とくべつ",
                "meaning": "special"
            },
            {
                "word": "別々",
                "reading": "べつべつ",
                "meaning": "separately; individually"
            },
            {
                "word": "区別",
                "reading": "くべつ",
                "meaning": "distinction; differentiation"
            }
        ]
    },
    {
        "kanji": "続",
        "meaning": [
            "continue; follow"
        ],
        "onyomi": [
            "ゾク"
        ],
        "kunyomi": [
            "つづ.く",
            "つづ.ける"
        ],
        "jlpt": "N4",
        "stroke_count": 13,
        "examples": [
            {
                "word": "継続",
                "reading": "けいぞく",
                "meaning": "continuation"
            },
            {
                "word": "連続",
                "reading": "れんぞく",
                "meaning": "consecutive; successive"
            },
            {
                "word": "続き",
                "reading": "つづき",
                "meaning": "continuation; sequel"
            }
        ]
    },
    {
        "kanji": "止",
        "meaning": [
            "stop; cease"
        ],
        "onyomi": [
            "シ"
        ],
        "kunyomi": [
            "と.まる",
            "と.める",
            "や.める"
        ],
        "jlpt": "N4",
        "stroke_count": 4,
        "examples": [
            {
                "word": "禁止",
                "reading": "きんし",
                "meaning": "prohibition; ban"
            },
            {
                "word": "中止",
                "reading": "ちゅうし",
                "meaning": "suspension; cancellation"
            },
            {
                "word": "停止",
                "reading": "ていし",
                "meaning": "stoppage; suspension"
            }
        ]
    },
    {
        "kanji": "動",
        "meaning": [
            "move; motion; action"
        ],
        "onyomi": [
            "ドウ"
        ],
        "kunyomi": [
            "うご.く",
            "うご.かす"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "運動",
                "reading": "うんどう",
                "meaning": "exercise; movement"
            },
            {
                "word": "活動",
                "reading": "かつどう",
                "meaning": "activity; action"
            },
            {
                "word": "動物",
                "reading": "どうぶつ",
                "meaning": "animal"
            }
        ]
    },
    {
        "kanji": "働",
        "meaning": [
            "work; labor"
        ],
        "onyomi": [
            "ドウ"
        ],
        "kunyomi": [
            "はたら.く"
        ],
        "jlpt": "N4",
        "stroke_count": 13,
        "examples": [
            {
                "word": "労働",
                "reading": "ろうどう",
                "meaning": "labor; work"
            },
            {
                "word": "働き",
                "reading": "はたらき",
                "meaning": "work; function; earning"
            },
            {
                "word": "働き者",
                "reading": "はたらきもの",
                "meaning": "hard worker"
            }
        ]
    },
    {
        "kanji": "使",
        "meaning": [
            "use; employ; messenger"
        ],
        "onyomi": [
            "シ"
        ],
        "kunyomi": [
            "つか.う"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "使用",
                "reading": "しよう",
                "meaning": "use; application"
            },
            {
                "word": "大使",
                "reading": "たいし",
                "meaning": "ambassador"
            },
            {
                "word": "使い方",
                "reading": "つかいかた",
                "meaning": "how to use; usage"
            }
        ]
    },
    {
        "kanji": "送",
        "meaning": [
            "send; accompany"
        ],
        "onyomi": [
            "ソウ"
        ],
        "kunyomi": [
            "おく.る"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "送料",
                "reading": "そうりょう",
                "meaning": "shipping fee"
            },
            {
                "word": "放送",
                "reading": "ほうそう",
                "meaning": "broadcast"
            },
            {
                "word": "見送り",
                "reading": "みおくり",
                "meaning": "seeing off; farewell"
            }
        ]
    },
    {
        "kanji": "受",
        "meaning": [
            "receive; accept; take"
        ],
        "onyomi": [
            "ジュ"
        ],
        "kunyomi": [
            "う.ける",
            "う.かる"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "受付",
                "reading": "うけつけ",
                "meaning": "reception; front desk"
            },
            {
                "word": "受験",
                "reading": "じゅけん",
                "meaning": "taking an exam"
            },
            {
                "word": "受け取る",
                "reading": "うけとる",
                "meaning": "to receive; to accept"
            }
        ]
    },
    {
        "kanji": "取",
        "meaning": [
            "take; get"
        ],
        "onyomi": [
            "シュ"
        ],
        "kunyomi": [
            "と.る"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "取り出す",
                "reading": "とりだす",
                "meaning": "to take out"
            },
            {
                "word": "受け取る",
                "reading": "うけとる",
                "meaning": "to receive"
            },
            {
                "word": "取引",
                "reading": "とりひき",
                "meaning": "transaction; trade"
            }
        ]
    },
    {
        "kanji": "持",
        "meaning": [
            "hold; carry; have"
        ],
        "onyomi": [
            "ジ"
        ],
        "kunyomi": [
            "も.つ"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "持ち物",
                "reading": "もちもの",
                "meaning": "one's belongings"
            },
            {
                "word": "持続",
                "reading": "じぞく",
                "meaning": "continuation; persistence"
            },
            {
                "word": "気持ち",
                "reading": "きもち",
                "meaning": "feeling; mood"
            }
        ]
    },
    {
        "kanji": "置",
        "meaning": [
            "put; place; leave"
        ],
        "onyomi": [
            "チ"
        ],
        "kunyomi": [
            "お.く"
        ],
        "jlpt": "N4",
        "stroke_count": 13,
        "examples": [
            {
                "word": "位置",
                "reading": "いち",
                "meaning": "position; location"
            },
            {
                "word": "放置",
                "reading": "ほうち",
                "meaning": "leaving alone; neglect"
            },
            {
                "word": "措置",
                "reading": "そち",
                "meaning": "measure; step; action"
            }
        ]
    },
    {
        "kanji": "落",
        "meaning": [
            "fall; drop; come off"
        ],
        "onyomi": [
            "ラク"
        ],
        "kunyomi": [
            "お.ちる",
            "お.とす"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "落ち着く",
                "reading": "おちつく",
                "meaning": "to calm down; to settle"
            },
            {
                "word": "落第",
                "reading": "らくだい",
                "meaning": "failure; flunking"
            },
            {
                "word": "滝",
                "reading": "たき",
                "meaning": "waterfall"
            }
        ]
    },
    {
        "kanji": "直",
        "meaning": [
            "fix; honest; straight"
        ],
        "onyomi": [
            "チョク",
            "ジキ"
        ],
        "kunyomi": [
            "なお.す",
            "なお.る",
            "す.ぐ"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "正直",
                "reading": "しょうじき",
                "meaning": "honest; honesty"
            },
            {
                "word": "直接",
                "reading": "ちょくせつ",
                "meaning": "direct; immediate"
            },
            {
                "word": "直ちに",
                "reading": "ただちに",
                "meaning": "immediately; at once"
            }
        ]
    },
    {
        "kanji": "壊",
        "meaning": [
            "break; demolish; ruin"
        ],
        "onyomi": [
            "カイ"
        ],
        "kunyomi": [
            "こわ.す",
            "こわ.れる"
        ],
        "jlpt": "N4",
        "stroke_count": 16,
        "examples": [
            {
                "word": "破壊",
                "reading": "はかい",
                "meaning": "destruction; demolition"
            },
            {
                "word": "崩壊",
                "reading": "ほうかい",
                "meaning": "collapse; disintegration"
            },
            {
                "word": "壊れる",
                "reading": "こわれる",
                "meaning": "to break; to be broken"
            }
        ]
    },
    {
        "kanji": "消",
        "meaning": [
            "erase; extinguish; disappear"
        ],
        "onyomi": [
            "ショウ"
        ],
        "kunyomi": [
            "き.える",
            "け.す"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "消える",
                "reading": "きえる",
                "meaning": "to disappear; to go out"
            },
            {
                "word": "消費",
                "reading": "しょうひ",
                "meaning": "consumption"
            },
            {
                "word": "消防",
                "reading": "しょうぼう",
                "meaning": "firefighting"
            }
        ]
    },
    {
        "kanji": "付",
        "meaning": [
            "attach; accompany"
        ],
        "onyomi": [
            "フ"
        ],
        "kunyomi": [
            "つ.ける",
            "つ.く"
        ],
        "jlpt": "N4",
        "stroke_count": 5,
        "examples": [
            {
                "word": "気付く",
                "reading": "きづく",
                "meaning": "to notice; to realize"
            },
            {
                "word": "受け付ける",
                "reading": "うけつける",
                "meaning": "to accept; to receive"
            },
            {
                "word": "付近",
                "reading": "ふきん",
                "meaning": "vicinity; neighborhood"
            }
        ]
    },
    {
        "kanji": "開",
        "meaning": [
            "open; begin; hold"
        ],
        "onyomi": [
            "カイ"
        ],
        "kunyomi": [
            "あ.ける",
            "あ.く",
            "ひら.く"
        ],
        "jlpt": "N4",
        "stroke_count": 12,
        "examples": [
            {
                "word": "開発",
                "reading": "かいはつ",
                "meaning": "development"
            },
            {
                "word": "開始",
                "reading": "かいし",
                "meaning": "start; commencement"
            },
            {
                "word": "公開",
                "reading": "こうかい",
                "meaning": "open to the public; release"
            }
        ]
    },
    {
        "kanji": "閉",
        "meaning": [
            "close; shut"
        ],
        "onyomi": [
            "ヘイ"
        ],
        "kunyomi": [
            "し.める",
            "し.まる",
            "と.じる"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "閉まる",
                "reading": "しまる",
                "meaning": "to close (intrans.)"
            },
            {
                "word": "閉店",
                "reading": "へいてん",
                "meaning": "store closing"
            },
            {
                "word": "閉会",
                "reading": "へいかい",
                "meaning": "closing (of a meeting)"
            }
        ]
    },
    {
        "kanji": "選",
        "meaning": [
            "choose; select"
        ],
        "onyomi": [
            "セン"
        ],
        "kunyomi": [
            "えら.ぶ"
        ],
        "jlpt": "N4",
        "stroke_count": 15,
        "examples": [
            {
                "word": "選択",
                "reading": "せんたく",
                "meaning": "choice; selection"
            },
            {
                "word": "選手",
                "reading": "せんしゅ",
                "meaning": "athlete; player"
            },
            {
                "word": "選挙",
                "reading": "せんきょ",
                "meaning": "election"
            }
        ]
    },
    {
        "kanji": "並",
        "meaning": [
            "line up; ordinary; average"
        ],
        "onyomi": [
            "ヘイ"
        ],
        "kunyomi": [
            "なら.ぶ",
            "なら.べる"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "並木",
                "reading": "なみき",
                "meaning": "roadside trees; tree-lined street"
            },
            {
                "word": "並べる",
                "reading": "ならべる",
                "meaning": "to line up; to arrange"
            },
            {
                "word": "大並み",
                "reading": "おおなみ",
                "meaning": "large wave"
            }
        ]
    },
    {
        "kanji": "比",
        "meaning": [
            "compare; ratio"
        ],
        "onyomi": [
            "ヒ"
        ],
        "kunyomi": [
            "くら.べる"
        ],
        "jlpt": "N4",
        "stroke_count": 4,
        "examples": [
            {
                "word": "比べる",
                "reading": "くらべる",
                "meaning": "to compare"
            },
            {
                "word": "比率",
                "reading": "ひりつ",
                "meaning": "ratio; proportion"
            },
            {
                "word": "日比",
                "reading": "にっぴ",
                "meaning": "Japan-Philippines"
            }
        ]
    },
    {
        "kanji": "調",
        "meaning": [
            "investigate; tone; prepare"
        ],
        "onyomi": [
            "チョウ"
        ],
        "kunyomi": [
            "しら.べる",
            "ととの.える"
        ],
        "jlpt": "N4",
        "stroke_count": 15,
        "examples": [
            {
                "word": "調べる",
                "reading": "しらべる",
                "meaning": "to investigate; to check"
            },
            {
                "word": "調査",
                "reading": "ちょうさ",
                "meaning": "investigation; survey"
            },
            {
                "word": "調理",
                "reading": "ちょうり",
                "meaning": "cooking; preparation of food"
            }
        ]
    },
    {
        "kanji": "笑",
        "meaning": [
            "laugh; smile"
        ],
        "onyomi": [
            "ショウ"
        ],
        "kunyomi": [
            "わら.う",
            "え.む"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "笑顔",
                "reading": "えがお",
                "meaning": "smiling face"
            },
            {
                "word": "苦笑",
                "reading": "くしょう",
                "meaning": "wry smile; bitter smile"
            },
            {
                "word": "大笑い",
                "reading": "おおわらい",
                "meaning": "laughing heartily"
            }
        ]
    },
    {
        "kanji": "泣",
        "meaning": [
            "cry; weep"
        ],
        "onyomi": [
            "キュウ"
        ],
        "kunyomi": [
            "な.く"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "泣く",
                "reading": "なく",
                "meaning": "to cry; to weep"
            },
            {
                "word": "号泣",
                "reading": "ごうきゅう",
                "meaning": "crying out loud; wailing"
            },
            {
                "word": "泣き声",
                "reading": "なきごえ",
                "meaning": "crying voice; cry"
            }
        ]
    },
    {
        "kanji": "怒",
        "meaning": [
            "get angry; rage"
        ],
        "onyomi": [
            "ド",
            "ヌ"
        ],
        "kunyomi": [
            "おこ.る",
            "いか.る"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "怒る",
                "reading": "おこる",
                "meaning": "to get angry"
            },
            {
                "word": "激怒",
                "reading": "げきど",
                "meaning": "fury; rage"
            },
            {
                "word": "怒鳴る",
                "reading": "どなる",
                "meaning": "to shout angrily; to yell"
            }
        ]
    },
    {
        "kanji": "安",
        "meaning": [
            "cheap; safe; peace"
        ],
        "onyomi": [
            "アン"
        ],
        "kunyomi": [
            "やす.い"
        ],
        "jlpt": "N4",
        "stroke_count": 6,
        "examples": [
            {
                "word": "安全",
                "reading": "あんぜん",
                "meaning": "safety; security"
            },
            {
                "word": "安心",
                "reading": "あんしん",
                "meaning": "relief; peace of mind"
            },
            {
                "word": "不安",
                "reading": "ふあん",
                "meaning": "anxiety; unease"
            }
        ]
    },
    {
        "kanji": "危",
        "meaning": [
            "dangerous; perilous"
        ],
        "onyomi": [
            "キ"
        ],
        "kunyomi": [
            "あぶ.ない",
            "あや.うい"
        ],
        "jlpt": "N4",
        "stroke_count": 6,
        "examples": [
            {
                "word": "危険",
                "reading": "きけん",
                "meaning": "danger; hazard"
            },
            {
                "word": "危機",
                "reading": "きき",
                "meaning": "crisis"
            },
            {
                "word": "危ない",
                "reading": "あぶない",
                "meaning": "dangerous; watch out!"
            }
        ]
    },
    {
        "kanji": "強",
        "meaning": [
            "strong; powerful"
        ],
        "onyomi": [
            "キョウ",
            "ゴウ"
        ],
        "kunyomi": [
            "つよ.い",
            "し.いる"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "強力",
                "reading": "きょうりょく",
                "meaning": "powerful; strong"
            },
            {
                "word": "強調",
                "reading": "きょうちょう",
                "meaning": "emphasis; stress"
            },
            {
                "word": "勉強",
                "reading": "べんきょう",
                "meaning": "study; diligence"
            }
        ]
    },
    {
        "kanji": "弱",
        "meaning": [
            "weak; feeble"
        ],
        "onyomi": [
            "ジャク"
        ],
        "kunyomi": [
            "よわ.い",
            "よわ.まる"
        ],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "弱点",
                "reading": "じゃくてん",
                "meaning": "weak point; weakness"
            },
            {
                "word": "弱気",
                "reading": "よわき",
                "meaning": "weak-minded; bearish"
            },
            {
                "word": "弱める",
                "reading": "よわめる",
                "meaning": "to weaken"
            }
        ]
    },
    {
        "kanji": "深",
        "meaning": [
            "deep; profound"
        ],
        "onyomi": [
            "シン"
        ],
        "kunyomi": [
            "ふか.い",
            "ふか.まる"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "深夜",
                "reading": "しんや",
                "meaning": "late night; midnight"
            },
            {
                "word": "深呼吸",
                "reading": "しんこきゅう",
                "meaning": "deep breath"
            },
            {
                "word": "奥深い",
                "reading": "おくぶかい",
                "meaning": "profound; deep"
            }
        ]
    },
    {
        "kanji": "浅",
        "meaning": [
            "shallow; superficial"
        ],
        "onyomi": [
            "セン"
        ],
        "kunyomi": [
            "あさ.い"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "浅い",
                "reading": "あさい",
                "meaning": "shallow"
            },
            {
                "word": "浅草",
                "reading": "あさくさ",
                "meaning": "Asakusa (place)"
            },
            {
                "word": "浅知恵",
                "reading": "あさぢえ",
                "meaning": "shallow wisdom; superficiality"
            }
        ]
    },
    {
        "kanji": "細",
        "meaning": [
            "thin; narrow; fine; detail"
        ],
        "onyomi": [
            "サイ"
        ],
        "kunyomi": [
            "ほそ.い",
            "こま.かい"
        ],
        "jlpt": "N4",
        "stroke_count": 11,
        "examples": [
            {
                "word": "詳細",
                "reading": "しょうさい",
                "meaning": "details; particulars"
            },
            {
                "word": "細かい",
                "reading": "こまかい",
                "meaning": "fine; detailed; small"
            },
            {
                "word": "繊細",
                "reading": "せんさい",
                "meaning": "delicate; sensitive"
            }
        ]
    },
    {
        "kanji": "太",
        "meaning": [
            "fat; thick; bold"
        ],
        "onyomi": [
            "タイ",
            "タ"
        ],
        "kunyomi": [
            "ふと.い"
        ],
        "jlpt": "N4",
        "stroke_count": 4,
        "examples": [
            {
                "word": "太い",
                "reading": "ふとい",
                "meaning": "thick; fat"
            },
            {
                "word": "太陽",
                "reading": "たいよう",
                "meaning": "sun"
            },
            {
                "word": "丸太",
                "reading": "まるた",
                "meaning": "log; round timber"
            }
        ]
    },
    {
        "kanji": "厚",
        "meaning": [
            "thick; kind; warm"
        ],
        "onyomi": [
            "コウ"
        ],
        "kunyomi": [
            "あつ.い"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "厚い",
                "reading": "あつい",
                "meaning": "thick; generous"
            },
            {
                "word": "厚手",
                "reading": "あつで",
                "meaning": "thick (fabric/material)"
            },
            {
                "word": "親厚",
                "reading": "したあつ",
                "meaning": "close friendship"
            }
        ]
    },
    {
        "kanji": "薄",
        "meaning": [
            "thin; light; pale; weak"
        ],
        "onyomi": [
            "ハク"
        ],
        "kunyomi": [
            "うす.い",
            "うす.める"
        ],
        "jlpt": "N4",
        "stroke_count": 16,
        "examples": [
            {
                "word": "薄い",
                "reading": "うすい",
                "meaning": "thin; pale; light (color)"
            },
            {
                "word": "薄着",
                "reading": "うすぎ",
                "meaning": "wearing light clothing"
            },
            {
                "word": "希薄",
                "reading": "きはく",
                "meaning": "thin; sparse; dilute"
            }
        ]
    },
    {
        "kanji": "丁",
        "meaning": [
            "polite; even number; street block"
        ],
        "onyomi": [
            "テイ",
            "チョウ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 2,
        "examples": [
            {
                "word": "丁寧",
                "reading": "ていねい",
                "meaning": "polite; careful"
            },
            {
                "word": "丁度",
                "reading": "ちょうど",
                "meaning": "just right; exactly"
            },
            {
                "word": "一丁目",
                "reading": "いっちょうめ",
                "meaning": "1st block (address)"
            }
        ]
    },
    {
        "kanji": "寧",
        "meaning": [
            "peaceful; rather; preferably"
        ],
        "onyomi": [
            "ネイ"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 14,
        "examples": [
            {
                "word": "丁寧",
                "reading": "ていねい",
                "meaning": "polite; careful; thorough"
            },
            {
                "word": "安寧",
                "reading": "あんねい",
                "meaning": "peace; public order"
            },
            {
                "word": "寧ろ",
                "reading": "むしろ",
                "meaning": "rather; instead"
            }
        ]
    },
    {
        "kanji": "正",
        "meaning": [
            "correct; right; honest"
        ],
        "onyomi": [
            "セイ",
            "ショウ"
        ],
        "kunyomi": [
            "ただ.しい",
            "まさ"
        ],
        "jlpt": "N4",
        "stroke_count": 5,
        "examples": [
            {
                "word": "正直",
                "reading": "しょうじき",
                "meaning": "honest"
            },
            {
                "word": "正確",
                "reading": "せいかく",
                "meaning": "accurate; exact"
            },
            {
                "word": "正式",
                "reading": "せいしき",
                "meaning": "formal; official"
            }
        ]
    },
    {
        "kanji": "直",
        "meaning": [
            "straight; honest; fix"
        ],
        "onyomi": [
            "チョク",
            "ジキ"
        ],
        "kunyomi": [
            "なお.す",
            "ただ.ちに"
        ],
        "jlpt": "N4",
        "stroke_count": 8,
        "examples": [
            {
                "word": "正直",
                "reading": "しょうじき",
                "meaning": "honest; honesty"
            },
            {
                "word": "直接",
                "reading": "ちょくせつ",
                "meaning": "direct; immediate"
            },
            {
                "word": "素直",
                "reading": "すなお",
                "meaning": "honest; obedient"
            }
        ]
    },
    {
        "kanji": "特",
        "meaning": [
            "special; exceptional"
        ],
        "onyomi": [
            "トク"
        ],
        "kunyomi": [],
        "jlpt": "N4",
        "stroke_count": 10,
        "examples": [
            {
                "word": "特別",
                "reading": "とくべつ",
                "meaning": "special"
            },
            {
                "word": "特に",
                "reading": "とくに",
                "meaning": "especially; particularly"
            },
            {
                "word": "特急",
                "reading": "とっきゅう",
                "meaning": "limited express"
            }
        ]
    },
    {
        "kanji": "自",
        "meaning": [
            "self; oneself; from"
        ],
        "onyomi": [
            "ジ",
            "シ"
        ],
        "kunyomi": [
            "みずか.ら"
        ],
        "jlpt": "N4",
        "stroke_count": 6,
        "examples": [
            {
                "word": "自分",
                "reading": "じぶん",
                "meaning": "oneself"
            },
            {
                "word": "自由",
                "reading": "じゆう",
                "meaning": "freedom; liberty"
            },
            {
                "word": "自然",
                "reading": "しぜん",
                "meaning": "nature; natural"
            }
        ]
    },
    {
        "kanji": "由",
        "meaning": [
            "reason; cause; freedom"
        ],
        "onyomi": [
            "ユウ",
            "ユ",
            "ユイ"
        ],
        "kunyomi": [
            "よし",
            "よ.る"
        ],
        "jlpt": "N4",
        "stroke_count": 5,
        "examples": [
            {
                "word": "自由",
                "reading": "じゆう",
                "meaning": "freedom; liberty"
            },
            {
                "word": "理由",
                "reading": "りゆう",
                "meaning": "reason; cause"
            },
            {
                "word": "由来",
                "reading": "ゆらい",
                "meaning": "origin; history; source"
            }
        ]
    },
    {
        "kanji": "必",
        "meaning": [
            "certainly; inevitable; necessary"
        ],
        "onyomi": [
            "ヒツ"
        ],
        "kunyomi": [
            "かなら.ず"
        ],
        "jlpt": "N4",
        "stroke_count": 5,
        "examples": [
            {
                "word": "必要",
                "reading": "ひつよう",
                "meaning": "necessary; needed"
            },
            {
                "word": "必ず",
                "reading": "かならず",
                "meaning": "certainly; without fail"
            },
            {
                "word": "必死",
                "reading": "ひっし",
                "meaning": "desperate; with all one's might"
            }
        ]
    },
    {
        "kanji": "要",
        "meaning": [
            "need; main point; essential"
        ],
        "onyomi": [
            "ヨウ"
        ],
        "kunyomi": [
            "い.る",
            "かなめ"
        ],
        "jlpt": "N4",
        "stroke_count": 9,
        "examples": [
            {
                "word": "必要",
                "reading": "ひつよう",
                "meaning": "necessary"
            },
            {
                "word": "重要",
                "reading": "じゅうよう",
                "meaning": "important; significant"
            },
            {
                "word": "要求",
                "reading": "ようきゅう",
                "meaning": "demand; requirement"
            }
        ]
    },
    {
        "kanji": "十",
        "meaning": [
            "ten; sufficient; cross"
        ],
        "onyomi": [
            "ジュウ"
        ],
        "kunyomi": [
            "とお"
        ],
        "jlpt": "N4",
        "stroke_count": 2,
        "examples": [
            {
                "word": "十分",
                "reading": "じゅうぶん",
                "meaning": "sufficient; enough"
            },
            {
                "word": "不十分",
                "reading": "ふじゅうぶん",
                "meaning": "insufficient"
            },
            {
                "word": "二十",
                "reading": "にじゅう",
                "meaning": "twenty"
            }
        ]
    },
    {
        "kanji": "分",
        "meaning": [
            "minute; part; understand; divide"
        ],
        "onyomi": [
            "フン",
            "ブン"
        ],
        "kunyomi": [
            "わ.かる",
            "わ.ける"
        ],
        "jlpt": "N4",
        "stroke_count": 4,
        "examples": [
            {
                "word": "十分",
                "reading": "じゅうぶん",
                "meaning": "enough; sufficient"
            },
            {
                "word": "部分",
                "reading": "ぶぶん",
                "meaning": "part; portion"
            },
            {
                "word": "成分",
                "reading": "せいぶん",
                "meaning": "ingredient; component"
            }
        ]
    }
]

VOCABULARY = [
    {
        "expression": "今",
        "reading": "いま",
        "meaning": "now",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "今日",
        "reading": "きょう",
        "meaning": "today",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "明日",
        "reading": "あした",
        "meaning": "tomorrow",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "昨日",
        "reading": "きのう",
        "meaning": "yesterday",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "明後日",
        "reading": "あさって",
        "meaning": "day after tomorrow",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "一昨日",
        "reading": "おととい",
        "meaning": "day before yesterday",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "朝",
        "reading": "あさ",
        "meaning": "morning",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "昼",
        "reading": "ひる",
        "meaning": "noon; daytime",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "夕方",
        "reading": "ゆうがた",
        "meaning": "evening; late afternoon",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "夜",
        "reading": "よる",
        "meaning": "night; evening",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "午前",
        "reading": "ごぜん",
        "meaning": "AM; morning",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "午後",
        "reading": "ごご",
        "meaning": "PM; afternoon",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "時",
        "reading": "じ",
        "meaning": "o'clock (counter for hours)",
        "jlpt": "N5",
        "pos": "counter",
        "category": "time_and_calendar"
    },
    {
        "expression": "分",
        "reading": "ふん／ぷん",
        "meaning": "minute (counter)",
        "jlpt": "N5",
        "pos": "counter",
        "category": "time_and_calendar"
    },
    {
        "expression": "秒",
        "reading": "びょう",
        "meaning": "second (counter)",
        "jlpt": "N5",
        "pos": "counter",
        "category": "time_and_calendar"
    },
    {
        "expression": "半",
        "reading": "はん",
        "meaning": "half; half past",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "今週",
        "reading": "こんしゅう",
        "meaning": "this week",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "来週",
        "reading": "らいしゅう",
        "meaning": "next week",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "先週",
        "reading": "せんしゅう",
        "meaning": "last week",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "今月",
        "reading": "こんげつ",
        "meaning": "this month",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "来月",
        "reading": "らいげつ",
        "meaning": "next month",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "先月",
        "reading": "せんげつ",
        "meaning": "last month",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "今年",
        "reading": "ことし",
        "meaning": "this year",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "来年",
        "reading": "らいねん",
        "meaning": "next year",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "去年",
        "reading": "きょねん",
        "meaning": "last year",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "月曜日",
        "reading": "げつようび",
        "meaning": "Monday",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "火曜日",
        "reading": "かようび",
        "meaning": "Tuesday",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "水曜日",
        "reading": "すいようび",
        "meaning": "Wednesday",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "木曜日",
        "reading": "もくようび",
        "meaning": "Thursday",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "金曜日",
        "reading": "きんようび",
        "meaning": "Friday",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "土曜日",
        "reading": "どようび",
        "meaning": "Saturday",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "日曜日",
        "reading": "にちようび",
        "meaning": "Sunday",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "一月",
        "reading": "いちがつ",
        "meaning": "January",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "二月",
        "reading": "にがつ",
        "meaning": "February",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "三月",
        "reading": "さんがつ",
        "meaning": "March",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "四月",
        "reading": "しがつ",
        "meaning": "April",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "五月",
        "reading": "ごがつ",
        "meaning": "May",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "六月",
        "reading": "ろくがつ",
        "meaning": "June",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "七月",
        "reading": "しちがつ",
        "meaning": "July",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "八月",
        "reading": "はちがつ",
        "meaning": "August",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "九月",
        "reading": "くがつ",
        "meaning": "September",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "十月",
        "reading": "じゅうがつ",
        "meaning": "October",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "十一月",
        "reading": "じゅういちがつ",
        "meaning": "November",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "十二月",
        "reading": "じゅうにがつ",
        "meaning": "December",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "春",
        "reading": "はる",
        "meaning": "spring",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "夏",
        "reading": "なつ",
        "meaning": "summer",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "秋",
        "reading": "あき",
        "meaning": "autumn; fall",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "冬",
        "reading": "ふゆ",
        "meaning": "winter",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "週末",
        "reading": "しゅうまつ",
        "meaning": "weekend",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "毎日",
        "reading": "まいにち",
        "meaning": "every day",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "毎週",
        "reading": "まいしゅう",
        "meaning": "every week",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "毎年",
        "reading": "まいとし",
        "meaning": "every year",
        "jlpt": "N5",
        "pos": "noun",
        "category": "time_and_calendar"
    },
    {
        "expression": "一",
        "reading": "いち",
        "meaning": "one",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "二",
        "reading": "に",
        "meaning": "two",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "三",
        "reading": "さん",
        "meaning": "three",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "四",
        "reading": "し／よん",
        "meaning": "four",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "五",
        "reading": "ご",
        "meaning": "five",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "六",
        "reading": "ろく",
        "meaning": "six",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "七",
        "reading": "しち／なな",
        "meaning": "seven",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "八",
        "reading": "はち",
        "meaning": "eight",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "九",
        "reading": "く／きゅう",
        "meaning": "nine",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "十",
        "reading": "じゅう",
        "meaning": "ten",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "百",
        "reading": "ひゃく",
        "meaning": "hundred",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "千",
        "reading": "せん",
        "meaning": "thousand",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "万",
        "reading": "まん",
        "meaning": "ten thousand",
        "jlpt": "N5",
        "pos": "noun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "何",
        "reading": "なん／なに",
        "meaning": "what; how many",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜つ",
        "reading": "〜つ",
        "meaning": "general counter (1-9 things)",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜本",
        "reading": "〜ほん",
        "meaning": "counter for long thin objects",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜枚",
        "reading": "〜まい",
        "meaning": "counter for flat objects",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜台",
        "reading": "〜だい",
        "meaning": "counter for machines/vehicles",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜冊",
        "reading": "〜さつ",
        "meaning": "counter for books",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜匹",
        "reading": "〜ひき",
        "meaning": "counter for small animals",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜頭",
        "reading": "〜とう",
        "meaning": "counter for large animals",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜人",
        "reading": "〜にん",
        "meaning": "counter for people",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜番",
        "reading": "〜ばん",
        "meaning": "number ~; counter for order/rank",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜階",
        "reading": "〜かい",
        "meaning": "counter for floors of a building",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜個",
        "reading": "〜こ",
        "meaning": "counter for small objects",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "〜杯",
        "reading": "〜はい",
        "meaning": "counter for cups/bowls",
        "jlpt": "N5",
        "pos": "counter",
        "category": "numbers_and_counting"
    },
    {
        "expression": "おはようございます",
        "reading": "おはようございます",
        "meaning": "Good morning (polite)",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "おはよう",
        "reading": "おはよう",
        "meaning": "Good morning (casual)",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "こんにちは",
        "reading": "こんにちは",
        "meaning": "Hello; Good afternoon",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "こんばんは",
        "reading": "こんばんは",
        "meaning": "Good evening",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "さようなら",
        "reading": "さようなら",
        "meaning": "Goodbye (formal)",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "じゃ（また）",
        "reading": "じゃ（また）",
        "meaning": "See you (casual)",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "ありがとうございます",
        "reading": "ありがとうございます",
        "meaning": "Thank you (polite)",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "すみません",
        "reading": "すみません",
        "meaning": "Excuse me; I'm sorry",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "ごめんなさい",
        "reading": "ごめんなさい",
        "meaning": "I'm sorry",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "はい",
        "reading": "はい",
        "meaning": "Yes",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "いいえ",
        "reading": "いいえ",
        "meaning": "No",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "どうぞ",
        "reading": "どうぞ",
        "meaning": "Please; Here you go",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "どうも",
        "reading": "どうも",
        "meaning": "Thanks; somehow",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "いただきます",
        "reading": "いただきます",
        "meaning": "Expression before eating",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "ごちそうさまでした",
        "reading": "ごちそうさまでした",
        "meaning": "Expression after eating",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "よろしくお願いします",
        "reading": "よろしくおねがいします",
        "meaning": "Nice to meet you; please treat me well",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "はじめまして",
        "reading": "はじめまして",
        "meaning": "Nice to meet you (first time)",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "もしもし",
        "reading": "もしもし",
        "meaning": "Hello (telephone)",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "ちょっと",
        "reading": "ちょっと",
        "meaning": "A little; Hey (calling attention)",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "そうですね",
        "reading": "そうですね",
        "meaning": "That's right; I see",
        "jlpt": "N5",
        "pos": "expression",
        "category": "greetings_and_expressions"
    },
    {
        "expression": "人",
        "reading": "ひと",
        "meaning": "person; people",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "私",
        "reading": "わたし",
        "meaning": "I; me",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "people_and_family"
    },
    {
        "expression": "あなた",
        "reading": "あなた",
        "meaning": "you",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "people_and_family"
    },
    {
        "expression": "彼",
        "reading": "かれ",
        "meaning": "he; him; boyfriend",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "people_and_family"
    },
    {
        "expression": "彼女",
        "reading": "かのじょ",
        "meaning": "she; her; girlfriend",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "people_and_family"
    },
    {
        "expression": "家族",
        "reading": "かぞく",
        "meaning": "family",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "父",
        "reading": "ちち",
        "meaning": "(my) father",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "母",
        "reading": "はは",
        "meaning": "(my) mother",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "お父さん",
        "reading": "おとうさん",
        "meaning": "father (someone else's; polite)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "お母さん",
        "reading": "おかあさん",
        "meaning": "mother (someone else's; polite)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "兄",
        "reading": "あに",
        "meaning": "(my) older brother",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "姉",
        "reading": "あね",
        "meaning": "(my) older sister",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "お兄さん",
        "reading": "おにいさん",
        "meaning": "older brother (polite)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "お姉さん",
        "reading": "おねえさん",
        "meaning": "older sister (polite)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "弟",
        "reading": "おとうと",
        "meaning": "younger brother",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "妹",
        "reading": "いもうと",
        "meaning": "younger sister",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "子供",
        "reading": "こども",
        "meaning": "child; children",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "男",
        "reading": "おとこ",
        "meaning": "man; male",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "女",
        "reading": "おんな",
        "meaning": "woman; female",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "男の子",
        "reading": "おとこのこ",
        "meaning": "boy",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "女の子",
        "reading": "おんなのこ",
        "meaning": "girl",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "友達",
        "reading": "ともだち",
        "meaning": "friend",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "先生",
        "reading": "せんせい",
        "meaning": "teacher",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "学生",
        "reading": "がくせい",
        "meaning": "student",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "みんな",
        "reading": "みんな",
        "meaning": "everyone; all",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "祖父",
        "reading": "そふ",
        "meaning": "(my) grandfather",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "祖母",
        "reading": "そぼ",
        "meaning": "(my) grandmother",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "おじいさん",
        "reading": "おじいさん",
        "meaning": "grandfather; old man",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "おばあさん",
        "reading": "おばあさん",
        "meaning": "grandmother; old woman",
        "jlpt": "N5",
        "pos": "noun",
        "category": "people_and_family"
    },
    {
        "expression": "体",
        "reading": "からだ",
        "meaning": "body",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "頭",
        "reading": "あたま",
        "meaning": "head",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "顔",
        "reading": "かお",
        "meaning": "face",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "目",
        "reading": "め",
        "meaning": "eye(s)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "耳",
        "reading": "みみ",
        "meaning": "ear(s)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "口",
        "reading": "くち",
        "meaning": "mouth",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "鼻",
        "reading": "はな",
        "meaning": "nose",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "歯",
        "reading": "は",
        "meaning": "tooth; teeth",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "手",
        "reading": "て",
        "meaning": "hand",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "足",
        "reading": "あし",
        "meaning": "foot; leg",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "腕",
        "reading": "うで",
        "meaning": "arm",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "背中",
        "reading": "せなか",
        "meaning": "back (of body)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "お腹",
        "reading": "おなか",
        "meaning": "stomach; belly",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "心",
        "reading": "こころ",
        "meaning": "heart; mind",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "病気",
        "reading": "びょうき",
        "meaning": "illness; disease",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "薬",
        "reading": "くすり",
        "meaning": "medicine",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "病院",
        "reading": "びょういん",
        "meaning": "hospital",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "医者",
        "reading": "いしゃ",
        "meaning": "doctor",
        "jlpt": "N5",
        "pos": "noun",
        "category": "body_and_health"
    },
    {
        "expression": "痛い",
        "reading": "いたい",
        "meaning": "painful; sore",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "body_and_health"
    },
    {
        "expression": "元気",
        "reading": "げんき",
        "meaning": "healthy; energetic; fine",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "body_and_health"
    },
    {
        "expression": "ご飯",
        "reading": "ごはん",
        "meaning": "rice (cooked); meal",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "パン",
        "reading": "パン",
        "meaning": "bread",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "肉",
        "reading": "にく",
        "meaning": "meat",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "魚",
        "reading": "さかな",
        "meaning": "fish",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "野菜",
        "reading": "やさい",
        "meaning": "vegetables",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "果物",
        "reading": "くだもの",
        "meaning": "fruit",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "卵",
        "reading": "たまご",
        "meaning": "egg",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "牛乳",
        "reading": "ぎゅうにゅう",
        "meaning": "milk",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "水",
        "reading": "みず",
        "meaning": "water",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "お茶",
        "reading": "おちゃ",
        "meaning": "tea (green tea)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "コーヒー",
        "reading": "コーヒー",
        "meaning": "coffee",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "ジュース",
        "reading": "ジュース",
        "meaning": "juice",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "ビール",
        "reading": "ビール",
        "meaning": "beer",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "酒",
        "reading": "さけ",
        "meaning": "sake; alcohol",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "砂糖",
        "reading": "さとう",
        "meaning": "sugar",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "塩",
        "reading": "しお",
        "meaning": "salt",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "醤油",
        "reading": "しょうゆ",
        "meaning": "soy sauce",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "スープ",
        "reading": "スープ",
        "meaning": "soup",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "ケーキ",
        "reading": "ケーキ",
        "meaning": "cake",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "お菓子",
        "reading": "おかし",
        "meaning": "sweets; snacks",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "弁当",
        "reading": "べんとう",
        "meaning": "bento box; packed lunch",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "朝ご飯",
        "reading": "あさごはん",
        "meaning": "breakfast",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "昼ご飯",
        "reading": "ひるごはん",
        "meaning": "lunch",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "夕ご飯",
        "reading": "ゆうごはん",
        "meaning": "dinner; supper",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "牛肉",
        "reading": "ぎゅうにく",
        "meaning": "beef",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "鶏肉",
        "reading": "とりにく",
        "meaning": "chicken (meat)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "豚肉",
        "reading": "ぶたにく",
        "meaning": "pork",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "りんご",
        "reading": "りんご",
        "meaning": "apple",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "みかん",
        "reading": "みかん",
        "meaning": "mandarin orange",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "バナナ",
        "reading": "バナナ",
        "meaning": "banana",
        "jlpt": "N5",
        "pos": "noun",
        "category": "food_and_drink"
    },
    {
        "expression": "家",
        "reading": "いえ",
        "meaning": "house; home",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "部屋",
        "reading": "へや",
        "meaning": "room",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "台所",
        "reading": "だいどころ",
        "meaning": "kitchen",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "お風呂",
        "reading": "おふろ",
        "meaning": "bath; bathtub",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "トイレ",
        "reading": "トイレ",
        "meaning": "toilet; restroom",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "玄関",
        "reading": "げんかん",
        "meaning": "entrance hall; foyer",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "窓",
        "reading": "まど",
        "meaning": "window",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "ドア",
        "reading": "ドア",
        "meaning": "door",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "机",
        "reading": "つくえ",
        "meaning": "desk",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "椅子",
        "reading": "いす",
        "meaning": "chair",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "テーブル",
        "reading": "テーブル",
        "meaning": "table",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "ベッド",
        "reading": "ベッド",
        "meaning": "bed",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "冷蔵庫",
        "reading": "れいぞうこ",
        "meaning": "refrigerator",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "電子レンジ",
        "reading": "でんしレンジ",
        "meaning": "microwave oven",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "茶碗",
        "reading": "ちゃわん",
        "meaning": "rice bowl; teacup",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "お皿",
        "reading": "おさら",
        "meaning": "plate; dish",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "コップ",
        "reading": "コップ",
        "meaning": "cup; glass",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "箸",
        "reading": "はし",
        "meaning": "chopsticks",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "フォーク",
        "reading": "フォーク",
        "meaning": "fork",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "スプーン",
        "reading": "スプーン",
        "meaning": "spoon",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "花瓶",
        "reading": "かびん",
        "meaning": "flower vase",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "鍵",
        "reading": "かぎ",
        "meaning": "key; lock",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "電気",
        "reading": "でんき",
        "meaning": "electricity; light",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "テレビ",
        "reading": "テレビ",
        "meaning": "television",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "電話",
        "reading": "でんわ",
        "meaning": "telephone",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "時計",
        "reading": "とけい",
        "meaning": "clock; watch",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "カメラ",
        "reading": "カメラ",
        "meaning": "camera",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "本棚",
        "reading": "ほんだな",
        "meaning": "bookshelf",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "財布",
        "reading": "さいふ",
        "meaning": "wallet; purse",
        "jlpt": "N5",
        "pos": "noun",
        "category": "home_and_kitchen"
    },
    {
        "expression": "服",
        "reading": "ふく",
        "meaning": "clothes",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "シャツ",
        "reading": "シャツ",
        "meaning": "shirt",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "ズボン",
        "reading": "ズボン",
        "meaning": "trousers; pants",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "スカート",
        "reading": "スカート",
        "meaning": "skirt",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "コート",
        "reading": "コート",
        "meaning": "coat",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "靴",
        "reading": "くつ",
        "meaning": "shoes",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "靴下",
        "reading": "くつした",
        "meaning": "socks",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "帽子",
        "reading": "ぼうし",
        "meaning": "hat; cap",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "眼鏡",
        "reading": "めがね",
        "meaning": "glasses; spectacles",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "かばん",
        "reading": "かばん",
        "meaning": "bag; briefcase",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "着物",
        "reading": "きもの",
        "meaning": "kimono; traditional garment",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "色",
        "reading": "いろ",
        "meaning": "color",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "赤",
        "reading": "あか",
        "meaning": "red",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "青",
        "reading": "あお",
        "meaning": "blue; green",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "白",
        "reading": "しろ",
        "meaning": "white",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "黒",
        "reading": "くろ",
        "meaning": "black",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "黄色",
        "reading": "きいろ",
        "meaning": "yellow",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "緑",
        "reading": "みどり",
        "meaning": "green",
        "jlpt": "N5",
        "pos": "noun",
        "category": "clothing_and_appearance"
    },
    {
        "expression": "学校",
        "reading": "がっこう",
        "meaning": "school",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "大学",
        "reading": "だいがく",
        "meaning": "university",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "高校",
        "reading": "こうこう",
        "meaning": "high school",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "教室",
        "reading": "きょうしつ",
        "meaning": "classroom",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "図書館",
        "reading": "としょかん",
        "meaning": "library",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "本",
        "reading": "ほん",
        "meaning": "book",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "雑誌",
        "reading": "ざっし",
        "meaning": "magazine",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "新聞",
        "reading": "しんぶん",
        "meaning": "newspaper",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "ノート",
        "reading": "ノート",
        "meaning": "notebook",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "鉛筆",
        "reading": "えんぴつ",
        "meaning": "pencil",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "ペン",
        "reading": "ペン",
        "meaning": "pen",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "紙",
        "reading": "かみ",
        "meaning": "paper",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "授業",
        "reading": "じゅぎょう",
        "meaning": "class; lesson",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "試験",
        "reading": "しけん",
        "meaning": "exam; test",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "宿題",
        "reading": "しゅくだい",
        "meaning": "homework",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "質問",
        "reading": "しつもん",
        "meaning": "question",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "答え",
        "reading": "こたえ",
        "meaning": "answer",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "言葉",
        "reading": "ことば",
        "meaning": "word; language",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "日本語",
        "reading": "にほんご",
        "meaning": "Japanese language",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "英語",
        "reading": "えいご",
        "meaning": "English language",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "漢字",
        "reading": "かんじ",
        "meaning": "kanji characters",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "ひらがな",
        "reading": "ひらがな",
        "meaning": "hiragana script",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "カタカナ",
        "reading": "カタカナ",
        "meaning": "katakana script",
        "jlpt": "N5",
        "pos": "noun",
        "category": "school_and_education"
    },
    {
        "expression": "仕事",
        "reading": "しごと",
        "meaning": "work; job",
        "jlpt": "N5",
        "pos": "noun",
        "category": "work_and_business"
    },
    {
        "expression": "会社",
        "reading": "かいしゃ",
        "meaning": "company; office",
        "jlpt": "N5",
        "pos": "noun",
        "category": "work_and_business"
    },
    {
        "expression": "会社員",
        "reading": "かいしゃいん",
        "meaning": "company employee",
        "jlpt": "N5",
        "pos": "noun",
        "category": "work_and_business"
    },
    {
        "expression": "社長",
        "reading": "しゃちょう",
        "meaning": "company president; CEO",
        "jlpt": "N5",
        "pos": "noun",
        "category": "work_and_business"
    },
    {
        "expression": "電話",
        "reading": "でんわ",
        "meaning": "telephone",
        "jlpt": "N5",
        "pos": "noun",
        "category": "work_and_business"
    },
    {
        "expression": "お金",
        "reading": "おかね",
        "meaning": "money",
        "jlpt": "N5",
        "pos": "noun",
        "category": "work_and_business"
    },
    {
        "expression": "アルバイト",
        "reading": "アルバイト",
        "meaning": "part-time job",
        "jlpt": "N5",
        "pos": "noun",
        "category": "work_and_business"
    },
    {
        "expression": "郵便局",
        "reading": "ゆうびんきょく",
        "meaning": "post office",
        "jlpt": "N5",
        "pos": "noun",
        "category": "work_and_business"
    },
    {
        "expression": "店",
        "reading": "みせ",
        "meaning": "shop; store",
        "jlpt": "N5",
        "pos": "noun",
        "category": "shopping_and_money"
    },
    {
        "expression": "デパート",
        "reading": "デパート",
        "meaning": "department store",
        "jlpt": "N5",
        "pos": "noun",
        "category": "shopping_and_money"
    },
    {
        "expression": "スーパー",
        "reading": "スーパー",
        "meaning": "supermarket",
        "jlpt": "N5",
        "pos": "noun",
        "category": "shopping_and_money"
    },
    {
        "expression": "値段",
        "reading": "ねだん",
        "meaning": "price",
        "jlpt": "N5",
        "pos": "noun",
        "category": "shopping_and_money"
    },
    {
        "expression": "円",
        "reading": "えん",
        "meaning": "yen (Japanese currency)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "shopping_and_money"
    },
    {
        "expression": "いくら",
        "reading": "いくら",
        "meaning": "how much",
        "jlpt": "N5",
        "pos": "noun",
        "category": "shopping_and_money"
    },
    {
        "expression": "高い",
        "reading": "たかい",
        "meaning": "expensive; high",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "shopping_and_money"
    },
    {
        "expression": "安い",
        "reading": "やすい",
        "meaning": "cheap; inexpensive",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "shopping_and_money"
    },
    {
        "expression": "レジ",
        "reading": "レジ",
        "meaning": "cash register; checkout",
        "jlpt": "N5",
        "pos": "noun",
        "category": "shopping_and_money"
    },
    {
        "expression": "おつり",
        "reading": "おつり",
        "meaning": "change (money returned)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "shopping_and_money"
    },
    {
        "expression": "切手",
        "reading": "きって",
        "meaning": "postage stamp",
        "jlpt": "N5",
        "pos": "noun",
        "category": "shopping_and_money"
    },
    {
        "expression": "切符",
        "reading": "きっぷ",
        "meaning": "ticket",
        "jlpt": "N5",
        "pos": "noun",
        "category": "shopping_and_money"
    },
    {
        "expression": "電車",
        "reading": "でんしゃ",
        "meaning": "train; electric train",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "バス",
        "reading": "バス",
        "meaning": "bus",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "地下鉄",
        "reading": "ちかてつ",
        "meaning": "subway; metro",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "タクシー",
        "reading": "タクシー",
        "meaning": "taxi",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "自転車",
        "reading": "じてんしゃ",
        "meaning": "bicycle",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "車",
        "reading": "くるま",
        "meaning": "car; vehicle",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "飛行機",
        "reading": "ひこうき",
        "meaning": "airplane",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "船",
        "reading": "ふね",
        "meaning": "ship; boat",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "駅",
        "reading": "えき",
        "meaning": "station",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "空港",
        "reading": "くうこう",
        "meaning": "airport",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "道",
        "reading": "みち",
        "meaning": "road; path; way",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "信号",
        "reading": "しんごう",
        "meaning": "traffic light; signal",
        "jlpt": "N5",
        "pos": "noun",
        "category": "transportation"
    },
    {
        "expression": "天気",
        "reading": "てんき",
        "meaning": "weather",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "晴れ",
        "reading": "はれ",
        "meaning": "clear weather; sunny",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "雨",
        "reading": "あめ",
        "meaning": "rain",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "雪",
        "reading": "ゆき",
        "meaning": "snow",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "曇り",
        "reading": "くもり",
        "meaning": "cloudy weather",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "風",
        "reading": "かぜ",
        "meaning": "wind",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "空",
        "reading": "そら",
        "meaning": "sky",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "太陽",
        "reading": "たいよう",
        "meaning": "sun",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "月",
        "reading": "つき",
        "meaning": "moon; month",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "星",
        "reading": "ほし",
        "meaning": "star",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "山",
        "reading": "やま",
        "meaning": "mountain",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "川",
        "reading": "かわ",
        "meaning": "river",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "海",
        "reading": "うみ",
        "meaning": "sea; ocean",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "池",
        "reading": "いけ",
        "meaning": "pond",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "木",
        "reading": "き",
        "meaning": "tree",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "花",
        "reading": "はな",
        "meaning": "flower",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "動物",
        "reading": "どうぶつ",
        "meaning": "animal",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "犬",
        "reading": "いぬ",
        "meaning": "dog",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "猫",
        "reading": "ねこ",
        "meaning": "cat",
        "jlpt": "N5",
        "pos": "noun",
        "category": "nature_and_weather"
    },
    {
        "expression": "ここ",
        "reading": "ここ",
        "meaning": "here; this place",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "location_and_direction"
    },
    {
        "expression": "そこ",
        "reading": "そこ",
        "meaning": "there; that place",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "location_and_direction"
    },
    {
        "expression": "あそこ",
        "reading": "あそこ",
        "meaning": "over there; that place (far)",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "location_and_direction"
    },
    {
        "expression": "どこ",
        "reading": "どこ",
        "meaning": "where",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "location_and_direction"
    },
    {
        "expression": "右",
        "reading": "みぎ",
        "meaning": "right (direction)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "左",
        "reading": "ひだり",
        "meaning": "left (direction)",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "前",
        "reading": "まえ",
        "meaning": "front; before",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "後ろ",
        "reading": "うしろ",
        "meaning": "behind; back",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "上",
        "reading": "うえ",
        "meaning": "above; on top",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "下",
        "reading": "した",
        "meaning": "below; under",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "中",
        "reading": "なか",
        "meaning": "inside; middle",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "外",
        "reading": "そと",
        "meaning": "outside",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "横",
        "reading": "よこ",
        "meaning": "beside; side",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "隣",
        "reading": "となり",
        "meaning": "next to; neighboring",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "近く",
        "reading": "ちかく",
        "meaning": "nearby; close",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "遠く",
        "reading": "とおく",
        "meaning": "far away; distant",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "東",
        "reading": "ひがし",
        "meaning": "east",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "西",
        "reading": "にし",
        "meaning": "west",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "南",
        "reading": "みなみ",
        "meaning": "south",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "北",
        "reading": "きた",
        "meaning": "north",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "日本",
        "reading": "にほん",
        "meaning": "Japan",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "東京",
        "reading": "とうきょう",
        "meaning": "Tokyo",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "公園",
        "reading": "こうえん",
        "meaning": "park",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "銀行",
        "reading": "ぎんこう",
        "meaning": "bank",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "病院",
        "reading": "びょういん",
        "meaning": "hospital",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "レストラン",
        "reading": "レストラン",
        "meaning": "restaurant",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "喫茶店",
        "reading": "きっさてん",
        "meaning": "café; coffee shop",
        "jlpt": "N5",
        "pos": "noun",
        "category": "location_and_direction"
    },
    {
        "expression": "行く",
        "reading": "いく",
        "meaning": "to go",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "来る",
        "reading": "くる",
        "meaning": "to come",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "帰る",
        "reading": "かえる",
        "meaning": "to return; to go home",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "乗る",
        "reading": "のる",
        "meaning": "to ride; to get on",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "降りる",
        "reading": "おりる",
        "meaning": "to get off; to descend",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "歩く",
        "reading": "あるく",
        "meaning": "to walk",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "走る",
        "reading": "はしる",
        "meaning": "to run",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "止まる",
        "reading": "とまる",
        "meaning": "to stop; to come to a halt",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "入る",
        "reading": "はいる",
        "meaning": "to enter; to go into",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "出る",
        "reading": "でる",
        "meaning": "to exit; to leave; to come out",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "上がる",
        "reading": "あがる",
        "meaning": "to go up; to rise",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "下がる",
        "reading": "さがる",
        "meaning": "to go down; to fall",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "曲がる",
        "reading": "まがる",
        "meaning": "to turn; to curve",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "渡る",
        "reading": "わたる",
        "meaning": "to cross; to go across",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_motion"
    },
    {
        "expression": "食べる",
        "reading": "たべる",
        "meaning": "to eat",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "飲む",
        "reading": "のむ",
        "meaning": "to drink",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "見る",
        "reading": "みる",
        "meaning": "to see; to watch; to look",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "聞く",
        "reading": "きく",
        "meaning": "to listen; to hear; to ask",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "話す",
        "reading": "はなす",
        "meaning": "to speak; to talk",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "読む",
        "reading": "よむ",
        "meaning": "to read",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "書く",
        "reading": "かく",
        "meaning": "to write",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "買う",
        "reading": "かう",
        "meaning": "to buy",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "売る",
        "reading": "うる",
        "meaning": "to sell",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "使う",
        "reading": "つかう",
        "meaning": "to use",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "作る",
        "reading": "つくる",
        "meaning": "to make; to create",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "着る",
        "reading": "きる",
        "meaning": "to wear (clothing)",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "起きる",
        "reading": "おきる",
        "meaning": "to wake up; to get up",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "寝る",
        "reading": "ねる",
        "meaning": "to sleep; to go to bed",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "休む",
        "reading": "やすむ",
        "meaning": "to rest; to take a break",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "働く",
        "reading": "はたらく",
        "meaning": "to work",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "勉強する",
        "reading": "べんきょうする",
        "meaning": "to study",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "練習する",
        "reading": "れんしゅうする",
        "meaning": "to practice",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "洗う",
        "reading": "あらう",
        "meaning": "to wash",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "掃除する",
        "reading": "そうじする",
        "meaning": "to clean; to sweep",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "開ける",
        "reading": "あける",
        "meaning": "to open (something)",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "閉める",
        "reading": "しめる",
        "meaning": "to close (something)",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "切る",
        "reading": "きる",
        "meaning": "to cut",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "貸す",
        "reading": "かす",
        "meaning": "to lend",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "借りる",
        "reading": "かりる",
        "meaning": "to borrow; to rent",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "あげる",
        "reading": "あげる",
        "meaning": "to give (to others)",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "もらう",
        "reading": "もらう",
        "meaning": "to receive; to get",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "持つ",
        "reading": "もつ",
        "meaning": "to hold; to carry; to have",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "待つ",
        "reading": "まつ",
        "meaning": "to wait",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "会う",
        "reading": "あう",
        "meaning": "to meet",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "遊ぶ",
        "reading": "あそぶ",
        "meaning": "to play; to hang out",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_daily_actions"
    },
    {
        "expression": "ある",
        "reading": "ある",
        "meaning": "to exist; to be (inanimate)",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "いる",
        "reading": "いる",
        "meaning": "to exist; to be (animate)",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "する",
        "reading": "する",
        "meaning": "to do",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "なる",
        "reading": "なる",
        "meaning": "to become",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "わかる",
        "reading": "わかる",
        "meaning": "to understand",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "知る",
        "reading": "しる",
        "meaning": "to know",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "思う",
        "reading": "おもう",
        "meaning": "to think; to feel",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "好き",
        "reading": "すき",
        "meaning": "to like (な-adj)",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "嫌い",
        "reading": "きらい",
        "meaning": "to dislike (な-adj)",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "できる",
        "reading": "できる",
        "meaning": "to be able to; to be completed",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "忘れる",
        "reading": "わすれる",
        "meaning": "to forget",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "覚える",
        "reading": "おぼえる",
        "meaning": "to remember; to memorize",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "始まる",
        "reading": "はじまる",
        "meaning": "to begin; to start (intransitive)",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "終わる",
        "reading": "おわる",
        "meaning": "to end; to finish (intransitive)",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "死ぬ",
        "reading": "しぬ",
        "meaning": "to die",
        "jlpt": "N5",
        "pos": "verb",
        "category": "verbs_state_and_change"
    },
    {
        "expression": "大きい",
        "reading": "おおきい",
        "meaning": "big; large",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "小さい",
        "reading": "ちいさい",
        "meaning": "small; little",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "長い",
        "reading": "ながい",
        "meaning": "long",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "短い",
        "reading": "みじかい",
        "meaning": "short",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "高い",
        "reading": "たかい",
        "meaning": "tall; high; expensive",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "低い",
        "reading": "ひくい",
        "meaning": "low; short (height)",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "広い",
        "reading": "ひろい",
        "meaning": "wide; spacious",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "狭い",
        "reading": "せまい",
        "meaning": "narrow; cramped",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "新しい",
        "reading": "あたらしい",
        "meaning": "new",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "古い",
        "reading": "ふるい",
        "meaning": "old (objects)",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "若い",
        "reading": "わかい",
        "meaning": "young",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "多い",
        "reading": "おおい",
        "meaning": "many; much; a lot",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "少ない",
        "reading": "すくない",
        "meaning": "few; little",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "良い",
        "reading": "いい／よい",
        "meaning": "good",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "悪い",
        "reading": "わるい",
        "meaning": "bad",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "面白い",
        "reading": "おもしろい",
        "meaning": "interesting; funny",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "つまらない",
        "reading": "つまらない",
        "meaning": "boring; dull",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "難しい",
        "reading": "むずかしい",
        "meaning": "difficult",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "易しい",
        "reading": "やさしい",
        "meaning": "easy",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "楽しい",
        "reading": "たのしい",
        "meaning": "fun; enjoyable",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "嬉しい",
        "reading": "うれしい",
        "meaning": "happy; glad",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "悲しい",
        "reading": "かなしい",
        "meaning": "sad",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "暑い",
        "reading": "あつい",
        "meaning": "hot (weather)",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "寒い",
        "reading": "さむい",
        "meaning": "cold (weather)",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "暖かい",
        "reading": "あたたかい",
        "meaning": "warm",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "涼しい",
        "reading": "すずしい",
        "meaning": "cool; refreshing",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "熱い",
        "reading": "あつい",
        "meaning": "hot (to the touch)",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "冷たい",
        "reading": "つめたい",
        "meaning": "cold (to the touch)",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "重い",
        "reading": "おもい",
        "meaning": "heavy",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "軽い",
        "reading": "かるい",
        "meaning": "light (weight)",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "速い",
        "reading": "はやい",
        "meaning": "fast; quick",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "遅い",
        "reading": "おそい",
        "meaning": "slow; late",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "早い",
        "reading": "はやい",
        "meaning": "early",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "忙しい",
        "reading": "いそがしい",
        "meaning": "busy",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "美しい",
        "reading": "うつくしい",
        "meaning": "beautiful",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "白い",
        "reading": "しろい",
        "meaning": "white",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "黒い",
        "reading": "くろい",
        "meaning": "black",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "赤い",
        "reading": "あかい",
        "meaning": "red",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "青い",
        "reading": "あおい",
        "meaning": "blue; green",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "黄色い",
        "reading": "きいろい",
        "meaning": "yellow",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "丸い",
        "reading": "まるい",
        "meaning": "round; circular",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "正しい",
        "reading": "ただしい",
        "meaning": "correct; right",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "欲しい",
        "reading": "ほしい",
        "meaning": "wanted; desired",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "甘い",
        "reading": "あまい",
        "meaning": "sweet",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "辛い",
        "reading": "からい",
        "meaning": "spicy; hot",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "美味しい",
        "reading": "おいしい",
        "meaning": "delicious; tasty",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "まずい",
        "reading": "まずい",
        "meaning": "bad tasting; unpleasant",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "明るい",
        "reading": "あかるい",
        "meaning": "bright; cheerful",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "暗い",
        "reading": "くらい",
        "meaning": "dark; gloomy",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "近い",
        "reading": "ちかい",
        "meaning": "near; close",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "遠い",
        "reading": "とおい",
        "meaning": "far; distant",
        "jlpt": "N5",
        "pos": "i-adj",
        "category": "adjectives_i"
    },
    {
        "expression": "きれい",
        "reading": "きれい",
        "meaning": "pretty; clean",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "有名",
        "reading": "ゆうめい",
        "meaning": "famous",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "大切",
        "reading": "たいせつ",
        "meaning": "important; precious",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "大丈夫",
        "reading": "だいじょうぶ",
        "meaning": "OK; all right; safe",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "上手",
        "reading": "じょうず",
        "meaning": "skilled; good at",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "下手",
        "reading": "へた",
        "meaning": "unskilled; poor at",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "得意",
        "reading": "とくい",
        "meaning": "good at; one's strong point",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "苦手",
        "reading": "にがて",
        "meaning": "bad at; weak point",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "静か",
        "reading": "しずか",
        "meaning": "quiet; calm",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "賑やか",
        "reading": "にぎやか",
        "meaning": "lively; bustling",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "親切",
        "reading": "しんせつ",
        "meaning": "kind; gentle",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "丁寧",
        "reading": "ていねい",
        "meaning": "polite; courteous",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "暇",
        "reading": "ひま",
        "meaning": "free time; not busy",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "便利",
        "reading": "べんり",
        "meaning": "convenient; handy",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "不便",
        "reading": "ふべん",
        "meaning": "inconvenient",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "必要",
        "reading": "ひつよう",
        "meaning": "necessary; needed",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "大変",
        "reading": "たいへん",
        "meaning": "tough; difficult; very",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "好き",
        "reading": "すき",
        "meaning": "like; fond of",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "嫌い",
        "reading": "きらい",
        "meaning": "dislike; hate",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "元気",
        "reading": "げんき",
        "meaning": "healthy; energetic",
        "jlpt": "N5",
        "pos": "na-adj",
        "category": "adjectives_na"
    },
    {
        "expression": "とても",
        "reading": "とても",
        "meaning": "very; extremely",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "すごく",
        "reading": "すごく",
        "meaning": "very; amazingly (casual)",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "もっと",
        "reading": "もっと",
        "meaning": "more",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "もう",
        "reading": "もう",
        "meaning": "already; anymore",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "まだ",
        "reading": "まだ",
        "meaning": "still; not yet",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "また",
        "reading": "また",
        "meaning": "again; also",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "ちょっと",
        "reading": "ちょっと",
        "meaning": "a little; just a moment",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "少し",
        "reading": "すこし",
        "meaning": "a little; a few",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "たくさん",
        "reading": "たくさん",
        "meaning": "many; a lot; plenty",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "いつも",
        "reading": "いつも",
        "meaning": "always; usually",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "時々",
        "reading": "ときどき",
        "meaning": "sometimes",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "たまに",
        "reading": "たまに",
        "meaning": "occasionally; once in a while",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "全然",
        "reading": "ぜんぜん",
        "meaning": "not at all (with negative)",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "あまり",
        "reading": "あまり",
        "meaning": "not very (with negative)",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "もちろん",
        "reading": "もちろん",
        "meaning": "of course",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "一緒に",
        "reading": "いっしょに",
        "meaning": "together",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "一人で",
        "reading": "ひとりで",
        "meaning": "alone; by oneself",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "早く",
        "reading": "はやく",
        "meaning": "quickly; early",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "ゆっくり",
        "reading": "ゆっくり",
        "meaning": "slowly; leisurely",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "まっすぐ",
        "reading": "まっすぐ",
        "meaning": "straight ahead; directly",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "だいたい",
        "reading": "だいたい",
        "meaning": "generally; mostly; about",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "どうして",
        "reading": "どうして",
        "meaning": "why; how come",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "どのくらい",
        "reading": "どのくらい",
        "meaning": "how long; how much; how far",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "はじめて",
        "reading": "はじめて",
        "meaning": "for the first time",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "adverbs_and_degree"
    },
    {
        "expression": "これ",
        "reading": "これ",
        "meaning": "this (thing near speaker)",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "communication"
    },
    {
        "expression": "それ",
        "reading": "それ",
        "meaning": "that (thing near listener)",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "communication"
    },
    {
        "expression": "あれ",
        "reading": "あれ",
        "meaning": "that (thing far from both)",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "communication"
    },
    {
        "expression": "どれ",
        "reading": "どれ",
        "meaning": "which (of three or more)",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "communication"
    },
    {
        "expression": "この",
        "reading": "この",
        "meaning": "this ~ (modifier)",
        "jlpt": "N5",
        "pos": "prefix",
        "category": "communication"
    },
    {
        "expression": "その",
        "reading": "その",
        "meaning": "that ~ (modifier near listener)",
        "jlpt": "N5",
        "pos": "prefix",
        "category": "communication"
    },
    {
        "expression": "あの",
        "reading": "あの",
        "meaning": "that ~ (modifier far)",
        "jlpt": "N5",
        "pos": "prefix",
        "category": "communication"
    },
    {
        "expression": "どの",
        "reading": "どの",
        "meaning": "which ~ (modifier)",
        "jlpt": "N5",
        "pos": "prefix",
        "category": "communication"
    },
    {
        "expression": "誰",
        "reading": "だれ",
        "meaning": "who",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "communication"
    },
    {
        "expression": "何",
        "reading": "なに／なん",
        "meaning": "what",
        "jlpt": "N5",
        "pos": "pronoun",
        "category": "communication"
    },
    {
        "expression": "いつ",
        "reading": "いつ",
        "meaning": "when",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "communication"
    },
    {
        "expression": "どう",
        "reading": "どう",
        "meaning": "how; in what way",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "communication"
    },
    {
        "expression": "どうして",
        "reading": "どうして",
        "meaning": "why",
        "jlpt": "N5",
        "pos": "adverb",
        "category": "communication"
    },
    {
        "expression": "名前",
        "reading": "なまえ",
        "meaning": "name",
        "jlpt": "N5",
        "pos": "noun",
        "category": "communication"
    },
    {
        "expression": "住所",
        "reading": "じゅうしょ",
        "meaning": "address",
        "jlpt": "N5",
        "pos": "noun",
        "category": "communication"
    },
    {
        "expression": "意味",
        "reading": "いみ",
        "meaning": "meaning",
        "jlpt": "N5",
        "pos": "noun",
        "category": "communication"
    },
    {
        "expression": "例",
        "reading": "れい",
        "meaning": "example",
        "jlpt": "N5",
        "pos": "noun",
        "category": "communication"
    },
    {
        "expression": "音楽",
        "reading": "おんがく",
        "meaning": "music",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "映画",
        "reading": "えいが",
        "meaning": "movie; film",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "写真",
        "reading": "しゃしん",
        "meaning": "photograph",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "旅行",
        "reading": "りょこう",
        "meaning": "travel; trip",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "スポーツ",
        "reading": "スポーツ",
        "meaning": "sports",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "サッカー",
        "reading": "サッカー",
        "meaning": "soccer; football",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "野球",
        "reading": "やきゅう",
        "meaning": "baseball",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "テニス",
        "reading": "テニス",
        "meaning": "tennis",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "水泳",
        "reading": "すいえい",
        "meaning": "swimming",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "散歩",
        "reading": "さんぽ",
        "meaning": "walk; stroll",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "料理",
        "reading": "りょうり",
        "meaning": "cooking; cuisine",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "絵",
        "reading": "え",
        "meaning": "picture; drawing; painting",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "歌",
        "reading": "うた",
        "meaning": "song",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    },
    {
        "expression": "踊り",
        "reading": "おどり",
        "meaning": "dance",
        "jlpt": "N5",
        "pos": "noun",
        "category": "hobbies_and_leisure"
    }
]


async def seed():
    kana_sql = text(
        "INSERT INTO kana (kana, romaji, type, grp) VALUES (:kana, :romaji, :type, :grp) "
        "ON CONFLICT DO NOTHING"
    )
    kanji_sql = text(
        "INSERT INTO kanji (kanji, meaning, onyomi, kunyomi, jlpt, stroke_count, examples) "
        "VALUES (:kanji, CAST(:meaning AS text[]), CAST(:onyomi AS text[]), CAST(:kunyomi AS text[]), :jlpt, :stroke_count, :examples) "
        "ON CONFLICT (kanji) DO NOTHING"
    )
    vocab_sql = text(
        "INSERT INTO vocabulary (expression, reading, meaning, jlpt, pos, category) "
        "VALUES (:expression, :reading, :meaning, :jlpt, :pos, :category) "
        "ON CONFLICT (expression, reading) DO NOTHING"
    )
    kanji_params = [
        {**entry, "examples": json.dumps(entry["examples"], ensure_ascii=False)}
        for entry in KANJI
    ]

    try:
        async with SessionLocal() as db:
            for data, kana_type in [(HIRAGANA, "hiragana"), (KATAKANA, "katakana")]:
                await db.execute(kana_sql, [{"type": kana_type, **e} for e in data])
            await db.execute(kanji_sql, kanji_params)
            await db.execute(vocab_sql, list(VOCABULARY))
            await db.commit()
        print(f"Seed complete: {len(HIRAGANA)} hiragana, {len(KATAKANA)} katakana, {len(KANJI)} kanji, {len(VOCABULARY)} vocabulary")
    except Exception as e:
        print(f"Seed failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(seed())
