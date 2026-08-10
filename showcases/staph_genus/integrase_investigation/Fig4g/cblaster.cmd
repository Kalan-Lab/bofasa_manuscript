cblaster search -qf Staph_MiniMGE.faa --min_identity 88 --min_coverage 50 -r AAA_001955 --session_file cblaster_session.json --min_hits 6 -ig > cblaster_results.txt
cblaster extract_clusters -o cblaster_extracted_gbks/ cblaster_session.json
