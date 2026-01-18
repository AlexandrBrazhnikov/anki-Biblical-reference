# 📖 Biblical Reference

This add-on program will help you to automate pasting verses from the Bible to the specified fields in your card according to given Biblical Reference.

It will add button `Biblical Reference` to top-bar menu when you are creating a new card or view the card in Browser.

There is a built in database that contains several Public Domain translations of the Bible into different languages.

Currently supported:
* **King James Version (KJV)** - Gospels.
* **Russian Synodal Bible** - Gospels.

## Quick Start
1. Add a new field with name `Biblical Reference` to your card. That will pass your reference phrase the program.
2. Add a new field to your card named in accordance to keys of `output_fields` or assign existing field name to the translation code there. It will receive and store verse output from the program. Default names: `KJV Translation`, `Synodal Translation`.
3. Create a new card.
4. Write reference phrase to the `Biblical Reference` field in format: `[Book], [Chapter]:[Verse]`. Example: `The Gospel of Mark, 1:1`. Be aware: search is sensitive to the letter case and separators: comma-space and colon.
5. Press `Biblical Reference` button on the top-bar or keyboard shortcut `Ctrl+Shift+B`/`Cmd+Shift+B`.

## Deep Dive
To find the verse from the Bible add-on program needs 4 parameters:
* Book name
* Chapter number
* Verse number
* Required translation

You need to give a clue for the program where to search them in your card by adjusting configuration file, that you can get an access in `Anki -> Tools -> Add-ons`.

First three parameters `book`, `chapter` and `verse` are similar. For each of them you need to pass a list contains three strings:
1. Name of the field that contains the paramterer.
2. Regular expresion with _**one defined group**_ to extract only necessary text, because regularly one field could contain string with more than one parameter or have any decorative text.
3. Field part to search. The field consists of `header` (name/title of the field) and `body` (text placed by you into that field). That allows you to make search parameter by constant field header or various field body.

> Let me emphasize twice: regular expression must contain only _**one defined group**_. The program will use the first one. 

The `Required translation` parameter, but to be honest its code, will must appear in `output_fields` with the name of the field that you want paste verse text in.

By this you can select multiple fields in your card to paste different translations of verses at once, just assign target field names to the target translation.

Database has several most common names for each book in each language, but if you want to have total control over it, or want to assign a specific name for the book you may use aliases. Just add a new one `[your_book_name]: [any_database_book_name]` pair.

If you don't want to program rewrite the text in target fields, set `rewrite_fields` to `false`. By default it's `true`.

## Examples
**Conditions:**
You are English native and learning Russian. You want to have fields named `Mark` and `Марк`. You want to write in `chapter` and `verse` in a format: `[chapter]:[verse]` to the `Mark` field and get English and Russian verse.
```JSON
{
    "00_book": ["Mark", "(.*)", "header"],
    "00_chapter": ["Mark", "(\\d+):\\d+", "body"],
    "00_verse": ["Mark", "\\d+:(\\d+)", "body"],
    "01_rewrite_fields": true,
    "02_output_fields": {
        "Mark": "KJV",
        "Марк": "SYNO"
    },
    "03_book_aliases": {
        "Mark": "The Gospel According to Saint Mark"
    }
}
```

**Conditions:**
You are Chinese native and learning English. You want to have field `Biblical Reference` to write in `book`, `chapter` and `verse` parameters in a format: `[chinese_book_name] - Chapter:[chapter], Verse: [verse]` and get in output English verse to the `Mk.` field.
```JSON
{
    "00_book": ["Biblical Reference", "([\\w.\\s]+) - Chapter:\\d+, Verse:\\d+", "body"],
    "00_chapter": ["Biblical Reference", "[\\w.\\s]+ - (Chapter:\\d+), Verse:\\d+", "body"],
    "00_verse": ["Biblical Reference", "[\\w.\\s]+ - Chapter:\\d+, (Verse:\\d+)", "body"],
    "01_rewrite_fields": true,
    "02_output_fields": {
        "Mk.": "KJV"
    },
    "03_book_aliases": {
        "马可福音": "The Gospel According to Saint Mark"
    }
}
```

> Hint: You can assign more than one alias to the database book name.


## Available Books, Translations and Abbreviations

### **The Gospel According to Saint Matthew**
* **EN - King James Version: Code `KJV`**
    * **Variants:** The Gospel According to Saint Matthew, The Gospel of Matthew, Matthew, Matt., Mt
* **RU - Russian Synodal Bible: Code `SYNO`**
    * **Variants:** Св. Евангелие от Матфея, Евангелие от Матфея, От Матфея, Матфей, Мф., Мф

### **The Gospel According to Saint Mark**
* **EN - King James Version: Code `KJV`**
    * **Variants:** The Gospel According to Saint Mark, The Gospel of Mark, Mark, Mk., Mk
* **RU - Russian Synodal Bible: Code `SYNO`**
    * **Variants:** Св. Евангелие от Марка, Евангелие от Марка, От Марка, Марк, Мк., Мк

### **The Gospel According to Saint Luke**
* **EN - King James Version: Code `KJV`**
    * **Variants:** The Gospel According to Saint Luke, The Gospel of Luke, Luke, Lk., Lk
* **RU - Russian Synodal Bible: Code `SYNO`**
    * **Variants:** Св. Евангелие от Луки, Евангелие от Луки, От Луки, Лука, Лк., Лк

### **The Gospel According to Saint John**
* **EN - King James Version: Code `KJV`**
    * **Variants:** The Gospel According to Saint John, The Gospel of John, John, Jn., Jn
* **RU - Russian Synodal Bible: Code `SYNO`**
    * **Variants:** Св. Евангелие от Иоанна, Евангелие от Иоанна, От Иоанна, Иоанн, Ин., Ин