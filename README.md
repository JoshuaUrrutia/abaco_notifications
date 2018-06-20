# Add a notification for a generic HTTP callback

```shell
$ python add_notify_requestbin.py data-sd2e-community /sample/tacc-cloud
assocationIds = 1573501675986751976-242ac114-0001-002
notification id: 1447480736450407960-242ac118-0001-011
notification url: https://requestbin.agaveapi.co/1n1rknb1
```

# Upload a new file to the destination

```shell
$ files-upload -F $(python get_cat.py) -S data-sd2e-community /sample/tacc-cloud
```

# Inspect hit log for the requestbin

```shell
$ requestbin-requests-list -V 1n1rknb1

[
  {
    "content_length": 685,
    "body": "{\"file\":{\"name\":\"572.png\",\"uuid\":\"4471370744494297576-242ac113-0001-002\",\"owner\":\"sd2eadm\",\"internalUsername\":null,\"lastModified\":\"2018-06-20T11:37:38.000-05:00\",\"source\":\"http://129.114.97.130/572.png\",\"path\":\"sample/tacc-cloud/572.png\",\"status\":\"STAGING_QUEUED\",\"systemId\":\"data-sd2e-community\",\"nativeFormat\":\"raw\",\"_links\":{\"self\":{\"href\":\"https://api.sd2e.org/files/v2/media/system/data-sd2e-community//sample/tacc-cloud/572.png\"},\"system\":{\"href\":\"https://api.sd2e.org/systems/v2/data-sd2e-community\"},\"profile\":{\"href\":\"https://api.sd2e.org/profiles/v2/sd2eadm\"},\"history\":{\"href\":\"https://api.sd2e.org/files/v2/history/system/data-sd2e-community//sample/tacc-cloud/572.png\"}}}}",
    "form_data": [],
    "remote_addr": "129.114.99.64",
    "method": "POST",
    "headers": {
      "Content-Length": "685",
      "X-Forwarded-Server": "agaveapi.co",
      "X-Newrelic-Id": "UA4CVl9RGwIJU1NXAQgG",
      "X-Forwarded-Host": "requestbin.agaveapi.co",
      "X-Forwarded-For": "129.114.99.64",
      "X-Newrelic-Transaction": "PxRUBQcBXFFTVgNUAglVUgIEFB8EBw8RVU4aAVxZVlZRBgsDB1QLAFBQAkNKQQ5SAVUDWgEEFTs=",
      "User-Agent": "Agave-Hookbot/null",
      "Host": "requestbin.agaveapi.co",
      "X-Forwarded-Proto": "https",
      "X-Agave-Notification": "1447480736450407960-242ac118-0001-011",
      "Content-Type": "application/json",
      "X-Agave-Delivery": "4566847871779344872-242ac118-0001-042",
      "Accept-Encoding": "gzip,deflate"
    },
    "content_type": "application/json",
    "time": 1529512660.367105,
    "query_string": {},
    "path": "/1n1rknb1",
    "id": "12ckez"
  }
]
```

The files service generates a *POST* event!

Here is the POST body, formatted for human consumption:

```json
{
  "file": {
    "name": "572.png",
    "uuid": "4471370744494297576-242ac113-0001-002",
    "owner": "sd2eadm",
    "internalUsername": null,
    "lastModified": "2018-06-20T11:37:38.000-05:00",
    "source": "http://129.114.97.130/572.png",
    "path": "sample/tacc-cloud/572.png",
    "status": "STAGING_QUEUED",
    "systemId": "data-sd2e-community",
    "nativeFormat": "raw",
    "_links": {
      "self": {
        "href": "https://api.sd2e.org/files/v2/media/system/data-sd2e-community//sample/tacc-cloud/572.png"
      },
      "system": {
        "href": "https://api.sd2e.org/systems/v2/data-sd2e-community"
      },
      "profile": {
        "href": "https://api.sd2e.org/profiles/v2/sd2eadm"
      },
      "history": {
        "href": "https://api.sd2e.org/files/v2/history/system/data-sd2e-community//sample/tacc-cloud/572.png"
      }
    }
  }
}
```

Since this notification subscribes to all events (`*`), it catches all actions, which is why this initial
event is `STAGING_QUEUED`. Consulting the SD2E Logtrail, I can see that the `STAGING_COMPLETE` action also was triggered.

# Add a notification for a TACC Reactor

```shell
$ python add_notify_reactor.py data-sd2e-community /sample/tacc-cloud gO0JeWaBM4p3J
assocationIds = 1573501675986751976-242ac114-0001-002
notification id: 1447480736450407960-242ac118-0001-011
notification url: https://requestbin.agaveapi.co/1n1rknb1
```

# Upload a new file to the destination

```shell
$ files-upload -F $(python get_cat.py) -S data-sd2e-community /sample/tacc-cloud
```

:star: The reactor will fire!

# Other events

Delete one of the cat pictures you've uploaded. The requestbin as well as the
Reactor should trigger.

