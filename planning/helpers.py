itemcode_regex_pattern = "^[a-z0-9]+([_-]?[a-z0-9])*$"
plan_regex_pattern = "^[a-z0-9A-Z]+([ _-]?[a-z0-9A-Z])*$"
name_regex_pattern = "^[a-z0-9A-Z]+([ ]?[a-z0-9A-Z])*$"
integer_regex_pattern = "^[0-9]+$"
uom_regex_pattern = "^[a-z]+$"
float_regex_pattern = "^[-+]?([0-9]+(\.[0-9]+)?|\.[0-9]+)$"

def regex_pattern_match(pattern, text):
    import re
    return re.match(pattern, text)