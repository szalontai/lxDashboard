from pydantic import  BaseSettings
 

class Settings(BaseSettings):
    sql_server_name: str = "dev-erp-db.linxdev.local"
    sql_server_port: str = "1435"
    sql_database: str = "andriello"
    sql_username: str = "inovacao.erp"
    sql_password: str = "Zvh}1#K{7qa00+oXZ31"
    sql_odbc_driver: str = "{ODBC Driver 18 for SQL Server}"
    sql_echo: bool = True  # exibição do comando SQL no Console

    custom_base_path: str = "c:\\vsts\\poc\\PythonLib\\"

    jwt_secret: str = "LiNx_SiStEmAs_E_cOnSuLtOrIa_Ltda"
    jwt_issuer: str = "Linx Sistemas e Consultoria Ltda"
    jwt_audience: str = "Linx New ERP"
    jwt_expiration_hours: int = 1


class SettingsLocal(BaseSettings):
    sql_server_name: str = "MTZNOTFS048722"
    sql_server_port: str = "1433"
    sql_database: str = "INOVACAO_LinxERP_DEV_bala"
    sql_username: str = "sa"
    sql_password: str = "Time.1oop"
    sql_odbc_driver: str = "{ODBC Driver 18 for SQL Server}"
    sql_echo: bool = True  # exibição do comando SQL no Console

    custom_base_path: str = "c:\\vsts\\poc\\PythonLib\\"

    jwt_secret: str = "LiNx_SiStEmAs_E_cOnSuLtOrIa_Ltda"
    jwt_issuer: str = "Linx Sistemas e Consultoria Ltda"
    jwt_audience: str = "Linx New ERP"
    jwt_expiration_hours: int = 1


settings = SettingsLocal()
