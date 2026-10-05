def set_environment():
  
  env = ProjectSuite.Variables.env

  if env != '':
    if 'int' in env.lower():
      ProjectSuite.Variables.base_path = 'https://sib.integrazione.servizi.allitude.it'
      ProjectSuite.Variables.keycloak_url = 'https://keycloak.integrazione.servizi.allitude.it/auth/realms/Allitude-B2B/protocol/openid-connect/token'
      ProjectSuite.Variables.MSS_LEASING = 'MSS_LEASING_INT'
      ProjectSuite.Variables.MSS_ASSET_DIRECTORY = 'MSS_ASSET_DIRECTORY_INT'
    elif 'svi' in env.lower():
      ProjectSuite.Variables.base_path = 'https://sib.sviluppo.servizi.allitude.it'
      ProjectSuite.Variables.keycloak_url = 'https://keycloak.sviluppo.servizi.allitude.it/auth/realms/Allitude-B2B/protocol/openid-connect/token'
      ProjectSuite.Variables.MSS_LEASING = 'MSS_LEASING_SVI'
      ProjectSuite.Variables.MSS_ASSET_DIRECTORY = 'MSS_ASSET_DIRECTORY_SVI'