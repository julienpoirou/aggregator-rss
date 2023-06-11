"""RSS feed aggregator.

Usage:
======
    python aggregator-rss.py [option] [value]

    Options:
    -h, --help     : Show this help message and exit
                        Usage: py aggregator-rss.py -h
    -e, --exec     : Execute the script
                        Usage: py aggregator-rss.py -e
    -u, --update   : Update the database
                        Usage: py aggregator-rss.py -u
    -c, --clear    : Clean Logs file and/or database
                        Usage: py aggregator-rss.py -c [argument]
                        Arguments:
                            db : Clean database
                            database : Clean database
                            logs : Clean Logs file
                            all : Clean Logs file and database
"""

__authors__ = ("Julien Poirou")
__contact__ = ("julienpoirou@protonmail.com")
__copyright__ = "MIT"
__date__ = "2023-06-10"
__version__= "0.5.0"

import feedparser
import json
import sys
import os
import yaml
import time
import signal
from os import path
from datetime import datetime
from colorama import Fore, Style

CONFIG = yaml.load(open("./config.yaml", 'r'), Loader=yaml.Loader)
DATABASE_FILE = str(CONFIG['config']['database_file'])
LOGS_FILE = str(CONFIG['config']['logs_file'])
ACTIVE_LOGS = bool(CONFIG['config']['enable_logs'])
SYNC_TIME = int(CONFIG['config']['sync_time'])

ERROR_INVALID_FEED = Fore.RED+'[ERROR]'+Style.RESET_ALL+' Feed url is invalid:'
ERROR_INVALID_DATABASE_STRUCTURE = Fore.RED+'[ERROR]'+Style.RESET_ALL+' Your database ('+DATABASE_FILE+') structure is broken!'
SUCCESS_CREATE_DATABASE = Fore.GREEN+'[SUCCESS]'+Style.RESET_ALL+' Your database ('+DATABASE_FILE+') is created!'
SUCCESS_ADD_FEED = Fore.GREEN+'[SUCCESS]'+Style.RESET_ALL+' The feed has been added:'
SUCCESS_UPDATE_FEED = Fore.GREEN+'[SUCCESS]'+Style.RESET_ALL+' The feed has been updated:'
SUCCESS_CREATE_LOGS = Fore.GREEN+'[SUCCESS]'+Style.RESET_ALL+' Your logs file ('+LOGS_FILE+') is created!'
INFO_FEED_UNCHANGED = Fore.BLUE+'[INFO]'+Style.RESET_ALL+' The feed is already up-to-date:'
INFO_EXIT_SCRIPT = Fore.BLUE+'[INFO]'+Style.RESET_ALL+' Ctrl-c was pressed. Do you really want to exit?'
ERROR_INVALID_FEED_LOGS = '[ERROR] Feed url is invalid:'
ERROR_INVALID_DATABASE_STRUCTURE_LOGS = '[ERROR] Your database ('+DATABASE_FILE+') structure is broken!'
SUCCESS_CREATE_DATABASE_LOGS = '[SUCCESS] Your database ('+DATABASE_FILE+') is created!'
SUCCESS_ADD_FEED_LOGS = '[SUCCESS] The feed has been added:'
SUCCESS_UPDATE_FEED_LOGS = '[SUCCESS] The feed has been updated:'
INFO_FEED_UNCHANGED_LOGS = '[INFO] The feed is already up-to-date:'


def check_feed(url):
    """Check the validity of feed url."""
    feed = feedparser.parse(url)
    if len(feed.entries) < 1:
        return False
    else:
        return True


def get_last_feed(url):
    """Get the latest rss feed."""
    feed = feedparser.parse(url)
    for i in range (0, len(feed.entries)):
        if i == (len(feed.entries)-1):
            return feed.entries[0]


def load_database(database):
    """Get the data of the database."""
    with open(database, encoding='utf-8') as file:
        data = json.load(file)
        return data


def push_in_database(database, new_data):
    """Push in the database the new data."""
    with open(database, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4, separators=(',',': '), ensure_ascii=False)


