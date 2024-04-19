#/bin/pythoon3
"""Renames decomposed time folders where the precision has slipped.
For example, 16999.9999999 will become 17000.
The uniform/time file will also be deleted for consistency.
The script will prompt the user before carry out the renaming procedure.

Jeffrey Johnston	NotDrJeff@gmail.com		April 2024
"""

from pathlib import Path
import re

def main():
	casedir = Path.cwd()
	processordirs = [dir for dir in casedir.iterdir() if re.fullmatch('processor[0-9]+', dir.name)]

	subdirs =[]
	for processordir in processordirs:
		subdirs.extend([dir for dir in processordir.iterdir()])

	dirs_to_rename = []
	new_dirs = []
	for dir in subdirs:
		try:
			int(dir.name)
		except ValueError:
			try:
				time = float(dir.name)
			except ValueError:
				continue
			
			new_time = round(time,6)
			if (time - new_time) != 0:
				dirs_to_rename.append(dir)
				
				if new_time - round(new_time) == 0:
					new_time = round(new_time)
				new_dirs.append(dir.parent / str(int(new_time)))
				
		continue

	messages = []
	for i, dir in enumerate(dirs_to_rename):
		messages.append(f'{dir.name} ----> {new_dirs[i].name}')
		
	for message in set(messages):
		print(message)

	overwrite = input('About to overwrite. Are these changes correct? (y/n): ').lower().strip() == 'y'

	if overwrite:
		for i, dir in enumerate(dirs_to_rename):
			files_to_remove = [file for file in (dir / 'uniform').iterdir() if file.stem == 'time']
			for file in files_to_remove:
				file.unlink()
				
			dir.rename(new_dirs[i])
			
			
if __name__ == '__main__':
    main()
    