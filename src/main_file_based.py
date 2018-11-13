#!/usr/bin/env python
"""
Very brief demonstration of the type of exception raised by Neo4j when long strings are used in indices.

In this test case, specific inputs from a realistic dataset that was found to cause this problem is used.
"""

__author__ = "Athanasios Anastasiou"

import sys
import os
import neo4j
import neomodel


class SomeEntity(neomodel.StructuredNode):
    """
        A bare minimum entity specified in neomodel to demonstrate the error condition and how to enter it.
    """
    serial_num = neomodel.UniqueIdProperty()
    payload = neomodel.StringProperty(unique_index=True)


if __name__ == "__main__":
    # Get credentials
    try:
        username = os.environ["NEO4J_USERNAME"]
        password = os.environ["NEO4J_PASSWORD"]
    except KeyError:
        sys.stderr.write("ERROR: Please make sure that the NEO4J_USERNAME and NEO4J_PASSWORD environment variables"
                         " have been properly set for this session by using `export NEO4J_USERNAME=something`"
                         " and `export NEO4J_PASSWORD=something_else`.\n")
        sys.exit(1)

    # Connect to the database
    try:
        neomodel.db.set_connection("bolt://{}:{}@localhost:7687".format(username, password))
    except neo4j.exceptions.ServiceUnavailable:
        sys.stderr.write("ERROR: Please make sure that your Neo4j server is up and running.\n")

    # DEFINE PAYLOADS
    #
    # Some payloads that have been found to cause problems. The content of the string payload does not matter at all,
    # what matters is that:
    # 1. The payload contains Unicode characters.
    # 2. The payload's length is within certain limits
    #
    # The point here is how this error is handled depending on the length of the payload.
    #
    non_problematic_payload = u"The standard english phrase 'Hello World' translates to 'Χαίρε Κόσμε', in Greek \
but sounds odd, just like any other word-to-word translation does."

    with open("testcase1.txt", "rt", encoding="utf-8") as fd:
        problematic_payload_1 = fd.read()

    with open("testcase2.txt", "rt", encoding="utf-8") as fd:
        problematic_payload_2 = fd.read()

    # SCENARIO 1
    # Starting with a completely clean database but WITH the schema that is applied by running `establishmodels.sh`,
    # this node creation will succeed.
    try:
        SomeEntity(payload=non_problematic_payload).save()
    except neo4j.exceptions.DatabaseError:
        sys.stderr.write("ERROR: Creation of Node 1 failed. (Database should require restart).\n")

    # Then this node will be attempted to be created and it will ALSO succeed.
    # In actual fact, after creating this node, the database server is in a risky state already (judging by the logs)
    # NOTE: Please note, the payload here is `problematic_payload_1` with length 3933 and byte length 4059. 4059 is
    # smaller than 4095 which is supposed to be the maximum index key length.
    try:
        SomeEntity(payload=problematic_payload_1).save()
    except neo4j.exceptions.DatabaseError as e:
        sys.stderr.write(e.message)
    #
    # At this point, everything appears to be working normally. The server responds to simplistic queries such as :
    # `MATCH (a) return a limit 5;` but is already in an unstable state.
    # To demonstrate this, at this point run:
    # `MATCH (a) detach delete a;` (either using the browser or `$NEO4J_HOME/bin/cypher-shell`
    # The database still appears to be running normally at this point reporting that 2 nodes were deleted and if the
    # simplistic `MATCH (a) return a limit 5;` is attempted it will return with absolutely no complaints.... **BUT**
    #
    # Run this file again. Now the database is completely empty (after running the above query) and the script should
    # not return any errors, **BUT** at this point, the script fails on the creation OF THE FIRST NODE, which was not
    # even the one with the problematic payload, indicating that the node (or rather its index) were NOT affected by
    # the delete that took place above.
    #
    # To recover from this error, it is not enough to restart the database. The data directory has to be erased (or
    # rather, the file that stores the index of that attribute. This might create more problems than it attempts to
    # solve however, so better erase everything if this can be done).

    # SCENARIO 2
    # For a similar condition to the above but one that leaves the server in a usable state, substitute
    # `problematic_payload_1` with `problematic_payload_2`. This works fine. It is identified as a very long string to
    # be used in indexing, the error can be handled via the exception handling and the database responds predictably
    # to erase / re-query.