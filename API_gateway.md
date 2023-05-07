# AWS API Gateway

We use AWS API Gateway to allow users and the frontend to interface with our backend.

# /answer_questions
Using a POST request, we trigger the `TunaBackend` state machine.
The response is the `executionArn` of our request.

The input should be:
```
{
    "stateMachineArn": <Arn for the TunaBackend Arn>,
    "input": "{"UseDocumentRetrieval": "true", {"data": {"text_inputs": "How do I bake a pizza?"}}}"
}
```

The response should look like:
```
{
    "executionArn": <arn>
    "timestamp": ...
}
```

# /execution_history
Using a POST request, we get the output of the `TunaBackend` execution that corresponds to the given `executionArn`

The input should look like:
```
{
    "executionArn": <arn>
}
```

The output should look like:
```
[
    "Preheat an oven to 400...
    ...
]
```