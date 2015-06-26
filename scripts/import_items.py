#!/usr/bin/env python
import csv
import os
import sys

sys.path.append("../")
sys.path.append(".")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from main.models import Item


csv_file_path = "%s/Amazon.csv" % os.path.dirname(os.path.abspath(__file__))

csv_file = open(csv_file_path, 'r')
line = 0

try:
    reader = csv.reader(csv_file)
    print dir(reader)
    for row in reader:
        item_id = row[0]
        title = row[1]
        description = row[2]
        manufacturer = row[3]
        try:
            price = float(row[4])
        except:
            print"Failed conversion %s %s" % (line, row[4])
            price = 0

        new_item = Item()
        new_item.name = title
        new_item.descipriton = description
        new_item.weight = 0
        new_item.price = price
        new_item.tags = manufacturer

        try:
            new_item.save()
        except Exception, e:
            print e
            pass

        line = line + 1
        print line
        print title
        print price

finally:
    csv_file.close()



