CKAN DCAT Amsterdam
=====================

This CKAN extension adds the DCAT metadata fields to the datasets as well as some Amsterdam-specific settings

This project was developed by [Civity](http://www.civity.nl) and DataLab Amsterdam.

Installation
------------
Install this extension in your CKAN instance is as easy as installing any other CKAN extension.

>  Download the source code and install the extension manually. To do so, execute the following commands:
> ```
> $ git clone https://github.com/datalab/ckanext-dcatAmsterdam.git
> $ cd ckanext-dcatAmsterdam
> $ python setup.py install
> ```

* **Note**: Dont forget to activate your virtual environment
```
. /usr/lib/ckan/default/bin/activate
```


* Modify your configuration file (generally in `/etc/ckan/default/production.ini`) and add `dcatAmsterdam` in the `ckan.plugins` property.
```
ckan.plugins = <OTHER_PLUGINS> dcatAmsterdam
```
* Restart your server
* That's All!

