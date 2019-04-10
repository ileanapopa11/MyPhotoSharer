import argparse
import os
import datetime
import zipfile
import re
import sys


parser = argparse.ArgumentParser()
parser.add_argument('-iWant', help = 'Type of photos you want separated by the '+' sign. Default: cr+jpg', 
					default = "cr2+jpg", type = str)

parser.add_argument('-photoPath', help = 'The path to your photos.', 
					default = None, type = str)

args = parser.parse_args()

types = tuple(args.iWant.lower().split("+"))

for t in types:
	if not re.match(r'[a-z][a-z0-9]*', t):
		print("[TRY AGAIN]\n"
			  "\tFound invalid photo extension '{}'\n"
			  "\tExamples of valid argument: -iWant cr2+jpg".format(t))
		sys.exit(0)

if not os.path.exists(args.photoPath):
	print("[TRY AGAIN]\n\tYour photo path is not valid.")
	sys.exit(0)

time = datetime.datetime.now()
output_folder = 'output_' + time.strftime("%H.%M.%S(%d%B%y)")
os.mkdir(os.path.join(os.getcwd(), output_folder))

files = os.listdir(args.photoPath)
limit = 2 * pow(10, 9)

current_size = 0
batches = []
batch = []
for f in files:
	if f.lower().endswith(types):
		full_path = os.path.join(args.photoPath, f)
		size = os.path.getsize(full_path)
		if current_size + size <= limit:
			batch.append(full_path)
			current_size += size
		else:
			batches.append(batch)
			batch = [full_path]
			current_size = size


arch_name = os.path.basename(args.photoPath) + "{}.zip"

for index in range(len(batches)):
	batch = batches[index]
	arch_path = os.path.join(output_folder, arch_name.format(str(index + 1)))
	
	with zipfile.ZipFile(arch_path, 'w') as zip_arch:
		for photo in batch:
			if photo.lower().endswith(types):
				zip_arch.write(photo, os.path.basename(photo))
