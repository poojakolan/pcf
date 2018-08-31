import subprocess
import shlex
import json
import datetime
import time
import xlsxwriter
import httplib, urllib
import math

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

foundry_list = {'foundry-1': ['https://api.run.pivotal.io', 'Lakshmiredz@gmail.com', 'Pooja@123', 'concourse2', 'ci', 'console.run.pivotal.io']}
timestamp_str = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')

workbook = xlsxwriter.Workbook('top_apps_'+timestamp_str+'.xlsx')
bold = workbook.add_format({'bold': True})

for foundry in foundry_list:
    flist = foundry_list[foundry]
    api = flist[0]
    user = flist[1]
    pwd = flist[2]
    org = flist[3]
    space = flist[4]

    login_command = 'cf login -a ' + api + ' -u ' + user + ' -p ' + pwd + ' -o ' + org + ' -s ' + space + ' --skip-ssl-validation'
    list_all_orgs = 'cf curl /v2/organizations'+'?results-per-page=100'
    
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
    for org_obj in org_json['resources']:
        cf_list_spaces_command = 'cf curl '+org_obj['entity']['spaces_url']+'?results-per-page=100'
        process = subprocess.Popen(shlex.split(cf_list_spaces_command), stdout=subprocess.PIPE)
        raw_spaces_json = process.communicate()[0]
        spaces_json = json.loads(raw_spaces_json)
        for space_obj in spaces_json['resources']:
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

            token_proc = subprocess.Popen(shlex.split('cf oauth-token'), stdout=subprocess.PIPE)
            token = token_proc.communicate()[0]
            token = token.replace("\n", "")
            for app in sorted_resources: 
                params = urllib.urlencode({})
                headers = {"Authorization": token}
                conn = httplib.HTTPConnection(flist[5])
                conn.request("GET", "/proxy/api/v3/apps/"+app['metadata']['guid']+"/processes/web/stats", params, headers)
                print("console.run.pivotal.io"+"/proxy/api/v3/apps/"+app['metadata']['guid']+"/processes/web/stats")
                response = conn.getresponse()
                print response.status, response.reason
                data = response.read()
                json_stats = json.loads(data)                
                usage_data = json_stats["resources"][0]
                conn.close()
                worksheet.write(row, col,     app['entity']['name'])
                worksheet.write(row, col + 1, app['entity']['memory'])
                worksheet.write(row, col + 2, app['entity']['instances'])
                worksheet.write(row, col + 3, app['entity']['disk_quota'])
                worksheet.write(row, col + 4, app['entity']['state'])
                if(usage_data['state'] == "DOWN"):
                    worksheet.write(row, col+5, "NA")
                    worksheet.write(row, col+6, "NA")
                    worksheet.write(row, col+7, "NA")
                else:
                    print(app['entity']['name']+"   **** app name UP")
                    print(json_stats)
                    usage_details = usage_data['usage']
                    worksheet.write(row, col+5, usage_details['cpu'])
                    worksheet.write(row, col+6, usage_details['mem'])
                    worksheet.write(row, col+7, usage_details['disk'])
                row += 1
workbook.close()
