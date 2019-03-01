# Data conversion tools for the Avida Digital Evolution Platform

Avida is a digital evolution platform in which self-replicating computer programs
(digital organisms) compete, mutate, and evolve. Find the Avida software platform
[here](https://avida.devosoft.org/) or on [GitHub](https://github.com/devosoft/avida).
Read more about Avida in [(Ofria and Wilke, 2004)](https://doi.org/10.1162/106454604773563612) 
or [(Ofria et al., 2009)](https://doi.org/10.1007/978-1-84882-285-6_1).

This repository contains tools for converting from default Avida output formats to
the [ALife standard data formats](https://github.com/alife-data-standards/alife-data-standards).

## Example Data

Find some example Avida data and the converted standard form of that data in [./example_data/](./example_data/).
The `.spop` files are Avida population files (default Avida output files). They

## Phylogeny/Lineage Converter

At the moment, there's only a Python implementation available.

### Python

The phylogeny (and lineage) data conversion tool can be found in
[./avida_converters/phylogeny.py](./avida_converters/phylogeny.py). 

#### Usage

[./avida_converters/phylogeny.py](./avida_converters/phylogeny.py) can be used as
either a stand-alone script or be imported into your own python script.

Stand-alone usage:

``` bash
usage: phylogeny.py [-h] [-output OUTPUT] [-format FORMAT] [-minimal]
                    [-list_formats]
                    input

Avida .spop to ALife standard-compliant phylogeny converter.

positional arguments:
  input                 Input avida .spop file.

optional arguments:
  -h, --help            show this help message and exit
  -output OUTPUT, -out OUTPUT
                        Name to assign to standard-compliant output file.
  -format FORMAT        What standard file format should this script output?
                        Valid options: ['csv', 'json']
  -minimal              Store minimal data in output file.
  -list_formats, -lsf   List available output formats.
```

## References

Ofria, C., & Wilke, C. O. (2004). Avida: A Software Platform for Research in Computational Evolutionary Biology. Artificial Life, 10(2), 191–229. <https://doi.org/10.1162/106454604773563612>

Ofria, C., Bryson, D. M., & Wilke, C. O. (2009). Avida: A software platform for research in computational evolutionary biology. In Artificial Life Models in Software (Vol. 10, pp. 3–35). London: Springer London. <https://doi.org/10.1007/978-1-84882-285-6_1>