import re

import json
from mitreattack.stix20 import MitreAttackData

atk = MitreAttackData("enterprise-attack.json")

techs = atk.get_techniques()

q = {}
q_long = {}
for t in techs:
    short_question = "Should this be tagged as MITRE Att&ck Technique: " + t.name + "?"
    
    cleaned_description = re.sub(r"\s*\(Citation:[^)]*\)", "", t.description).replace("\n\n", " ").replace("  ", " ").replace("<code>", "").replace("</code>", "").strip()
    cleaned_description = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", cleaned_description).replace("\u2019", "'").replace("\u201C", "\"").replace("\u201D", "\"")
    long_question = " ".join([short_question, cleaned_description])
    
    # DATA CLEANLINESS ASSUMPTION that there is always one reference of this source_name in the list and that it is unique
    mitre_tag = [ref.external_id for ref in t.external_references if ref.source_name == "mitre-attack"][0] 
    
    q[mitre_tag] = { 'type' : 'noul', 'instructions' : short_question }
    q_long[mitre_tag] = { 'type' : 'noul', 'instructions' : long_question }

with open("q_short.json", "w", encoding="utf-8") as fp:
    json.dump(q, fp, sort_keys=False, indent=4)

with open("q_long.json", "w", encoding="utf-8") as fp:
    json.dump(q_long, fp, sort_keys=False, indent=4)