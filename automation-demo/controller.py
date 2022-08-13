import requests
import urllib3
import time
from getpass import getpass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONTROLLER_FQDN="https://nginxcontroller.westeurope.cloudapp.azure.com"
DEBUG=True

def main_procedure():
    user=""
    passw=""
    session = auth_controller(user, passw)
    create_app1_ifconfig(session)
    create_app2_httpbin(session)
    create_app3_devcentral_app(session)
    create_app4_waffler(session)
    create_app5_petstore(session)
    # ask if cleanup needed
    if question("Cleanup?"):
        cleanup(session)

    


def question(q):
    i = 0
    while i < 2:
        answer = input(q+" (yes or no): ")
        if any(answer.lower() == f for f in ["yes", 'y', '1', 'ye']):
            return 1
        elif any(answer.lower() == f for f in ['no', 'n', '0']):
            return 0
        else:
            i += 1
            if i < 2:
                print('Please enter yes or no')
            else:
                return 0

def create_app1_ifconfig(session):
    #
    # Create GW1
    #
    endpoint = "/api/v1/services/environments/prod/gateways/gw-gcp-app-1"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
    {
        "metadata": {
            "name": "gw-gcp-app-1",
            "tags": []
        },
        "desiredState": {
            "configSnippets": {},
            "ingress": {
            "placement": {
                "instanceGroupRefs": [
                {
                    "ref": "/infrastructure/instance-groups/gcp-app"
                }
                ]
            },
            "uris": {
                "http://app1.test.com": {}
            }
            }
        }
        }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("GW1 Created")
    time.sleep(5)

    # Create App1
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app1"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
    {
    "metadata": {
        "name": "gcp-demo-app1",
        "displayName": "",
        "description": "",
        "tags": []
    },
    "desiredState": {}
    }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("App1 Created")
    time.sleep(5)

    # 
    # Create App Comp 1
    #
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app1/components/gcp-demo-app1-comp1"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
        {
        "metadata": {
            "name": "gcp-demo-app1-comp1",
            "tags": []
        },
        "desiredState": {
            "backend": {
            "ntlmAuthentication": "DISABLED",
            "preserveHostHeader": "DISABLED",
            "workloadGroups": {
                "wl_ifconfig": {
                "loadBalancingMethod": {
                    "type": "ROUND_ROBIN"
                },
                "uris": {
                    "https://ifconfig.me": {
                    "isBackup": false,
                    "isDown": false,
                    "isDrain": false
                    }
                }
                }
            }
            },
            "ingress": {
            "gatewayRefs": [
                {
                "ref": "/services/environments/prod/gateways/gw-gcp-app-1"
                }
            ],
            "uris": {
                "/": {}
            }
            },
            "logging": {
            "accessLog": {
                "state": "DISABLED"
            },
            "errorLog": "DISABLED"
            },
            "security": {
            "strategyRef": {
                "ref": "/security/strategies/balanced_default"
            },
            "waf": {
                "isEnabled": false,
                "isMonitorOnly": false,
                "signatureOverrides": {}
            }
            },
            "programmability": {
            "requestHeaderModifications": [
                {
                "action": "ADD",
                "headerName": "Host",
                "headerValue": "ifconfig.me"
                }
            ]
            }
        }
        }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("App Component1 Created")
    time.sleep(5)

