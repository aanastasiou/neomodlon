#!/bin/bash

#Athanasios Anastasiou Nov 2018
#A very simple script that leverages on neomodel's tools to establish the schema on the neo4j database
#Note that for this script to work, the environment variables NEO4J_USERNAME and NEO4J_PASSWORD should be set.

neomodel_install_labels main.py --db bolt://$NEO4J_USERNAME:$NEO4J_PASSWORD@localhost:7687