def push_in_logs(logs, line):
    """Push in the logs file the new actions."""
    if ACTIVE_LOGS == True:
        with open(logs, 'a', encoding='utf-8') as file:
            file.write(line+'\n')

def push_in_logs(logs, line):
    """Push in the logs file the new actions."""
    if ACTIVE_LOGS == True:
        with open(logs, 'a', encoding='utf-8') as file:
            file.write(line+'\n')


def handler(signum, frame):
    """Catch Ctrl-c and exist the script."""
    res = input(INFO_EXIT_SCRIPT+" [y/n]")
    if res == 'y':
        exit(1)


def help():
    """Print the help."""
    string = """    Usage: python """+sys.argv[0]+""" [option] [value]

    RSS feed aggregator.

    Options:
    -h, --help     : Show this help message and exit
                        Usage: py """+sys.argv[0]+""" -h
    -e, --exec     : Execute the script
                        Usage: py """+sys.argv[0]+""" -e
    -u, --update   : Update the database
                        Usage: py """+sys.argv[0]+""" -u
    -c, --clear    : Clean Logs file and/or database
                        Usage: py """+sys.argv[0]+""" -c [argument]
                        Arguments:
                            db : Clean database
                            database : Clean database
                            logs : Clean Logs file
                            all : Clean Logs file and database
        
    Good use."""
    return print(string)