def create_app2_httpbin(session):
    #
    # Create GW2
    #
    endpoint = "/api/v1/services/environments/prod/gateways/gw-gcp-app-2"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
    {
        "metadata": {
            "name": "gw-gcp-app-2",
            "tags": []
        },
        "desiredState": {
            "configSnippets": {},
            "ingress": {
            "placement": {
                "instanceGroupRefs": [
                {
                    "ref": "/infrastructure/instance-groups/gcp-app"
                }
                ]
            },
            "uris": {
                "http://app2.test.com": {}
            }
            }
        }
        }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("GW2 Created")
    time.sleep(5)

    # Create App2
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app2"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
    {
    "metadata": {
        "name": "gcp-demo-app2",
        "displayName": "",
        "description": "",
        "tags": []
    },
    "desiredState": {}
    }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("App2 Created")
    time.sleep(5)

    # 
    # Create comp
    #
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app2/components/gcp-demo-app2-comp1"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
        {
        "metadata": {
            "name": "gcp-demo-app2-comp1",
            "tags": []
        },
        "desiredState": {
            "backend": {
            "ntlmAuthentication": "DISABLED",
            "preserveHostHeader": "DISABLED",
            "workloadGroups": {
                "wl_httpbin": {
                "loadBalancingMethod": {
                    "type": "ROUND_ROBIN"
                },
                "uris": {
                    "http://httpbin.org": {
                    "isBackup": false,
                    "isDown": false,
                    "isDrain": false
                    }
                }
                }
            }
            },
            "ingress": {
            "gatewayRefs": [
                {
                "ref": "/services/environments/prod/gateways/gw-gcp-app-2"
                }
            ],
            "uris": {
                "/": {}
            }
            },
            "logging": {
            "accessLog": {
                "state": "DISABLED"
            },
            "errorLog": "DISABLED"
            },
            "security": {
            "strategyRef": {
                "ref": "/security/strategies/balanced_default"
            },
            "waf": {
                "isEnabled": true,
                "isMonitorOnly": false,
                "signatureOverrides": {}
            }
            }
        }
        }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("App Component2 Created")
    time.sleep(5)

def create_app3_devcentral_app(session):
    #
    # Create GW3
    #
    endpoint = "/api/v1/services/environments/prod/gateways/gw-gcp-app-3"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
        {
        "metadata": {
            "name": "gw-gcp-app-3",
            "tags": []
        },
        "desiredState": {
            "configSnippets": {
            "httpSnippet": {
                "directives": [
                {
                    "directive": "map",
                    "args": [
                    "$http_upgrade",
                    "$connection_upgrade"
                    ],
                    "block": [
                    {
                        "directive": "default",
                        "args": [
                        "upgrade"
                        ]
                    },
                    {
                        "directive": "",
                        "args": [
                        "close"
                        ]
                    }
                    ]
                }
                ]
            }
            },
            "ingress": {
            "placement": {
                "instanceGroupRefs": [
                {
                    "ref": "/infrastructure/instance-groups/gcp-app"
                }
                ]
            },
            "uris": {
                "http://app3.test.com": {}
            }
            }
        }
        }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("GW3 Created")
    time.sleep(5)

    # Create App3
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app3"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
    {
    "metadata": {
        "name": "gcp-demo-app3",
        "displayName": "",
        "description": "",
        "tags": []
    },
    "desiredState": {}
    }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("App3 Created")
    time.sleep(5)

    # 
    # Create comp 3
    #
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app3/components/gcp-demo-app3-comp1"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
        {
        "metadata": {
            "name": "gcp-demo-app3-comp1",
            "tags": []
        },
        "desiredState": {
            "configSnippets": {
            "uriSnippets": [
                {
                "directives": [
                    {
                    "directive": "proxy_set_header",
                    "args": [
                        "Upgrade",
                        "$http_upgrade"
                    ]
                    },
                    {
                    "directive": "proxy_set_header",
                    "args": [
                        "Connection",
                        "$connection_upgrade"
                    ]
                    }
                ]
                }
            ]
            },
            "backend": {
            "ntlmAuthentication": "DISABLED",
            "preserveHostHeader": "DISABLED",
            "workloadGroups": {
                "wl_docker": {
                "loadBalancingMethod": {
                    "type": "ROUND_ROBIN"
                },
                "uris": {
                    "http://10.138.0.5/": {
                    "isBackup": false,
                    "isDown": false,
                    "isDrain": false
                    }
                }
                }
            }
            },
            "ingress": {
            "gatewayRefs": [
                {
                "ref": "/services/environments/prod/gateways/gw-gcp-app-3"
                }
            ],
            "uris": {
                "/": {}
            }
            },
            "logging": {
            "accessLog": {
                "state": "DISABLED"
            },
            "errorLog": "DISABLED"
            },
            "security": {
            "strategyRef": {
                "ref": "/security/strategies/balanced_default"
            },
            "waf": {
                "isEnabled": false,
                "isMonitorOnly": false,
                "signatureOverrides": {}
            }
            }
        }
        }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("App Component3 Created")
    time.sleep(5)

