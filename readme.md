Download all ClassDojo photos and videos in your timeline.

This script was written originally by kecebongsoft. This version is based on a modified [GitHub Gist by Guy Kloss](https://gist.github.com/dedy-purwanto/6ad1fa7c702981f35f25da780c50914d).

How it works:

1. Fetch list of items in the timeline, if there are multiple pages,
   it will fetch for all pages.
2. Collect list of URLs for the attachment for each item
3. Download the files into local temporary directory, and also save
   the timeline activity as a json file.

How to use:

1. Modify the session cookie in this script, check your session cookie
   by opening [ClassDojo](https://www.classdojo.com) in browser and copy the following cookies:
   dojo_log_session_id, dojo_login.sid, and dojo_home_login.sid
2. Run this script and wait for it to finish.

If error happens:

1. I ran this script in windows, make sure your path is correct if you
   are on linux
2. Make sure "classdojo_output" directory exists in the same folder as
   this script
3. Make sure you have a correct session cookies set in this script.
4. Make sure you can open the FEED_URL listed in this script from
   within your browser (assuming you can open ClassDojo website)