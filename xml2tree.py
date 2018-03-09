import os
import re
import argparse
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('input', help='input XML')
args = parser.parse_args()

html = ""
with open("html.html", 'r') as html_file:
	html = html_file.read()

def recur_xml(root, x, y, sizex, sizey, ignore_first = False):
	#data = "<svg width=\"{0}%\" height=\"{1}%\" x=\"{2}%\" y=\"{3}%\"><g>".format(sizex, sizey, x, y)
	line_thickness = 0.2 * (sizey / 4 + sizex / 4)
	if ignore_first:
		size_each = sizex
		if len(root) != 0:
			size_each = sizex / len(root)
		data = ""
		for idx, child in enumerate(root):
			 data += recur_xml(child, x + size_each * idx, y, size_each, sizey)
		return data
	data = "<rect width=\"{0}%\" height=\"{1}%\" x=\"{2}%\" y=\"{3}%\" style=\"fill:rgb(255,255,255);stroke-width:{4};stroke:rgb(0,0,0)\" />".format(sizex / 100 * 95, sizey / 4, x + sizex / 100 * 2.5, y + sizey / 8, line_thickness)
	data += "<text x=\"{0}%\" y=\"{1}%\" fill=\"black\" style=\"font-size: {3}px;\">{2}</text>".format(x + sizex / 100 * 4, y + sizey / 6, root.tag, 0.4 * (sizey / 4 + sizex))
	data += "<text x=\"{0}%\" y=\"{1}%\" fill=\"black\" style=\"font-size: {3}px;\">{2}</text>".format(x + sizex / 100 * 4, y + sizey / 100 * 20, root.text, 0.2 * (sizey / 4 + sizex))
	if len(root) > 0:
		data += "<line x1=\"{0}%\" y1=\"{1}%\" x2=\"{2}%\" y2=\"{3}%\" style=\"stroke:rgb(0,0,0);stroke-width:{4}\" />".format(x + sizex / 2, y + sizey / 4 + sizey / 8, x + sizex / 2 , y + sizey / 2, line_thickness)
	size_each = sizex
	if len(root) != 0:
		size_each = sizex / len(root)
	for idx, child in enumerate(root):
		center_x = x + size_each * (idx + 0.5)
		center_y = y + sizey / 2 + sizey / 4
		if len(root) > 1:
			data += "<line x1=\"{0}%\" y1=\"{1}%\" x2=\"{2}%\" y2=\"{3}%\" style=\"stroke:rgb(0,0,0);stroke-width:{4}\" />".format(center_x, y + sizey / 2, x + sizex / 4 , y + sizey / 2, line_thickness)
		data += "<line x1=\"{0}%\" y1=\"{1}%\" x2=\"{2}%\" y2=\"{3}%\" style=\"stroke:rgb(0,0,0);stroke-width:{4}\" />".format(center_x, y + sizey / 2, center_x, y + sizey / 2 + sizey / 8, line_thickness)
		data += recur_xml(child, x + size_each * idx, y + sizey / 2, size_each, sizey / 2)
	#data += "</g></svg>"
	return data

with open(args.input, 'r') as xml:
	tree = ET.parse(xml)
	root = tree.getroot()
	data = recur_xml(root, 0, 0, 100, 100, True)
	print(html.format( data))
