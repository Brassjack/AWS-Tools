#!/usr/bin/python
import boto3
import argparse
import datetime


def parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', "--region",
                        help="the region you're in. default: eu-west-1",
                        default='eu-west-1')
    parser.add_argument('-k', "--key",
                        help="AWS key")
    parser.add_argument('-s', "--secret",
                        help="AWS secret")
    parser.add_argument('-d', "--days",
                        help="older than this is deleted")
    return parser.parse_args()


def main():
    # Connect to AWS
    args = parsed_args()
    accountid =  boto3.client('sts').get_caller_identity()['Account']
    ec2 = boto3.client('ec2',
                       region_name=args.region,
                       aws_access_key_id=args.key,
                       aws_secret_access_key=args.secret,
                       )
    snapshots = ec2.describe_snapshots(OwnerIds=[accountid])['Snapshots']
    for snap in snapshots[:]:
        date_object = snap['StartTime']
        delta_date = datetime.timedelta(int(args.days))
        acceptable_date = datetime.datetime.now() - delta_date
        if date_object.replace(tzinfo=None) < acceptable_date:
            # Delete it here
            print("Deleting snapshot: " + snap['SnapshotId'] + " which was created: " + str(date_object))
            ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])


main()
