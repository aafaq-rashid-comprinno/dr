def layer_match_map(layer_arn):
    # Mapping of deprecated runtime versions to their latest versions
    layer_versions_mapping = {

        'arn:aws:lambda:ap-south-1:432542842095:layer:pandas:3': 'arn:aws:lambda:ap-south-2:142792260686:layer:pandas:3',
        'arn:aws:lambda:ap-south-1:432542842095:layer:pymongo:2': 'arn:aws:lambda:ap-south-2:142792260686:layer:pymongo:4',
        'arn:aws:lambda:ap-south-1:432542842095:layer:s18_pre_pan_scorecard:1': 'arn:aws:lambda:ap-south-2:142792260686:layer:s18_pre_pan_scorecard:3',
        'arn:aws:lambda:ap-south-1:432542842095:layer:s1_gps_dedupe:2': 'arn:aws:lambda:ap-south-2:142792260686:layer:s1_gps_dedupe:4',
        'arn:aws:lambda:ap-south-1:432542842095:layer:Jooq-generated-entities:306': 'arn:aws:lambda:ap-south-2:142792260686:layer:Jooq-generated-entities:304',
        'arn:aws:lambda:ap-south-1:432542842095:layer:DailyMonitoringSystem:60': 'arn:aws:lambda:ap-south-2:142792260686:layer:DailyMonitoringSystem:154',
        'arn:aws:lambda:ap-south-1:432542842095:layer:s2_sms_dedupe:2': 'arn:aws:lambda:ap-south-2:142792260686:layer:s2_sms_dedupe:4',
        'arn:aws:lambda:ap-south-1:432542842095:layer:S9_Email_dedupe_layer:1': 'arn:aws:lambda:ap-south-2:142792260686:layer:S9_Email_dedupe_layer:3',
        'arn:aws:lambda:ap-south-1:432542842095:layer:jooq_all_schema:5': 'arn:aws:lambda:ap-south-2:142792260686:layer:jooq_all_schema:7',
        'arn:aws:lambda:ap-south-1:432542842095:layer:s8_bs_responsiveness_layer:2': 'arn:aws:lambda:ap-south-2:142792260686:layer:s8_bs_responsiveness_layer:4',
        'arn:aws:lambda:ap-south-1:432542842095:layer:s7_bs_segment_layer:2': 'arn:aws:lambda:ap-south-2:142792260686:layer:s7_bs_segment_layer:4',
        'arn:aws:lambda:ap-south-1:432542842095:layer:Jooq-generated-entities:321': 'arn:aws:lambda:ap-south-2:142792260686:layer:Jooq-generated-entities:319',
        'arn:aws:lambda:ap-south-1:432542842095:layer:jooq_all_schema_qa:3': 'arn:aws:lambda:ap-south-2:142792260686:layer:jooq_all_schema_qa:4',
        'arn:aws:lambda:ap-south-1:432542842095:layer:Jooq-generated-entities:252': 'arn:aws:lambda:ap-south-2:142792260686:layer:Jooq-generated-entities:250',
        'arn:aws:lambda:ap-south-1:432542842095:layer:Jooq-generated-entities:216': 'arn:aws:lambda:ap-south-2:142792260686:layer:Jooq-generated-entities:214',
        'arn:aws:lambda:ap-south-1:432542842095:layer:Jooq-generated-entities:320': 'arn:aws:lambda:ap-south-2:142792260686:layer:Jooq-generated-entities:318',
        'arn:aws:lambda:ap-south-1:432542842095:layer:s14_limit_enhancement:2': 'arn:aws:lambda:ap-south-2:142792260686:layer:s14_limit_enhancement:4',
        'arn:aws:lambda:ap-south-1:432542842095:layer:pandas2:1': 'arn:aws:lambda:ap-south-2:142792260686:layer:pandas2:3',
        'arn:aws:lambda:ap-south-1:432542842095:layer:s6_penny_drop:2': 'arn:aws:lambda:ap-south-2:142792260686:layer:s6_penny_drop:4',
        'arn:aws:lambda:ap-south-1:432542842095:layer:s11_piramal_layer:2': 'arn:aws:lambda:ap-south-2:142792260686:layer:s11_piramal_layer:4',
        'arn:aws:lambda:ap-south-1:432542842095:layer:esutils:41': 'arn:aws:lambda:ap-south-2:142792260686:layer:esutils:43',
        'arn:aws:lambda:ap-south-1:432542842095:layer:S16_Pan_dedupe_layer:1': 'arn:aws:lambda:ap-south-2:142792260686:layer:S16_Pan_dedupe_layer:3',

    }

    return layer_versions_mapping.get(layer_arn)