import subprocess
import shlex
import json
import datetime
import time
import xlsxwriter
import httplib, urllib
import math
import bitmath
import mysql.connector

foundry_list = {'sample-foundry':['api.run.pivotal.io', 'Lakshmiredz@gmail.com','Pooja@123','concourse2','ci', "console.run.pivotal.io"]}

timestamp_str = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')

workbook = xlsxwriter.Workbook('top_apps_'+timestamp_str+'.xlsx')
bold = workbook.add_format({'bold': True})

get_foundry_id_sql = "SELECT id FROM foundries WHERE foundry_name = %s"
get_org_id_sql = "SELECT id FROM pcf_org WHERE org_name = %s and foundry_id = %s"
get_space_id_sql = "SELECT id FROM pcf_space WHERE space_name = %s and org_id = %s"
get_app_id_sql = "SELECT id FROM pcf_apps WHERE name = %s and space_id = %s"

insert_foundry_sql = ("INSERT INTO foundries "
               "(foundry_name, memory_consumption_percent, last_updated) "
               "VALUES (%s, %s, %s)")
insert_org_sql = ("INSERT INTO pcf_org "
               "(org_name, foundry_id, memory_consumption_percent, last_updated) "
               "VALUES (%s, %s, %s, %s)")
insert_space_sql = ("INSERT INTO pcf_space "
               "(space_name,org_id, memory_consumption_percent, last_updated) "
               "VALUES (%s, %s, %s, %s)")

insert_app_sql = ("INSERT INTO pcf_apps "
               "(name, memory, instances, disk_space, state, cpu_used, memory_used, disk_used, space_id, memory_consumption_percent, last_updated) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
update_app_sql = "UPDATE pcf_apps SET name = %s, memory = %s , instances = %s , disk_space = %s, state = %s, cpu_used = %s, memory_used = %s, disk_used = %s, space_id = %s where id = %s and space_id = %s"
update_foundry_mempry_percent = "UPDATE foundries SET memory_consumption_percent = %s, last_updated = %s"
app_memory_percent = "UPDATE pcf_apps SET memory_consumption_percent = %s, last_updated = %s"
truncate_apps = "TRUNCATE TABLE grafana.pcf_apps"
truncate_orgs = "TRUNCATE TABLE grafana.pcf_org"
truncate_space = "TRUNCATE TABLE grafana.pcf_space"

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="grafana"
)

