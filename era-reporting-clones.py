#!/usr/bin/python
#####################################################################################
# Nutanix Era Reporting Script
# Author: Magnus Andersson - Principal Architect Nutanix
#
# Date: 2021-05-25
# Version 0.1
#
#####################################################################################
# Import whatever needs to be imported
#
import requests
import json
from datetime import datetime
#####################################################################################
#
#####################################################################################
# Time definition
#
now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H%M")
#####################################################################################
#
#####################################################################################
# Consumer config section. Define the following values
#
#
era_report_user_local_dir = "_Report_Folder_Destination_Ending_With_A_Slash/"
era_ip = "_Era_Server_FQDN/IP"
era_user = "_Era_user"
era_password = "_Era_password"
#
#
# Select what to include in the report. Change Y for N if you wish to exclude a section
include_dbvms = "Y"
include_profiles = "Y"
#
# End of consumer section section
#
#####################################################################################
#
#####################################################################################
# - Define report name
era_report_file = era_report_user_local_dir + date_time + "-Era_report.csv"
#
#####################################################################################
#
#####################################################################################
# Suppress warning about "Unverified HTTPS request"
#
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#####################################################################################
#
#####################################################################################
# Define ERA URL and URI
#
era_protocol = "https://"
era_profile_uri1 ="/era/v0.9/profiles?type=Software"
era_profile_uri2 ="/era/v0.9/profiles?type=Compute"
era_profile_uri3 ="/era/v0.9/profiles?type=Network"
era_profile_uri4 ="/era/v0.9/profiles?type=Database_Parameter"
era_sla_uri1 = "/era/v0.9/slas"
era_tm_uri1 = "/era/v0.9/tms?detailed=false&load-database=true&load-clones=true&load-metrics=true&load-associated-clusters=true"
era_clones_uri1 = "/era/v0.9/clones?load-metrics=true&detailed=true&load-dbserver-cluster=false&order-by-dbserver-cluster=false&order-by-dbserver-logical-cluster=false"
era_dbvm_uri1 = "/era/v0.9/dbservers?load-metrics=true&detailed=true&load-databases=true&load-clones=true"
era_ntnxcluster_uri1 = "/era/v0.9/clusters?include-management-server-info=true"
era_user_uri1 = "/era/v0.9/users/"
#####################################################################################
#
#####################################################################################
# Set headers
#
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
#####################################################################################
#
#####################################################################################
# Define Functions
#
# List to String with space
def LTS(list):
    # initialize an empty string
    str = " "
    # return string
    return (str.join(list))
#
# List to String with space
def LTSNoSpace(list):
    # initialize an empty string
    str = ""
    # return string
    return (str.join(list))
#####################################################################################
#
#####################################################################################
# Start getting the information required
#
# ------------------ Get Nutanix Cluster Info ------------------
#
erantnxclustersurl = era_protocol + era_ip + era_ntnxcluster_uri1
erantnxcluster = requests.get(
    erantnxclustersurl,
    headers=headers,
    auth=(era_user, era_password),
    verify=False
)
#
if erantnxcluster.status_code == 200:
    response_ntnxcluster_list = list()
    era_returned_ntnxcluster_list = json.loads(erantnxcluster.content)
    for ntnxcluster in era_returned_ntnxcluster_list:
        ntnxcluster_id_get = ntnxcluster['id']
        ntnxcluster_name_get = ntnxcluster['name']
        ntnxcluster_dict = {"ntnxcluster_id": ntnxcluster_id_get, "ntnxcluster_name": ntnxcluster_name_get}
        response_ntnxcluster_list.append(ntnxcluster_dict)
else:
    print("REST API Response Code:", erantnxcluster.status_code)
    print("exiting....")
    exit (1)
#
# Check if Era multi cluster is enabled
if len(response_ntnxcluster_list) == 1:
    era_multi_cluster = "N"
else:
    era_multi_cluster = "Y"
#
# ------------------ Get DB VM Info ------------------
#
eradbvmsurl = era_protocol + era_ip + era_dbvm_uri1
eradbvms = requests.get(
        eradbvmsurl,
        headers=headers,
        auth=(era_user, era_password),
        verify=False
    )
#
if eradbvms.status_code == 200:
     era_returned_dbvms_list = json.loads(eradbvms.content)
