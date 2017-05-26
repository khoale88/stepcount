
def process(input_path, xml_filename, output_path=None):
    import os
    if output_path is None:
        output_path = input_path
    if "xml" in xml_filename:
        csv_filename = xml_filename[:-4] + '.csv'
    #reformat the paths
    input_path = os.path.abspath(input_path)
    input_path = os.path.join(input_path, xml_filename)

    output_path = os.path.abspath(output_path)
    output_path = os.path.join(output_path, csv_filename)

    # if os.path.exists(input_path):
    #     os.remove(input_path)
    if os.path.exists(output_path):
        os.remove(output_path)

    result = count_from_xml(input_path)
    write_result_csv(output_path, result)
    return output_path

def count_from_xml(input_path):
    import xml.etree.ElementTree as ET
    tree = ET.parse(input_path)
    root = tree.getroot()

    # source name (user), value, unit, creation date, start day, end date, type
    result = {}

    # source_name = None
    current = {}
    for child in root:
        if child.tag == "Record":
            attrib = child.attrib
            # check user (sourName), if new user create new
            source_name = attrib['sourceName']
            if attrib['sourceName'] not in result:
                result[source_name] = {}

            # get current user data from result
            current = result[source_name]

            # check if an activity type is new, if new create new
            acti_type = attrib['type']
            if acti_type not in current:
                current[acti_type] = {}

            # check if an activity day is new, if new create new day
            acti_day = attrib['startDate'].split(" ")[0]
            if acti_day not in current[acti_type]:
                aday = {}
                aday["unit"] = attrib['unit']
                # check type and map accordingly
                if attrib['unit'] == "count":
                    value = int(attrib['value'])
                elif attrib['unit'] == "mi":
                    value = float(attrib['value'])
                else:
                    value = attrib['value']
                aday['value'] = value
                # assign back the aday
                current[acti_type][acti_day] = aday
            else:
                unit = current[acti_type][acti_day]['unit']
                if unit == 'count':
                    current[acti_type][acti_day]['value'] += int(attrib['value'])
                elif unit == 'mi':
                    current[acti_type][acti_day]['value'] += float(attrib['value'])
            result[source_name] = current
    return result

def write_result_csv(output_path, result):
    with open(output_path, 'w') as f:
        headers = ['user', 'activity type', 'day', 'value', 'unit']
        f.write(','.join(headers) + '\n')
        for user in result:
            for acti_type in result[user]:
                for acti_day in result[user][acti_type]:
                    line = []
                    line.append(user)
                    line.append(acti_type)
                    line.append(acti_day)
                    line.append(str(result[user][acti_type][acti_day]['value']))
                    line.append(result[user][acti_type][acti_day]['unit'])
                    # line = [user, acti_type, acti_day, acti_day['value'], acti_day['unit']]
                    line = [item.encode('ascii', 'ignore') for item in line]
                    str_line = ','.join(line) + '\n'
                    f.write(str_line)
    f.close()
