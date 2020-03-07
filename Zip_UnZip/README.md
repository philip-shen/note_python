# Purpose  
Take note of Zip and UnZip  

# Table of Contents  
[]()  

# 
[Python: How to unzip a file | Extract Single, multiple or all files from a ZIP archive December 1, 2018](https://thispointer.com/python-how-to-unzip-a-file-extract-single-multiple-or-all-files-from-a-zip-archive/)  
```
def main():
 
    print('Extract all files in ZIP to current directory')
    # Create a ZipFile Object and load sample.zip in it
    with ZipFile('sampleDir.zip', 'r') as zipObj:
       # Extract all the contents of zip file in current directory
       zipObj.extractall()
 
    print('Extract all files in ZIP to different directory')
 
    # Create a ZipFile Object and load sample.zip in it
    with ZipFile('sampleDir.zip', 'r') as zipObj:
       # Extract all the contents of zip file in different directory
       zipObj.extractall('temp')
 
    print('Extract single file from ZIP')
 
    # Create a ZipFile Object and load sample.zip in it
    with ZipFile('sampleDir.zip', 'r') as zipObj:
       # Get a list of all archived file names from the zip
       listOfFileNames = zipObj.namelist()
       # Iterate over the file names
       for fileName in listOfFileNames:
           # Check filename endswith csv
           if fileName.endswith('.csv'):
               # Extract a single file from zip
               zipObj.extract(fileName, 'temp_csv')
 
 
 
if __name__ == '__main__':
   main()
```

[pythonでzipファイルを再帰的に展開 Jun 01, 2017](https://qiita.com/arwtyxouymz0110/items/2caed2f760d586969972)  

```
 expand_zip.py

# -*- coding: utf-8 -*-
import os
import sys
import zipfile
import glob


def unzip(filename):
    with zipfile.ZipFile(filename, "r") as zf:
        zf.extractall(path=os.path.dirname(filename))
    delete_zip(filename)


def delete_zip(zip_file):
    os.remove(zip_file)


def walk_in_dir(dir_path):
    for filename in glob.glob(os.path.join(dir_path, "*.zip")):
        unzip(filename=os.path.join(dir_path,filename))

    for dirname in (d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))):
        walk_in_dir(os.path.join(dir_path, dirname))


if __name__ == "__main__":
    args = sys.argv
    try:
        if(os.path.isdir(args[1])):
            walk_in_dir(args[1])
        else:
            unzip(os.path.join(args[1]))
            name, _ = os.path.splitext(args[1])
            if (os.path.isdir(name)):
                walk_in_dir(name)
    except IndexError:
        print('IndexError: Usage "python %s ZIPFILE_NAME" or "python %s DIR_NAME"' % (args[0], args[0]))
    except IOError:
        print('IOError: Couldn\'t open "%s"' % args[1])
```

# Troubleshooting


# Reference


* []()
![alt tag]()

# h1 size

## h2 size

### h3 size

#### h4 size

##### h5 size

*strong*strong  
**strong**strong  

> quote  
> quote

- [ ] checklist1
- [x] checklist2

* 1
* 2
* 3

- 1
- 2
- 3
