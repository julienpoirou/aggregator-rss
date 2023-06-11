# Aggregator RSS

An open-source RSS feed aggregator for discord bot.



## Features

- [X] Add and remove unlimited RSS feed
- [X] Synchronizes RSS feeds every x seconds
- [X] YAML configuration file
- [X] Enable or disable logs
- [X] Clean logs and/or database
- [X] Catch Ctrl+c to exit script
- [X] Help



## Install

Download the python script: aggregator-rss.py.

Install dependencies: `pip3 install -r ./requirements.txt`

Configure the file: config.yaml
```yaml
config:
  enable_logs: True  # Enable or Disable logs
  sync_time: 30  # Get new feed, all x seconds
  logs_file: ./history.logs  # The file with history of the script
  database_file: ./db.json  # The file with all feeds save
feeds:  # Add unlimited feeds
  - name: Adala
    url: https://adala-news.fr/feed/
  - name: Journal Du Japon
    url: https://feeds.feedburner.com/journaldujapon/gOqY/
```

Run the python dependencies script: aggregator-rss.py.



## Python dependencies

- feedparser
- json
- pyyaml
- os
- sys
- datetime
- colorama
- time
- signal



## Usage

Execute in the script directory : `cd ./sample`

Execute the script : `py ./aggregator-rss.py`



## TODO

- [ ] Configure Discord Bot
- [ ] Add pictures for feeds
- [ ] Add and remove unlimited Atom feed
- [ ] Clean code



## License

<details>

```
MIT License

Copyright (c) 2023 Julien Poirou

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</details>