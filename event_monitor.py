from kubernetes import config, dynamic
from kubernetes.client import api_client

import traceback
import sys
import datetime
from datetime import timedelta
import pytz
from pytz import timezone

def check_monitoring_time(event_time):
    previous_date = datetime.datetime.utcnow() - timedelta(minutes=30)

    return event_time > previous_date

nodeEventList = ['NodeNotReady','FailedNodeAllocatableEnforcement','HostPortConflict','ContainerFCFailed','Rebooted']

def main():
    try:
        client = dynamic.DynamicClient(
            api_client.ApiClient(configuration=config.load_kube_config())
        )

        v1_events = client.resources.get(api_version='v1', kind='Event')

        event_list = v1_events.get()

        for event in event_list.items:
            converted_date = datetime.datetime.strptime(event.metadata.creationTimestamp,"%Y-%m-%dT%H:%M:%SZ")
            converted_date_utc = pytz.utc.localize(converted_date)

            if check_monitoring_time(converted_date) == True:
                converted_date_kst = converted_date_utc.astimezone(timezone('Asia/Seoul')).strftime("%Y-%m-%dT%H:%M:%SZ")

                if event.involvedObject.kind == "Node" and event.reason in nodeEventList:
                    print(converted_date_kst,"|",event.involvedObject.kind,"|",event.metadata.name,"|",event.reason,"|",event.note)
            
    except Exception as e:
        traceback.print_exc()

if __name__ == '__main__':
    main()
