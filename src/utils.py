import os
import git
import requests

def make_sha_filename(basename, ext):
    """
    Generate a filename with the current git commit SHA.
    
    Args:
        basename (str): The base name of the file.
        ext (str): The file extension.
    
    Returns:
        str: Filename with SHA and potential '-dirty' suffix if uncommitted changes are present.
    """
    repo = git.Repo(search_parent_directories=True)
    head_commit_id = repo.head.commit.hexsha[:10]
    is_dirty = repo.is_dirty()
    postfix = f"{head_commit_id}-dirty" if is_dirty else head_commit_id
    return f"{basename}-{postfix}{ext}"

def download_file(url, dir_path, filename, force_download=False):
    """
    Download a file if it has not been downloaded already.
    
    Args:
        url (str): The URL to download from.
        dir_path (str): Directory to save the file.
        filename (str): Name of the file to save.
        force_download (bool): Force download even if the file is present.
    
    Returns:
        str: Full path of the downloaded file.
    """
    dirfile = os.path.join(dir_path, filename)
    os.makedirs(dir_path, exist_ok=True)
    
    if os.path.isfile(dirfile) and not force_download:
        print(" ... already downloaded ... ")
    else:
        if os.path.isfile(dirfile):
            os.remove(dirfile)
        print(" ... downloading ... ")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(dirfile, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    return dirfile
