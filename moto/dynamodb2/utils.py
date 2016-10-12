from __future__ import unicode_literals


def parse_filter_expression(expression, attr_names, attr_values):
    # {"FilterExpression": "#n0 = :v0", "ExpressionAttributeValues": {":v0": {"BOOL": false}}, "ExpressionAttributeNames": {"#n0": "ready"}}

    if ' AND ' in expression:
        lhs, rhs = expression.split(' AND ', 1)
        if 'BETWEEN' in lhs:
            return parse_filter_expression(expression.replace(' AND ', ' _AND_ ', 1), attr_names, attr_values)
        else:
            results = parse_filter_expression(lhs.strip(), attr_names, attr_values)
            results.update(parse_filter_expression(rhs.strip(), attr_names, attr_values))
            return results
    else:
        expression_components = expression.strip('()').split()
        if 'BETWEEN' in expression:
            comparison_operator = 'BETWEEN'
            comparison_values = [attr_values[expression_components[2]], attr_values[expression_components[4]]]
        elif 'IN' in expression:
            comparison_operator = 'IN'
            comparison_values = [attr_values[comp.strip('(),')] for comp in expression_components[2:]]
        else:
            comparison_operator = expression_components[1]
            comparison_values = [attr_values[expression_components[2]]]

        return {attr_names[expression_components[0]]: (comparison_operator, comparison_values)}