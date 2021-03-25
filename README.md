# Hermes Formatter

## Overview

Whilst working for Vytaliving in Kidderminster I initiated and
implemented this project in order to reduce the time I spent
on one of my responsibilities in the office.

The task involved formatting (line by line) CSV files
containing up to 2000 orders exported from Shopify to be
compatible with Hermes, ensuring the correct shipping
labels would be assigned to relevant orders.

## Running
### Dependencies
Before running, install dependencies by executing the following:
```
 .../hermes_csv_formatter/ $ pip install -r requirements.txt
```

### Running preconfigured formatter
To start the program:
```
 .../hermes_csv_formatter/ $ python3 -m hermes_csv_formatter.main 
```

### Running program manually<a name="running"></a>
To start the python interpreter:
```
 .../hermes_csv_formatter/ $ python3
```

To load the functions and classes required:
```
>>> from hermes_csv_formatter import *
```
