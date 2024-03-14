def get_latest_runtime_version(runtime):
    # Mapping of deprecated runtime versions to their latest versions
    runtime_versions_mapping = {
        'nodejs10.x': 'nodejs20.x',
        'nodejs12.x': 'nodejs20.x',
        'nodejs4.3': 'nodejs20.x',
        'nodejs8.10': 'nodejs20.x',
        'nodejs8.10': 'nodejs20.x',
        'python2.7': 'python3.12',
        'python3.6': 'python3.12',
 
        # Supported
        'nodejs20.x': 'nodejs20.x',
        'provided.al2023': 'provided.al2023',
        'python3.12': 'python3.12',
        'java17': 'java17',
        'provided': 'provided',
        'nodejs16.x': 'nodejs16.x',
        'nodejs14.x': 'nodejs14.x',
        'ruby2.7': 'ruby2.7',
        'python3.10':  'python3.10',
        'java11': 'java11',
        'python3.11': 'python3.11',
        'dotnet6': 'dotnet6',
        'go1.x': 'go1.x',
        'java21': 'java21',
        'nodejs18.x': 'nodejs18.x',
        'provided.al2': 'provided.al2',
        'java8': 'java8',
        'java8.al2': 'java8.al2',
        'ruby3.2': 'ruby3.2',
        'python3.7': 'python3.7',
        'python3.8': 'python3.8',
        'python3.9': 'python3.9',
        # Add mappings for other deprecated runtimes
    }

    return runtime_versions_mapping.get(runtime, runtime)