mycursor = db.cursor()
mycursor.execute(truncate_apps)
db.commit()
for foundry in foundry_list:
    foundry_avail_mem = 0
    foundry_app_mem_usage = 0
    flist = foundry_list[foundry]
    api = flist[0]
    user = flist[1]
    pwd = flist[2]
    org = flist[3]
    space = flist[4]

    login_command = 'cf login -a ' + api + ' -u ' + user + ' -p ' + pwd + ' -o ' + org + ' -s ' + space + ' --skip-ssl-validation'
    list_all_orgs = 'cf curl /v2/organizations'+'?results-per-page=100'
    get_org_quota = 'cf curl /v2/quota_definitions/'

    #running cf login shell command for login and running commands
    process = subprocess.Popen(shlex.split(login_command), stdout=subprocess.PIPE)
    login_output = process.communicate()[0]
    print(login_output)

    #listing all orgs
    process = subprocess.Popen(shlex.split(list_all_orgs), stdout=subprocess.PIPE)
    raw_org_json = process.communicate()[0]

    org_json = json.loads(raw_org_json)
    print(org_json['total_results'])

    worksheet = workbook.add_worksheet(foundry)
    row = 1
    col = 0
    foundry_id = 0
    mycursor.execute(get_foundry_id_sql, (foundry,))
    myresult = mycursor.fetchall()
    db.commit()
    if(len(myresult) == 1):
        foundry_id = myresult[0][0]
        print('foundry value', myresult[0][0])
    else:
        mycursor.execute(insert_foundry_sql, (foundry,0,time.strftime('%Y-%m-%d %H:%M:%S')))
        foundry_id = mycursor.lastrowid
        db.commit()
    for org_obj in org_json['resources']:
        org_id = 0 
        quota_cmd = get_org_quota+org_obj['entity']['quota_definition_guid']
        token_proc = subprocess.Popen(shlex.split('cf oauth-token'), stdout=subprocess.PIPE)
        token = token_proc.communicate()[0]
        token = token.replace("\n", "")
        params = urllib.urlencode({})
        headers = {"Authorization": token}
        conn = httplib.HTTPSConnection(flist[5])
        conn.request("GET", "/proxy/api/v2/organizations/"+org_obj['metadata']['guid']+"/memory_usage", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data_asigned_quota = response.read()
        conn.close()
        data_asigned_quota_json = json.loads(data_asigned_quota)
        print("quota asigned "+ str(data_asigned_quota))
        '''process = subprocess.Popen(shlex.split(quota_cmd), stdout=subprocess.PIPE)
        raw_org_quota = process.communicate()[0]
        org_quota_json = json.loads(raw_org_quota)
        print(org_quota_json)'''
        foundry_avail_mem = foundry_avail_mem + data_asigned_quota_json['memory_usage_in_mb']
        mycursor.execute(get_org_id_sql, (org_obj['entity']['name'], foundry_id,))
        myresult = mycursor.fetchall()
        if(len(myresult) == 1):
            org_id = myresult[0][0]
            print('org id found value', myresult[0][0])
        else:
            mycursor.execute(insert_org_sql, (org_obj['entity']['name'],foundry_id, 0,time.strftime('%Y-%m-%d %H:%M:%S')))
            org_id = mycursor.lastrowid
            db.commit()
        cf_list_spaces_command = 'cf curl '+org_obj['entity']['spaces_url']+'?results-per-page=100'
        process = subprocess.Popen(shlex.split(cf_list_spaces_command), stdout=subprocess.PIPE)
        raw_spaces_json = process.communicate()[0]
        spaces_json = json.loads(raw_spaces_json)
        
        for space_obj in spaces_json['resources']:
            space_id = 0 
            mycursor.execute(get_space_id_sql, (space_obj['entity']['name'],org_id,))
            myresult = mycursor.fetchall()
            if(len(myresult) == 1):
                space_id = myresult[0][0]
                print('space id found value', myresult[0][0])
            else:
                mycursor.execute(insert_space_sql, (space_obj['entity']['name'],org_id, 0,time.strftime('%Y-%m-%d %H:%M:%S')))
                space_id = mycursor.lastrowid
                db.commit()
            worksheet.set_row(row, None, bold)
            worksheet.write(row, col, 'Organization:')
            worksheet.write(row+1, col, org_obj['entity']['name'])
            worksheet.set_row(row+3, None, bold)
            worksheet.write(row+3, col, "Space:")
            worksheet.write(row+4, col, space_obj['entity']['name'])
            cf_list_apps_command = 'cf curl '+space_obj['entity']['apps_url']+'?results-per-page=100'
            process = subprocess.Popen(shlex.split(cf_list_apps_command), stdout=subprocess.PIPE)
            raw_apps_json = process.communicate()[0]
            apps_json = json.loads(raw_apps_json)
            worksheet.set_row(row+6, None, bold)
            worksheet.write(row+6, col,'Applications')
            worksheet.set_row(row+7, None, bold)
            worksheet.write(row+7, col,  'Name')
            worksheet.write(row+7, col+1, 'Memory')
            worksheet.write(row+7, col+2, 'Instances')
            worksheet.write(row+7, col+3, 'Disk space')
            worksheet.write(row+7, col+4, 'State')
            worksheet.write(row+7, col+5, 'Used cpu')
            worksheet.write(row+7, col+6, 'Used memory')
            worksheet.write(row+7, col+7, 'Used disk')
            row = row + 9
            resources = apps_json['resources']
            sorted_resources = sorted(resources, key=lambda k: k['entity'].get('memory', 0), reverse=True)
            for app in sorted_resources:
                params = urllib.urlencode({})
                headers = {"Authorization": token}
                conn = httplib.HTTPSConnection(flist[5])
                conn.request("GET", "/proxy/api/v3/apps/"+app['metadata']['guid']+"/processes/web/stats", params, headers)
                response = conn.getresponse()
                print(response.status, response.reason)
                data = response.read()
                conn.close()
                json_stats = json.loads(data)
                cpu_total = 0
                mem_total = 0
                disk_total = 0
                for resource in json_stats["resources"]:
                    if(resource['state'] == "RUNNING"):
                        cpu_total = cpu_total + resource['usage']['cpu']
                        mem_total = mem_total + resource['usage']['mem']
                        disk_total = resource['usage']['cpu'] + resource['usage']['disk']

                #usage_data = json_stats["resources"][0]
                worksheet.write(row, col,     app['entity']['name'])
                worksheet.write(row, col + 1, app['entity']['memory'])
                worksheet.write(row, col + 2, app['entity']['instances'])
                worksheet.write(row, col + 3, app['entity']['disk_quota'])
                worksheet.write(row, col + 4, app['entity']['state'])
                '''mycursor.execute(get_app_id_sql, (app['entity']['name'],space_id,))
                myresult = mycursor.fetchall()
                app_id = 0
                if(len(myresult) == 1):
                    print('app value found', myresult[0][0])
                    app_id = myresult[0][0]
                    db.commit()
                    mycursor.execute(update_app_sql, (app['entity']['name'],app['entity']['memory'],app['entity']['instances'],app['entity']['disk_quota'],app['entity']['state'],cpu_total,mem_total,disk_total, space_id, app_id, space_id))
                    db.commit()
                else:'''
                app_mem_per = 100 * (bitmath.Byte(mem_total).to_MB().value/app['entity']['memory'])
                foundry_app_mem_usage = foundry_app_mem_usage + bitmath.Byte(mem_total).to_GB().value
                mycursor.execute(insert_app_sql, (app['entity']['name'],app['entity']['memory'],app['entity']['instances'],app['entity']['disk_quota'],app['entity']['state'],cpu_total,mem_total,disk_total, space_id, app_mem_per,time.strftime('%Y-%m-%d %H:%M:%S')))
                app_id = mycursor.lastrowid
                db.commit()

                if(cpu_total == 0 and mem_total == 0 and disk_total==0):
                    worksheet.write(row, col+5, "NA")
                    worksheet.write(row, col+6, "NA")
                    worksheet.write(row, col+7, "NA")
                else:
                    mem_gb = str(bitmath.Byte(mem_total).to_GB())
                    disk_gb = str(bitmath.Byte(disk_total).to_GB())
                    worksheet.write(row, col+5, str(cpu_total) + "%")
                    worksheet.write(row, col+6, mem_gb)
                    worksheet.write(row, col+7, disk_gb)
                row += 1
    print(foundry_app_mem_usage)
    print(foundry_avail_mem)
    foundry_used_per = 100 * (foundry_app_mem_usage/foundry_avail_mem)  
    print(foundry_used_per)
    mycursor.execute(update_foundry_mempry_percent, (foundry_used_per,time.strftime('%Y-%m-%d %H:%M:%S')))
    db.commit()
workbook.close()

filename = 'top_apps_'+timestamp_str+'.xlsx'
fromaddr = ''
toaddr = ''
subject = ''
body = ''
cmd = 'echo '+body+' | mail -s '+subject+' -r '+fromaddr+' -a '+filename+' '+toaddr
send=subprocess.call(cmd,shell=True)

#remove file
process3 = subprocess.Popen(shlex.split('rm '+filename), stdout=subprocess.PIPE)
stdout3 = process3.communicate()[0]
print(stdout3)
