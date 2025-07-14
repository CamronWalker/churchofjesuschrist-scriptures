# churchofjesuschrist-scriptures
Borrowed a starting point lds-scriptures.txt file from [scriptures.nephi.org](https://scriptures.nephi.org).

My goal is to not just post what I'm using but to also post the python script I'm using so someone can customize how they want the scriptures to look in Obsidian for themselves.

Requirements Python 3. Open AI API. 

### Link Creator
If you want to link to another resource you can use the gospel_link_creator.py file to generate the lds_scriptures_urls.json. This json file is used in md_scriptures_creator.ph to link these external resources directly into the chapter note.

### Markup File Creator
Open and Run md_scriptures_creator.py
```
python3 md_scriptures_creator.py
```

Take a look at the "Scriptures" folder output files. Make any adjustments you like.

### AI Summary Generator

Ensure your .env file contains your `OPENAI_API_KEY`

```
# instlal requirements if nessissary
pip3 install openai
pip3 install pyyaml
pip3 install python-dotenv
# run script
python3 gpt_summary.py
```