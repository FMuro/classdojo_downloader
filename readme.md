Download all ClassDojo photos and videos in your timeline.

This script was written originally by kecebongsoft. This version is based on a modified [GitHub Gist by Guy Kloss](https://gist.github.com/dedy-purwanto/6ad1fa7c702981f35f25da780c50914d).

How it works:

1. Fetch list of items in the timeline, if there are multiple pages,
   it will fetch for all pages.
2. Collect list of URLs for the attachment for each item.
3. Download the files into local temporary directory, and also save
   the timeline activity as a `.json` file.

How to use:

1. Run the script `dojodownload.py`.
2. Follow the instructions.
3. Wait for the download to finish.

At the end, you'll see a temporary folder `tmp*` within the folder where you run the script. This folder contains two subfolders:

- `images` contains all photos and viewos.
- `text_files` contains parents's comments and other data.