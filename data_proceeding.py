import socket
import json
import sqlite3
from discord_webhook import DiscordWebhook, DiscordEmbed

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 6468)) # IP address of server + port
    s.listen()
    conn, addr = s.accept()
    with conn:
        data = conn.recv(1024)
        conn.close()
    d = data.decode('utf-8')
    j = json.loads(d)
    conn = sqlite3.connect('trackerlog.db')
    c = conn.cursor()
    usrname, name, cargo, source, destination, mass, truck, distance, fuel, consumption, hours, minutes = j["user"], j["name"], j["cargo"], j["source"], j["destination"], j["mass"], j["Truck"], j["distance"], j["fuel"], j["consumption"], j["Hours"], j["Minutes"]
    if distance > 2:
        c.execute("CREATE TABLE IF NOT EXISTS {} (user TEXT, cargo TEXT, fromd TEXT, tod TEXT, cargo_mass INT, truck TEXT, distance INT, fuel INT, consumption INT, hours INT, minutes INT)".format(usrname))
        c.execute("INSERT INTO {0} VALUES (?,?,?,?,?,?,?,?,?,?,?)".format(usrname), (name, cargo, source, destination, mass, truck, distance, fuel, consumption, hours, minutes))
        conn.commit()
        conn.close()
    webhook = DiscordWebhook(url='webhook_url')
    embed = DiscordEmbed(title='Job delivered - {}'.format(j["name"]), color=0xa9181c)
    embed.add_embed_field(name='Cargo', value=j["cargo"], inline=False)
    embed.add_embed_field(name='From', value=j["source"])
    embed.add_embed_field(name='To', value=j["destination"])
    embed.add_embed_field(name="Cargo mass", value='{} kg'.format(j["mass"]))
    embed.add_embed_field(name='Truck', value=j["Truck"])
    embed.add_embed_field(name='Distance', value='{} km'.format(j["distance"]))
    embed.add_embed_field(name='Fuel', value='{} l'.format(round(j["fuel"])))
    embed.add_embed_field(name='Fuel consumption', value='{} l/100km'.format(j["consumption"]))
    embed.add_embed_field(name='Time taken', value='{} hours, {} minutes'.format(round(j["Hours"]), round(j["Minutes"])))
    if distance < 2:
        embed.set_footer(text='Delivery not logged due to short distance!')
    webhook.add_embed(embed)
    response = webhook.execute()
    print('Sent')
