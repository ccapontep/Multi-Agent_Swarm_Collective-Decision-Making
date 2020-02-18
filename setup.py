from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["config/*"]

setup(name = "pysage",
      version = "100",
      description = "a simple simulator for mobile agents",
      author = "Vito Trianni",
      author_email = "vito.trianni@istc.cnr.it",
      url = "http://www.istc.cnr.it/people/vito-trianni",
      # Name the folder where your packages live:
      #(If you have other packages (dirs) or modules (py files) then
      #put them into the package directory - they will be found 
      #recursively.)
      packages = ['pysage'],
      #'src' package must contain files (see list above)
      #I called the package 'package' thus cleverly confusing the whole issue...
      #This dict maps the package name =to=> directories
      #It says, package *needs* these files.
      package_data = {'pysage' : files },
      #'[pysage' is in the root.
      scripts = ["run_pysage"],
      long_description = """A simple simulator for mobile agents."""
      #
      #This next part it for the Cheese Shop, look a little down the page.
      #classifiers = []     
) 
