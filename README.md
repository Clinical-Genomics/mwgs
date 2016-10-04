#MWGS
##QC-pipeline for microbial whole genome sequencing

###Folder structure and naming convention

```
<project>
│
└───<sample_name>
	│
    └───<sample_name>..._1.fastq.gz
	│
	└───<sample_name>..._2.fastq.gz
```

###Usage
```
mwgs.py /path_to/sample_folder/
```

###Output
- Fraction of reads aligned to reference genome
- Duplication rate
- Median insert size

###Requirements
- Python 3.x
- Java 1.7
- Picard 1.141
- Samtools
- BWA


###Example config file
```
$ cat config.py
LIMS_URI = 'https://example-lims.domain.com'
LIMS_USER = 'lims_user'
LIMS_PASSWORD = 'lims_password'
ENTREZ_EMAIL = 'user@example.com' #Can be any email-address
#System specific constants
REF_FOLDER = '/mnt/hds/proj/bioinfo/MICROBIAL/REFERENCES/'
PICARD_JAR = '/mnt/hds/proj/bioinfo/MICROBIAL/picard-tools-1.141/picard.jar'
JAVA = '/mnt/hds/proj/bioinfo/mip/modules/jre1.7.0_45/bin/java'
```
