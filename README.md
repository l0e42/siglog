# SIGLOG Monthly Newsletter Generator

- Given a newsletter in the format described below, in a file called `209-anything.txt`
- Use `python3 process.py 209` to compile
- Then run `python3 html.py` to generate the webpage
- Then run `python3 html.py email` to generate the email
- Then run `python3 tex.py` to generate the tex

## Format

<pre>

# For the master render date
  -dd date 

# For verbatim dates to be added (from previous newsletters)
  -dM Name: date


Acronym: Title
  Meta data
  Meta data
Type of Announcement # first word determines TOC (CALL FOR ..., JOBS, ANNOUNCEMENT)
* ELEMENT
  continuation of element
* Other element
  continuation of element
  - Sub list
  - Sub list
* Yet another element (Perhaps about dates!)
  -d Date name: date  # Preferred format Mon Day, Year. Shown only here
  -dH Date name: date  # Acronym: date (Date name) goes in special dates header
  -dv Date name: verbatim date # System will not try to parse the date (necessary for date ranges)

Another Acronym: Another Title that comes after at least one clear line
  etc!
</pre>


## Non-standard Dependencies

* `dateparser` from pip
* `css-inliner` from [here](https://github.com/turanct/css-inliner)