def create_app4_waffler(session):
    #
    # Create GW4
    #
    endpoint = "/api/v1/services/environments/prod/gateways/gw-gcp-app-4"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
    {
        "metadata": {
            "name": "gw-gcp-app-4",
            "tags": []
        },
        "desiredState": {
            "configSnippets": {},
            "ingress": {
            "placement": {
                "instanceGroupRefs": [
                {
                    "ref": "/infrastructure/instance-groups/gcp-app"
                }
                ]
            },
            "uris": {
                "http://app4.test.com": {}
            }
            }
        }
        }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("GW4 Created")
    time.sleep(5)

    # Create App4
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app4"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
    {
    "metadata": {
        "name": "gcp-demo-app4",
        "displayName": "",
        "description": "",
        "tags": []
    },
    "desiredState": {}
    }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("App4 Created")
    time.sleep(5)

    # 
    # Create App Comp 4
    #
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app4/components/gcp-demo-app4-comp1"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
        {
        "metadata": {
            "name": "gcp-demo-app4-comp1",
            "tags": []
        },
        "desiredState": {
            "backend": {
            "ntlmAuthentication": "DISABLED",
            "preserveHostHeader": "DISABLED",
            "workloadGroups": {
                "wl_waffler_docker": {
                "loadBalancingMethod": {
                    "type": "ROUND_ROBIN"
                },
                "uris": {
                    "http://10.138.0.5:8080/": {
                    "isBackup": false,
                    "isDown": false,
                    "isDrain": false
                    }
                }
                }
            }
            },
            "ingress": {
            "gatewayRefs": [
                {
                "ref": "/services/environments/prod/gateways/gw-gcp-app-4"
                }
            ],
            "uris": {
                "/": {}
            }
            },
            "logging": {
            "accessLog": {
                "state": "DISABLED"
            },
            "errorLog": "DISABLED"
            },
            "security": {
            "strategyRef": {
                "ref": "/security/strategies/balanced_default"
            },
            "waf": {
                "isEnabled": false,
                "isMonitorOnly": false,
                "signatureOverrides": {}
            }
            },
            "programmability": {
            }
        }
        }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("App 4 Component1 Created")
    time.sleep(5)

def create_app5_petstore(session):
    #
    # Create GW4
    #
    endpoint = "/api/v1/services/environments/prod/gateways/gw-gcp-app-5"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
    {
        "metadata": {
            "name": "gw-gcp-app-5",
            "tags": []
        },
        "desiredState": {
            "configSnippets": {},
            "ingress": {
            "placement": {
                "instanceGroupRefs": [
                {
                    "ref": "/infrastructure/instance-groups/gcp-app"
                }
                ]
            },
            "uris": {
                "http://app5.test.com": {}
            }
            }
        }
        }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("GW5 Created")
    time.sleep(5)

    # Create App1
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app5"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
    {
    "metadata": {
        "name": "gcp-demo-app5",
        "displayName": "",
        "description": "",
        "tags": []
    },
    "desiredState": {}
    }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("App5 Created")
    time.sleep(5)

    # 
    # Create App Comp 1
    #
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app5/components/gcp-demo-app5-comp1"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
        {
        "metadata": {
            "name": "gcp-demo-app5-comp1",
            "tags": []
        },
        "desiredState": {
            "backend": {
            "ntlmAuthentication": "DISABLED",
            "preserveHostHeader": "DISABLED",
            "workloadGroups": {
                "wl_waffler_docker": {
                "loadBalancingMethod": {
                    "type": "ROUND_ROBIN"
                },
                "uris": {
                    "https://petstore.swagger.io/": {
                    "isBackup": false,
                    "isDown": false,
                    "isDrain": false
                    }
                }
                }
            }
            },
            "ingress": {
            "gatewayRefs": [
                {
                "ref": "/services/environments/prod/gateways/gw-gcp-app-5"
                }
            ],
            "uris": {
                "/": {}
            }
            },
            "logging": {
            "accessLog": {
                "state": "DISABLED"
            },
            "errorLog": "DISABLED"
            },
            "programmability": {
            "requestHeaderModifications": [
                {
                "action": "ADD",
                "headerName": "Host",
                "headerValue": "petstore.swagger.io"
                }
            ]
            },
            "security": {
            "strategyRef": {
                "ref": "/security/strategies/strategy_swagger_petstore"
            },
            "waf": {
                "isEnabled": true
            }
            }
        }
        }
    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("App 5 Component1 Created")
    time.sleep(5)