#
# ------------------ Get Time Machine Info ------------------
#
eratmurl = era_protocol + era_ip + era_tm_uri1
eratm = requests.get(
        eratmurl,
        headers=headers,
        auth=(era_user, era_password),
        verify=False
    )
#
if eratm.status_code == 200:
     era_returned_tm = json.loads(eratm.content)
#
# ------------------ Get SLAs ------------------
#
eraslaurl = era_protocol + era_ip + era_sla_uri1
erasla = requests.get(
        eraslaurl,
        headers=headers,
        auth=(era_user, era_password),
        verify=False
    )
#
if erasla.status_code == 200:
     response_sla_list = list()
     era_returned_sla_list = json.loads(erasla.content)
     for sla in era_returned_sla_list:
        sla_id_get = sla['id']
        sla_name_get = sla['name']
        sla_dict = {"sla_id": sla_id_get, "sla_name": sla_name_get}
        response_sla_list.append(sla_dict)
#
# ------------------ Get profiles ------------------
# Software Profile
erasoftwareprofileurl = era_protocol + era_ip + era_profile_uri1
erasoftwareprofile = requests.get(
        erasoftwareprofileurl,
        headers=headers,
        auth=(era_user, era_password),
        verify=False
    )
#
if erasoftwareprofile.status_code == 200:
     response_software_profile_list = list()
     era_returned_software_profile_list = json.loads(erasoftwareprofile.content)
     for software_profile in era_returned_software_profile_list:
        sw_profile_id_get = software_profile['id']
        sw_profile_name_get = software_profile['name']
        software_profile_dict = {"software_profile_id": sw_profile_id_get, "software_profile_name": sw_profile_name_get}
        response_software_profile_list.append(software_profile_dict)
#
# Compute Profile
eracomputeprofileurl = era_protocol + era_ip + era_profile_uri2
eracomputeprofile = requests.get(
        eracomputeprofileurl,
        headers=headers,
        auth=(era_user, era_password),
        verify=False
    )
#
if eracomputeprofile.status_code == 200:
     response_compute_profile_list = list()
     era_returned_compute_profile_list = json.loads(eracomputeprofile.content)
     for compute_profile in era_returned_compute_profile_list:
        cm_profile_id_get = compute_profile['id']
        cm_profile_name_get = compute_profile['name']
        compute_profile_dict = {"compute_profile_id": cm_profile_id_get, "compute_profile_name": cm_profile_name_get}
        response_compute_profile_list.append(compute_profile_dict)
#
# Network Profile
eranetworkprofileurl = era_protocol + era_ip + era_profile_uri3
eranetworkprofile = requests.get(
        eranetworkprofileurl,
        headers=headers,
        auth=(era_user, era_password),
        verify=False
    )
#
if eranetworkprofile.status_code == 200:
     response_network_profile_list = list()
     era_returned_network_profile_list = json.loads(eranetworkprofile.content)
     for network_profile in era_returned_network_profile_list:
        net_profile_id_get = network_profile['id']
        net_profile_name_get = network_profile['name']
        network_profile_dict = {"network_profile_id": net_profile_id_get, "network_profile_name": net_profile_name_get}
        response_network_profile_list.append(network_profile_dict)
#
# Database Profile
eradbprofileurl = era_protocol + era_ip + era_profile_uri4
eradbprofile = requests.get(
        eradbprofileurl,
        headers=headers,
        auth=(era_user, era_password),
        verify=False
    )
#
if eradbprofile.status_code == 200:
     response_db_profiledb_list = list()
     era_returned_db_profile_list = json.loads(eradbprofile.content)
     for db_profile in era_returned_db_profile_list:
        database_profile_id_get = db_profile['id']
        database_profile_name_get = db_profile['name']
        db_profile_dict = {"db_profile_id": database_profile_id_get, "db_profile_name": database_profile_name_get}
        response_db_profiledb_list.append(db_profile_dict)
#
# ------------------ Get User Info ------------------
#
erauserurl = era_protocol + era_ip + era_user_uri1
erauser = requests.get(
        erauserurl,
        headers=headers,
        auth=(era_user, era_password),
        verify=False
    )
#
if erauser.status_code == 200:
     response_user_list = list()
     era_returned_user_list = json.loads(erauser.content)
     for user in era_returned_user_list:
        user_id_get = user['id']
        user_name_get = user['username']
        user_dict = {"user_id": user_id_get, "user_name": user_name_get}
        response_user_list.append(user_dict)
