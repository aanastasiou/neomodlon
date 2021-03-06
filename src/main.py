#!/usr/bin/env python
"""
Very brief demonstration of the type of exception raised by Neo4j when long strings are used in indices.
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

    problematic_payload_1 = u"Το Lorem Ipsum είναι απλά ένα κείμενο χωρίς νόημα για τους επαγγελματίες της τυπογραφίας \
και στοιχειοθεσίας. Το Lorem Ipsum είναι το επαγγελματικό πρότυπο όσον αφορά το κείμενο χωρίς νόημα, από τον 15ο αιώνα \
, όταν ένας ανώνυμος τυπογράφος πήρε ένα δοκίμιο και ανακάτεψε τις λέξεις για να δημιουργήσει ένα δείγμα βιβλίου. Όχι \
μόνο επιβίωσε πέντε αιώνες, αλλά κυριάρχησε στην ηλεκτρονική στοιχειοθεσία, παραμένοντας με κάθε τρόπο αναλλοίωτο. \
Έγινε δημοφιλές τη δεκαετία του '60 με την έκδοση των δειγμάτων της Letraset όπου περιελάμβαναν αποσπάσματα του Lorem \
Ipsum, και πιο πρόσφατα με το λογισμικό ηλεκτρονικής σελιδοποίησης όπως το Aldus PageMaker που περιείχαν εκδοχές του \
Lorem Ipsum.\nΓιατί το χρησιμοποιούμε;\nΕίναι πλέον κοινά παραδεκτό ότι ένας αναγνώστης αποσπάται από το περιεχόμενο \
που διαβάζει, όταν εξετάζει τη διαμόρφωση μίας σελίδας. Η ουσία της χρήσης του Lorem Ipsum είναι ότι έχει λίγο-πολύ \
μία ομαλή κατανομή γραμμάτων, αντίθετα με το να βάλει κανείς κείμενο όπως 'Εδώ θα μπει κείμενο, εδώ θα μπει κείμενο', \
κάνοντάς το να φαίνεται σαν κανονικό κείμενο. Πολλά λογισμικά πακέτα ηλεκτρονικής σελιδοποίησης και επεξεργαστές \
ιστότοπων πλέον χρησιμοποιούν το Lorem Ipsum σαν προκαθορισμένο δείγμα κειμένου, και η αναζήτησ για τις λέξεις 'lorem \
ipsum'  στο διαδίκτυο θα αποκαλύψει πολλά web site που βρίσκονται στο στάδιο της δημιουργίας. Διάφορες εκδοχές έχουν \
προκύψει με το πέρασμα των χρόνων, άλλες φορές κατά λάθος, άλλες φορές σκόπιμα (με σκοπό το χιούμορ και άλλα συναφή).\n\
Απο που προέρχεται;\n\
Αντίθετα με αυτό που θεωρεί η πλειοψηφία, το Lorem Ipsum δεν είναι απλά ένα τυχαίο κείμενο. Οι ρίζες του βρίσκονται σε \
ένα κείμενο Λατινικής λογοτεχνίας του 45 π.Χ., φτάνοντας την ηλικία του πάνω από 2000 έτη. Ο Richard McClintock, \
καθηγητής Λατινικών στο κολλέγιο Hampden-Dydney στην Βιρτζίνια, αναζήτησε μία από τις πιο σπάνιες Λατινικές λέξεις, \
την consectetur, από ένα απόσπασμα του Lorem Ipsum, και ανάμεσα σε όλα τα έργα της κλασσικής λογοτεχνίας, ανακάλυψε \
την αναμφισβήτητη πηγή του. To Lorem Ipsum προέρχεται από τις ενότητες 1.10.32 και 1.10.33 του 'de Finibus Bonorum et \
Malorum' (Τα άκρα του καλού και του κακού) από τον Cicero (Σισερό), γραμμένο το 45 π.Χ. Αυτό το βιβλίο είναι μία \
διατριβή στην θεωρία της Ηθικής, πολύ δημοφιλής κατά την αναγέννηση. Η πρώτη γραμμή του Lorem Ipsum, 'Lorem ipsum \
dolor sit amet...', προέρχεται από μία γραμμή στην ενότητα 1.10.32."

    problematic_payload_2 = u"Το Lorem Ipsum είναι απλά ένα κείμενο χωρίς νόημα για τους επαγγελματίες της τυπογραφίας \
και στοιχειοθεσίας. Το Lorem Ipsum είναι το επαγγελματικό πρότυπο όσον αφορά το κείμενο χωρίς νόημα, από τον 15ο αιώνα \
, όταν ένας ανώνυμος τυπογράφος πήρε ένα δοκίμιο και ανακάτεψε τις λέξεις για να δημιουργήσει ένα δείγμα βιβλίου. Όχι \
μόνο επιβίωσε πέντε αιώνες, αλλά κυριάρχησε στην ηλεκτρονική στοιχειοθεσία, παραμένοντας με κάθε τρόπο αναλλοίωτο. \
Έγινε δημοφιλές τη δεκαετία του '60 με την έκδοση των δειγμάτων της Letraset όπου περιελάμβαναν αποσπάσματα του Lorem \
Ipsum, και πιο πρόσφατα με το λογισμικό ηλεκτρονικής σελιδοποίησης όπως το Aldus PageMaker που περιείχαν εκδοχές του \
Lorem Ipsum.\nΓιατί το χρησιμοποιούμε;\nΕίναι πλέον κοινά παραδεκτό ότι ένας αναγνώστης αποσπάται από το περιεχόμενο \
που διαβάζει, όταν εξετάζει τη διαμόρφωση μίας σελίδας. Η ουσία της χρήσης του Lorem Ipsum είναι ότι έχει λίγο-πολύ \
μία ομαλή κατανομή γραμμάτων, αντίθετα με το να βάλει κανείς κείμενο όπως 'Εδώ θα μπει κείμενο, εδώ θα μπει κείμενο', \
κάνοντάς το να φαίνεται σαν κανονικό κείμενο. Πολλά λογισμικά πακέτα ηλεκτρονικής σελιδοποίησης και επεξεργαστές \
ιστότοπων πλέον χρησιμοποιούν το Lorem Ipsum σαν προκαθορισμένο δείγμα κειμένου, και η αναζήτησ για τις λέξεις 'lorem \
ipsum'  στο διαδίκτυο θα αποκαλύψει πολλά web site που βρίσκονται στο στάδιο της δημιουργίας. Διάφορες εκδοχές έχουν \
προκύψει με το πέρασμα των χρόνων, άλλες φορές κατά λάθος, άλλες φορές σκόπιμα (με σκοπό το χιούμορ και άλλα συναφή).\n\
Απο που προέρχεται;\n\
Αντίθετα με αυτό που θεωρεί η πλειοψηφία, το Lorem Ipsum δεν είναι απλά ένα τυχαίο κείμενο. Οι ρίζες του βρίσκονται σε \
ένα κείμενο Λατινικής λογοτεχνίας του 45 π.Χ., φτάνοντας την ηλικία του πάνω από 2000 έτη. Ο Richard McClintock, \
καθηγητής Λατινικών στο κολλέγιο Hampden-Dydney στην Βιρτζίνια, αναζήτησε μία από τις πιο σπάνιες Λατινικές λέξεις, \
την consectetur, από ένα απόσπασμα του Lorem Ipsum, και ανάμεσα σε όλα τα έργα της κλασσικής λογοτεχνίας, ανακάλυψε \
την αναμφισβήτητη πηγή του. To Lorem Ipsum προέρχεται από τις ενότητες 1.10.32 και 1.10.33 του 'de Finibus Bonorum et \
Malorum' (Τα άκρα του καλού και του κακού) από τον Cicero (Σισερό), γραμμένο το 45 π.Χ. Αυτό το βιβλίο είναι μία \
διατριβή στην θεωρία της Ηθικής, πολύ δημοφιλής κατά την αναγέννηση. Η πρώτη γραμμή του Lorem Ipsum, 'Lorem ipsum \
dolor sit amet...', προέρχεται από μία γραμμή στην ενότητα 1.10.32.\nΠου μπορώ να βρώ μερικές;\nΥπάρχουν πολλές \
εκδοχές των αποσπασμάτων του Lorem Ipsum διαθέσιμες, αλλά η πλειοψηφία τους έχει δεχθεί κάποιας μορφής αλλοιώσεις, με \
ενσωματωμένους αστεεισμούς, ή τυχαίες λέξεις που δεν γίνονται καν πιστευτές. Εάν πρόκειται να χρησιμοποιήσετε ένα \
κομμάτι του Lorem Ipsum, πρέπει να είστε βέβαιοι πως δεν βρίσκεται κάτι προσβλητικό κρυμμένο μέσα στο κείμενο. Όλες οι \
γεννήτριες Lorem Ipsum στο διαδίκτυο τείνουν να επαναλαμβάνουν προκαθορισμένα κομμάτια του Lorem Ipsum κατά απαίτηση, \
καθιστώνας την παρούσα γεννήτρια την πρώτη πραγματική γεννήτρια στο διαδίκτυο. Χρησιμοποιεί ένα λεξικό με πάνω από 200 \
λατινικές λέξεις, συνδυασμένες με ένα εύχρηστο μοντέλο σύνταξης προτάσεων, ώστε να παράγει Lorem Ipsum που δείχνει \
λογικό. Από εκεί και πέρα, το Lorem Ipsum παραμένει πάντα ανοιχτό σε επαναλήψεις, ενσωμάτωση χιούμορ, μη κατανοητές \
λέξεις κλπ.\
Το καθιερωμένο κομμάτι του Lorem Ipsum που χρησιμοποιείται από τον 15ο αιώνα αναπαράγεται παρακάτω για αυτούς που \
ενδιαφέρονται. Οι ενότητες 1.10.32 και 1.10.33 από το de Finibus Bonorum et Malorum' από τον Σισερό επίσης \
αναπαράγονται στην ακριβή αυθεντική τους μορφή, συνοδευόμενες από Αγγλικές εκδοχές από την μετάφραση του 1914 \
από τον H. Rackham."

    # SCENARIO 1
    # Starting with a completely clean database but WITH the schema that is applied by running `establishmodels.sh`,
    # this node creation will succeed.
    try:
        SomeEntity(payload=non_problematic_payload).save()
    except neo4j.exceptions.DatabaseError:
        sys.stderr.write("ERROR: Creation of Node 1 failed. (Database should require restart).\n")

    # Then this node will be attempted to be created and it will ALSO succeed.
    # In actual fact, after creating this node, the database server is in a risky state already (judging by the logs)
    # NOTE: Please note, the payload here is `problematic_payload_1` with length 2387 and byte length 4076. 4076 is
    # smaller than 4095 which is supposed to be the maximum index key length.
    try:
        SomeEntity(payload=problematic_payload_1).save()
    except neo4j.exceptions.DatabaseError as e:
        sys.stderr.write(e.message)

    # AT THIS POINT:
    # The database server will behave as if nothing is wrong, so go ahead and erase everything with:
    # `match (a) detach delete a;` (No complaints here as well, only 1 node will be reported as being deleted).
    # Run this script again.
    # This time around, creation of the FIRST NODE will fail with something like:
    # org.neo4j.io.pagecache.CursorException: Read unreliable key, keySize=4084, keyValueSizeCap=4047,
    # keyHasTombstone=false, offset=3442, pos=0 | GB+Tree[file:[blahblahblah]/data/databases/
    # debug_affiliation.db/schema/index/lucene_native-2.0/1/string-1.0/index-1, layout:StringLayout[version:0.1,
    # identifier:24016946018123776], generation:4/6]
    # org.neo4j.io.pagecache.CursorException: Read unreliable key, keySize=4084, keyValueSizeCap=4047,
    # keyHasTombstone=false, offset=3442, pos=0 | GB+Tree[file:[blahblahblah]data/databases/debug_affiliation.db/
    # schema/index/lucene_native-2.0/1/string-1.0/index-1, layout:StringLayout[version:0.1,
    # identifier:24016946018123776], generation:4/6]

    # # SCENARIO 2
    # # If you are trying to run Scenario 2 right after Scenario 1 THEN DO THE FOLLOWING FIRST:
    # #  1. Stop the database
    # #  2. Remove the database directory from $NEO4J_HOME/data/databases/
    # #  3. Restart the database
    # #  4. Run `establishmodels.sh` again, so that the indices become effective
    # #  5. Comment SCENARIO 1
    # #
    # # So, entering scenario 2, again with a completely clean database state, creation of the first node is successful.
    # try:
    #     SomeEntity(payload=non_problematic_payload).save()
    # except neo4j.exceptions.DatabaseError:
    #     sys.stderr.write("ERROR: Creation of Node 1 failed. (Database should require restart).\n")
    #
    # # But when attempting to create this second node (with a bigger payload this time), an exception will be raised
    # # with a hint to what is actually going wrong: The fact that the index length is finite and the length of the string
    # # is larger than that. The "problem" here is that the length of the string is reported in bytes which of course
    # # does not depend on the length of the string in a straightforward way due to the way Unicode characters are
    # # represented.
    # # NOTE: Please note, the payload here is `problematic_payload_2` with length 3610 and byte length 6198. 6198 is
    # # much larger than 4095 and this works fine.
    # try:
    #     SomeEntity(payload=problematic_payload_2).save()
    # except neo4j.exceptions.DatabaseError as e:
    #     sys.stderr.write(e.message)
    #
    # # AT THIS POINT:
    # # This time around, the database is left in working order and is possible to recover from the error gracefully.