def cleanup(session):
    print("Cleanup...")

    # Delete comp 5
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app5/components/gcp-demo-app5-comp1"
    endpoint = CONTROLLER_FQDN+endpoint
    headers = { 'content-type': "application/json" }
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)
    # Delete App5
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app5"
    endpoint = CONTROLLER_FQDN+endpoint
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)
    # Delete GW5
    endpoint = "/api/v1/services/environments/prod/gateways/gw-gcp-app-5"
    endpoint = CONTROLLER_FQDN+endpoint
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)
    # Delete comp 4
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app4/components/gcp-demo-app4-comp1"
    endpoint = CONTROLLER_FQDN+endpoint
    headers = { 'content-type': "application/json" }
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)
    # Delete App4
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app4"
    endpoint = CONTROLLER_FQDN+endpoint
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)
    # Delete GW4
    endpoint = "/api/v1/services/environments/prod/gateways/gw-gcp-app-4"
    endpoint = CONTROLLER_FQDN+endpoint
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)

    # Delete comp 3
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app3/components/gcp-demo-app3-comp1"
    endpoint = CONTROLLER_FQDN+endpoint
    headers = { 'content-type': "application/json" }
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)
    # Delete App3
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app3"
    endpoint = CONTROLLER_FQDN+endpoint
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5) 
    # Delete GW3
    endpoint = "/api/v1/services/environments/prod/gateways/gw-gcp-app-3"
    endpoint = CONTROLLER_FQDN+endpoint
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)

    # Delete comp 2
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app2/components/gcp-demo-app2-comp1"
    endpoint = CONTROLLER_FQDN+endpoint
    headers = { 'content-type': "application/json" }
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)
    # Delete App2
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app2"
    endpoint = CONTROLLER_FQDN+endpoint
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)
    # Delete GW2
    endpoint = "/api/v1/services/environments/prod/gateways/gw-gcp-app-2"
    endpoint = CONTROLLER_FQDN+endpoint
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)

    # Delete comp 1
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app1/components/gcp-demo-app1-comp1"
    endpoint = CONTROLLER_FQDN+endpoint
    headers = { 'content-type': "application/json" }
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)
    # Delete App5
    endpoint = "/api/v1/services/environments/prod/apps/gcp-demo-app1"
    endpoint = CONTROLLER_FQDN+endpoint
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)
    # Delete GW5
    endpoint = "/api/v1/services/environments/prod/gateways/gw-gcp-app-1"
    endpoint = CONTROLLER_FQDN+endpoint
    response = session.delete(endpoint, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    time.sleep(5)

def template_call(session):
    endpoint = "/api/v1/services/environments/prod/apps/my-cool-app/components/my-cool-app-comp1"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """

    """
    headers = { 'content-type': "application/json" }
    response = session.put(endpoint, data=payload, headers=headers, verify=False)
    if(DEBUG):
        print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    if (200 <= response.status_code <= 210):
        print("login successful")
    time.sleep(5)

def auth_controller(u, p):
    if len(u)==0 or len(u)==0:
        u = input("Enter username: ")
        p = getpass("Enter password: ")

    endpoint = "/api/v1/platform/login"
    endpoint = CONTROLLER_FQDN+endpoint
    payload = """
    {
    "credentials": {
        "type": "BASIC",
        "username": "xxxxusernamexxxx",
        "password": "xxxxpasswordxxxx"
    }
    }
    """
    payload = payload.replace("xxxxusernamexxxx",u)
    payload = payload.replace("xxxxpasswordxxxx",p)

    headers = { 'content-type': "application/json" }
    session = requests.session()
    response = session.post(endpoint, data=payload, headers=headers, verify=False)
    if (200 <= response.status_code <= 210):
        print("login successful")
    else:
        print("login failed")
        if(DEBUG):
            print(endpoint + "\r\n" + str(response.status_code) + "\r\n"  + response.text)
    return session



main_procedure()