if __name__ == "__main__":
    # Get datetime
    datetime_publication = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    # Catch Ctrl+c
    signal.signal(signal.SIGINT, handler)

    # Check arguments
    if len(sys.argv) == 2:
        if sys.argv[1] == "--exec" or sys.argv[1] == "-e":
            if int(SYNC_TIME) >= 0:
                while True:
                    # Wait x seconds
                    time.sleep(int(SYNC_TIME))
                    # Check if logs file exists
                    if path.isfile(LOGS_FILE) is False:
                        # Create the new logs file
                        with open(LOGS_FILE, 'w') as file:
                            pass
                        print(SUCCESS_CREATE_LOGS+' ('+datetime_publication+')')

                    # Check if database exists
                    if path.isfile(DATABASE_FILE) is False:
                        # Create the new database file
                        with open(DATABASE_FILE, 'w') as file:
                            pass
                        # Create the structure of the new database
                        db = {}
                        new_db = {
                            "feeds": {
                            }
                        }
                        # Push the structure in the new database
                        db.update(new_db)
                        push_in_database(DATABASE_FILE, db)
                        print(SUCCESS_CREATE_DATABASE+' ('+datetime_publication+')')
                        push_in_logs(LOGS_FILE, SUCCESS_CREATE_DATABASE_LOGS+' ('+datetime_publication+')')

                    # Load database
                    db = load_database(DATABASE_FILE)
                    for items in db['feeds']:
                        feed_url = db['feeds'][items]['url']
                        # Check if feed url is valid
                        if check_feed(feed_url) == True:
                            # Load feed data
                            last_feed = get_last_feed(feed_url)

                            # Checks database structure
                            if "feeds" in db:
                                # Checks if feed in database exists
                                if feed_url in db['feeds']:
                                    # Check if it's new news
                                    if last_feed['title'] != db['feeds'][feed_url]['title']:
                                        # Update the news in the database
                                        db['feeds'][feed_url]['title'] = last_feed['title']
                                        db['feeds'][feed_url]['description'] = last_feed['description']
                                        db['feeds'][feed_url]['link'] = last_feed['link']
                                        db['feeds'][feed_url]['datetime'] = datetime_publication
                                        push_in_database(DATABASE_FILE, db)
                                        print(SUCCESS_UPDATE_FEED+" "+feed_url+' ('+datetime_publication+')')
                                        push_in_logs(LOGS_FILE, SUCCESS_UPDATE_FEED_LOGS+" "+feed_url+' ('+datetime_publication+')')
                                    else:
                                        print(INFO_FEED_UNCHANGED+" "+feed_url+' ('+db['feeds'][feed_url]['datetime']+')')
                                        push_in_logs(LOGS_FILE, INFO_FEED_UNCHANGED_LOGS+" "+feed_url+' ('+db['feeds'][feed_url]['datetime']+')')
                            else:
                                print(ERROR_INVALID_DATABASE_STRUCTURE+' ('+datetime_publication+')')
                                push_in_logs(LOGS_FILE, ERROR_INVALID_DATABASE_STRUCTURE_LOGS+' ('+datetime_publication+')')
                        else:
                            print(ERROR_INVALID_FEED+" "+feed_url+' ('+datetime_publication+')')
                            push_in_logs(LOGS_FILE, ERROR_INVALID_FEED_LOGS+" "+feed_url+' ('+datetime_publication+')')
            else:
                # Check if logs file exists
                if path.isfile(LOGS_FILE) is False:
                    # Create the new logs file
                    with open(LOGS_FILE, 'w') as file:
                        pass
                    print(SUCCESS_CREATE_LOGS+' ('+datetime_publication+')')

                # Check if database exists
                if path.isfile(DATABASE_FILE) is False:
                    # Create the new database file
                    with open(DATABASE_FILE, 'w') as file:
                        pass
                    # Create the structure of the new database
                    db = {}
                    new_db = {
                        "feeds": {
                        }
                    }
                    # Push the structure in the new database
                    db.update(new_db)
                    push_in_database(DATABASE_FILE, db)
                    print(SUCCESS_CREATE_DATABASE+' ('+datetime_publication+')')
                    push_in_logs(LOGS_FILE, SUCCESS_CREATE_DATABASE_LOGS+' ('+datetime_publication+')')

                # Load database
                db = load_database(DATABASE_FILE)
                for items in db['feeds']:
                    feed_url = db['feeds'][items]['url']
                    # Check if feed url is valid
                    if check_feed(feed_url) == True:
                        # Load feed data
                        last_feed = get_last_feed(feed_url)

                        # Checks database structure
                        if "feeds" in db:
                            # Checks if feed in database exists
                            if feed_url in db['feeds']:
                                # Check if it's new news
                                if last_feed['title'] != db['feeds'][feed_url]['title']:
                                    # Update the news in the database
                                    db['feeds'][feed_url]['title'] = last_feed['title']
                                    db['feeds'][feed_url]['description'] = last_feed['description']
                                    db['feeds'][feed_url]['link'] = last_feed['link']
                                    db['feeds'][feed_url]['datetime'] = datetime_publication
                                    push_in_database(DATABASE_FILE, db)
                                    print(SUCCESS_UPDATE_FEED+" "+feed_url+' ('+datetime_publication+')')
                                    push_in_logs(LOGS_FILE, SUCCESS_UPDATE_FEED_LOGS+" "+feed_url+' ('+datetime_publication+')')
                                else:
                                    print(INFO_FEED_UNCHANGED+" "+feed_url+' ('+db['feeds'][feed_url]['datetime']+')')
                                    push_in_logs(LOGS_FILE, INFO_FEED_UNCHANGED_LOGS+" "+feed_url+' ('+db['feeds'][feed_url]['datetime']+')')
                        else:
                            print(ERROR_INVALID_DATABASE_STRUCTURE+' ('+datetime_publication+')')
                            push_in_logs(LOGS_FILE, ERROR_INVALID_DATABASE_STRUCTURE_LOGS+' ('+datetime_publication+')')
                    else:
                        print(ERROR_INVALID_FEED+" "+feed_url+' ('+datetime_publication+')')
                        push_in_logs(LOGS_FILE, ERROR_INVALID_FEED_LOGS+" "+feed_url+' ('+datetime_publication+')')
        elif sys.argv[1] == "--update" or sys.argv[1] == "-u":
            # Check if database exists
            if path.isfile(DATABASE_FILE) is True:
                # Load database
                db = load_database(DATABASE_FILE)
                # Checks database structure
                if "feeds" in db:
                    # Create the new database file
                    with open(DATABASE_FILE, 'w') as file:
                        pass
                    # Create the structure of the new database
                    db = {}
                    new_db = {
                        "feeds": {
                        }
                    }
                    # Push the structure in the new database
                    db.update(new_db)
                    push_in_database(DATABASE_FILE, db)
                    for items in CONFIG['feeds']:
                        # Get new feed data
                        feed_url = items['url']
                        feed_name = items['name']
                        # Add the news in the database
                        new_feed = {
                            feed_url: {
                                "name": feed_name,
                                "url": feed_url,
                                "title": "",
                                "description": "",
                                "link": "",
                                "datetime": ""
                            }
                        }
                        db['feeds'].update(new_feed)
                        push_in_database(DATABASE_FILE, db)
                        print(SUCCESS_ADD_FEED+" "+feed_url+' ('+datetime_publication+')')
                        push_in_logs(LOGS_FILE, SUCCESS_ADD_FEED_LOGS+" "+feed_url+' ('+datetime_publication+')')
                    # Load database
                    db = load_database(DATABASE_FILE)
                    for items in db['feeds']:
                        feed_url = db['feeds'][items]['url']
                        # Check if feed url is valid
                        if check_feed(feed_url) == True:
                            # Load feed data
                            last_feed = get_last_feed(feed_url)

                            # Checks database structure
                            if "feeds" in db:
                                # Checks if feed in database exists
                                if feed_url in db['feeds']:
                                    # Check if it's new news
                                    if last_feed['title'] != db['feeds'][feed_url]['title']:
                                        # Update the news in the database
                                        db['feeds'][feed_url]['title'] = last_feed['title']
                                        db['feeds'][feed_url]['description'] = last_feed['description']
                                        db['feeds'][feed_url]['link'] = last_feed['link']
                                        db['feeds'][feed_url]['datetime'] = datetime_publication
                                        push_in_database(DATABASE_FILE, db)
                                        print(SUCCESS_UPDATE_FEED+" "+feed_url+' ('+datetime_publication+')')
                                        push_in_logs(LOGS_FILE, SUCCESS_UPDATE_FEED_LOGS+" "+feed_url+' ('+datetime_publication+')')
                                    else:
                                        print(INFO_FEED_UNCHANGED+" "+feed_url+' ('+db['feeds'][feed_url]['datetime']+')')
                                        push_in_logs(LOGS_FILE, INFO_FEED_UNCHANGED_LOGS+" "+feed_url+' ('+db['feeds'][feed_url]['datetime']+')')
                            else:
                                print(ERROR_INVALID_DATABASE_STRUCTURE+' ('+datetime_publication+')')
                                push_in_logs(LOGS_FILE, ERROR_INVALID_DATABASE_STRUCTURE_LOGS+' ('+datetime_publication+')')
                        else:
                            print(ERROR_INVALID_FEED+" "+feed_url+' ('+datetime_publication+')')
                            push_in_logs(LOGS_FILE, ERROR_INVALID_FEED_LOGS+" "+feed_url+' ('+datetime_publication+')')
                else:
                    print(ERROR_INVALID_DATABASE_STRUCTURE+' ('+datetime_publication+')')
                    push_in_logs(LOGS_FILE, ERROR_INVALID_DATABASE_STRUCTURE_LOGS+' ('+datetime_publication+')')
            else:
                # Create the new database file
                with open(DATABASE_FILE, 'w') as file:
                    pass
                # Create the structure of the new database
                db = {}
                new_db = {
                    "feeds": {
                    }
                }
                # Push the structure in the new database
                db.update(new_db)
                push_in_database(DATABASE_FILE, db)
                print(SUCCESS_CREATE_DATABASE+' ('+datetime_publication+')')
                push_in_logs(LOGS_FILE, SUCCESS_CREATE_DATABASE_LOGS+' ('+datetime_publication+')')
                # Load database
                db = load_database(DATABASE_FILE)
                for items in CONFIG['feeds']:
                    feed_url = items['url']
                    feed_name = items['name']
                    # Add the news in the database
                    new_feed = {
                        feed_url: {
                            "name": feed_name,
                            "title": "",
                            "description": "",
                            "link": "",
                            "datetime": ""
                        }
                    }
                    db['feeds'].update(new_feed)
                    push_in_database(DATABASE_FILE, db)
                    print(SUCCESS_ADD_FEED+" "+feed_url+' ('+datetime_publication+')')
                    push_in_logs(LOGS_FILE, SUCCESS_ADD_FEED_LOGS+" "+feed_url+' ('+datetime_publication+')')
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            help()
        else:
            help()
    elif len(sys.argv) == 3:
        if sys.argv[1] == "--clear" or sys.argv[1] == "-c":
            if sys.argv[2] == "database" or sys.argv[2] == "db":
                # Check if database exists
                if path.isfile(DATABASE_FILE) is True:
                    # Remove database
                    os.remove(DATABASE_FILE)
                    # Create the new database file
                    with open(DATABASE_FILE, 'w') as file:
                        pass
                    # Create the structure of the new database
                    db = {}
                    new_db = {
                        "feeds": {
                        }
                    }
                    # Push the structure in the new database
                    db.update(new_db)
                    push_in_database(DATABASE_FILE, db)
                    print(SUCCESS_CREATE_DATABASE+' ('+datetime_publication+')')
                    push_in_logs(LOGS_FILE, SUCCESS_CREATE_DATABASE_LOGS+' ('+datetime_publication+')')
                else:
                    # Create the new database file
                    with open(DATABASE_FILE, 'w') as file:
                        pass
                    # Create the structure of the new database
                    db = {}
                    new_db = {
                        "feeds": {
                        }
                    }
                    # Push the structure in the new database
                    db.update(new_db)
                    push_in_database(DATABASE_FILE, db)
                    print(SUCCESS_CREATE_DATABASE+' ('+datetime_publication+')')
                    push_in_logs(LOGS_FILE, SUCCESS_CREATE_DATABASE_LOGS+' ('+datetime_publication+')')
            elif sys.argv[2] == "logs":
                # Check if logs file exists
                if path.isfile(LOGS_FILE) is True:
                    # Remove logs file
                    os.remove(LOGS_FILE)
                    # Create the new logs file
                    with open(LOGS_FILE, 'w') as file:
                        pass
                    print(SUCCESS_CREATE_LOGS+' ('+datetime_publication+')')
                else:
                    # Create the new logs file
                    with open(LOGS_FILE, 'w') as file:
                        pass
                    print(SUCCESS_CREATE_LOGS+' ('+datetime_publication+')')
            elif sys.argv[2] == "all":
                # Check if database exists
                if path.isfile(DATABASE_FILE) is True:
                    # Remove database
                    os.remove(DATABASE_FILE)
                    # Create the new database file
                    with open(DATABASE_FILE, 'w') as file:
                        pass
                    # Create the structure of the new database
                    db = {}
                    new_db = {
                        "feeds": {
                        }
                    }
                    # Push the structure in the new database
                    db.update(new_db)
                    push_in_database(DATABASE_FILE, db)
                    print(SUCCESS_CREATE_DATABASE+' ('+datetime_publication+')')
                    push_in_logs(LOGS_FILE, SUCCESS_CREATE_DATABASE_LOGS+' ('+datetime_publication+')')
                else:
                    # Create the new database file
                    with open(DATABASE_FILE, 'w') as file:
                        pass
                    # Create the structure of the new database
                    db = {}
                    new_db = {
                        "feeds": {
                        }
                    }
                    # Push the structure in the new database
                    db.update(new_db)
                    push_in_database(DATABASE_FILE, db)
                    print(SUCCESS_CREATE_DATABASE+' ('+datetime_publication+')')
                    push_in_logs(LOGS_FILE, SUCCESS_CREATE_DATABASE_LOGS+' ('+datetime_publication+')')

                # Check if logs file exists
                if path.isfile(LOGS_FILE) is True:
                    # Remove logs file
                    os.remove(LOGS_FILE)
                    # Create the new logs file
                    with open(LOGS_FILE, 'w') as file:
                        pass
                    print(SUCCESS_CREATE_LOGS+' ('+datetime_publication+')')
                else:
                    # Create the new logs file
                    with open(LOGS_FILE, 'w') as file:
                        pass
                    print(SUCCESS_CREATE_LOGS+' ('+datetime_publication+')')
            else:
                help()
        else:
            help()
    else:
        help()