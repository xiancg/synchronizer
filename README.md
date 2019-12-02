# Synchronizer

CGI utilities to copy files from one place to another, find out basic stat differences between them and handle file sequences and textures (tx files).

# Basic Usage:
1. Copies src_path to trg_path. Takes both files and directories as source. If given source is a file and it's part of a sequence it'll find and copy the entire sequence of files.
```python
from synchronizer import copier
copier.processpaths(src_path, trg_path, force_overwrite=True, **kwargs)
```
kwargs: 
    include_tx = True
    only_tx = True
    find_sequence = True`

2. Compares two files or directory paths and return sync status. Sync status refers to name and os.stat() comparisons
```python
from synchronizer import syncstatus
syncstatus.get_sync_status(
            src_path, trg_path,
            ignore_name=False,
            ignore_stats=['st_uid', 'st_gid', 'st_atime',
                    'st_ctime', 'st_ino', 'st_dev'])
```

2. Compares two paths and returns whichever has the most recent stat time. Default stat used for comparison is st_mtime which is: Time of most recent content modification.
```python
from synchronizer import syncstatus
syncstatus.get_most_recent(src_path, trg_path, use_stat='st_mtime')
```

