import os
import sys

import requests
from setuptools import find_packages, setup


def download_file(url, outfile):
    """
    Download a file from a url and save it to outfile

    Args: 
        url (str): url of file to download
        outfile (str): path to save file to
    """
    print("Downloading {0} to {1}".format(url, outfile))
    headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
    r = requests.get(url, stream=True, headers=headers)
    with open(outfile, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)


on_rtd = os.environ.get('READTHEDOCS') == 'True'
shift_only = False
if "--shift-only" in sys.argv:
    shift_only = True
    sys.argv.remove("--shift-only")

if on_rtd:
    setup(
        name="SpecMatch-Emp",
        version="0.3",
        packages=find_packages(),
        include_package_data=True
    )
else:
    setup(
        name="SpecMatch-Emp",
        version="0.3",
        packages=find_packages(),
        install_requires=[
        ],
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'smemp=specmatchemp.cli:main'
            ],
        },
    )

    HOMEDIR = os.path.expanduser("~")
    SPECMATCHDIR = "{0}/.specmatchemp/".format(HOMEDIR)

    # download library
    if not shift_only:
        if not os.path.exists(SPECMATCHDIR):
            os.mkdir(SPECMATCHDIR)

        def reporthook(blocknum, blocksize, totalsize):
            readsofar = blocknum * blocksize
            if totalsize > 0:
                percent = readsofar * 1e2 / totalsize
                s = "\r%5.1f%% %*d / %d" % (
                    percent, len(str(totalsize)), readsofar, totalsize)
                sys.stderr.write(s)
                if readsofar >= totalsize:  # near the end
                    sys.stderr.write("\n")
            else:  # total size is unknown
                sys.stderr.write("read %d\n" % (readsofar,))

        LIBPATH = os.path.join(SPECMATCHDIR,
                               "library.h5")
        if not os.path.exists(LIBPATH):
            download_file("https://www.dropbox.com/s/po0kzgjn1j9ha2v/library.h5#", LIBPATH)

    # Additional csv files
    csv_url_list = ["https://www.dropbox.com/s/8wv38eb8dzg1ou2/hires_telluric_mask.csv#",
                    "https://www.dropbox.com/s/ugqzpux73mgjuyj/detrend.csv#",
                    "https://www.dropbox.com/s/lxz0cb57a8xvsfl/uncertainties.csv#"]
    for csv_url in csv_url_list:
        outfile = os.path.join(SPECMATCHDIR,
                               csv_url.split('/')[-1][:-1]
                               )
        download_file(csv_url, outfile)

    specdir = os.path.join(SPECMATCHDIR, 'shifted_spectra')
    if not os.path.exists(specdir):
        os.mkdir(specdir)
        # download references
        ref_url_list = ["https://www.dropbox.com/s/4aygfh3qnmorws1/nso_adj.fits#",
                    "https://www.dropbox.com/s/sgkqhwe2kfm9yvp/j26.532_adj.fits#",
                    "https://www.dropbox.com/s/lthwgat0e2s4gqu/j72.718_adj.fits#",
                    "https://www.dropbox.com/s/vqqjlcnw7duuq54/j59.1926_adj.fits#"]
        for ref_url in ref_url_list:
            outfile = os.path.join(specdir,
                                   ref_url.split('/')[-1][:-1]
                                   )
            download_file(ref_url, outfile)
