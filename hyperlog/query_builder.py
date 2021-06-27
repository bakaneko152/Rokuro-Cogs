import json
from typing import Tuple, List
import pathlib
import discord
from discord.utils import DISCORD_EPOCH

from hyperlog import utils


def message_values(message:discord.Message, deleted=False,ver=1,other_data={}):
    return {
        "guild_id": message.guild.id if message.guild is not None else 0,
        "channel_id":message.channel.id,
        "message_id": message.id,
        "ver": ver,
        "is_dm_or_group":1 if isinstance(message.channel,(discord.DMChannel, discord.GroupChannel)) else 0,
        "author_id": message.author.id,
        "pinned":message.pinned,
        "embeds":json.dumps({i: message.embeds[i].to_dict() for i in range(len(message.embeds))},ensure_ascii=False) if message.embeds is not None and len(message.embeds)!=0 else {},
        "attachments":json.dumps({i:{"id":message.attachments[i].id,"filename":message.attachments[i].filename,"size":message.attachments[i].size,"is_spoiler":message.attachments[i].is_spoiler(),"urls":[message.attachments[i].url,message.attachments[i].proxy_url]} for i in range(len(message.attachments))},ensure_ascii=False) if message.attachments is not None and len(message.attachments)!=0 else {},
        "jump_url":message.jump_url,
        "created_at_jst":utils.unixtojst(((message.id >> 22) + DISCORD_EPOCH) / 1000),
        "changed_at_jst":utils.utctojst(message.edited_at) if message.edited_at is not None else None,
        "content":message.content if not message.is_system() else message.system_content,
        "stickers":json.dumps({i:{"id":message.stickers[i].id,"name":message.stickers[i].name,"description":message.stickers[i].description,"pack_id":message.stickers[i].pack_id} for i in range(len(message.stickers))},ensure_ascii=False) if message.stickers is not None and len(message.stickers)!=0 else {},
        "mention_everyone":message.mention_everyone,
        "mentions":json.dumps({i:{"id":message.mentions[i].id,"display_name":message.mentions[i].display_name,"discriminator":message.mentions[i].discriminator,"is_bot":message.mentions[i].bot} for i in range(len(message.mentions))},ensure_ascii=False) if message.mentions is not None and len(message.mentions)!=0 else {},
        "channel_mentions":json.dumps({i:{"id":message.channel_mentions[i].id,"name":message.channel_mentions[i].name} for i in range(len(message.channel_mentions))},ensure_ascii=False) if message.channel_mentions is not None and len(message.channel_mentions)!=0 else {},
        "role_mentions":json.dumps({i:{"id":message.role_mentions[i].id,"name":message.role_mentions[i].name} for i in range(len(message.role_mentions))},ensure_ascii=False) if message.role_mentions is not None and len(message.role_mentions)!=0 else {},
        "reference":json.dumps(message.reference.to_dict()+{"url":message.reference.jump_url},ensure_ascii=False) if message.reference is not None else {},
        "tts":message.tts,
        "other_data":other_data,
        "type":message.type,
        "is_deleted": deleted,
    }
