Synchronizer's Docs
========================================
A collection of utilities for CGI-VFX to copy files from one place to another, find out basic stat differences between them and handle file sequences and textures (with tx files).

Installation
---------------
    .. code-block:: python

        pip install synchronizer

Getting Started
-----------------

These are some examples of what can be done. For further info please see the API reference which goes really into depth into each function.

1. Process paths
    Copies ``src_path`` to ``trg_path``. Takes both files and directories as source. 
    If given source is a file and it's part of a sequence it'll find and copy 
    the entire sequence of files.

    .. code-block:: python
    
        from synchronizer import copier
        copier.process_paths(src_path, trg_path, force_overwrite=True, **kwargs)
        '''
        kwargs:
        include_tx = True
        only_tx = True
        find_sequence = True
        '''

2. Sync status
    Compares two files or directory paths and return sync status. Sync status 
    refers to ``name`` and ``os.stat()`` comparisons.

    .. code-block:: python
    
        from synchronizer import syncstatus
        syncstatus.get_sync_status(
            src_path, trg_path,
            ignore_name=False,
            ignore_stats=['st_uid', 'st_gid', 'st_atime',
                    'st_ctime', 'st_ino', 'st_dev'])

3. Get most recent
    Compares two paths and returns whichever has the most recent stat time.
    Default stat used for comparison is ``st_mtime`` which is: Time of most 
    recent content modification.

    .. code-block:: python

        from synchronizer import syncstatus
        syncstatus.get_most_recent(src_path, trg_path, use_stat='st_mtime')


4. Get sequence files
    Find and return all files that are part of a sequence matching ``file_path``.
    If no sequence found, returns ``None``. Two files are enough to make a sequence,
    even if they're not sequential. This assumes the sequence digits are right 
    beside the file extension.

    e.g.:
        - C_myfile_v568.jpg
        - MJ_thisisafileseq_455868.dpx
        - MB_udimsforthewin.1008.tx
    
    .. code-block:: python

        from synchronizer import utils
        utils.get_sequence_files(file_path)


.. toctree::
   :maxdepth: 3
   :caption: API Reference
   
   copier
   syncstatus
   utilities

.. toctree::
   :maxdepth: 3
   :caption: Changelog and Roadmap
   
   roadmap
   changelog
