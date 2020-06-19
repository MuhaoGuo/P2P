s = [2, "12347", "MeterValues",

       {"connectorId": 1,
        "transactionId": 111,
        "meterValue":List=field(default_factory=[
            {"timestamp":"2020-06-07T05:59:07.967228"},
            {"sampledValue":[{"value":"2"}]}
        ])
        }]

s = [2, "12347", "MeterValues",{"connectorId": 1,"transactionId": 111,"meterValue":field([{"timestamp":"2020-06-07T05:59:07.967228"},{"sampledValue":[{"value":"2"}]}])}]
print(s[150:])



[2,"12347", "MeterValues",{"connectorId": 1, "transactionId": 111, "meterValue":List=field(default_factory=[{"timestamp":"2020-06-07T05:59:07.967228"},{"sampledValue":[{"value":"2"}]}])}]