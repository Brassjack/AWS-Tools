#!/usr/bin/python
import boto3
import datetime
import argparse


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
    client = boto3.client('rds',
                          region_name=args.region,
                          aws_access_key_id=args.key,
                          aws_secret_access_key=args.secret,
                          )
    response = client.describe_db_snapshots()
    list_snapshots = response['DBSnapshots']
    for snap in list_snapshots:
        # Only want to delete the manual snapshots
        if snap['SnapshotType'] == 'automated':
            continue
        date_object = snap['SnapshotCreateTime']
        delta_date = datetime.timedelta(days=int(args.days))
        acceptable_date = datetime.datetime.now() - delta_date
        if date_object.replace(tzinfo=None) < acceptable_date:
            # Delete it here
            print "Deleting snapshot: " + snap['DBSnapshotIdentifier']
            client.delete_db_snapshot(snap['DBSnapshotIdentifier'])


main()
