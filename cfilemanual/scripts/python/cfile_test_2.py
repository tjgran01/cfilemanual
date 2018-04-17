from qualtricsparser import QualtricsParser

q = QualtricsParser(cond_file="./MyQualtricsDownload/cfile_test_2.csv")
q.parse_at_marks()
q.parse_marked_data()