def history_message_values(bfm:discord.Message,afm:discord.Message,deleted=False,ver=1,other_data={}):
    flag1 = 1#00000001
    flag2 = 2 #00000010
    flag3 = 4#00000100
    flag4 = 8 #00001000
    flag5 = 16 #00010000
    flag6 = 32 #00100000
    flag7 = 64#01000000
    flag8 = 128#10000000
    
    flag=0
    if bfm.pinned!=afm.pinned:
        flag+=flag1
    if bfm.embeds!=afm.embeds:
        flag+=flag2
    if bfm.attachments!=afm.attachments:
        flag+=flag3
    if bfm.content!=afm.content:
        flag+=flag4
    if bfm.mention_everyone!=afm.mention_everyone:
        flag+=flag5
    if bfm.mentions!=afm.mentions or bfm.channel_mentions!=afm.channel_mentions or bfm.role_mentions != afm.role_mentions:
        flag+=flag6
    if deleted:
        flag+=flag7
    return {
        "guild_id": afm.guild.id if afm.guild is not None else 0,
        "channel_id":afm.channel.id,
        "message_id": afm.id,
        "change_code":flag,
        "ver": ver,
        "is_dm_or_group":1 if isinstance(afm.channel,(discord.DMChannel, discord.GroupChannel)) else 0,
        "author_id": afm.author.id,
        "pinned":afm.pinned,
        "embeds":json.dumps({i: afm.embeds[i].to_dict() for i in range(len(afm.embeds))},ensure_ascii=False) if afm.embeds is not None and len(afm.embeds)!=0 else {},
        "attachments":json.dumps({i:{"id":afm.attachments[i].id,"filename":afm.attachments[i].filename,"size":afm.attachments[i].size,"is_spoiler":afm.attachments[i].is_spoiler(),"urls":[afm.attachments[i].url,afm.attachments[i].proxy_url]} for i in range(len(afm.attachments))},ensure_ascii=False) if afm.attachments is not None and len(afm.attachments)!=0 else {},
        "jump_url":afm.jump_url,
        "created_at_jst":utils.unixtojst(((afm.id >> 22) + DISCORD_EPOCH) / 1000),
        "changed_at_jst":utils.utctojst(afm.edited_at) if afm.edited_at is not None else None,
        "content":afm.content if not afm.is_system() else afm.system_content,
        "stickers":json.dumps({i:{"id":afm.stickers[i].id,"name":afm.stickers[i].name,"description":afm.stickers[i].description,"pack_id":afm.stickers[i].pack_id} for i in range(len(afm.stickers))},ensure_ascii=False) if afm.stickers is not None and len(afm.stickers)!=0 else {},
        "mention_everyone":afm.mention_everyone,
        "mentions":json.dumps({i:{"id":afm.mentions[i].id,"display_name":afm.mentions[i].display_name,"discriminator":afm.mentions[i].discriminator,"is_bot":afm.mentions[i].bot} for i in range(len(afm.mentions))},ensure_ascii=False) if afm.mentions is not None and len(afm.mentions)!=0 else {},
        "channel_mentions":json.dumps({i:{"id":afm.channel_mentions[i].id,"name":afm.channel_mentions[i].name} for i in range(len(afm.channel_mentions))},ensure_ascii=False) if afm.channel_mentions is not None and len(afm.channel_mentions)!=0 else {},
        "role_mentions":json.dumps({i:{"id":afm.role_mentions[i].id,"name":afm.role_mentions[i].name} for i in range(len(afm.role_mentions))},ensure_ascii=False) if afm.role_mentions is not None and len(afm.role_mentions)!=0 else {},
        "reference":json.dumps(afm.reference.to_dict()+{"url":afm.reference.jump_url},ensure_ascii=False) if afm.reference is not None else {},
        "tts":afm.tts,
        "other_data":other_data,
        "type":afm.type,
        "is_deleted": deleted,
    }

def insert_message_sql():
    return "INSERT INTO messages (guild_id,channel_id,message_id,ver,is_dm_or_group,author_id,pinned,embeds,attachments,jump_url,created_at_jst,changed_at_jst,content,stickers,mention_everyone,mentions,channel_mentions,role_mentions,reference,tts,other_data,type,is_deleted) VALUES(%(guild_id)s,%(channel_id)s,%(message_id)s,%(ver)s,%(is_dm_or_group)s,%(author_id)s,%(pinned)s,%(embeds)s,%(attachments)s,%(jump_url)s,%(created_at_jst)s,%(changed_at_jst)s,%(content)s,%(stickers)s,%(mention_everyone)s,%(mentions)s,%(channel_mentions)s,%(role_mentions)s,%(reference)s,%(tts)s,%(other_data)s,%(type)s,%(is_deleted)s);"

def insert_message_history_sql():
    return "INSERT INTO messages_history (guild_id,channel_id,message_id,change_code,ver,is_dm_or_group,author_id,pinned,embeds,attachments,jump_url,created_at_jst,changed_at_jst,content,stickers,mention_everyone,mentions,channel_mentions,role_mentions,reference,tts,other_data,type,is_deleted) VALUES(%(guild_id)s,%(channel_id)s,%(message_id)s,%(change_code)s,%(ver)s,%(is_dm_or_group)s,%(author_id)s,%(pinned)s,%(embeds)s,%(attachments)s,%(jump_url)s,%(created_at_jst)s,%(changed_at_jst)s,%(content)s,%(stickers)s,%(mention_everyone)s,%(mentions)s,%(channel_mentions)s,%(role_mentions)s,%(reference)s,%(tts)s,%(other_data)s,%(type)s,%(is_deleted)s);"

