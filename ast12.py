import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, left={self.left}, right={self.right})"

# Helper function to handle parentheses and logical operators properly
def create_rule(rule_string):
    # Normalize spaces in the rule string
    rule_string = re.sub(r'\s+', ' ', rule_string).strip()

    # Parse condition (field operator value)
    def parse_condition(condition):
        match = re.match(r'(\w+)\s*([><=]+)\s*([\w\'"]+)', condition)
        if match:
            return Node("operand", value=(match.group(1), match.group(2), match.group(3).strip("'\"")))
        raise ValueError(f"Invalid condition: {condition}")

    # Parse logical expressions with parentheses
    def parse_rule(rule_string):
        rule_string = rule_string.strip()

        # Base case: if no parentheses are present, parse the condition directly
        if '(' not in rule_string and ')' not in rule_string:
            # Handle logical operators (AND, OR)
            if ' AND ' in rule_string:
                parts = rule_string.split(' AND ', 1)
                return Node("operator", parse_rule(parts[0]), parse_rule(parts[1]), 'AND')
            elif ' OR ' in rule_string:
                parts = rule_string.split(' OR ', 1)
                return Node("operator", parse_rule(parts[0]), parse_rule(parts[1]), 'OR')
            else:
                return parse_condition(rule_string)

        # Handle parentheses and recursive parsing
        open_parens = 0
        for i, char in enumerate(rule_string):
            if char == '(':
                open_parens += 1
            elif char == ')':
                open_parens -= 1

            # Split at the outermost AND/OR outside parentheses
            if open_parens == 0 and (' AND ' in rule_string[i:] or ' OR ' in rule_string[i:]):
                if ' AND ' in rule_string[i:]:
                    parts = rule_string.split(' AND ', 1)
                    return Node("operator", parse_rule(parts[0]), parse_rule(parts[1]), 'AND')
                elif ' OR ' in rule_string[i:]:
                    parts = rule_string.split(' OR ', 1)
                    return Node("operator", parse_rule(parts[0]), parse_rule(parts[1]), 'OR')

        # Recursively parse the inner expression within parentheses
        if rule_string.startswith('(') and rule_string.endswith(')'):
            return parse_rule(rule_string[1:-1])

    return parse_rule(rule_string)

def evaluate_rule(ast, data):
    if ast.type == "operand":
        field, operator, value = ast.value
        field_value = data.get(field)

        # Debug print to see values during evaluation
        print(f"Evaluating condition: field={field}, operator={operator}, value={value}, field_value={field_value}")

        # Handle type conversion
        try:
            if field_value is not None and isinstance(field_value, str) and field_value.replace('.', '', 1).isdigit():
                field_value = float(field_value)
            if value.replace('.', '', 1).isdigit():
                value = float(value)
            else:
                value = str(value)
        except ValueError:
            pass

        # Perform the comparison
        if operator == ">":
            return field_value > value
        elif operator == "<":
            return field_value < value
        elif operator == "=":
            return field_value == value
        elif operator == ">=":
            return field_value >= value
        elif operator == "<=":
            return field_value <= value
        elif operator == "!=":
            return field_value != value

    elif ast.type == "operator":
        print(f"Evaluating logical operator: {ast.value}")
        if ast.value == "AND":
            return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
        elif ast.value == "OR":
            return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)
    
    return False
