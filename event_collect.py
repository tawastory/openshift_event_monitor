from kubernetes import config, dynamic
from kubernetes.client import api_client

import traceback
import sys
import datetime

def main():
    try:
        client = dynamic.DynamicClient(
            api_client.ApiClient(configuration=config.load_kube_config())
        )

        v1_events = client.resources.get(api_version='v1', kind='Event')

        event_list = v1_events.get()

        for event in event_list.items:
            print(event.metadata.creationTimestamp,"|",event.metadata.name,"|",event.reason,"|",event.note)
            
    except Exception as e:
        traceback.print_exc()

if __name__ == '__main__':
    main()