def update_message_sql():
    return "UPDATE messages SET messages.ver=%(ver)s,messages.pinned=%(pinned)s,messages.embeds=%(embeds)s,messages.attachments=%(attachments)s,messages.changed_at_jst=%(changed_at_jst)s,messages.content=%(content)s,messages.stickers=%(stickers)s,messages.mention_everyone=%(mention_everyone)s,messages.mentions=%(mentions)s,messages.channel_mentions=%(channel_mentions)s,messages.role_mentions=%(role_mentions)s,messages.reference=%(reference)s,messages.tts=%(tts)s,messages.other_data=%(other_data)s,messages.type=%(type)s,messages.is_deleted=%(is_deleted)s WHERE messages.guild_id = %(guild_id)s AND messages.channel_id = %(channel_id)s AND messages.message_id=%(message_id)s;"


def create_tables():
    query_list=[]
    
    query_list.append("SET sql_notes = 0;")# Temporarily disable the "Table already exists" warning
    message_table="""
    CREATE TABLE IF NOT EXISTS messages (
  guild_id bigint unsigned NOT NULL,
  channel_id bigint unsigned NOT NULL,
  message_id bigint unsigned NOT NULL,
  ver int unsigned NOT NULL DEFAULT '1',
  is_dm_or_group bit(1) NOT NULL DEFAULT b'0',
  author_id bigint unsigned DEFAULT NULL,
  pinned bit(1) NOT NULL DEFAULT b'0',
  embeds json DEFAULT NULL,
  attachments json DEFAULT NULL,
  jump_url varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_ja_0900_as_cs_ks DEFAULT NULL,
  created_at_jst datetime NOT NULL,
  changed_at_jst datetime DEFAULT NULL,
  content varchar(2304) CHARACTER SET utf8mb4 COLLATE utf8mb4_ja_0900_as_cs_ks DEFAULT NULL,
  stickers json DEFAULT NULL,
  mention_everyone bit(1) NOT NULL DEFAULT b'0',
  mentions json DEFAULT NULL,
  channel_mentions json DEFAULT NULL,
  role_mentions json DEFAULT NULL,
  reference json DEFAULT NULL,
  tts bit(1) NOT NULL DEFAULT b'0',
  other_data json DEFAULT NULL,
  type enum('default','recipient_add','recipient_remove','call','channel_name_change','channel_icon_change','pins_add','new_member','premium_guild_subscription','premium_guild_tier_1','premium_guild_tier_2','premium_guild_tier_3','channel_follow_add') CHARACTER SET utf8mb4 COLLATE utf8mb4_ja_0900_as_cs_ks DEFAULT NULL,
  is_deleted bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (guild_id,channel_id,message_id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_ja_0900_as_cs_ks ROW_FORMAT=DYNAMIC;
"""
    
    
    message_history_table="""
    CREATE TABLE IF NOT EXISTS messages_history (
  guild_id bigint unsigned NOT NULL,
  channel_id bigint unsigned NOT NULL,
  message_id bigint unsigned NOT NULL,
  change_code smallint unsigned NOT NULL DEFAULT '0',
  ver int unsigned NOT NULL DEFAULT '1',
  is_dm_or_group bit(1) NOT NULL DEFAULT b'0',
  author_id bigint unsigned DEFAULT NULL,
  pinned bit(1) NOT NULL DEFAULT b'0',
  embeds json DEFAULT NULL,
  attachments json DEFAULT NULL,
  jump_url varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_ja_0900_as_cs_ks DEFAULT NULL,
  created_at_jst datetime NOT NULL,
  changed_at_jst datetime DEFAULT NULL,
  content varchar(2304) CHARACTER SET utf8mb4 COLLATE utf8mb4_ja_0900_as_cs_ks DEFAULT NULL,
  stickers json DEFAULT NULL,
  mention_everyone bit(1) NOT NULL DEFAULT b'0',
  mentions json DEFAULT NULL,
  channel_mentions json DEFAULT NULL,
  role_mentions json DEFAULT NULL,
  reference json DEFAULT NULL,
  tts bit(1) NOT NULL DEFAULT b'0',
  other_data json DEFAULT NULL,
  type enum('default','recipient_add','recipient_remove','call','channel_name_change','channel_icon_change','pins_add','new_member','premium_guild_subscription','premium_guild_tier_1','premium_guild_tier_2','premium_guild_tier_3','channel_follow_add') CHARACTER SET utf8mb4 COLLATE utf8mb4_ja_0900_as_cs_ks DEFAULT NULL,
  is_deleted bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (guild_id,channel_id,message_id,change_code,ver) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_ja_0900_as_cs_ks ROW_FORMAT=DYNAMIC;
"""
    query_list.append(message_table)
    query_list.append(message_history_table)
    query_list.append("SET sql_notes = 1;")# re-enable the warning again
    
    return query_list