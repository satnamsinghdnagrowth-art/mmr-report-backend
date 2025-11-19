consolidateDataResponse = {}


def saveResponse(reportId, responseData: dict):
    global consolidateDataResponse
    consolidateDataResponse[reportId] = responseData
    return consolidateDataResponse
