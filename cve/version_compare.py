import re
from packaging import version

def compare_versions(installed, condition):
    """
    Checks if installed version satisfies a CVE condition.
    Examples of condition input:
        '<= 2.4.54'
        '>= 1.18.0'
        '= 5.2.1'
        '< 3.1.4'
    """

    match = re.match(r"(<=|>=|<|>|=|==)\s*([\d\.]+)", condition)
    if not match:
        return False

    operator, vulnerable_version = match.groups()
    installed_v = version.parse(installed)
    target_v = version.parse(vulnerable_version)

    if operator in ("=", "=="):
        return installed_v == target_v
    if operator == "<":
        return installed_v < target_v
    if operator == "<=":
        return installed_v <= target_v
    if operator == ">":
        return installed_v > target_v
    if operator == ">=":
        return installed_v >= target_v

    return False
