import boto3

def lambda_handler(event, context):
    #Connect to the API.
    ec2 = boto3.client('ec2')

    #Create a list of regions that we can iterate over
    regions = ec2.describe_regions().get('Regions')

    #Lets iterate over all regions and create snapshots for anything with a tag-name backup and a tag-value of true.
    for region in regions:
        print "Checking for volumes in %s" % region['RegionName']
        reg = region['RegionName']

        #Connect to each region and check for our volumes
        ec2 = boto3.client('ec2', region_name=reg)

        #Again, setting our filter for anything tagged backup: true
        result = ec2.describe_volumes(Filters=[{'Name': 'tag-key', 'Values': ['backup']}, {'Name': 'tag-value', 'Values': ['true', 'True']}])
        
        #Loop over our volumes return by our filter
        for volume in result['Volumes']:
            #Handle some common variables here for readability
            volumeid = volume['VolumeId']
            instanceid = volume['Attachments'][0]['InstanceId']
            az = volume['AvailabilityZone']

            print "Volume found, snapshotting Volume ID: %s from Instance ID: %s in Availability Zone: %s" % (volumeid, instanceid, az)
            #Creating Snapshot
            snap = ec2.create_snapshot(VolumeId=volumeid, Description="Snapshot created from EBS Snapshot Lambda")
