# Synchronizer

[![Documentation Status](https://readthedocs.org/projects/synchronizer/badge/?version=latest)](https://synchronizer.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/xiancg/synchronizer.svg?branch=master)](https://travis-ci.org/xiancg/synchronizer)
[![Coverage Status](https://coveralls.io/repos/github/xiancg/synchronizer/badge.svg?branch=master)](https://coveralls.io/github/xiancg/synchronizer?branch=master)

A collection of utilities for CGI-VFX to copy files from one place to another, find out basic stat differences between them and handle file sequences and textures (tx files).

# Installation
```python
pip install synchronizer
```

# Documentation
[Synchronizer Docs](https://synchronizer.rtfd.io)

# Basic Usage:
1. Copies src_path to trg_path. Takes both files and directories as source. If given source is a file and it's part of a sequence it'll find and copy the entire sequence of files.
```python
from synchronizer import copier
copier.process_paths(src_path, trg_path, force_overwrite=True, **kwargs)
```
kwargs: 
    include_tx = True
    only_tx = True
    find_sequence = True

2. Compares two files or directory paths and return sync status. Sync status refers to name and os.stat() comparisons
```python
from synchronizer import syncstatus
syncstatus.get_sync_status(
            src_path, trg_path,
            ignore_name=False,
            ignore_stats=['st_uid', 'st_gid', 'st_atime',
                    'st_ctime', 'st_ino', 'st_dev'])
```

3. Compares two paths and returns whichever has the most recent stat time. Default stat used for comparison is st_mtime which is: Time of most recent content modification.
```python
from synchronizer import syncstatus
syncstatus.get_most_recent(src_path, trg_path, use_stat='st_mtime')
```

4. Find and return all files that are part of a sequence matching file_path. If no sequence found, returns None. Two files are enough to make a sequence, even if they're not sequential. This assumes the sequence digits are right beside the file extension.
    ie: C_myfile_v568.jpg
        MJ_thisisafileseq_455868.dpx
        MB_udimsforthewin.1008.tx
```python
from synchronizer import utils
utils.get_sequence_files(file_path)
```