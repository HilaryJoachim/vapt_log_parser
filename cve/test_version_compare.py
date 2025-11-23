from cve.version_compare import compare_versions

tests = [
    ("2.4.29", "<= 2.4.54"),
    ("7.1.0", "< 7.0.0"),
    ("1.18.0", ">= 1.17.0"),
    ("5.0.1", "= 5.0.1"),
]

for installed, rule in tests:
    print(installed, rule, "=>", compare_versions(installed, rule))
