from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS, EC2, Lambda
from diagrams.k8s.compute import Pod
from diagrams.ibm.user import Sensor
from diagrams.aws.compute import Compute
from diagrams.programming.language import Python
from diagrams.gcp.storage import GCS
from diagrams.k8s.clusterconfig import HPA
from diagrams.aws.database import Redshift
from diagrams.aws.database import Aurora
from diagrams.aws.network import ELB
from diagrams.gcp.iot import IotCore


with Diagram("", show=True, direction="LR"):
    sensor = Sensor("Sensor")

    with Cluster ("Device"):
        with Cluster("Hardware"):
            ampl_board = Lambda("Amplifier board")
            dq_board = EC2("DAQ board")
            periphery = ECS("Periphery")
            
            ampl_board >> dq_board
            dq_board >> ampl_board

            sensor >> ampl_board
            ampl_board >> sensor

        with Cluster("Raspberry pi"):
            raspi = Compute("")

            with Cluster("Data"):
                exp_data = GCS("Exp data")
                pi_data_proc = Python("data preprocessing")
                # exp_data - pi_data_proc
                dq_board >> exp_data                
            
            with Cluster("API"):
                http_server = HPA("data server")
                with Cluster("Tango"):
                    tango_server = HPA("tango server")
                    database = IotCore("mySQL")
                    # http_server - tango_server - database


                tango_server - raspi
                exp_data >> http_server

        
                raspi >> dq_board



    # with Cluster("Front client"):
    bliss = ELB("Bliss")
    gui = Redshift("GUI")

    tango_server - gui
    tango_server - bliss
    http_server - gui
    http_server - bliss





