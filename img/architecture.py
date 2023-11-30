from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2, Lambda, Fargate
from diagrams.aws.network import TransitGateway, ALB
from diagrams.aws.security import Cognito
from diagrams.onprem.client import Client
from diagrams.gcp.compute import GCE
from diagrams.aws.iot import IotJobs, IotRule, IotCore
from diagrams.aws.iot import IotMqtt, IotAnalyticsDataStore
from diagrams.aws.database import DDB

with Diagram(None, show=True, direction="TB"):
    web = Client("Web Dashboard")

    with Cluster("AWS Cloud"):
        gateway = TransitGateway("Transit Gateway")
        with Cluster("AWS VPC (Public Subnet)"):
            public_subnet_m = [Cognito("Cognito"),
                               EC2("Amazon EC2\nBastion Host")]
        with Cluster("          Rapic VPC (Private Subnet)"):
            private_subnet = [IotCore("IoT Core"),
                              IotRule("IoT Rule"),
                              Lambda("Transform\nLambda"),
                              DDB("Dynamo DB"),
                              IotJobs("Web app\ntask"),
                              Fargate("Fargate"),
                              ALB("ALB")]

    with Cluster("Pfizer/Lab network"):
        broker = [IotMqtt("Mosquitto\nBroker/Bridge"),
                  IotAnalyticsDataStore("InfluxDB")]
        with Cluster("PAT sensors"):
            pats = [GCE("Liquid level sensor"),
                    GCE("pH sensor"),
                    GCE("UV probe")]

    public_subnet_m[0] >> web >> public_subnet_m[0]
    public_subnet_m[0] >> gateway >> public_subnet_m[0]
    private_subnet[6] >> gateway >> private_subnet[6]
    private_subnet[0] << broker[0] >> pats[1]
    broker[0] << private_subnet[0]
    pats[1] >> broker[0]
