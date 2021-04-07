import json
import boto3

s3 = boto3.client('s3')


def block_assignment_from_units(assignment, unit_to_block_mapping):
    """ Create block assignment file from given districtr assignment

    Args:
        assignment (dict<str, int>): mapping between districtr units (blockgroups/precincts) and 
                                     district ids
        unit_to_block_mapping (dict<str, str>): mapping between districtr units ids (GEOIDS, etc.)
                                                and block geoids

    Returns:
        dict<str, int>: mapping between block geoids and district ids
    """
    block_assignment = {}
    for unit, dist in assignment.items():
        for block in unit_to_block_mapping[unit]:
            block_assignment[block] = dist
    return block_assignment


def lambda_handler(event, context):
    # TODO implement
    bucket = "districtr"
    state = event["state"].lower().replace(" ", "_")
    units = event["units"]
    assignment = event["assignment"]
    key = "block_assign/{}_{}.json".format(state, units)
    
    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        state_mapping = json.load(data['Body'])
        block_assignment = block_assignment_from_units(assignment, state_mapping)
        return {
            'statusCode': 200,
            'body': json.dumps(block_assignment)
        }
    
    except Exception as e:
        print(e)
        raise e
    