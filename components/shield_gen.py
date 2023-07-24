import json


gp_models = [100,122,135,198,204,303,306,401,411,499,507]
gpx_models = [1,2,3,4,5]

gp_description = "@upgrades/shield.image@Originally designed by General Physics over a century ago, the now “General Purpose” family of small craft shields has been produced by virtually all factions in the human sphere of influence."

gpx_description = "@upgrades/shield.image@Protecting mercantile craft for over a century, this line of products by General Physics is significantly more expensive and complex to manufacture. As a result, it is produced by a small number of licensees. It is also of better and consistent quality."

gp_power = [75, 150, 300, 400, 500, 600, 700, 800, 900, 1000]
gpx_power = [1200, 1400, 1600, 1800, 2000]

gp_model_description = [" The weakest model in the range, the gp-100 is best suited for orbital shuttles in well policed worlds.", " An update of the basic, gp-100 model, the gp-122 is a popular choice of inner system shuttles and other commercial crafts.", " Like coffee and doughnuts, the gp-135 is used extensively by rent-a-cops and traffic control enforcers.", " A step up from smaller models, the gp-198 is well suited for budding space explorers, deep space miners and intersystem shuttles.", " the gp-204 is typically used in light fighters and scouts, where flight, rather than fight is the typical choice.", " Packing serious protection into a small package, the gp-303 is typically used in small fighters, where space is at a premium.", " A mid-life update of the gp-303, the gp-306 offers better protection in nearly the same size package. Power draw, unfortunately, is significantly higher."," Robust and still compact, the gp-401 is used by long range scouts and heavier fighters.", " Based on a heavily modified gp-401, the gp-411 is used primarily by heavy fighters.", " A heavily modified variant of the 4xx series, the gp-499 is mostly used by bombers and fighter-bombers.", " The final and largest of the gp models, the gp-507 provides the ultimate in protection." ]

gpx_model_description = [" The smallest of the gpx models, the gpx-1 is typically used by merchants on the larger, cargo transports.", " A step up, the gpx-2 is a favorite of commercial passenger spaceliners.", " The gpx-3 is the go to choice for large ships in risky areas. Be it, diplomatic, merchant or military.", " Originally designed for sub-capital ships, the gpx-4 is still used by capital ships of the smaller worlds.", " The ultimate model in the gpx range, the gpx-5 is the best (and most expensive) shield system you can buy commercially."]

with open('master_component_list.json') as f:
    components = json.loads(f.read())
    
    for component in components:
        if component['file'].startswith('quadshield'):
            index = int(component['file'][10:]) -1

            if index < 10:
                component['description'] = gp_description + gp_model_description[index]
            else:
                component['description'] = gpx_description + gpx_model_description[index-10]

with open('new.json', 'w') as f:
    json.dump(components, f, ensure_ascii=False, indent=4)

    
    
