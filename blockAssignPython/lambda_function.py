import json
import boto3

s3 = boto3.client('s3')


def block_assignment_from_blockgroups(assignment, blockgroup_mapping):
    """ Create block assignment file from given districtr assignment

    Args:
        assignment (dict<str, int>): mapping between districtr units and district ids
        blockgroup_mapping (dict<str, str>): mapping between blockgroups geoids and block geoids

    Returns:
        dict<str, int>: mapping between block geoids and district ids
    """
    block_assignment = {}
    for bg, dist in assignment.items():
        for block in blockgroup_mapping[bg]:
            block_assignment[block] = dist
    return block_assignment


def lambda_handler(event, context):
    # TODO implement
    bucket = "districtr"
    state = event["state"]
    units = event["units"]
    assignment = event["assignment"]
    key = "block_assign/{}_{}.json".format(state, units)
    
    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        state_mapping = json.load(data['Body'])
        block_assignment = block_assignment_from_blockgroups(assignment, state_mapping)
        return {
            'statusCode': 200,
            'body': json.dumps(block_assignment)
        }
    
    except Exception as e:
        print(e)
        raise e
    