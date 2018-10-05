queries:

select foundry.foundry_name, apps.name,apps.memory,apps.instances,apps.disk_space,apps.state,apps.cpu_used,apps.memory_used,apps.disk_used, spaces.space_name,orgs.org_name from grafana.foundries as foundry, grafana.pcf_apps as apps, grafana.pcf_org as orgs, grafana.pcf_space as spaces where apps.space_id = spaces.id and spaces.org_id = orgs.id and orgs.foundry_id = foundry.id and foundry.foundry_name in (${foundry_list}) and orgs.org_name in (${ORG_NAMES});

select foundry.foundry_name, apps.name,apps.memory,apps.instances,apps.disk_space,apps.state,apps.cpu_used,apps.memory_used,apps.disk_used, spaces.space_name,orgs.org_name from grafana.foundries as foundry, grafana.pcf_apps as apps, grafana.pcf_org as orgs, grafana.pcf_space as spaces where apps.space_id = spaces.id and spaces.org_id = orgs.id and orgs.foundry_id = foundry.id;
