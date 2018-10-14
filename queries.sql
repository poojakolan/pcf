queries:

select foundry.foundry_name, apps.name,apps.memory,apps.instances,apps.disk_space,apps.state,apps.cpu_used,apps.memory_used,apps.disk_used, spaces.space_name,orgs.org_name from grafana.foundries as foundry, grafana.pcf_apps as apps, grafana.pcf_org as orgs, grafana.pcf_space as spaces where apps.space_id = spaces.id and spaces.org_id = orgs.id and orgs.foundry_id = foundry.id and foundry.foundry_name in (${foundry_list}) and orgs.org_name in (${ORG_NAMES});

select foundry.foundry_name, apps.name,apps.memory,apps.instances,apps.disk_space,apps.state,apps.cpu_used,apps.memory_used,apps.disk_used, spaces.space_name,orgs.org_name from grafana.foundries as foundry, grafana.pcf_apps as apps, grafana.pcf_org as orgs, grafana.pcf_space as spaces where apps.space_id = spaces.id and spaces.org_id = orgs.id and orgs.foundry_id = foundry.id;


select foundry.foundry_name, apps.name,apps.memory,apps.instances,apps.disk_space,apps.state,apps.cpu_used,apps.memory_used,apps.disk_used, spaces.space_name,orgs.org_name from grafana.foundries as foundry, grafana.pcf_apps as apps, grafana.pcf_org as orgs, grafana.pcf_space as spaces where apps.space_id = spaces.id and spaces.org_id = orgs.id and orgs.foundry_id = foundry.id and foundry.foundry_name in (${foundry_list}) and orgs.org_name in (${ORG_NAMES}) order by apps.memory_used desc limit 10;

generated 

select foundry.foundry_name, apps.name,apps.memory,apps.instances,apps.disk_space,apps.state,apps.cpu_used,apps.memory_used,apps.disk_used, spaces.space_name,orgs.org_name from grafana.foundries as foundry, grafana.pcf_apps as apps, grafana.pcf_org as orgs, grafana.pcf_space as spaces where apps.space_id = spaces.id and spaces.org_id = orgs.id and orgs.foundry_id = foundry.id and foundry.foundry_name in (${foundry_list}) and orgs.org_name in (${ORG_NAMES}) order by apps.memory_used desc limit 10;

Present Query

select foundry.foundry_name, apps.name,apps.memory,apps.instances,apps.disk_space,apps.state,apps.cpu_used,apps.memory_used,apps.disk_used, spaces.space_name,orgs.org_name from grafana.foundries as foundry, grafana.pcf_apps as apps, grafana.pcf_org as orgs, grafana.pcf_space as spaces where apps.space_id = spaces.id and spaces.org_id = orgs.id and orgs.foundry_id = foundry.id and foundry.foundry_name in ($foundry_list) and orgs.org_name in ($ORG_NAMES) order by apps.memory_used asc;




select foundry.foundry_name, apps.name,apps.memory,apps.instances,apps.disk_space,apps.state,apps.cpu_used,apps.memory_used,apps.disk_used, spaces.space_name,orgs.org_name from grafana.foundries as foundry, grafana.pcf_apps as apps, grafana.pcf_org as orgs, grafana.pcf_space as spaces where apps.space_id = spaces.id and spaces.org_id = orgs.id and orgs.foundry_id = foundry.id and foundry.foundry_name in (${foundry_list}) and orgs.org_name in (${ORG_NAMES}) order by apps.memory_used desc, apps.state limit 10;


select apps.memory_used as memory, UNIX_TIMESTAMP(apps.updated) as time_sec from grafana.foundries as foundry, grafana.pcf_apps as apps, grafana.pcf_org as orgs, grafana.pcf_space as spaces where apps.space_id = spaces.id and spaces.org_id = orgs.id and orgs.foundry_id = foundry.id;
