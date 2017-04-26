import httplib2
from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow

def get_credential():
  # For this example, the client id and client secret are command-line arguments.
  client_id = "973852989413-e775gmsn91q9g9el36t9260hc3ba4t9u.apps.googleusercontent.com"
  client_secret = "Nlnh4KrrmdtWOIXAw8FJ3t1S"

  # The scope URL for read/write access to a user's calendar data
  scope = 'https://www.googleapis.com/auth/analytics.readonly'

  # Create a flow object. This object holds the client_id, client_secret, and
  # scope. It assists with OAuth 2.0 steps to get user authorization and
  # credentials.
  flow = OAuth2WebServerFlow(client_id, client_secret, scope)

  storage = Storage('credentials.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())

  http = httplib2.Http()
  http = credentials.authorize(http)
  # Build the Analytics Reporting API V4 authorized service object.
  analyticsReporting = build(
      'analyticsreporting',
      'v4',
      http=http,
      discoveryServiceUrl='https://analyticsreporting.googleapis.com/$discovery/rest')

  return analyticsReporting

def urlData(analyticsReporting,token):
    try:
        response = analyticsReporting.reports().batchGet(

            body={
                "reportRequests": [
                    {
                        "viewId": "65709396",
                        "dateRanges": [
                            {
                                "startDate": "2016-09-29",
                                "endDate": "2016-09-30"
                            }
                        ],
                        "metrics": [
                            {
                                "expression": "ga:pageValue"
                            },
                            {
                                "expression": "ga:pageviews"

                            },
                            {
                                "expression": "ga:entrances"

                            },
                            {
                                "expression": "ga:entranceRate"

                            },
                            {
                                "expression": "ga:pageviewsPerSession"

                            },
                            {
                                "expression": "ga:uniquePageviews"

                            },
                            {
                                "expression": "ga:timeOnPage"

                            },
                            {
                                "expression": "ga:avgTimeOnPage"

                            },
                            {
                                "expression": "ga:exits"

                            },
                            {
                                "expression": "ga:exitRate"

                            },
                        ],
                        "dimensions": [
                            {
                                "name": "ga:pagePath"
                            }
                            ],
                        "dimensionFilterClauses":[{
                            "operator" :"AND",
                            "filters": [{
                                "dimension_name": "ga:pagePath",
                                "not": True,
                                "operator": "PARTIAL",
                                "expressions": ["LoginAndRegistration"]
                            },
                            {
                                "dimension_name": "ga:pagePath",
                                "not": True,
                                "operator": "PARTIAL",
                                "expressions": ["customersupport"]

                            },
                            {
                                "dimension_name": "ga:pagePath",
                                "not": False,
                                "operator": "REGEXP",
                                "expressions": ["\/[a-z-]*\/[0-9a-z-]*\/[0-9]+[?]+"]
                            }
                            ]
                        }],
                        "pageToken":token,
                        "pageSize": 1000,

                    }

                ]
            }
        ).execute()
    except AccessTokenRefreshError:
        # The AccessTokenRefreshError exception is raised if the credentials
        # have been revoked by the user or they have expired.
        print('The credentials have been revoked or expired, please re-run the application to re-authorize')

    return response

def skuData(analyticsReporting,token):
    try:
        response = analyticsReporting.reports().batchGet(

            body={
                "reportRequests": [
                    {
                        "viewId": "65709396",
                        "dateRanges": [
                            {
                                "startDate": "2016-07-26",
                                "endDate": "2016-07-26"
                            }],
                        "metrics": [
                            {
                                "expression": "ga:itemQuantity"
                            },
                            {
                                 "expression":"ga:uniquePurchases"
                            },
                            {
                                "expression": "ga:revenuePerItem"
                            },
                            {
                                "expression": "ga:itemRevenue"
                            },

                            {
                                "expression": "ga:itemsPerPurchase"
                            },
                            {
                                "expression": "ga:productRevenuePerPurchase"
                            },

                        ],
                        "dimensions": [
                            {
                                  "name": "ga:productSku"
                            }
                        ],
                        "pageToken": token,
                        "pageSize": 1000,
                    }
                ]
            }
        ).execute()
    except AccessTokenRefreshError:
        # The AccessTokenRefreshError exception is raised if the credentials
        # have been revoked by the user or they have expired.
        print('The credentials have been revoked or expired, please re-run the application to re-authorize')

    return response

