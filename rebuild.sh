#!/bin/bash

cd js_sources
bash ./mk_megascript.sh
cd ../templates
bash mk_templates.sh
cd ../