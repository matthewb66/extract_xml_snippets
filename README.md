# Synopsys Create Snippets from XML files Script - extract_xml_snippets.py
# INTRODUCTION

This script is provided under an OSS license as an example of how to use the Black Duck APIs to ignore snippet matches.

It does not represent any extension of licensed functionality of Synopsys software itself and is provided as-is, without warranty or liability.

# DESCRIPTION

The `extract_xml_snippets.py` script extracts embedded source code from XML formatted files for snippet analysis.

The scan location will default to the invocation folder (or can be specified) and file extensions to be scanned must be specified.
The code extract files will be created in the `.snippet_scan` created under the scan folder (or can be specified as a different location).
If this folder exists then the script will terminate; alternatively a delete option can be specified.

The scan process will search for `<language>XXX</language>` entries and will extract the code within the <body> section.
Currently the language C++ is supported and will write .cpp files for the code extracts. Additional languages can be added by changing the code.

# PREREQUISITES

Python 3 and the Black Duck https://github.com/blackducksoftware/hub-rest-api-python package must be installed and configured to enable the Python API scripts for Black Duck prior to using this script.

An API key for the Black Duck server must also be configured in the `.restconfig.json` file in the package folder.

# USAGE

The `extract_xml_snippets.py` script can be invoked as follows:

    usage: extract_xml_snippets.py [-h] -s SOURCEPATH
                               [-e [EXTENSION [EXTENSION ...]]] [-d]
                               [-o OUTPUTFOLDER]

    Extract source embedded within specified XML format files into .snippet_scan
    folder (or -o folder) ready for snippet analysis using Detect script.

    optional arguments:
      -h, --help            show this help message and exit
      -s SOURCEPATH, --sourcepath SOURCEPATH
                            Path to scan
      -e [EXTENSION [EXTENSION ...]], --extension [EXTENSION [EXTENSION ...]]
                            File extension(s) to scan for (multiple extensions can
                            be specified)
      -d, --deletesnippetfolder
                        Delete .snippet_scan folder if it exists
      -o OUTPUTFOLDER, --outputfolder OUTPUTFOLDER
                        Specify output folder (default .snippet_scan)

# SNIPPET ANALYSIS

After the script has created the code extract files in the .snippet_scan folder, the Synopsys Detect script can be used to perform snippet analysis.

# EXAMPLE EXECUTION

Consider a source location /opt/user/mysource which contains the file `myfile.esx` with the following embedded source segment:

    <region xmi:id="_nBcJgPMNEeiMwvLnGvgCsg" name="Region1">
	   <transition xmi:id="_nBcJgvMNEeiMwvLnGvgCsg" name="ping" kind="internal" source="_0m9ZdPMMEeiMwvLnGvgCsg" target="_0m9ZdPMMEeiMwvLnGvgCsg">
		 <effect xmi:type="uml:OpaqueBehavior" xmi:id="_yjoaUPMNEeiMwvLnGvgCsg" name="Effect">
		   <language>C++</language>
		   <body>namespace quickbook&#xD;
    {&#xD;
        string_stream::string_stream()&#xD;
            : buffer_ptr(new std::string())&#xD;
            , stream_ptr(new ostream(boost::iostreams::back_inserter(*buffer_ptr.get())))&#xD;
        {}&#xD;
    }</body>
		</effect>
	  </transition>
	</region>

Use the following command to extract the segment to a snippet file:

    python3 examples/extract_xml_snippets.py -s /opt/user/mysource -e .esx

This will create the folder /opt/user/mysource/.snippet_scan containing the file `myfile_esx_snip1.cpp` with the following contents:

	namespace quickbook
	{
		string_stream::string_stream()
			: buffer_ptr(new std::string())
		, stream_ptr(new ostream(boost::iostreams::back_inserter(*buffer_ptr.get())))
		{}
	}
