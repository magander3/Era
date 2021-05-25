#!/usr/bin/python
#####################################################################################
# Nutanix Era Reporting Script
# Author: Magnus Andersson - Principal Architect Nutanix
#
# Date: 2021-04-10
# Version 1.0.1
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
# User config section. Define the following values
#
#
era_report_user_local_dir = "_Report_Folder_Destination_Ending_With_A_Slash/"
era_ip = "_Era_Server_FQDN/IP"
era_user = "_Era_user"
era_password = "_Era_password"
#
#
# Select what to include in the report. Change Y for N if you wish to exclude a section
include_time_machine = "Y"
include_dbvms = "Y"
include_profiles = "Y"
include_tags = "Y"
#
# End of user config section
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
era_db_uri1 = "/era/v0.9/databases?detailed=true&load-dbserver-cluster=false&order-by-dbserver-cluster=false&order-by-dbserver-logical-cluster=false"
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
# ------------------ Get DB Info ------------------
userdbinstanceurl = era_protocol + era_ip + era_db_uri1
userdbinstance = requests.get(
        userdbinstanceurl,
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
f.write("Database/Instance name,Database(s),Type,Database Version,Database Profile,Size GB,Database Owner,Database/Instance Create Date & Time,Number of clones")
f.close()
#
if include_time_machine == "Y" and era_multi_cluster == "Y":
    f = open(era_report_file, "a")
    f.write(",Time Machine Name,Time Machine Size GB,Time Machine SLA (Name-/-Nutanix Cluster)")
    f.close()
if include_time_machine == "Y" and era_multi_cluster == "N":
    f = open(era_report_file, "a")
    f.write(",Time Machine Name,Time Machine Size GB,Time Machine SLA")
    f.close()
if include_dbvms == "Y":
    f = open(era_report_file, "a")
    f.write(",Server VM(s) Name,Server VM(s) IP,Nutanix Cluster Placement")
    f.close()
if include_profiles == "Y":
    f = open(era_report_file, "a")
    f.write(",Software Profile,Compute Profile,Network Profile")
    f.close()
if include_tags == "Y":
    f = open(era_report_file, "a")
    f.write(",Database Tags (Name-/-Value),Time Machine Tags (Name-/-Value),Database Server VM Tags (Name-/-Value)")
    f.close()
#
#
#####################################################################################
#
#####################################################################################
# Start Building the Report
#
if userdbinstance.status_code == 200:
    response_db_list = list()
    era_returned_db_list = json.loads(userdbinstance.content)
    for db_inst in era_returned_db_list:
        #
        #####################################################################################
        # Database Information Section
        #
        # Get Instance Name
        db_inst_name_get=db_inst["name"]
        #
        #
        # Get Database(s)
        for ref_id in db_inst['properties']:
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
                for ref_id in db_inst['properties']:
                    if ref_id["name"] == "db_name":
                        databases_get = ref_id["value"]
        #
        #
        # Get DB Engine definition
        db_engine = db_inst["type"]
        db_engine_split = db_engine.split("_")
        db_engine_get = db_engine_split[0]
        #
        #
        # Get Database Version
        for ref_id in db_inst['properties']:
            if ref_id["name"] == "version":
                db_version_get = ref_id["value"]
        #
        #
        # Get DB Profile
        for ref_id in db_inst['properties']:
            if ref_id["name"] == "db_parameter_profile_id":
                db_profile_id_get = ref_id["value"]
        for db_profile in response_db_profiledb_list:
            if db_profile["db_profile_id"] == db_profile_id_get:
                db_db_profile_name_get = db_profile["db_profile_name"]
                #print(db_db_profile_name_get)
        #
        #
        # Get Database Owner
        for user in response_user_list:
            if user["user_id"] == db_inst['ownerId']:
                db_owner_get = user["user_name"]
        #
        #
        # Get Instance Create Date
        db_instance_create_date_get = db_inst["dateCreated"]
        #
        #
        # Get Size GB
        for ref_id in db_inst['properties']:
            if ref_id["name"] == "SIZE":
                db_size_name_get_full = ref_id["value"]
                db_size_name_get = db_size_name_get_full.split(".")[0]
        #
        #
        # Get Clone Count
        for ref_id in db_inst["timeMachine"]["properties"]:
            if ref_id["name"] == "CLONE_COUNT":
                db_inst_clone_count_get = ref_id["value"]
        #
        #
        #####################################################################################
        # Time Machine Section
        #
        if include_time_machine == "Y":
        #
            # Get Time Machine Name
            tm_get = db_inst["timeMachine"]["name"]
            #
            #
            #
            # Get Time Machine Size
            tm_id = db_inst["timeMachine"]["id"]
            for tm in era_returned_tm:
                if tm_id == tm["id"]:
                    tm_size_float = tm["metric"]["aggregateStorage"]["size"]
                    tm_size_get = str(round(tm_size_float/1024, 2))
            #
            #
            # Get Time Machine SLA name(s)
            if era_multi_cluster == "Y":
                for tm in era_returned_tm:
                    if tm["id"] == db_inst["timeMachine"]["id"]:
                        tm_name_list = list()
                        for tms in tm["associatedClusters"]:
                            tm_slaid = tms['slaId']
                            tm_ntnxcluster_id = tms['nxClusterId']
                            for sla in response_sla_list:
                                if sla["sla_id"] == tm_slaid:
                                    tm_sla_name = sla["sla_name"]
                                    tm_name_list.append(tm_sla_name)
                                    tm_name_hyphen = "-/-"
                                    tm_name_list.append(tm_name_hyphen)
                            for ntnxcluster in response_ntnxcluster_list:
                                if ntnxcluster['ntnxcluster_id'] == tm_ntnxcluster_id:
                                    tm_ntnxcluster_name = ntnxcluster["ntnxcluster_name"]
                                    tm_name_list.append(tm_ntnxcluster_name)
                                    tm_name_space = " "
                                    tm_name_list.append(tm_name_space)
                        tm_sla_get = (LTSNoSpace(tm_name_list))
            else:
                tm_sla = db_inst["timeMachine"]["slaId"]
                for sla in response_sla_list:
                    if sla["sla_id"] == tm_sla:
                        tm_sla_get = sla["sla_name"]
        #
        #
        #####################################################################################
        # Database Server VM section
        #
        if include_dbvms == "Y":
            # Get DB Server VM(s) Name
            if not db_inst['databaseNodes']:
                db_server_vm_name_get = "Provisioning in progress.."
            elif db_inst['databaseNodes'] and db_inst['clustered'] == True:
                name_list = list()
                for dbs in db_inst['databaseNodes']:
                    #if dbs['properties'][0]['value']:
                    db_server_vm_name = dbs["dbserver"]["name"]
                        #print (db_server_vm_name)
                    name_list.append(db_server_vm_name)
                db_server_vm_name_get = (LTS(name_list))
            else:
                db_server_vm_name_get = db_inst["databaseNodes"][0]["dbserver"]["name"]
            #
            #
            # Get DB Server VM(s) Ip Address
            if not db_inst['databaseNodes']:
                   db_server_vm_ip_get = "Provisioning in progress.."
            elif db_inst['databaseNodes'] and db_inst['clustered'] == True:
                ip_list = list()
                for dbs in db_inst['databaseNodes']:
                    #if dbs['properties'][0]['value']:
                    db_server_vm_ip = dbs["dbserver"]["ipAddresses"][0]
                    ip_list.append(db_server_vm_ip)
                db_server_vm_ip_get = (LTS(ip_list))
            else:
                db_server_vm_ip_get = db_inst["databaseNodes"][0]["dbserver"]["ipAddresses"][0]
            #
                #
                #
            # Get Nutanix Cluster Placement
            if not db_inst['databaseNodes']:
                ntnxcluster_name_get = "Provisioning in progress.."
            elif db_inst['databaseNodes'] and db_inst['clustered'] == True:
                ntnxcluster_list = list()
                for dbs in db_inst['databaseNodes']:
                    ntnxcluster_id = dbs["dbserver"]["nxClusterId"]
                    for ntnxcluster in response_ntnxcluster_list:
                        if ntnxcluster["ntnxcluster_id"] == ntnxcluster_id:
                            ntnxcluster_name = ntnxcluster["ntnxcluster_name"]
                            ntnxcluster_list.append(ntnxcluster_name)
                # Get uniq values from the list
                # ntnxcluster_name_get_uniq = list(set(ntnxcluster_list))
                # Get entire list
                ntnxcluster_name_get = ntnxcluster_list
                #
                ntnxcluster_name_get = (LTS(ntnxcluster_name_get))
                # print(ntnxcluster_name_get)
            else:
                for dbs in db_inst['databaseNodes']:
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
            if not db_inst['databaseNodes']:
                software_profile_name_get = "Provisioning in progress.."
            elif db_inst['databaseNodes'] and db_inst['clustered'] == True:
                software_profile_list = list()
                for dbs in db_inst['databaseNodes']:
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
                for dbs in db_inst['databaseNodes']:
                    for ref_id in dbs['dbserver']['properties']:
                        if ref_id["name"] == "software_profile_id":
                            software_profile_ref_id = ref_id["value"]
                            for software_profile in response_software_profile_list:
                                if software_profile["software_profile_id"] == software_profile_ref_id:
                                    software_profile_name_get = software_profile["software_profile_name"]
            #
            #
            # Get Compute Profile
            if not db_inst['databaseNodes']:
                compute_profile_name_get = "Provisioning in progress.."
            elif db_inst['databaseNodes'] and db_inst['clustered'] == True:
                compute_profile_list = list()
                for dbs in db_inst['databaseNodes']:
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
                for dbs in db_inst['databaseNodes']:
                    for ref_id in dbs['dbserver']['properties']:
                        if ref_id["name"] == "compute_profile_id":
                            compute_profile_ref_id = ref_id["value"]
                            for compute_profile in response_compute_profile_list:
                                if compute_profile["compute_profile_id"] == compute_profile_ref_id:
                                    compute_profile_name_get = compute_profile["compute_profile_name"]
            #
            #
            # Get Network Profile
            if not db_inst['databaseNodes']:
                network_profile_name_get = "Provisioning in progress.."
            elif db_inst['databaseNodes'] and db_inst['clustered'] == True:
                network_profile_list = list()
                for dbs in db_inst['databaseNodes']:
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
                for dbs in db_inst['databaseNodes']:
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
        if include_tags == "Y":
            # Database Tags
            dbtag_list = list()
            if not db_inst['tags']:
                db_tag_get = "n/a"
            else:
                for tags in db_inst['tags']:
                    db_tagname = tags['tagName']
                    dbtag_list.append(db_tagname)
                    db_taghyphen = "-/-"
                    dbtag_list.append(db_taghyphen)
                    db_tagvalue = tags['value']
                    dbtag_list.append(db_tagvalue)
                    db_tagspace = " "
                    dbtag_list.append(db_tagspace)
                db_tag_get = (LTSNoSpace(dbtag_list))
            #
            #
            # Time Machine Tags
            tmtag_list = list()
            if not db_inst['timeMachine']['tags']:
                tm_tag_get = "n/a"
            else:
                for tags in db_inst['timeMachine']['tags']:
                    tm_tagname = tags['tagName']
                    tmtag_list.append(tm_tagname)
                    tm_taghyphen = "-/-"
                    tmtag_list.append(tm_taghyphen)
                    tm_tagvalue = tags['value']
                    tmtag_list.append(tm_tagvalue)
                    tm_tagspace = " "
                    tmtag_list.append(tm_tagspace)
                tm_tag_get = (LTSNoSpace(tmtag_list))
            #
            #
            # DB Server VM Tags
            dbsvmtag_list = list()
            for dbs in db_inst['databaseNodes']:
                if not dbs["dbserver"]["tags"]:
                    dbsvm_tag_get = "n/a"
                else:
                    for tags in dbs["dbserver"]["tags"]:
                        dbsvmtag_tagname = tags['tagName']
                        dbsvmtag_list.append(dbsvmtag_tagname)
                        dbsvmtag_taghyphen = "-/-"
                        dbsvmtag_list.append(dbsvmtag_taghyphen)
                        dbsvmtag_tagvalue = tags['value']
                        dbsvmtag_list.append(dbsvmtag_tagvalue)
                        dbsvmtag_tagspace = " "
                        dbsvmtag_list.append(dbsvmtag_tagspace)
                    dbsvm_tag_get = (LTSNoSpace(dbsvmtag_list))
        #
#####################################################################################
        # Add the information to the report
        db_dict = "\n"+db_inst_name_get+","+databases_get+","+db_engine_get+","+db_version_get+","+db_db_profile_name_get+","+db_size_name_get+","+db_owner_get+","+db_instance_create_date_get+","+db_inst_clone_count_get
        response_db_list.append(db_dict)
        f = open(era_report_file, "a")
        f.write(str(db_dict))
        #
        if include_time_machine == "Y":
            db_dict_tm = ","+tm_get+","+tm_size_get+","+tm_sla_get
            response_db_list.append(db_dict_tm)
            f.write(str(db_dict_tm))
        if include_dbvms == "Y":
            db_dict_dbvms = ","+db_server_vm_name_get+","+db_server_vm_ip_get+","+ntnxcluster_name_get
            response_db_list.append(db_dict_dbvms)
            f.write(str(db_dict_dbvms))
        if include_profiles == "Y":
            db_dict_profiles = ","+software_profile_name_get+","+compute_profile_name_get+","+network_profile_name_get
            response_db_list.append(db_dict_profiles)
            f.write(str(db_dict_profiles))
        if include_tags == "Y":
            db_dict_tags = ","+db_tag_get+","+tm_tag_get+","+dbsvm_tag_get
            response_db_list.append(db_dict_tags)
            f.write(str(db_dict_tags))
        f.close()
else:
    print("Error getting Era information:", userdbinstance.status_code)
