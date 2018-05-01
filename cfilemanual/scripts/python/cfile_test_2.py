from qualtricsparser import QualtricsParser

q = QualtricsParser(qual_export="./MyQualtricsDownload/cfile_test_2.csv")
q.parse_at_marks()
q.parse_marked_data()
