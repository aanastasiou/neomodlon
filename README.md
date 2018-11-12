# The length of string node attributes when used as indices in Neo4J and its validation

When using a string attribute as part of an `index` or `unique_index` in Neo4j, then the length of that string cannot 
be infinite.

This causes certain problems and has an impact to:

1. The way `neomodel` does validation
2. Neo4j itself

The code in this repository demonstrates how to put the server in these problematic conditions and also suggests a fix.


# The problem

In Neo4J, node attributes of type `string` can contain what appears to be infinitely long strings as valid inputs. 
But when the same property is used in an index, Neo4J imposes a (perfectly valid) limit on the number of characters 
that can be used in the index. 

This limit appears to be 4095 **bytes** as reported by exceptions.

This **byte** length, is **not** equal to the number of characters in the string as it would be returned by Python's 
`len`. This is because [Unicode](https://en.wikipedia.org/wiki/Unicode) characters *can* use more than one bytes per 
character to map the character of a specific language to its glyph.

The problem is that when the **byte length** of the string is <4095 characters but close to that limit, the transaction 
**does go ahead**, absolutely no error is reported but the database enters an unrecoverable state.

*Unrecoverable* here means that the database has to be restarted. In my personal experience, a simple restart is not 
enough and the database data directory has to be removed as well.


# Fixing the problem

A simple remedy for the problem is to trim the length of a string attribute that is going to be used for indexing 
to the appropriate length. This cannot be done with a simple truncation because this might render multi-byte characters
invalid.

However, it turns out that trimming at the 4095 limit (strictly) still produces some errors in a way that suggests that 
something else may be added to the key, once the attribute has crossed the wire and is at the server. For this reason, 
the current function is trimming at 4000 characters (but unfortunately, even this seems to be causing problems).
