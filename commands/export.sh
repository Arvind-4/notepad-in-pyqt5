#!/bin/bash

poetry config warnings.export false

poetry export --without-hashes --without-urls | awk '{ print $1 }' FS=';' > requirements.txt

poetry export --without-hashes --without-urls --with dev | awk '{ print $1 }' FS=';' > requirements-dev.txt