#
# ------------------ Get Clones Info ------------------
userclonesurl = era_protocol + era_ip + era_clones_uri1
userclones = requests.get(
        userclonesurl,
        headers=headers,
        auth=(era_user, era_password),
        verify=False
    )
#
# ------------------ Getting the information required completed ------------------
#####################################################################################
#
#####################################################################################
# Create the report file structure including report objects.
#
# Create initial reporting doc structure
f = open(era_report_file, "w")
f.write("Clone name,Database(s),Type,Database Version,Database Profile,Size GB,Database Owner,Database/Instance Create Date & Time,Database/Instance Data Date & Time,Source Time Machine Name,Clone Tags (Name-/-Value)")
f.close()
#
if include_dbvms == "Y":
    f = open(era_report_file, "a")
    f.write(",Server VM(s) Name,Server VM(s) IP,Nutanix Cluster Placement")
    f.close()
if include_profiles == "Y":
    f = open(era_report_file, "a")
    f.write(",Software Profile,Compute Profile,Network Profile")
    f.close()
#
#
#####################################################################################
#
#####################################################################################
# Start Building the Report
#
if userclones.status_code == 200:
    response_clone_list = list()
    era_returned_clone_list = json.loads(userclones.content)
    for db_clones in era_returned_clone_list:
        #
        #####################################################################################
        # Database Information Section
        #
        # Get Clone Name
        db_clone_name_get=db_clones["name"]
        #
        #
        # Get Database(s)
        for ref_id in db_clones['properties']:
            if ref_id["name"] == "database_list":
                # extract the list of database names
                db_names_list = list()
                db_names_str = ref_id["value"]
                db_name_temp_list = db_names_str.split("{'name': '")
                db_name_temp_list.pop(0)
                for db_name_temp_str in db_name_temp_list:
                    db_names_list.append(db_name_temp_str.split("',")[0])
                databases_get_list = (LTS(db_names_list))
                databases_get = (LTS(db_names_list))
                break
            else:
                databases_get = db_clones['databaseName']
        #
        #
        # Get DB Engine definition
        db_engine = db_clones["type"]
        db_engine_split = db_engine.split("_")
        db_engine_get = db_engine_split[0]
        #
        #
        # Get Database Version
        for ref_id in db_clones['properties']:
            if ref_id["name"] == "version":
                db_version_get = ref_id["value"]
        #
        #
        # Get DB Profile
        for ref_id in db_clones['properties']:
            if ref_id["name"] == "db_parameter_profile_id":
                db_profile_id_get = ref_id["value"]
                for db_profile in response_db_profiledb_list:
                    if db_profile["db_profile_id"] == db_profile_id_get:
                        clone_db_profile_name = db_profile["db_profile_name"]
                clone_db_profile_name_get = clone_db_profile_name
                break
            else:
                clone_db_profile_name_get = "n/a"
        #
        #
        # Get Clone Owner
        for user in response_user_list:
            if user["user_id"] == db_clones['ownerId']:
                clone_owner_get = user["user_name"]
        #
        #
        # Get Instance Create Date
        db_clone_create_date_get = db_clones["dateCreated"]
        #
        #
        # Get Size GB
        db_size_float = round(db_clones['metric']['aggregateStorage']['usedSize']/1024/1024/1024, 4)
        clone_size_get = str(db_size_float)
        #
        #
        # Last Time Refreshed
        refresh_time_get = db_clones['metadata']['lastRefreshTimestamp']
        #
        #
        #####################################################################################
        # Time Machine Section
        #
        for tm in era_returned_tm:
            if tm["id"] == db_clones["parentTimeMachineId"]:
                tm_get = tm["name"]
                break
            else:
                tm_get = "Source TM Not Available"
        #
        #
        #####################################################################################
        # Database Server VM section
        #
        if include_dbvms == "Y":
            # Get DB Server VM(s) Name
            if not db_clones['databaseNodes']:
                db_server_vm_name_get = "Provisioning in progress.."
            elif db_clones['databaseNodes'] and db_clones['clustered'] == True:
                name_list = list()
                for dbs in db_clones['databaseNodes']:
                    dbservernameid = dbs['dbserverId']
                    for vm in era_returned_dbvms_list:
                        #print ("VM ID:",vm["name"])
                        if dbservernameid == vm["id"]:
                            db_server_vm_name = vm["name"]
                            name_list.append(db_server_vm_name)
                    db_server_vm_name_get = (LTS(name_list))
            else:
                dbservernameid = db_clones["databaseNodes"][0]["dbserverId"]
                for vm in era_returned_dbvms_list:
                    if dbservernameid == vm["id"]:
                        db_server_vm_name_get = vm["name"]
            #
            #
            # Get DB Server VM(s) Ip Address
            if not db_clones['databaseNodes']:
                   db_server_vm_ip_get = "Provisioning in progress.."
            elif db_clones['databaseNodes'] and db_clones['clustered'] == True:
                ip_list = list()
                for dbs in db_clones['databaseNodes']:
                    dbservernameid = dbs['dbserverId']
                    for vm in era_returned_dbvms_list:
                        if dbservernameid == vm["id"]:
                            db_server_vm_ip_list = vm["ipAddresses"]
                            db_server_vm_ip = (LTS(db_server_vm_ip_list))
                            ip_list.append(db_server_vm_ip)
                    db_server_vm_ip_get = (LTS(ip_list))
            else:
                dbserveridip = db_clones["databaseNodes"][0]["dbserverId"]
                for vm in era_returned_dbvms_list:
                    if dbserveridip == vm["id"]:
                        db_server_vm_ip = vm["ipAddresses"]
                        db_server_vm_ip_get = (LTS(db_server_vm_ip))
            #
            # Get Nutanix Cluster Placement
            if not db_clones['databaseNodes']:
                ntnxcluster_name_get = "Provisioning in progress.."
            elif db_clones['databaseNodes'] and db_clones['clustered'] == True:
                ntnxcluster_list = list()
                for dbs in db_clones['databaseNodes']:
                    dbservernameid = dbs['dbserverId']
                    for vm in era_returned_dbvms_list:
                        if dbservernameid == vm["id"]:
                            db_server_vm_ntnxcluid = vm["nxClusterId"]
                            for ntnxcluster in response_ntnxcluster_list:
                                if ntnxcluster["ntnxcluster_id"] == db_server_vm_ntnxcluid:
                                    ntnxcluster_name = ntnxcluster["ntnxcluster_name"]
                                    ntnxcluster_list.append(ntnxcluster_name)
                                ntnxcluster_name_get = (LTS(ntnxcluster_list))
            else:
                for dbs in db_clones['databaseNodes']:
                    ntnxcluster_id = dbs["dbserver"]["nxClusterId"]
                    for ntnxcluster in response_ntnxcluster_list:
                        if ntnxcluster["ntnxcluster_id"] == ntnxcluster_id:
                            ntnxcluster_name_get = ntnxcluster["ntnxcluster_name"]
        #
        #####################################################################################
        # Profile section
        #
        if include_profiles == "Y":
            # Get Software Profile
            if not db_clones['databaseNodes']:
                software_profile_name_get = "Provisioning in progress.."
            elif db_clones['databaseNodes'] and db_clones['clustered'] == True:
                software_profile_list = list()
                for dbs in db_clones['databaseNodes']:
                    for ref_id in dbs['dbserver']['properties']:
                        if ref_id["name"] == "software_profile_id":
                            software_profile_ref_id = ref_id["value"]
                            for software_profile in response_software_profile_list:
                                if software_profile["software_profile_id"] == software_profile_ref_id:
                                    software_profile_name = software_profile["software_profile_name"]
                                    software_profile_list.append(software_profile_name)
                # Get uniq values from the list
                software_profile_name_get_uniq = list(set(software_profile_list))
                # Get entire list
                #software_profile_name_get = software_profile_list
                #
                software_profile_name_get = (LTS(software_profile_name_get_uniq))
            else:
                for dbs in db_clones['databaseNodes']:
                    for ref_id in dbs['dbserver']['properties']:
                        if ref_id["name"] == "software_profile_id":
                            software_profile_ref_id = ref_id["value"]
                            for software_profile in response_software_profile_list:
                                if software_profile["software_profile_id"] == software_profile_ref_id:
                                    software_profile_name_get = software_profile["software_profile_name"]
            #
            #
            # Get Compute Profile
            if not db_clones['databaseNodes']:
                compute_profile_name_get = "Provisioning in progress.."
            elif db_clones['databaseNodes'] and db_clones['clustered'] == True:
                compute_profile_list = list()
                for dbs in db_clones['databaseNodes']:
                    for ref_id in dbs['dbserver']['properties']:
                        if ref_id["name"] == "compute_profile_id":
                            compute_profile_ref_id = ref_id["value"]
                            for compute_profile in response_compute_profile_list:
                                if compute_profile["compute_profile_id"] == compute_profile_ref_id:
                                    compute_profile_name = compute_profile["compute_profile_name"]
                                    compute_profile_list.append(compute_profile_name)
                # Get uniq values from the list
                compute_profile_name_get_uniq = list(set(compute_profile_list))
                # Get entire list
                #compute_profile_name_get = compute_profile_list
                #
                compute_profile_name_get = (LTS(compute_profile_name_get_uniq))
            else:
                for dbs in db_clones['databaseNodes']:
                    for ref_id in dbs['dbserver']['properties']:
                        if ref_id["name"] == "compute_profile_id":
                            compute_profile_ref_id = ref_id["value"]
                            for compute_profile in response_compute_profile_list:
                                if compute_profile["compute_profile_id"] == compute_profile_ref_id:
                                    compute_profile_name_get = compute_profile["compute_profile_name"]
            #
            #
            # Get Network Profile
            if not db_clones['databaseNodes']:
                network_profile_name_get = "Provisioning in progress.."
            elif db_clones['databaseNodes'] and db_clones['clustered'] == True:
                network_profile_list = list()
                for dbs in db_clones['databaseNodes']:
                    for ref_id in dbs['dbserver']['properties']:
                        if ref_id["name"] == "network_profile_id":
                            network_profile_ref_id = ref_id["value"]
                            for network_profile in response_network_profile_list:
                                if network_profile["network_profile_id"] == network_profile_ref_id:
                                    network_profile_name = network_profile["network_profile_name"]
                                    network_profile_list.append(network_profile_name)
                # Get uniq values from the list
                network_profile_name_get_uniq = list(set(network_profile_list))
                # Get entire list
                #network_profile_name_get = network_profile_list
                #
                network_profile_name_get = (LTS(network_profile_name_get_uniq))
            else:
                for dbs in db_clones['databaseNodes']:
                    for ref_id in dbs['dbserver']['properties']:
                        if ref_id["name"] == "network_profile_id":
                            network_profile_ref_id = ref_id["value"]
                            for network_profile in response_network_profile_list:
                                if network_profile["network_profile_id"] == network_profile_ref_id:
                                    network_profile_name_get = network_profile["network_profile_name"]
        #
        #
        #####################################################################################
        # Tags Section
        #
        # Clone Tags
        clonetag_list = list()
        if not db_clones['tags']:
            clone_tag_get = "n/a"
        else:
            for tags in db_clones['tags']:
                clone_tagname = tags['tagName']
                clonetag_list.append(clone_tagname)
                clone_taghyphen = "-/-"
                clonetag_list.append(clone_taghyphen)
                clone_tagvalue = tags['value']
                clonetag_list.append(clone_tagvalue)
                clone_tagspace = " "
                clonetag_list.append(clone_tagspace)
            clone_tag_get = (LTSNoSpace(clonetag_list))
        #
#####################################################################################
        # Add the information to the report
        clone_dict = "\n"+db_clone_name_get+","+databases_get+","+db_engine_get+","+db_version_get+","+clone_db_profile_name_get+","+clone_size_get+","+clone_owner_get+","+db_clone_create_date_get+","+refresh_time_get+","+tm_get+","+clone_tag_get
        response_clone_list.append(clone_dict)
        f = open(era_report_file, "a")
        f.write(str(clone_dict))
        #
        if include_dbvms == "Y":
            clone_dict_dbvms = ","+db_server_vm_name_get+","+db_server_vm_ip_get+","+ntnxcluster_name_get
            response_clone_list.append(clone_dict_dbvms)
            f.write(str(clone_dict_dbvms))
        if include_profiles == "Y":
            clone_dict_profiles = ","+software_profile_name_get+","+compute_profile_name_get+","+network_profile_name_get
            response_clone_list.append(clone_dict_profiles)
            f.write(str(clone_dict_profiles))
        f.close()
else:
    print("Error getting Era information:", userclones.status_code)
