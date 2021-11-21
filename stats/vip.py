from fabric import connection

def add_vip(steamid,server):
    config_dir = server.path_to_vip_file
    command = f"""
            python3 -c 'import auto_vip; auto_vip.add_vip("{steamid}")'
            """
    conn = connection.Connection(server.ssh_ip,server.ssh_user,server.ssh_port,connect_kwargs={"password":server.ssh_psswd})
    with conn.cd(config_dir):
        conn.run(command)
    

def del_vip(steamid, server):
    config_dir = server.path_to_vip_file
    command =f"""
        python3 -c 'import auto_vip; auto_vip.del_vip("{steamid}")'
        """
    conn = connection.Connection(server.ssh_ip,server.ssh_user,server.ssh_port,connect_kwargs={"password":server.ssh_psswd})
    with conn.cd(config_dir):
        conn.run(command)